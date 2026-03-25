from typing import Optional
from fastapi import APIRouter
from fastapi.responses import JSONResponse

from schemas.common import ErrorResponse
from schemas.feeds import (
    FeedCreateRequest,
    FeedCreateResponse,
    FeedResponse,
    FeedStatus,
    FeedListResponse)
from schemas.jobs import JobStatus
from store import feeds, jobs, feed_counter, job_counter

router = APIRouter(tags=["Feeds"])

feed_id = f"f_{feed_counter['value']}"
feed_counter["value"] += 1

job_id = f"j_{job_counter['value']}"
job_counter["value"] += 1

@router.post("/feeds", response_model=FeedCreateResponse, summary="Create a new feed",
description="Submits a partner product feed and creates an associated processing job.")
def create_feed(feed: FeedCreateRequest):
    feed_id = f"f_{feed_counter['value']}"
    feed_counter["value"] += 1

    job_id = f"j_{job_counter['value']}"
    job_counter["value"] += 1

    feeds[feed_id] = {
        "feed_id": feed_id,
        "partner_name": feed.partner_name,
        "file_name": feed.file_name,
        "status": FeedStatus.uploaded,
    }

    jobs[job_id] = {
        "job_id": job_id,
        "feed_id": feed_id,
        "status": JobStatus.queued,
        "job_type": "feed_submission",
    }

    return {
        "feed_id": feed_id,
        "status": FeedStatus.uploaded,
        "job_id": job_id,
    }
@router.get(
    "/feeds/{feed_id}",
    response_model=FeedResponse,
    responses={404: {"model": ErrorResponse, "description": "Feed not found"}}, summary="Get feed by ID",
description="Retrieves details for a specific feed."
)
def get_feed(feed_id: str):
    feed = feeds.get(feed_id)
    if not feed:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": "FEED_NOT_FOUND",
                "message": f"Feed {feed_id} not found",
                "details": {"feed_id": feed_id},
            },
        )
    return feed

@router.post("/feeds/{feed_id}/validate", summary="Start feed validation",
description="Creates a validation job for the specified feed and updates the feed status to validating.")
def validate_feed(feed_id: str):
    if feed_id not in feeds:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": "FEED_NOT_FOUND",
                "message": f"Feed {feed_id} not found",
                "details": {"feed_id": feed_id},
            },
        )

    job_id = f"j_{job_counter['value']}"
    job_counter["value"] += 1

    jobs[job_id] = {
        "job_id": job_id,
        "feed_id": feed_id,
        "status": JobStatus.running,
        "job_type": "validation",
    }

    feeds[feed_id]["status"] = FeedStatus.validating

    return {
        "message": "Validation started",
        "feed_id": feed_id,
        "job_id": job_id,
        "status": FeedStatus.validating,
    }

@router.get("/feeds", response_model=FeedListResponse, summary="List feeds",
description="Returns a paginated list of feeds with optional filtering by status.")
def list_feeds(status: Optional[FeedStatus] = None, limit: int = 10, offset: int = 0):
    all_feeds = list(feeds.values())

    if status:
        all_feeds = [f for f in all_feeds if f["status"] == status]

    result = all_feeds[offset:offset + limit]

    return {
        "items": result,
        "total": len(all_feeds),
        "limit": limit,
        "offset": offset
    }