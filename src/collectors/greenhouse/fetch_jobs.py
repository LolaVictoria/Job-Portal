
"""Fetch public job listings from a Greenhouse job board."""

import requests

BASE_URL = "https://boards-api.greenhouse.io/v1/boards"
########################################
# Source adapters
##########################################
def fetch_jobs(board_token: str) -> list[dict]:
    """Return published jobs from a company's public Greenhouse board."""
    url = f"{BASE_URL}/{board_token}/jobs"
    response = requests.get(
        url,
        timeout=20,
        headers={"User-Agent": "PeronalJobAlerts/1.0"},
    )
    response.raise_for_status()
    data = response.json()
    return data
