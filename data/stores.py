from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from db import get_connection, q, DB_TYPE


FEED_COLUMNS = [
    "feed_id",
    "partner_name",
    "file_name",
    "content_type",
    "status",
    "uploaded_at",
    "validation_job_id",
]

JOB_COLUMNS = [
    "job_id",
    "job_type",
    "status",
    "created_at",
    "feed_id",
    "message",
]


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def feed_row_to_dict(row) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    if DB_TYPE == "sqlite":
        return dict(row)
    return dict(zip(FEED_COLUMNS, row))


def job_row_to_dict(row) -> Optional[dict[str, Any]]:
    if row is None:
        return None
    if DB_TYPE == "sqlite":
        return dict(row)
    return dict(zip(JOB_COLUMNS, row))


def create_feed(
    feed_id: str,
    partner_name: str,
    file_name: str,
    content_type: str,
    status: str,
    uploaded_at: str,
    validation_job_id: Optional[str] = None,
) -> dict[str, Any]:
    with get_connection() as conn:
        conn.execute(q("""
            INSERT INTO feeds (
                feed_id,
                partner_name,
                file_name,
                content_type,
                status,
                uploaded_at,
                validation_job_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """), (
            feed_id,
            partner_name,
            file_name,
            content_type,
            status,
            uploaded_at,
            validation_job_id,
        ))
        conn.commit()

    return get_feed(feed_id)


def get_feed(feed_id: str) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
            q("""
                SELECT
                    feed_id,
                    partner_name,
                    file_name,
                    content_type,
                    status,
                    uploaded_at,
                    validation_job_id
                FROM feeds
                WHERE feed_id = ?
            """),
            (feed_id,)
        ).fetchone()

    return feed_row_to_dict(row)


def update_feed_status(
    feed_id: str,
    status: str,
    validation_job_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        if validation_job_id is None:
            conn.execute(q("""
                UPDATE feeds
                SET status = ?
                WHERE feed_id = ?
            """), (status, feed_id))
        else:
            conn.execute(q("""
                UPDATE feeds
                SET status = ?, validation_job_id = ?
                WHERE feed_id = ?
            """), (status, validation_job_id, feed_id))

        conn.commit()

    return get_feed(feed_id)


def create_job(
    job_id: str,
    job_type: str,
    status: str,
    created_at: str,
    feed_id: str,
    message: Optional[str] = None,
) -> dict[str, Any]:
    with get_connection() as conn:
        conn.execute(q("""
            INSERT INTO jobs (
                job_id,
                job_type,
                status,
                created_at,
                feed_id,
                message
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """), (
            job_id,
            job_type,
            status,
            created_at,
            feed_id,
            message,
        ))
        conn.commit()

    return get_job(job_id)


def get_job(job_id: str) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        row = conn.execute(
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

    return job_row_to_dict(row)


def update_job_status(
    job_id: str,
    status: str,
    message: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        conn.execute(q("""
            UPDATE jobs
            SET status = ?, message = ?
            WHERE job_id = ?
        """), (status, message, job_id))
        conn.commit()

    return get_job(job_id)


"""
def map_feed_to_response(feed: dict[str, Any]) -> dict[str, Any]:
    return {
        "feed_id": feed["feed_id"],
        "partner_name": feed["partner_name"],
        "file_name": feed["file_name"],
        "content_type": feed["content_type"],
        "uploaded_at": feed["uploaded_at"],
        "status": feed["status"],
        "validation_job_id": feed["validation_job_id"],
    }
"""