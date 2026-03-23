from fastapi import APIRouter
from fastapi.responses import JSONResponse

from schemas.common import ErrorResponse
from schemas.jobs import JobResponse

router = APIRouter(tags=["Jobs"])

from store import jobs

@router.get(
    "/jobs/{job_id}",
    response_model=JobResponse,
    responses={404: {"model": ErrorResponse, "description": "Job not found"}}
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