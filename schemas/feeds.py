from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr

class FeedStatus(str, Enum):
    uploaded = "uploaded"
    validating = "validating"
    validated = "validated"
    failed = "failed"

class FeedCreateRequest(BaseModel):
    partner_name: str
    file_name: str
    submitted_by: EmailStr
    notes: Optional[str] = None

class FeedResponse(BaseModel):
    feed_id: str
    partner_name: str
    file_name: str
    status: FeedStatus

class FeedCreateResponse(BaseModel):
    feed_id: str
    status: FeedStatus
    job_id: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "feed_id": "FD001",
                    "status": "uploaded",
                    "job_id": "JS001"
                }
            ]
        }
    }



class FeedListResponse(BaseModel):
    items: list[FeedResponse]
    total: int
    limit: int
    offset: int