TARGET_ROLES = [
    "frontend engineer",
    "software engineer",
    "graduate software engineer",
    "junior backend engineer",
    "backend engineer",
    "full stack engineer",
    "full-stack engineer",
    "technical writer",
    "project manager",
]

SENIORITY_EXCLUSIONS = [
    "senior",
    "sr.",
    "staff",
    "principal",
    "lead",
    "director",
    "head of",
    "head,",
    "vice president",
    "vp ",
    " vp",
    "distinguished",
]


def matches_role(job_title: str) -> bool:
    """Check whether a job title matches our target roles and level."""
    title = job_title.lower().strip()

    matches_target_role = any(
        role in title for role in TARGET_ROLES
    )

    is_too_senior = any(
        level in title for level in SENIORITY_EXCLUSIONS
    )

    return matches_target_role and not is_too_senior