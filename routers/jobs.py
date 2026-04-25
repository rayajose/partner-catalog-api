from __future__ import annotations

from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from schemas.common import ErrorResponse
from schemas.jobs import JobResponse
from db import get_connection, q, DB_TYPE
from security import require_api_key

router = APIRouter(
    prefix="/jobs",
    tags=["Jobs"],
    dependencies=[Depends(require_api_key)]
)

JOB_COLUMNS = [
    "job_id",
    "job_type",
    "status",
    "created_at",
    "feed_id",
    "message",
]


def job_row_to_dict(row):
    if DB_TYPE == "sqlite":
        return dict(row)
    return dict(zip(JOB_COLUMNS, row))


@router.get(
    "/{job_id}",
    response_model=JobResponse,
    responses={404: {"model": ErrorResponse, "description": "Job not found"}},
    summary="Get job status",
    description=(
        "Retrieves the status of a background job.\n\n"
        "Jobs are created during feed ingestion and ETL processing.\n\n"
        "Possible statuses:\n"
        "- queued\n"
        "- running\n"
        "- completed\n"
        "- failed\n\n"
        "Use this endpoint to monitor processing progress and identify errors."
    )
)
def get_job(job_id: str):
    with get_connection() as conn:
        job = conn.execute(
            q("""
                SELECT
                    job_id,
                    job_type,
                    status,
                    created_at,
                    feed_id,
                    message
                FROM jobs
                WHERE job_id = ?
            """),
            (job_id,)
        ).fetchone()

    if not job:
        return JSONResponse(
            status_code=404,
            content={
                "error_code": "JOB_NOT_FOUND",
                "message": f"Job {job_id} not found",
                "details": {"job_id": job_id},
            },
        )

    return job_row_to_dict(job)