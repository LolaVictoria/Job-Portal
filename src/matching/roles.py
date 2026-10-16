#########################################
#  checks job titles and seniority.
########################################
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
    "vice president",
    "vp ",
    "distinguished",
]


def matches_role(job_title: str) -> bool:
    """Return True if a job matches our target roles and seniority."""
    title = job_title.lower()

    matches_target_role = any(
        role in title for role in TARGET_ROLES
    )

    is_too_senior = any(
        level in title for level in SENIORITY_EXCLUSIONS
    )

    return matches_target_role and not is_too_senior

