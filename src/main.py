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
from src.matching.roles import matches_role
from src.matching.locations import matches_location_or_remote
from src.storage.database import (
    initialize_database,
    save_job,
    get_saved_jobs,
)
import csv
from pathlib import Path

COMPANIES_FILE = Path(__file__).resolve().parents[1] / "data" / "companies.csv"


def load_companies():
    """Load enabled companies from the CSV registry."""
    with COMPANIES_FILE.open(encoding="utf-8-sig", newline="") as file:
        companies = list(csv.DictReader(file))

    return [
        company for company in companies
        if company["enabled"].strip().lower() == "true"
    ]


def main():
    initialize_database()

    total_matching = 0
    total_new = 0

    companies = load_companies()

    for company in companies:
        source_type = company["source_type"].strip().lower()
        company_name = company["company_name"].strip()
        board_token = company["board_token"].strip()

        if not board_token:
            print(f"Skipping {company_name}: missing board token")
            continue

        print(f"\nChecking {company_name} ({source_type})")

        try:
            if source_type == "greenhouse":
                result = fetch_greenhouse_jobs(board_token)
                raw_jobs = result["jobs"]

                normalized_jobs = [
                    normalize_greenhouse_job(job)
                    for job in raw_jobs
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

            matching_jobs = [
                job for job in normalized_jobs
                if matches_role(job["title"])
                and matches_location_or_remote(job["location"])
            ]

            new_jobs = [
                job for job in matching_jobs
                if save_job(job)
            ]

            total_matching += len(matching_jobs)
            total_new += len(new_jobs)

            print(f"Matching jobs: {len(matching_jobs)}")
            print(f"New jobs saved: {len(new_jobs)}")
            print(
                f"Previously saved: "
                f"{len(matching_jobs) - len(new_jobs)}"
            )

        except Exception as error:
            print(f"Could not fetch {company_name}: {error}")
   

if __name__ == "__main__":
    main()