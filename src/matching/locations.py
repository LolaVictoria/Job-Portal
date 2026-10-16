#####################################################
#  checks countries, cities, and remote eligibility.
#####################################################

EUROPEAN_LOCATIONS = [
    "united kingdom",
    "ireland",
    "germany",
    "netherlands",
    "france",
    "spain",
    "portugal",
    "italy",
    "sweden",
    "norway",
    "denmark",
    "finland",
    "belgium",
    "austria",
    "switzerland",
    "poland",
    "czech republic",
    "czechia",
    "luxembourg",
    "estonia",
    "latvia",
    "lithuania",
    "romania",
    "bulgaria",
    "greece",
    "croatia",
    "slovakia",
    "slovenia",
    "hungary",
    "iceland",
    "london",
    "stockholm",
]

CANADIAN_LOCATIONS = [
    "canada",
    "ontario",
    "british columbia",
    "alberta",
    "quebec",
    "manitoba",
    "saskatchewan",
    "nova scotia",
    "new brunswick",
    "newfoundland and labrador",
    "prince edward island",
    "northwest territories",
    "nunavut",
    "yukon",
]

TARGET_LOCATIONS = EUROPEAN_LOCATIONS + CANADIAN_LOCATIONS



def matches_location(location: str) -> bool:
    """Return True if a job location matches our target regions."""
    normalized_location = location.lower()

    return any(
        target in normalized_location
        for target in TARGET_LOCATIONS
    )


def is_remote(location: str) -> bool:
    """Identify locations that suggest remote or location-independent work."""
    normalized_location = location.lower()

    remote_keywords = [
        "remote",
        "anywhere in",
        "work from home",
        "distributed",
    ]

    return any(
        keyword in normalized_location
        for keyword in remote_keywords
    )

def matches_location_or_remote(location: str) -> bool:
    """Match preferred locations or any advertised remote role."""
    return matches_location(location) or is_remote(location)
