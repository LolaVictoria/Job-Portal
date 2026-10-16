def normalize_job(job: dict, company_name: str) -> dict:
    """Convert a Lever posting into our standard job format."""
    categories = job.get("categories") or {}

    return {
        "source": "lever",
        "source_job_id": str(job["id"]),
        "company": company_name,
        "title": job["text"],
        "location": categories.get("location") or "Not specified",
        "url": job["hostedUrl"],
    }