from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from uuid import uuid4

app = FastAPI(
    title="Partner Catalog API",
    description="Demo API for partner feed submission, validation, and job tracking.",
    version="0.1.0"
)

jobs = {}

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

    jobs[job_id] = {
        "job_id": job_id,
        "feed_id": feed_id,
        "status": "queued",
        "job_type": "feed_submission"
    }

    return {
        "feed_id": feed_id,
        "status": "uploaded",
        "job_id": job_id,
        "partner_name": feed.partner_name,
        "file_name": feed.file_name
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
        return {"error": "Job not found", "job_id": job_id}
    return job