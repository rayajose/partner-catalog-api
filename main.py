from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4
from fastapi import HTTPException

app = FastAPI(
    title="Partner Catalog API",
    description="Demo API for partner feed submission, validation, and job tracking.",
    version="0.1.0"
)

jobs = {}
feeds = {}

class FeedCreateRequest(BaseModel):
    partner_name: str
    file_name: str
    submitted_by: str
    notes: Optional[str] = None

@app.get("/")
def read_root():
    return {"message": "Partner Catalog API is running"}

@app.post("/feeds")
def create_feed(feed: FeedCreateRequest):
    feed_id = str(uuid4())
    job_id = str(uuid4())

    feeds[feed_id] = {
        "feed_id": feed_id,
        "partner_name": feed.partner_name,
        "file_name": feed.file_name,
        "status": "uploaded"
    }

    jobs[job_id] = {
        "job_id": job_id,
        "feed_id": feed_id,
        "status": "queued",
        "job_type": "feed_submission"
    }

    return {
        "feed_id": feed_id,
        "status": "uploaded",
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

@app.get("/jobs/{job_id}")
def get_job(job_id: str):
    job = jobs.get(job_id)
    if not job:
        raise HTTPException(
            status_code=404,
            detail=f"Job {job_id} not found"
        )
    return job

@app.get("/feeds/{feed_id}")
def get_feed(feed_id: str):
    feed = feeds.get(feed_id)

    if not feed:
        raise HTTPException(
            status_code=404,
            detail=f"Feed {feed_id} not found"
        )

    return feed