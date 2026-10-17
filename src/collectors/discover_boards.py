
import csv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIRECTORY = ROOT / "data" / "ats_directory.csv"
CANDIDATES = ROOT / "data" / "board_candidates.csv"

TARGET_COMPANIES = {
    "adobe", "amazon", "amd", "asana", "atlassian",
    "canva", "canonical", "cloudflare", "databricks",
    "deepmind", "discord", "doordash", "dropbox",
    "figma", "github", "gitlab", "google",
    "hubspot", "indeed", "intercom", "linkedin",
    "meta", "microsoft", "mongodb", "netflix",
    "notion", "nvidia", "openai", "pinterest",
    "reddit", "rippling", "salesforce", "shopify",
    "slack", "snowflake", "stripe", "tiktok",
    "uber", "wise", "workday", "zapier", "zoom",
}


def main():
    with DIRECTORY.open(encoding="utf-8-sig", newline="") as file:
        directory = list(csv.DictReader(file))

    with CANDIDATES.open(encoding="utf-8-sig", newline="") as file:
        reader = csv.DictReader(file)
        candidates = list(reader)
        fields = reader.fieldnames

    existing = {
        (row["source_type"].lower(), row["board_token"].lower())
        for row in candidates
    }

    added = 0

    for row in directory:
        company = row["company_name"].strip()
        vendor = row["ats_vendor"].strip().lower()
        slug = row["board_slug"].strip()

        if company.lower() not in TARGET_COMPANIES:
            continue

        if vendor not in {"greenhouse", "lever"} or not slug:
            continue

        key = (vendor, slug.lower())
        if key in existing:
            continue

        candidates.append({
            "company_name": company,
            "source_type": vendor,
            "board_token": slug,
        })
        existing.add(key)
        added += 1

    with CANDIDATES.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fields)
        writer.writeheader()
        writer.writerows(candidates)

    print(f"New candidates added: {added}")
    print("Run the verifier next to check which boards are valid.")


if __name__ == "__main__":
    main()
