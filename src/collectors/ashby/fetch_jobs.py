"""Fetch public jobs from an Ashby job board."""

import requests


BASE_URL = "https://api.ashbyhq.com/posting-api/job-board"


def fetch_jobs(board_token: str) -> list[dict]:
    """Return published jobs from an Ashby board."""
    url = f"{BASE_URL}/{board_token}"

    response = requests.get(
        url,
        headers={"User-Agent": "PersonalJobAlerts/1.0"},
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("jobs", [])