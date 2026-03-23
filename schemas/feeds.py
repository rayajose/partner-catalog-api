from enum import Enum
from typing import Optional
from pydantic import BaseModel

class FeedStatus(str, Enum):
    uploaded = "uploaded"
    validating = "validating"
    validated = "validated"
    failed = "failed"

class FeedCreateRequest(BaseModel):
    partner_name: str
    file_name: str
    submitted_by: str
    notes: Optional[str] = None

class FeedCreateResponse(BaseModel):
    feed_id: str
    status: FeedStatus
    job_id: str

class FeedResponse(BaseModel):
    feed_id: str
    partner_name: str
    file_name: str
    status: FeedStatus

class FeedListResponse(BaseModel):
    items: list[FeedResponse]
    total: int
    limit: int
    offset: int