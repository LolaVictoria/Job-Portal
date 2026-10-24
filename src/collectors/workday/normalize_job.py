BASE_URL = "https://nvidia.wd5.myworkdayjobs.com"


def normalize_job(
    job: dict,
    company_name="NVIDIA",
    tenant="nvidia",
    site="NVIDIAExternalCareerSite",
    domain="wd5.myworkdayjobs.com",
) -> dict:
    """Convert a Workday posting into the common job format."""
    job_ids = job.get("bulletFields") or []
    external_path = job.get("externalPath", "")

    url = (
        f"https://{tenant}.{domain}/en-US/{site}{external_path}"
        if external_path else ""
    )

    print("DEBUG Workday externalPath:", external_path)
    print("DEBUG generated URL:", url)

    return {
        "source": "workday",
        "source_job_id": job_ids[0] if job_ids else external_path,
        "company": company_name,
        "title": job.get("title", ""),
        "location": job.get("locationsText", ""),
        "url": url,
    }