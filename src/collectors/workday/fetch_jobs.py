
import requests


def fetch_jobs(
    tenant="nvidia",
    site="NVIDIAExternalCareerSite",
    domain="wd5.myworkdayjobs.com",
    limit=20,
    max_jobs=500,
):
    """Fetch public job postings from a Workday career site."""
    base_url = f"https://{tenant}.{domain}"
    jobs_url = f"{base_url}/wday/cxs/{tenant}/{site}/jobs"

    jobs = []
    offset = 0

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "User-Agent": "PersonalJobAlerts/1.0",
    }

    while offset < max_jobs:
        page_size = min(limit, max_jobs - offset)

        response = requests.post(
            jobs_url,
            json={
                "appliedFacets": {},
                "limit": page_size,
                "offset": offset,
                "searchText": "",
            },
            headers=headers,
            timeout=30,
        )

        response.raise_for_status()
        data = response.json()
        batch = data.get("jobPostings", [])

        if not batch:
            break

        jobs.extend(batch)
        offset += len(batch)

        if offset >= data.get("total", 0):
            break

    return jobs
