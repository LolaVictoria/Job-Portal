import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "jobs.db"


def initialize_database():
    """Create the jobs table if it doesn't exist."""
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                source TEXT NOT NULL,
                source_job_id TEXT NOT NULL,
                company TEXT NOT NULL,
                title TEXT NOT NULL,
                location TEXT NOT NULL,
                url TEXT NOT NULL,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(source, source_job_id)
            )
        """)

        columns = connection.execute(
            "PRAGMA table_info(jobs)"
        ).fetchall()

        column_names = [column[1] for column in columns]

        if "notification_status" not in column_names:
            connection.execute("""
                ALTER TABLE jobs
                ADD COLUMN notification_status TEXT NOT NULL
                DEFAULT 'PENDING'
            """)

        connection.commit()
    finally:
        connection.close()


def save_job(job: dict) -> bool:
    """Save a job and return True only if it is new."""
    connection = sqlite3.connect(DB_PATH)

    try:
        cursor = connection.execute("""
            INSERT OR IGNORE INTO jobs (
                source,
                source_job_id,
                company,
                title,
                location,
                url
            )
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            job["source"],
            job["source_job_id"],
            job["company"],
            job["title"],
            job["location"],
            job["url"],
        ))

        connection.commit()

        return cursor.rowcount == 1
    finally:
        connection.close()
        
        
def get_saved_jobs() -> list[dict]:
    """Return all jobs currently stored in the database."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute("""
            SELECT *
            FROM jobs
            ORDER BY created_at DESC
        """).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()

def get_pending_jobs() -> list[dict]:
    """Return jobs awaiting notification."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute("""
            SELECT *
            FROM jobs
            WHERE notification_status = 'PENDING'
            ORDER BY created_at ASC
        """).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()
        
def mark_job_as_sent(job_id: int) -> None:
    """Mark a job as successfully notified."""
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            UPDATE jobs
            SET notification_status = 'SENT'
            WHERE id = ?
        """, (job_id,))
        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_notification_status
            ON jobs(notification_status)
        """)
        connection.commit()
    finally:
        connection.close()