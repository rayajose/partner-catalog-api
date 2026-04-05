from fastapi import APIRouter
#UploadFile, File, Form, HTTPException, status
from datetime import datetime, timezone
from typing import Any

router = APIRouter()

feeds: dict[str, dict[str, Any]] = {}
uploads: dict[str, bytes] = {}
jobs: dict[str, dict[str, Any]] = {}
products: dict[str, dict[str, Any]] = {}

feed_counter = 1
job_submit_counter = 1
job_validate_counter = 1
product_counter = 1

def utc_now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()

def next_feed_id() -> str:
    global feed_counter
    value = f"FD{feed_counter:03d}"
    feed_counter += 1
    return value

def next_submit_job_id() -> str:
    global job_submit_counter
    value = f"JS{job_submit_counter:03d}"
    job_submit_counter += 1
    return value

def next_validate_job_id() -> str:
    global job_validate_counter
    value = f"JV{job_validate_counter:03d}"
    job_validate_counter += 1
    return value

def next_product_id() -> str:
    global product_counter
    value = f"PR{product_counter:03d}"
    product_counter += 1
    return value