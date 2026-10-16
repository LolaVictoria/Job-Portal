from src.storage.database import get_pending_jobs
from src.notifications.email_digest import build_email_digest


def prepare_digest():
    """Prepare an email digest from pending jobs."""
    jobs = get_pending_jobs()

    if not jobs:
        print("No pending jobs to notify.")
        return None

    subject, body = build_email_digest(jobs)

    return {
        "job_ids": [job["id"] for job in jobs],
        "subject": subject,
        "body": body,
    }


if __name__ == "__main__":
    digest = prepare_digest()

    if digest:
        print("Subject:", digest["subject"])
        print("Jobs included:", len(digest["job_ids"]))
        print(digest["body"])