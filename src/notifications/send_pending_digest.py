from src.storage.database import get_pending_jobs, mark_job_as_sent
from src.notifications.email_digest import build_email_digest
from src.notifications.send_email import send_email


def send_pending_digest():
    """Email all pending jobs and mark them as sent."""
    jobs = get_pending_jobs()

    if not jobs:
        print("No pending jobs to notify.")
        return

    subject, body = build_email_digest(jobs)

    send_email(subject, body)

    for job in jobs:
        mark_job_as_sent(job["id"])

    print(f"Digest sent. Jobs notified: {len(jobs)}")


if __name__ == "__main__":
    send_pending_digest()