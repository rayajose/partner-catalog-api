from __future__ import annotations
import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

DB_TYPE = os.getenv("DB_TYPE", "sqlite").lower()

print("DB_TYPE =", DB_TYPE)

# SQLite config
DB_PATH = Path(__file__).resolve().parent / "partner_catalog.db"

# PostgreSQL config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "partner_catalog")
DB_USER = os.getenv("DB_USER", "postgres")
DB_PASSWORD = os.getenv("DB_PASSWORD", "")


def q(sql: str) -> str:
    """
    Convert generic ? placeholders to database-specific placeholders.
    SQLite uses ?, PostgreSQL uses %s.
    """
    if DB_TYPE == "postgres":
        return sql.replace("?", "%s")
    return sql


def get_connection():
    if DB_TYPE == "sqlite":
        # print("USING SQLITE")
        import sqlite3
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn

    if DB_TYPE == "postgres":
        """
        print("USING POSTGRES")
        print("POSTGRES HOST =", DB_HOST)
        print("POSTGRES PORT =", DB_PORT)
        print("POSTGRES DB =", DB_NAME)
        print("POSTGRES USER =", DB_USER)
        """
        import psycopg
        return psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
        )

    raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")


def init_db() -> None:
    with get_connection() as conn:
        if DB_TYPE == "sqlite":
            conn.execute(q("""
                CREATE TABLE IF NOT EXISTS id_counters (
                    prefix TEXT PRIMARY KEY,
                    last_value INTEGER NOT NULL
                )
            """))

            conn.execute(q("""
                CREATE TABLE IF NOT EXISTS feeds (
                    feed_id TEXT PRIMARY KEY,
                    partner_name TEXT NOT NULL,
                    file_name TEXT NOT NULL,
                    content_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    uploaded_at TEXT NOT NULL,
                    validation_job_id TEXT
                )
            """))

            conn.execute(q("""
                CREATE TABLE IF NOT EXISTS jobs (
                    job_id TEXT PRIMARY KEY,
                    job_type TEXT NOT NULL,
                    status TEXT NOT NULL,
                    created_at TEXT NOT NULL,
                    feed_id TEXT NOT NULL,
                    message TEXT,
                    FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
                )
            """))

            conn.execute(q("""
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
            """))

        elif DB_TYPE == "postgres":
            with conn.cursor() as cur:
                cur.execute(q("""
                    CREATE TABLE IF NOT EXISTS id_counters (
                        prefix TEXT PRIMARY KEY,
                        last_value INTEGER NOT NULL
                    )
                """))

                cur.execute(q("""
                    CREATE TABLE IF NOT EXISTS feeds (
                        feed_id TEXT PRIMARY KEY,
                        partner_name TEXT NOT NULL,
                        file_name TEXT NOT NULL,
                        content_type TEXT NOT NULL,
                        status TEXT NOT NULL,
                        uploaded_at TEXT NOT NULL,
                        validation_job_id TEXT
                    )
                """))

                cur.execute(q("""
                    CREATE TABLE IF NOT EXISTS jobs (
                        job_id TEXT PRIMARY KEY,
                        job_type TEXT NOT NULL,
                        status TEXT NOT NULL,
                        created_at TEXT NOT NULL,
                        feed_id TEXT NOT NULL,
                        message TEXT,
                        FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
                    )
                """))

                cur.execute(q("""
                    CREATE TABLE IF NOT EXISTS products (
                        product_id TEXT PRIMARY KEY,
                        feed_id TEXT NOT NULL,
                        partner_name TEXT NOT NULL,
                        sku TEXT,
                        product_name TEXT NOT NULL,
                        description TEXT,
                        brand TEXT,
                        category TEXT,
                        price DOUBLE PRECISION,
                        currency TEXT,
                        availability TEXT,
                        created_at TEXT NOT NULL,
                        FOREIGN KEY (feed_id) REFERENCES feeds(feed_id)
                    )
                """))

            conn.commit()

        else:
            raise ValueError(f"Unsupported DB_TYPE: {DB_TYPE}")


def _next_id_with_conn(conn, prefix: str) -> str:
    if DB_TYPE == "postgres":
        with conn.cursor() as cur:
            cur.execute(
                q("SELECT last_value FROM id_counters WHERE prefix = ?"),
                (prefix,)
            )
            row = cur.fetchone()

            if row is None:
                next_value = 1
                cur.execute(
                    q("INSERT INTO id_counters (prefix, last_value) VALUES (?, ?)"),
                    (prefix, next_value)
                )
            else:
                next_value = row[0] + 1
                cur.execute(
                    q("UPDATE id_counters SET last_value = ? WHERE prefix = ?"),
                    (next_value, prefix)
                )
    else:
        row = conn.execute(
            q("SELECT last_value FROM id_counters WHERE prefix = ?"),
            (prefix,)
        ).fetchone()

        if row is None:
            next_value = 1
            conn.execute(
                q("INSERT INTO id_counters (prefix, last_value) VALUES (?, ?)"),
                (prefix, next_value)
            )
        else:
            next_value = row["last_value"] + 1
            conn.execute(
                q("UPDATE id_counters SET last_value = ? WHERE prefix = ?"),
                (next_value, prefix)
            )

    return f"{prefix}{next_value:05d}"


def _next_id(prefix: str) -> str:
    with get_connection() as conn:
        next_value = _next_id_with_conn(conn, prefix)
        if DB_TYPE == "postgres":
            conn.commit()
        return next_value


def next_feed_id() -> str:
    return _next_id("FD")


def next_submission_job_id() -> str:
    return _next_id("JS")


def next_validation_job_id() -> str:
    return _next_id("JV")


def next_product_id() -> str:
    return _next_id("PR")


def next_product_id_with_conn(conn) -> str:
    return _next_id_with_conn(conn, "PR")