from fastapi import FastAPI
from pydantic import BaseModel
from uuid import uuid4
from enum import Enum
from typing import Optional, Dict, Any
from fastapi.responses import JSONResponse

app = FastAPI(
    title="Partner Catalog API",
    description="Demo API for partner feed submission, validation, and job tracking.",
    version="0.1.0"
)

jobs = {}
feeds = {}

class FeedStatus(str, Enum):
    uploaded = "uploaded"
    validating = "validating"
    validated = "validated"
    failed = "failed"


class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"

class FeedCreateRequest(BaseModel):
    partner_name: str
    file_name: str
    submitted_by: str
    notes: Optional[str] = None

class FeedResponse(BaseModel):
    feed_id: str
    partner_name: str
    file_name: str
    status: FeedStatus

class FeedCreateResponse(BaseModel):
    feed_id: str
    status: str
    job_id: str

class JobResponse(BaseModel):
    job_id: str
    feed_id: str
    status: JobStatus
    job_type: str

class ErrorResponse(BaseModel):
    error_code: str
    message: str
    details: Optional[Dict[str, Any]] = None
@app.get("/")
def read_root():
    return {"message": "Partner Catalog API is running"}

@app.post("/feeds", response_model=FeedCreateResponse)
def create_feed(feed: FeedCreateRequest):
    feed_id = str(uuid4())
    job_id = str(uuid4())

    feeds[feed_id] = {
        "feed_id": feed_id,
        "partner_name": feed.partner_name,
        "file_name": feed.file_name,
        "status": FeedStatus.uploaded
    }

    jobs[job_id] = {
        "job_id": job_id,
        "feed_id": feed_id,
        "status": JobStatus.queued,
        "job_type": "feed_submission"
    }

    return {
        "feed_id": feed_id,
        "status": FeedStatus.uploaded,
        "job_id": job_id
    }
@app.post("/feeds/{feed_id}/validate")
def validate_feed(feed_id: str):
    job_id = str(uuid4())

    jobs[job_id] = {
        "job_id": job_id,
        "feed_id": feed_id,
        "status": "running",
        "job_type": "validation"
    }

    return {
        "message": "Validation started",
        "feed_id": feed_id,
        "job_id": job_id,
        "status": "validating"
    }

@app.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Job not found"
        }
    }
)
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": "JOB_NOT_FOUND",
                "message": f"Job {job_id} not found",
                "details": {"job_id": job_id}
            }
        )
    return job

@app.get(
    "/feeds/{feed_id}",
    response_model=FeedResponse,
    responses={
        404: {
            "model": ErrorResponse,
            "description": "Feed not found"
        }
    }
)
def get_feed(feed_id: str):
    feed = feeds.get(feed_id)
    if not feed:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": "FEED_NOT_FOUND",
                "message": f"Feed {feed_id} not found",
                "details": {"feed_id": feed_id}
            }
        )
    return feed
