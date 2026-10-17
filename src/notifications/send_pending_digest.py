from src.storage.database import (
    get_pending_outbox_jobs,
    mark_outbox_as_sent,
    record_outbox_failure,
)
from src.notifications.email_digest import build_email_digest
from src.notifications.send_email import send_email


def send_pending_digest():
    """Send a digest for pending outbox entries."""
    jobs = get_pending_outbox_jobs()

    if not jobs:
        print("No pending outbox entries.")
        return

    outbox_ids = [job["outbox_id"] for job in jobs]

    try:
        subject, body = build_email_digest(jobs)
        send_email(subject, body)

        mark_outbox_as_sent(outbox_ids)
        print(f"Digest sent. Jobs notified: {len(jobs)}")

    except Exception as error:
        record_outbox_failure(outbox_ids, str(error))
        print(f"Digest failed. Entries remain pending: {error}")


if __name__ == "__main__":
    send_pending_digest()