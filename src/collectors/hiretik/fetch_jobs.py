
"""Fetch and normalize jobs from HireTik's public API."""

import requests

BASE_URL = "https://hiretik.com/api/v1/jobs"
PER_PAGE = 100
MAX_PAGES = 5


def fetch_jobs(max_pages: int = MAX_PAGES) -> list[dict]:
    """Fetch up to 500 jobs, using pagination."""
    jobs = []

    for page in range(1, max_pages + 1):
        response = requests.get(
            BASE_URL,
            params={"page": page, "per_page": PER_PAGE},
            timeout=30,
        )
        response.raise_for_status()
        page_jobs = response.json().get("jobs", [])

        if not page_jobs:
            break

        jobs.extend(page_jobs)

    return jobs


def normalize_job(job: dict) -> dict:
    """Convert a HireTik listing into our standard job format."""
    offices = job.get("offices") or []
    location_parts = [
        job.get("work_arrangement"),
        *offices,
        job.get("country"),
        job.get("geo_restriction"),
    ]
    location = ", ".join(
        dict.fromkeys(
            str(part).strip()
            for part in location_parts
            if part and str(part).strip()
        )
    )

    return {
        "source": "hiretik",
        "source_job_id": str(job["id"]),
        "company": job.get("company_name", "Unknown"),
        "title": job.get("title", ""),
        "location": location,
        "url": job.get("apply_url", ""),
        "seniority": job.get("seniority", ""),
        "geo_restriction": job.get("geo_restriction", ""),
        "visa_sponsorship": job.get("visa_sponsorship"),
    }


if __name__ == "__main__":
    raw_jobs = fetch_jobs()
    normalized_jobs = [normalize_job(job) for job in raw_jobs]
    print(f"Jobs fetched: {len(normalized_jobs)}")
    print("Sample:", normalized_jobs[0] if normalized_jobs else "No jobs found")
