from __future__ import annotations
import csv
import io
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException, status
from schemas.common import ErrorResponse
from schemas.feeds import FeedResponse
from data.stores import (
    create_feed,
    create_job,
    get_feed,
    map_feed_to_response,
    next_feed_id,
    next_submission_job_id,
    next_validation_job_id,
    utc_now_iso
)
from security import require_api_key

router = APIRouter(
    prefix="/feeds",
    tags=["Feeds"],
    dependencies=[Depends(require_api_key)]
)
@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
    summary="Upload a feed",
    description="Uploads a product feed into the system"
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
        reader = csv.DictReader(io.StringIO(decoded))
        _ = list(reader)

        if reader.fieldnames is None:
            raise ValueError("CSV header row is missing.")
    except Exception as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Invalid CSV file: {exc}"
        )

    feed_id = next_feed_id()
    submission_job_id = next_submission_job_id()
    validation_job_id = next_validation_job_id()
    now = utc_now_iso()

    create_feed(
        feed_id=feed_id,
        partner_name=partner_name,
        file_name=file.filename or "uploaded.csv",
        content_type=file.content_type,
        status="uploaded",
        uploaded_at=now,
        validation_job_id=validation_job_id,
    )

    create_job(
        job_id=submission_job_id,
        job_type="submission",
        status="completed",
        created_at=now,
        feed_id=feed_id,
        message="Feed upload accepted."
    )

    create_job(
        job_id=validation_job_id,
        job_type="validation",
        status="completed",
        created_at=now,
        feed_id=feed_id,
        message="CSV structure validation completed."
    )

    return {
        "feed_id": feed_id,
        "job_id": submission_job_id,
        "status": "uploaded",
        "partner_name": partner_name,
        "file_name": file.filename or "uploaded.csv"
    }

@router.get("/{feed_id}",
    response_model=FeedResponse,
    responses={404: {"model": ErrorResponse, "description": "Feed not found"}},
    summary="Get feed by ID",
    description="Retrieves details for a specific feed."
)
async def read_feed(feed_id: str):
    feed = get_feed(feed_id)
    if not feed:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Feed {feed_id} not found."
        )

    return map_feed_to_response(feed)
