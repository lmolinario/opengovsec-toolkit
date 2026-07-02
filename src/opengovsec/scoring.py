"""Risk scoring utilities for passive public-data assessment."""

from __future__ import annotations

SEVERITY_WEIGHTS = {
    "info": 0,
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4,
}


def score_from_severities(severities: list[str]) -> int:
    """Compute an integer risk score from finding severities."""

    return sum(SEVERITY_WEIGHTS.get(severity, 0) for severity in severities)


def level_from_score(score: int) -> str:
    """Map a numeric score to a simple risk level."""

    if score >= 9:
        return "critical"
    if score >= 6:
        return "high"
    if score >= 3:
        return "medium"
    return "low"


def is_machine_readable_format(value: str | None) -> bool:
    """Return true when a resource format is likely machine-readable."""

    if not value:
        return False

    normalized = value.strip().lower().lstrip(".")
    return normalized in {
        "csv",
        "json",
        "xml",
        "rdf",
        "ttl",
        "geojson",
        "parquet",
        "xlsx",
        "ods",
        "api",
    }
