from src.collectors.greenhouse.fetch_jobs import fetch_jobs
from src.collectors.greenhouse.normalize_job import normalize_job
from src.matching.roles import matches_role
from src.matching.locations import matches_location_or_remote
from src.storage.database import (
    initialize_database,
    save_job,
    get_saved_jobs,
)


GREENHOUSE_BOARDS = ["greenhouse"]


def main():
    initialize_database()

    total_matching = 0
    total_new = 0

    for board_token in GREENHOUSE_BOARDS:
        print(f"\nChecking Greenhouse board: {board_token}")

        try:
            result = fetch_jobs(board_token)
            jobs = [normalize_job(job) for job in result["jobs"]]

            matching_jobs = [
                job for job in jobs
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
            print(f"Could not fetch {board_token}: {error}")

    print(f"\nTotal matching jobs: {total_matching}")
    print(f"Total new jobs saved: {total_new}")
    print(f"Total jobs in database: {len(get_saved_jobs())}")


if __name__ == "__main__":
    main()