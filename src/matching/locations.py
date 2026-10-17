EUROPEAN_LOCATIONS = [
    "united kingdom", "uk", "great britain", "england", "scotland",
    "wales", "northern ireland", "ireland",
    "germany", "netherlands", "france", "spain", "portugal",
    "italy", "sweden", "norway", "denmark", "finland", "belgium",
    "austria", "switzerland", "poland", "czech republic", "czechia",
    "luxembourg", "estonia", "latvia", "lithuania", "romania",
    "bulgaria", "greece", "croatia", "slovakia", "slovenia",
    "hungary", "iceland",
    "london", "manchester", "edinburgh", "glasgow", "birmingham",
    "stockholm", "berlin", "munich", "amsterdam", "paris", "dublin",
]

CANADIAN_LOCATIONS = [
    "canada", "ontario", "british columbia", "alberta", "quebec",
    "manitoba", "saskatchewan", "nova scotia", "new brunswick",
    "newfoundland and labrador", "prince edward island",
    "northwest territories", "nunavut", "yukon", "toronto",
    "vancouver", "montreal", "ottawa", "calgary", "edmonton",
]

TARGET_LOCATIONS = EUROPEAN_LOCATIONS + CANADIAN_LOCATIONS

REMOTE_KEYWORDS = [
    "remote",
    "anywhere in",
    "work from home",
    "distributed",
]


def matches_location(location: str) -> bool:
    """Return True if a job location matches our target regions."""
    normalized_location = (location or "").strip().lower()

    return any(
        target in normalized_location
        for target in TARGET_LOCATIONS
    )


def is_remote(location: str) -> bool:
    """Identify locations that suggest remote work."""
    normalized_location = (location or "").strip().lower()

    return any(
        keyword in normalized_location
        for keyword in REMOTE_KEYWORDS
    )


def matches_location_or_remote(location: str) -> bool:
    """Match target locations or advertised remote roles."""
    return matches_location(location) or is_remote(location)


def classify_remote_scope(location: str) -> str:
    """Classify a remote job's advertised geographic scope."""
    normalized = (location or "").strip().lower()

    if not is_remote(normalized):
        return "not_remote"

    restrictions = {
        "usa": ["usa", "united states", "u.s."],
        "canada": ["canada"],
        "uk": ["united kingdom", "uk"],
        "india": ["india"],
        "brazil": ["brazil"],
        "europe": ["europe", "european union", "eu"],
    }

    for scope, keywords in restrictions.items():
        if any(keyword in normalized for keyword in keywords):
            return f"remote_{scope}"

    return "remote_scope_unspecified"