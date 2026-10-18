"""Fetch public jobs from a Recruitee career site."""

import requests

BASE_URL = "https://{}.recruitee.com/api/offers/"


def fetch_jobs(board_token: str) -> list[dict]:
    """Return published offers from a Recruitee board."""
    url = BASE_URL.format(board_token)

    response = requests.get(
        url,
        headers={"User-Agent": "PersonalJobAlerts/1.0"},
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()
    return data.get("offers", [])