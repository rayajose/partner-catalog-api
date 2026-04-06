from __future__ import annotations

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).resolve().parent / "partner_catalog.db"


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db() -> None:
    with get_connection() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS id_counters (
                prefix TEXT PRIMARY KEY,
                last_value INTEGER NOT NULL
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS feeds (
                feed_id TEXT PRIMARY KEY,
                partner_name TEXT NOT NULL,
                file_name TEXT NOT NULL,
                content_type TEXT NOT NULL,
                status TEXT NOT NULL,
                uploaded_at TEXT NOT NULL,
                validation_job_id TEXT
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id TEXT PRIMARY KEY,
                job_type TEXT NOT NULL,
                status TEXT NOT NULL,
                created_at TEXT NOT NULL,
                feed_id TEXT NOT NULL,
                message TEXT,
                FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
            )
        """)

        conn.commit()