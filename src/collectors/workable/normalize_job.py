"""Normalize Workable jobs into the shared job format."""


def normalize_job(job: dict, company_name: str) -> dict:
    """Convert a Workable posting into our standard job model."""
    locations = []

    for item in job.get("locations") or []:
        parts = [
            item.get("city"),
            item.get("region"),
            item.get("country"),
        ]
        location = ", ".join(
            part for part in parts if part
        )
        if location and location not in locations:
            locations.append(location)

    if not locations:
        parts = [
            job.get("city"),
            job.get("state"),
            job.get("country"),
        ]
        location = ", ".join(part for part in parts if part)
        if location:
            locations.append(location)

    telecommuting = job.get("telecommuting") is True
    location = " | ".join(locations) or "Location unspecified"

    # Telecommuting alone doesn't confirm worldwide eligibility.
    location_eligibility = (
        "UNVERIFIED" if telecommuting else "CHECK_LISTING"
    )

    return {
        "source": "workable",
        "source_job_id": str(
            job.get("shortcode") or job.get("url", "")
        ),
        "company": company_name,
        "title": job.get("title") or "",
        "location": location,
        "url": job.get("application_url") or job.get("url") or "",
        "is_remote": telecommuting,
        "workplace_type": "remote" if telecommuting else "unknown",
        "location_eligibility": location_eligibility,
    }