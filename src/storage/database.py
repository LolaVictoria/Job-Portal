
import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).resolve().parents[2] / "jobs.db"


def initialize_database():
    """Create the jobs table, outbox table, and indexes."""
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

        connection.execute("""
            CREATE TABLE IF NOT EXISTS email_outbox (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                job_id INTEGER NOT NULL UNIQUE,
                status TEXT NOT NULL DEFAULT 'PENDING',
                attempts INTEGER NOT NULL DEFAULT 0,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                sent_at TEXT,
                last_error TEXT,
                FOREIGN KEY (job_id) REFERENCES jobs(id)
            )
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_outbox_status
            ON email_outbox(status)
        """)

        connection.execute("""
            CREATE INDEX IF NOT EXISTS idx_jobs_notification_status
            ON jobs(notification_status)
        """)

        connection.commit()
    finally:
        connection.close()


def save_job(job: dict) -> bool:
    """Save a new job and its outbox entry atomically."""
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

        if cursor.rowcount == 0:
            connection.commit()
            return False

        job_id = cursor.lastrowid

        connection.execute("""
            INSERT INTO email_outbox (job_id)
            VALUES (?)
        """, (job_id,))

        connection.commit()
        return True

    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def get_saved_jobs() -> list[dict]:
    """Return all saved jobs."""
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
    """Return jobs awaiting notification using the legacy status."""
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
    """Mark a job as notified using the legacy workflow."""
    connection = sqlite3.connect(DB_PATH)

    try:
        connection.execute("""
            UPDATE jobs
            SET notification_status = 'SENT'
            WHERE id = ?
        """, (job_id,))

        connection.commit()
    finally:
        connection.close()


def get_pending_outbox_jobs() -> list[dict]:
    """Return jobs with pending outbox notifications."""
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row

    try:
        rows = connection.execute("""
            SELECT
                email_outbox.id AS outbox_id,
                jobs.id AS job_id,
                jobs.source,
                jobs.source_job_id,
                jobs.company,
                jobs.title,
                jobs.location,
                jobs.url,
                jobs.created_at
            FROM email_outbox
            JOIN jobs ON jobs.id = email_outbox.job_id
            WHERE email_outbox.status = 'PENDING'
            ORDER BY email_outbox.created_at ASC
        """).fetchall()

        return [dict(row) for row in rows]
    finally:
        connection.close()


def mark_outbox_as_sent(outbox_ids: list[int]) -> None:
    """Mark outbox entries and their jobs as sent."""
    if not outbox_ids:
        return

    connection = sqlite3.connect(DB_PATH)

    try:
        placeholders = ",".join("?" for _ in outbox_ids)

        connection.execute(
            f"""
            UPDATE email_outbox
            SET status = 'SENT',
                sent_at = CURRENT_TIMESTAMP,
                last_error = NULL
            WHERE id IN ({placeholders})
            """,
            outbox_ids,
        )

        connection.execute(
            f"""
            UPDATE jobs
            SET notification_status = 'SENT'
            WHERE id IN (
                SELECT job_id
                FROM email_outbox
                WHERE id IN ({placeholders})
            )
            """,
            outbox_ids,
        )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def record_outbox_failure(
    outbox_ids: list[int],
    error: str,
) -> None:
    """Record a failed attempt and leave entries pending for retry."""
    if not outbox_ids:
        return

    connection = sqlite3.connect(DB_PATH)

    try:
        placeholders = ",".join("?" for _ in outbox_ids)

        connection.execute(
            f"""
            UPDATE email_outbox
            SET attempts = attempts + 1,
                last_error = ?
            WHERE id IN ({placeholders})
              AND status = 'PENDING'
            """,
            [error[:1000], *outbox_ids],
        )

        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()
