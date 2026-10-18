"""Fetch public jobs from a Rippling ATS board."""

import requests

BASE_URL = (
    "https://api.rippling.com/platform/api/ats/v1/board/{}/jobs"
)


def fetch_jobs(board_token: str) -> list[dict]:
    """Return published jobs from a Rippling board."""
    url = BASE_URL.format(board_token)

    response = requests.get(
        url,
        headers={"User-Agent": "PersonalJobAlerts/1.0"},
        timeout=20,
    )
    response.raise_for_status()

    data = response.json()

    if not isinstance(data, list):
        raise ValueError("Unexpected Rippling jobs response format")

    return data