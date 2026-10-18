"""Normalize Ashby jobs into the shared job format."""


def normalize_job(job: dict, company_name: str) -> dict:
    """Convert an Ashby posting to our standard job model."""
    locations = []

    primary = job.get("location")
    if primary:
        locations.append(primary)

    for item in job.get("secondaryLocations") or []:
        location = item.get("location")
        if location and location not in locations:
            locations.append(location)

    workplace_type = (job.get("workplaceType") or "").strip().lower()
    remote_flag = job.get("isRemote")

    # Missing workplace type means we cannot reliably tell
    # whether this is remote or hybrid.
    scope_unverified = (
        remote_flag is True and workplace_type not in ("remote", "hybrid")
    )

    location = " | ".join(locations) or "Location unspecified"

    if scope_unverified:
        location += " (remote/location eligibility unverified)"

    return {
        "source": "ashby",
        "source_job_id": str(job.get("id") or job.get("jobUrl", "")),
        "company": company_name,
        "title": job.get("title") or "",
        "location": location,
        "url": job.get("jobUrl") or job.get("applyUrl") or "",
        "is_remote": workplace_type == "remote",
        "workplace_type": workplace_type or "unknown",
        "location_eligibility": (
            "UNVERIFIED" if scope_unverified else "CHECK_LISTING"
        ),
    }