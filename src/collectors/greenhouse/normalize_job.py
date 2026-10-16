
"""normalize public job listings from a Greenhouse job board into a consistent job model."""

BASE_URL = "https://boards-api.greenhouse.io/v1/boards"


###################################
# Normalization and validation
####################################
def normalize_job(job: dict) -> dict:
    """Convert a raw Greenhouse job into our standard job format."""
    return {
        "source": "greenhouse",
        "source_job_id": str(job["id"]),
        "company": job["company_name"],
        "title": job["title"],
        "location": job["location"]["name"],
        "url": job["absolute_url"],
    }