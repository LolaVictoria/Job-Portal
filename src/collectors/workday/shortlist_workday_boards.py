import csv

SOURCE = "data/verified_workday_boards.csv"
OUTPUT = "data/shortlisted_workday_boards.csv"

keywords = [
    "adobe", "salesforce", "cisco", "nvidia", "bloomberg",
    "crowdstrike", "autodesk", "broadcom", "snyk", "zoom",
    "zendesk", "expedia", "blackrock", "servicenow", "intuit",
    "intel", "amd", "qualcomm", "dell", "hewlett", "hp",
    "ibm", "sap", "siemens", "ericsson", "nokia", "bosch",
    "accenture", "deloitte", "ey", "pwc", "kpmg",
    "mastercard", "visa", "capitalone", "barclays",
    "deutschebank", "ubs", "allianz", "abb", "3m",
    "spotify", "netflix", "tiktok", "microsoft",
]

with open(SOURCE, newline="", encoding="utf-8-sig") as f:
    rows = list(csv.DictReader(f))

matches = [
    row for row in rows
    if any(word in row["company_name"].lower() for word in keywords)
]

seen = set()
unique = []
for row in matches:
    key = row["careers_url"].rstrip("/").lower()
    if key not in seen:
        seen.add(key)
        unique.append(row)

with open(OUTPUT, "w", newline="", encoding="utf-8-sig") as f:
    writer = csv.DictWriter(f, fieldnames=rows[0].keys())
    writer.writeheader()
    writer.writerows(unique)

print("Shortlisted boards:", len(unique))
print("Saved to:", OUTPUT)
for row in unique[:40]:
    print(row["company_name"], "-", row["careers_url"])
