from enum import Enum
from pydantic import BaseModel

class JobStatus(str, Enum):
    queued = "queued"
    running = "running"
    completed = "completed"
    failed = "failed"

class JobResponse(BaseModel):
    job_id: str
    feed_id: str
    status: JobStatus
    job_type: str