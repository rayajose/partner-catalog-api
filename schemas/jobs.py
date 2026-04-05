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

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "job_id": "JV001",
                    "feed_id": "FD001",
                    "status": "running",
                    "job_type": "feed_validation"
                }
            ]
        }
    }