"""Normalize Rippling jobs into the shared job format."""


def normalize_job(job: dict, company_name: str) -> dict:
    """Convert a Rippling posting to the shared format."""
    work_location = job.get("workLocation") or {}

    if isinstance(work_location, dict):
        location = work_location.get("label") or ""
    else:
        location = str(work_location or "")

    location = location.strip() or "Location unspecified"

    is_remote = "remote" in location.lower()

    return {
        "source": "rippling",
        "source_job_id": str(job.get("uuid") or ""),
        "company": company_name,
        "title": (job.get("name") or "").strip(),
        "location": location,
        "url": job.get("url") or "",
        "is_remote": is_remote,
        "workplace_type": (
            "remote" if is_remote else "unknown"
        ),
        "location_eligibility": "UNVERIFIED",
    }