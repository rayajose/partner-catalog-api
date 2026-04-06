from __future__ import annotations
from fastapi import (
    APIRouter,
    #HTTPException,
    Depends,
    #status
)
from fastapi.responses import JSONResponse
from schemas.common import ErrorResponse
from schemas.jobs import JobResponse
from data.stores import get_job as get_job_record
from security import require_api_key

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
    dependencies=[Depends(require_api_key)]
)

@router.get(
    "/{job_id}",
    response_model=JobResponse,
    responses={404: {"model": ErrorResponse, "description": "Job not found"}},
    summary="Get job status",
    description="Returns the current status and details of a processing job."
)
def get_job(job_id: str):
    job = get_job_record(job_id)
    if not job:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": "JOB_NOT_FOUND",
                "message": f"Job {job_id} not found",
                "details": {"job_id": job_id},
            },
        )
    return job