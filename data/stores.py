from __future__ import annotations

from datetime import datetime, timezone
from typing import Any, Optional

from db import get_connection


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def next_id(prefix: str) -> str:
    with get_connection() as conn:
        row = conn.execute(
            "SELECT last_value FROM id_counters WHERE prefix = ?",
            (prefix,)
        ).fetchone()

        if row is None:
            new_value = 1
            conn.execute(
                "INSERT INTO id_counters (prefix, last_value) VALUES (?, ?)",
                (prefix, new_value)
            )
        else:
            new_value = row["last_value"] + 1
            conn.execute(
                "UPDATE id_counters SET last_value = ? WHERE prefix = ?",
                (new_value, prefix)
            )

        conn.commit()

    return f"{prefix}{new_value:03d}"


def next_feed_id() -> str:
    return next_id("FD")


def next_submission_job_id() -> str:
    return next_id("JS")


def next_validation_job_id() -> str:
    return next_id("JV")


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
        conn.execute("""
            INSERT INTO feeds (
                feed_id,
                partner_name,
                filename,
                content_type,
                status,
                uploaded_at,
                validation_job_id
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
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
            "SELECT * FROM feeds WHERE feed_id = ?",
            (feed_id,)
        ).fetchone()

    return dict(row) if row else None


def update_feed_status(
    feed_id: str,
    status: str,
    validation_job_id: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        if validation_job_id is None:
            conn.execute("""
                UPDATE feeds
                SET status = ?
                WHERE feed_id = ?
            """, (status, feed_id))
        else:
            conn.execute("""
                UPDATE feeds
                SET status = ?, validation_job_id = ?
                WHERE feed_id = ?
            """, (status, validation_job_id, feed_id))

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
        conn.execute("""
            INSERT INTO jobs (
                job_id,
                job_type,
                status,
                created_at,
                feed_id,
                message
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
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
            "SELECT * FROM jobs WHERE job_id = ?",
            (job_id,)
        ).fetchone()

    return dict(row) if row else None


def update_job_status(
    job_id: str,
    status: str,
    message: Optional[str] = None,
) -> Optional[dict[str, Any]]:
    with get_connection() as conn:
        conn.execute("""
            UPDATE jobs
            SET status = ?, message = ?
            WHERE job_id = ?
        """, (status, message, job_id))
        conn.commit()

    return get_job(job_id)

def map_feed_to_response(feed: dict[str, Any]) -> dict[str, Any]:
    return {
        "feed_id": feed["feed_id"],
        "partner_name": feed["partner_name"],
        "file_name": feed["filename"],
        "content_type": feed["content_type"],
        "uploaded_at": feed["uploaded_at"],
        "status": feed["status"],
        "validation_job_id": feed["validation_job_id"],
    }
