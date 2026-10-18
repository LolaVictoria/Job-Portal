
import csv
from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.parse import urlparse

import requests

DIRECTORY = "data/job-board-directory.csv"
OUTPUT = "data/verified_workday_boards.csv"
BATCH_SIZE = 1362



def test_board(row):
    api_url = row["api_url"].strip()
    board_url = row["board_url"].strip()

    try:
        response = requests.post(
            api_url,
            json={
                "appliedFacets": {},
                "limit": 1,
                "offset": 0,
                "searchText": "",
            },
            headers={
                "Accept": "application/json",
                "Content-Type": "application/json",
                "User-Agent": "PersonalJobAlerts/1.0",
            },
            timeout=15,
        )

        if response.status_code != 200:
            return None

        data = response.json()
        if not isinstance(data.get("jobPostings"), list):
            return None

        from urllib.parse import urlparse

        host_parts = (urlparse(board_url).hostname or "").split(".")
        api_parts = [
            part for part in urlparse(api_url).path.split("/") if part
        ]

        if (
            len(host_parts) < 3
            or len(api_parts) < 5
            or api_parts[0:2] != ["wday", "cxs"]
            or api_parts[4] != "jobs"
        ):
            return None

        return {
            "company_name": row["company"].strip(),
            "source_type": "workday",
            "board_token": "",
            "careers_url": board_url,
            "enabled": "true",
            "tenant": api_parts[2],
            "site": api_parts[3],
            "domain": ".".join(host_parts[1:]),
        }

    except (requests.RequestException, ValueError, KeyError):
        return None


def main():
    with open(DIRECTORY, encoding="utf-8-sig", newline="") as file:
        rows = [
            row for row in csv.DictReader(file)
            if row.get("platform", "").strip().lower() == "workday"
            and row.get("api_url", "").strip()
            and row.get("board_url", "").strip()
        ]

    rows.sort(
        key=lambda row: int(row.get("open_roles") or 0),
        reverse=True,
    )
    batch = rows[:BATCH_SIZE]

    print(f"Workday boards available: {len(rows)}")
    print(f"Testing this batch: {len(batch)}")

    verified = []
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = [executor.submit(test_board, row) for row in batch]
        for future in as_completed(futures):
            result = future.result()
            if result:
                verified.append(result)
                print(f"Verified: {result['company_name']}")

    verified.sort(key=lambda row: row["company_name"].lower())

    with open(OUTPUT, "w", encoding="utf-8", newline="") as file:
        fields = [
            "company_name", "source_type", "board_token",
            "careers_url", "enabled", "tenant", "site", "domain",
        ]
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(verified)

    print(f"\nVerified boards: {len(verified)}")
    print(f"Saved to: {OUTPUT}")


if __name__ == "__main__":
    main()
