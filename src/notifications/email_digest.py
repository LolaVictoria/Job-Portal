def build_email_digest(jobs: list[dict]) -> tuple[str, str]:
    """Build an email subject and body from pending jobs."""
    subject = f"Job Alerts: {len(jobs)} new matching jobs"

    if not jobs:
        return "Job Alerts: No new jobs", "No new matching jobs were found."

    lines = ["Here are your new matching jobs:\n"]

    for job in jobs:
        lines.extend([
            f"Role: {job['title']}",
            f"Company: {job['company']}",
            f"Location: {job['location']}",
            f"Apply: {job['url']}",
            "",
        ])

    body = "\n".join(lines)
    return subject, body