
import csv
from pathlib import Path

from src.collectors.verify_board import verify_board

ROOT = Path(__file__).resolve().parents[2]
CANDIDATES_FILE = ROOT / "data" / "board_candidates.csv"
COMPANIES_FILE = ROOT / "data" / "companies.csv"


def main():
    with CANDIDATES_FILE.open(encoding="utf-8-sig", newline="") as file:
        candidates = list(csv.DictReader(file))

    with COMPANIES_FILE.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        fieldnames = reader.fieldnames
        companies = list(reader)

    existing = {
        (row["source_type"].strip().lower(),
         row["board_token"].strip().lower())
        for row in companies
    }

    added = 0

    for candidate in candidates:
        name = candidate["company_name"].strip()
        source = candidate["source_type"].strip().lower()
        token = candidate["board_token"].strip()

        if (source, token.lower()) in existing:
            print(f"Already registered: {name}")
            continue

        print(f"\nChecking {name}...")
        if verify_board(source, token):
            careers_url = (
                f"https://job-boards.greenhouse.io/{token}"
                if source == "greenhouse"
                else f"https://jobs.lever.co/{token}"
            )

            companies.append({
                "company_name": name,
                "source_type": source,
                "board_token": token,
                "careers_url": careers_url,
                "enabled": "true",
            })
            existing.add((source, token.lower()))
            added += 1
            print(f"Added: {name}")

    with COMPANIES_FILE.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(companies)

    print(f"\nNew companies added: {added}")


if __name__ == "__main__":
    main()
