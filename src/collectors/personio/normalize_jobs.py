"""Normalize Personio jobs into the shared job format."""


def normalize_job(
    job: dict,
    company_name: str,
    careers_url: str,
) -> dict:
    """Convert a Personio position to the shared format."""
    offices = [
        job.get("office", ""),
        job.get("additionalOffices", ""),
    ]

    location = " | ".join(
        value.strip()
        for value in offices
        if value and value.strip()
    ) or "Location unspecified"

    job_id = str(job.get("id") or "")
    base_url = careers_url.rstrip("/")

    url = f"{base_url}/job/{job_id}?language=en" if job_id else base_url

    is_remote = "remote" in location.lower()

    return {
        "source": "personio",
        "source_job_id": job_id,
        "company": job.get("subcompany") or company_name,
        "title": job.get("name") or "",
        "location": location,
        "url": url,
        "is_remote": is_remote,
        "workplace_type": "remote" if is_remote else "unknown",
        "location_eligibility": "UNVERIFIED",
    }