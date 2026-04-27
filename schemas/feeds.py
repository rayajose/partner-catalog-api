from enum import Enum
from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime

class FeedStatus(str, Enum):
    uploaded = "uploaded"
    validating = "validating"
    validated = "validated"
    failed = "failed"

class FeedResponse(BaseModel):
    feed_id: str
    partner_name: str
    file_name: str
    content_type: str
    status: str
    uploaded_at: datetime
    validation_job_id: Optional[str] = None
    validation_status: Optional[str] = None
    validation_message: Optional[str] = None
    raw_file_s3_key: Optional[str] = None
    raw_file_bucket: Optional[str] = None

class FeedCreateResponse(BaseModel):
    feed_id: str
    job_id: str
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "feed_id": "FD00001",
                    "job_id": "JS00001",
                    "status": "uploaded",
                    "products_ingested": 3
                }
            ]
        }
    }



class FeedListResponse(BaseModel):
    items: list[FeedResponse]
    total: int
    limit: int
    offset: int