"""Fetch public jobs from a Workable job board."""

import requests

BASE_URL = "https://apply.workable.com/api/v1/widget/accounts"


def fetch_jobs(board_token: str) -> list[dict]:
    """Return published jobs from a Workable board."""
    url = f"{BASE_URL}/{board_token}"

    response = requests.get(
        url,
        headers={"User-Agent": "PersonalJobAlerts/1.0"},
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("jobs", [])