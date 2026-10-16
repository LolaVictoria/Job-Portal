import requests


def fetch_jobs(board_token: str) -> list[dict]:
    """Fetch public job postings from a Lever company board."""
    url = f"https://api.lever.co/v0/postings/{board_token}"

    response = requests.get(
        url,
        params={"mode": "json"},
        timeout=30,
    )
    response.raise_for_status()

    jobs = response.json()

    if not isinstance(jobs, list):
        raise ValueError("Unexpected response from Lever API")

    return jobs