from __future__ import annotations

import csv
import io
import re

from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status

from schemas.common import ErrorResponse
from schemas.feeds import FeedResponse, FeedCreateResponse
from db import (
    get_connection,
    q,
    DB_TYPE,
    next_feed_id,
    next_submission_job_id,
    next_validation_job_id,
    next_product_id_with_conn,
)
from security import require_api_key
from utils import utc_now_iso
from services.s3_service import upload_raw_feed

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"],
    dependencies=[Depends(require_api_key)]
)

FEED_COLUMNS = [
    "feed_id",
    "partner_name",
    "file_name",
    "content_type",
    "status",
    "uploaded_at",
    "validation_job_id",
]


def clean_value(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    return value if value else None


def parse_price(value: str | None) -> float | None:
    cleaned = clean_value(value)
    if cleaned is None:
        return None

    cleaned = cleaned.replace("$", "").replace(",", "")

    try:
        return float(cleaned)
    except ValueError:
        return None


def slugify(value: str) -> str:
    value = value.lower().strip()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def feed_row_to_dict(row):
    if DB_TYPE == "sqlite":
        return dict(row)
    return dict(zip(FEED_COLUMNS, row))


@router.post(
    "/upload",
    response_model=FeedCreateResponse,
    status_code=status.HTTP_201_CREATED,
    summary="Upload a product feed",
    description=(
        "Uploads a CSV product feed for a partner. The feed is stored, "
        "processed, and validated.\n\n"
        "This operation triggers:\n"
        "- A submission job (JSxxxxx)\n"
        "- A validation job (JVxxxxx)\n\n"
        "The uploaded data is validated and, if successful, ingested into the "
        "product catalog for querying via the products endpoints."
    ),
    responses={
        400: {"model": ErrorResponse, "description": "Invalid CSV file"},
        401: {"description": "Unauthorized"},
    },
)
async def upload_feed(
    partner_name: str = Form(...),
    file: UploadFile = File(...)
):
    allowed_types = {"text/csv", "text/plain", "application/vnd.ms-excel"}

    if file.content_type not in allowed_types:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only CSV uploads are supported at this time."
        )

    content = await file.read()

    if not content:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Uploaded file is empty."
        )

    try:
        decoded = content.decode("utf-8-sig")
    except UnicodeDecodeError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="CSV file must be UTF-8 encoded."
        )

    try:
        reader = csv.DictReader(io.StringIO(decoded))

        if reader.fieldnames is None:
            raise ValueError("CSV header row is missing.")

        normalized_headers = {
            header.strip() for header in reader.fieldnames if header
        }

        required_headers = {"sku", "product_name"}
        missing_headers = required_headers - normalized_headers

        if missing_headers:
            raise ValueError(
                f"Missing required CSV headers: {', '.join(sorted(missing_headers))}"
            )

        rows = list(reader)

    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV file: {exc}"
        )

    feed_id = next_feed_id()
    submission_job_id = next_submission_job_id()
    validation_job_id = next_validation_job_id()
    now = utc_now_iso()
    products_ingested = 0

    original_filename = file.filename or "uploaded.csv"
    safe_partner_name = slugify(partner_name)

    raw_file_s3_key = (
        f"raw/partners/{safe_partner_name}/feeds/{feed_id}/{original_filename}"
    )

    try:
        upload_raw_feed(
            file_bytes=content,
            object_key=raw_file_s3_key,
            content_type=file.content_type or "text/csv",
        )
    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(exc),
        )

    with get_connection() as conn:
        conn.execute(
            q("""
                INSERT INTO feeds (
                    feed_id,
                    partner_name,
                    file_name,
                    content_type,
                    status,
                    uploaded_at,
                    validation_job_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """),
            (
                feed_id,
                partner_name,
                original_filename,
                file.content_type or "text/csv",
                "uploaded",
                now,
                validation_job_id,
            )
        )

        conn.execute(
            q("""
                INSERT INTO jobs (
                    job_id,
                    job_type,
                    status,
                    created_at,
                    feed_id,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """),
            (
                submission_job_id,
                "submission",
                "completed",
                now,
                feed_id,
                "Feed upload accepted."
            )
        )

        conn.execute(
            q("""
                INSERT INTO jobs (
                    job_id,
                    job_type,
                    status,
                    created_at,
                    feed_id,
                    message
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """),
            (
                validation_job_id,
                "validation",
                "completed",
                now,
                feed_id,
                "CSV structure validation completed."
            )
        )

        for row in rows:
            sku = clean_value(row.get("sku"))
            product_name = clean_value(row.get("product_name"))

            if not sku or not product_name:
                continue

            product_id = next_product_id_with_conn(conn)

            conn.execute(
                q("""
                    INSERT INTO products (
                        product_id,
                        feed_id,
                        partner_name,
                        sku,
                        product_name,
                        description,
                        brand,
                        category,
                        price,
                        currency,
                        availability,
                        created_at
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """),
                (
                    product_id,
                    feed_id,
                    partner_name,
                    sku,
                    product_name,
                    clean_value(row.get("description")),
                    clean_value(row.get("brand")),
                    clean_value(row.get("category")),
                    parse_price(row.get("price")),
                    clean_value(row.get("currency")),
                    clean_value(row.get("availability")),
                    now,
                )
            )

            products_ingested += 1

        if DB_TYPE == "postgres":
            conn.commit()

    return {
        "feed_id": feed_id,
        "job_id": submission_job_id,
        "status": "uploaded",
        "products_ingested": products_ingested
    }


@router.get(
    "/{feed_id}",
    response_model=FeedResponse,
    responses={404: {"model": ErrorResponse, "description": "Feed not found"}},
    summary="Retrieve feed details",
    description=(
        "Retrieves metadata for a specific feed, including upload status and "
        "associated validation job."
    ),
)
async def read_feed(feed_id: str):
    with get_connection() as conn:
        feed = conn.execute(
            q("""
                SELECT
                    feed_id,
                    partner_name,
                    file_name,
                    content_type,
                    status,
                    uploaded_at,
                    validation_job_id
                FROM feeds
                WHERE feed_id = ?
            """),
            (feed_id,)
        ).fetchone()

    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feed {feed_id} not found."
        )

    return feed_row_to_dict(feed)