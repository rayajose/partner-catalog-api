from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from schemas.common import ErrorResponse
from schemas.jobs import JobResponse

from security import require_api_key

router = APIRouter(
    tags=["Jobs"],
    dependencies=[Depends(require_api_key)]
)

from store import jobs

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
    responses={404: {"model": ErrorResponse, "description": "Job not found"}}, summary="Get job status",
description="Returns the current status and details of a processing job."
)
def get_job(job_id: str):
    job = jobs.get(job_id)
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