"""Fetch public jobs from a Personio XML feed."""

import xml.etree.ElementTree as ET

import requests


BASE_URL = "https://{}.jobs.personio.de/xml?language=en"


def fetch_jobs(board_token: str) -> list[dict]:
    """Return positions from a Personio public XML feed."""
    url = BASE_URL.format(board_token)

    response = requests.get(
        url,
        headers={"User-Agent": "PersonalJobAlerts/1.0"},
        timeout=20,
    )
    response.raise_for_status()

    root = ET.fromstring(response.content)
    jobs = []

    for position in root.findall(".//position"):
        job = {
            child.tag: "".join(child.itertext()).strip()
            for child in position
        }
        jobs.append(job)

    return jobs