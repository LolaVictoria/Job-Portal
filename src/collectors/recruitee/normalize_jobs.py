"""Normalize Recruitee jobs into the shared job format."""


def normalize_job(job: dict, company_name: str) -> dict:
    """Convert a Recruitee offer to the shared format."""
    locations = job.get("locations") or []

    if isinstance(locations, list):
        location_names = [
            item if isinstance(item, str)
            else item.get("location") or item.get("city") or ""
            for item in locations
        ]
    else:
        location_names = []

    location = (
        " | ".join(name for name in location_names if name)
        or job.get("location")
        or ", ".join(
            part for part in [
                job.get("city"),
                job.get("state_name"),
                job.get("country"),
            ]
            if part
        )
        or "Location unspecified"
    )

    is_remote = (
        job.get("remote") is True
        or job.get("location") == "Remote job"
    )

    return {
        "source": "recruitee",
        "source_job_id": str(job.get("id") or job.get("guid") or ""),
        "company": company_name,
        "title": job.get("title") or "",
        "location": location,
        "url": job.get("careers_url")
        or job.get("careers_apply_url")
        or "",
        "is_remote": is_remote,
        "workplace_type": (
            "remote" if is_remote
            else "hybrid" if job.get("hybrid")
            else "unknown"
        ),
        "location_eligibility": (
            "UNVERIFIED" if is_remote else "CHECK_LISTING"
        ),
    }