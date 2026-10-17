
import csv
from pathlib import Path

from src.collectors.greenhouse.fetch_jobs import (
    fetch_jobs as fetch_greenhouse_jobs,
)
from src.collectors.greenhouse.normalize_job import (
    normalize_job as normalize_greenhouse_job,
)
from src.collectors.lever.fetch_jobs import (
    fetch_jobs as fetch_lever_jobs,
)
from src.collectors.lever.normalize_job import (
    normalize_job as normalize_lever_job,
)
from src.collectors.hiretik.fetch_jobs import (
    fetch_jobs as fetch_hiretik_jobs,
    normalize_job as normalize_hiretik_job,
)
from src.collectors.workday.fetch_jobs import (
    fetch_jobs as fetch_workday_jobs,
)
from src.collectors.workday.normalize_job import (
    normalize_job as normalize_workday_job,
)

from src.matching.roles import matches_role
from src.matching.locations import matches_location_or_remote
from src.storage.database import initialize_database, save_job


COMPANIES_FILE = (
    Path(__file__).resolve().parents[1] / "data" / "companies.csv"
)


def load_companies():
    """Load enabled companies from the CSV registry."""
    with COMPANIES_FILE.open(encoding="utf-8-sig", newline="") as file:
        companies = list(csv.DictReader(file))

    return [
        company
        for company in companies
        if company["enabled"].strip().lower() == "true"
    ]


def process_jobs(jobs):
    """Filter jobs, save new matches, and report results."""
    matching_jobs = [
        job
        for job in jobs
        if matches_role(job["title"])
        and matches_location_or_remote(job["location"])
    ]

    new_jobs = [job for job in matching_jobs if save_job(job)]

    print(f"Matching jobs: {len(matching_jobs)}")
    print(f"New jobs saved: {len(new_jobs)}")
    print(f"Previously saved: {len(matching_jobs) - len(new_jobs)}")


def main():
    initialize_database()

    # Greenhouse and Lever
    for company in load_companies():
        source_type = company["source_type"].strip().lower()
        company_name = company["company_name"].strip()
        board_token = company["board_token"].strip()
        if source_type not in ("greenhouse", "lever"):
            continue
        if not board_token:
            print(f"Skipping {company_name}: missing board token")
            continue

        print(f"\nChecking {company_name} ({source_type})")

        try:
            if source_type == "greenhouse":
                raw_jobs = fetch_greenhouse_jobs(board_token)
                normalized_jobs = [
                    normalize_greenhouse_job(job) for job in raw_jobs
                ]

            elif source_type == "lever":
                raw_jobs = fetch_lever_jobs(board_token)
                normalized_jobs = [
                    normalize_lever_job(job, company_name)
                    for job in raw_jobs
                ]

            else:
                print(f"Unsupported source: {source_type}")
                continue

            print(f"Jobs fetched: {len(raw_jobs)}")
            process_jobs(normalized_jobs)

        except Exception as error:
            print(f"Could not fetch {company_name}: {error}")

    # HireTik
    print("\nChecking HireTik")

    try:
        raw_jobs = fetch_hiretik_jobs()
        normalized_jobs = [
            normalize_hiretik_job(job) for job in raw_jobs
        ]

        excluded_seniority = (
            "senior", "staff", "principal", "lead", "director",
            "manager", "executive", "head", "vice president",
            "c-level", "vp",
        )

        eligible_jobs = [
            job
            for job in normalized_jobs
            if not any(
                level in (job.get("seniority") or "").lower()
                for level in excluded_seniority
            )
        ]

        print(f"Jobs fetched: {len(raw_jobs)}")
        process_jobs(eligible_jobs)

    except Exception as error:
        print(f"Could not fetch HireTik: {error}")

    # Workday employers
    # Workday employers
for company in load_companies():
    if company["source_type"].strip().lower() != "workday":
        continue

    company_name = company["company_name"].strip()
    tenant = company["tenant"].strip()
    site = company["site"].strip()
    domain = company["domain"].strip()

    print(f"\nChecking {company_name} (workday)")

    try:
        raw_jobs = fetch_workday_jobs(
            tenant=tenant,
            site=site,
            domain=domain,
        )

        normalized_jobs = [
            normalize_workday_job(
                job,
                company_name=company_name,
                tenant=tenant,
                site=site,
                domain=domain,
            )
            for job in raw_jobs
        ]

        print(f"Jobs fetched: {len(raw_jobs)}")
        process_jobs(normalized_jobs)

    except Exception as error:
        print(f"Could not fetch {company_name}: {error}")
if __name__ == "__main__":
    main()
