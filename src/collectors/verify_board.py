import requests


def verify_board(source_type: str, board_token: str) -> bool:
    try:
        if source_type == "lever":
            url = f"https://api.lever.co/v0/postings/{board_token}"
            response = requests.get(
                url, params={"mode": "json"}, timeout=15
            )
        elif source_type == "greenhouse":
            url = (
                "https://boards-api.greenhouse.io/v1/boards/"
                f"{board_token}/jobs"
            )
            response = requests.get(url, timeout=15)
        else:
            print(f"Unsupported source: {source_type}")
            return False

        if response.status_code != 200:
            print(f"HTTP {response.status_code}: board not verified")
            return False

        data = response.json()
        jobs = data if source_type == "lever" else data.get("jobs", [])

        print(f"Board verified. Current postings: {len(jobs)}")
        return True

    except (requests.RequestException, ValueError) as error:
        print(f"Verification failed: {error}")
        return False


if __name__ == "__main__":
    source = input("Source (lever/greenhouse): ").strip().lower()
    token = input("Board token: ").strip()
    verify_board(source, token)