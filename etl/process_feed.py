from __future__ import annotations

import csv
import io

import boto3

from db import get_connection, q, DB_TYPE, next_product_id_with_conn
from services.s3_service import S3_RAW_BUCKET
from utils import utc_now_iso


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


def update_validation_job(feed_id: str, status: str, message: str) -> None:
    with get_connection() as conn:
        conn.execute(
            q("""
                UPDATE jobs
                SET status = ?, message = ?
                WHERE feed_id = ?
                  AND job_type = 'validation'
            """),
            (status, message, feed_id),
        )

        if DB_TYPE == "postgres":
            conn.commit()


def get_feed(feed_id: str) -> dict:
    with get_connection() as conn:
        feed = conn.execute(
            q("""
                SELECT
                    feed_id,
                    partner_name,
                    raw_file_s3_key,
                    raw_file_bucket
                FROM feeds
                WHERE feed_id = ?
            """),
            (feed_id,),
        ).fetchone()

    if not feed:
        raise ValueError(f"Feed {feed_id} not found.")

    if DB_TYPE == "sqlite":
        feed = dict(feed)
    else:
        feed = {
            "feed_id": feed[0],
            "partner_name": feed[1],
            "raw_file_s3_key": feed[2],
            "raw_file_bucket": feed[3],
        }

    if not feed["raw_file_s3_key"]:
        raise ValueError(f"Feed {feed_id} does not have an S3 raw file key.")

    return feed


def read_csv_from_s3(bucket: str, object_key: str) -> list[dict]:
    s3_client = boto3.client("s3")

    response = s3_client.get_object(
        Bucket=bucket,
        Key=object_key,
    )

    content = response["Body"].read().decode("utf-8-sig")
    reader = csv.DictReader(io.StringIO(content))

    return list(reader)


def load_products(feed: dict, rows: list[dict]) -> int:
    now = utc_now_iso()
    products_ingested = 0

    with get_connection() as conn:
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
                    feed["feed_id"],
                    feed["partner_name"],
                    sku,
                    product_name,
                    clean_value(row.get("description")),
                    clean_value(row.get("brand")),
                    clean_value(row.get("category")),
                    parse_price(row.get("price")),
                    clean_value(row.get("currency")),
                    clean_value(row.get("availability")),
                    now,
                ),
            )

            products_ingested += 1

        if DB_TYPE == "postgres":
            conn.commit()

    return products_ingested


def process_feed(feed_id: str) -> None:
    try:
        update_validation_job(
            feed_id=feed_id,
            status="running",
            message="ETL processing started.",
        )

        feed = get_feed(feed_id)
        bucket = feed["raw_file_bucket"] or S3_RAW_BUCKET

        rows = read_csv_from_s3(
            bucket=bucket,
            object_key=feed["raw_file_s3_key"],
        )

        products_ingested = load_products(feed, rows)

        update_validation_job(
            feed_id=feed_id,
            status="completed",
            message=f"ETL processing completed. Products ingested: {products_ingested}.",
        )

        print(f"Processed feed {feed_id}")
        print(f"Products ingested: {products_ingested}")

    except Exception as exc:
        update_validation_job(
            feed_id=feed_id,
            status="failed",
            message=f"ETL processing failed: {exc}",
        )
        raise


if __name__ == "__main__":
    feed_id = input("Enter feed ID to process: ").strip()
    process_feed(feed_id)