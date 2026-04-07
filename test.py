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

        conn.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id TEXT PRIMARY KEY,
                feed_id TEXT NOT NULL,
                partner_name TEXT NOT NULL,
                sku TEXT,
                product_name TEXT NOT NULL,
                description TEXT,
                brand TEXT,
                category TEXT,
                price REAL,
                currency TEXT,
                availability TEXT,
                created_at TEXT NOT NULL,
                FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
            )
        """)


def _next_id_with_conn(conn: sqlite3.Connection, prefix: str) -> str:
    row = conn.execute(
        "SELECT last_value FROM id_counters WHERE prefix = ?",
        (prefix,)
    ).fetchone()

    if row is None:
        next_value = 1
        conn.execute(
            "INSERT INTO id_counters (prefix, last_value) VALUES (?, ?)",
            (prefix, next_value)
        )
    else:
        next_value = row["last_value"] + 1
        conn.execute(
            "UPDATE id_counters SET last_value = ? WHERE prefix = ?",
            (next_value, prefix)
        )

    return f"{prefix}{next_value:03d}"


def _next_id(prefix: str) -> str:
    with get_connection() as conn:
        return _next_id_with_conn(conn, prefix)


def next_feed_id() -> str:
    return _next_id("FD")


def next_submission_job_id() -> str:
    return _next_id("JS")


def next_validation_job_id() -> str:
    return _next_id("JV")


def next_product_id() -> str:
    return _next_id("PR")


def next_product_id_with_conn(conn: sqlite3.Connection) -> str:
    return _next_id_with_conn(conn, "PR")