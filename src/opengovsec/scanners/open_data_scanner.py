"""Passive open-data metadata scanner.

This module evaluates dataset metadata records without probing live systems.
The first version is intentionally document-based: it checks the quality and
completeness of metadata fields, resource declarations, licenses, and dates.
"""

from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path

from opengovsec.schemas import DatasetAssessment, Finding
from opengovsec.scoring import is_machine_readable_format, level_from_score, score_from_severities

DATE_KEYS = (
    "metadata_modified",
    "modified",
    "updated",
    "last_modified",
    "metadata_created",
    "created",
)


def load_json_file(path: str) -> object:
    """Load dataset metadata from a local JSON file."""

    return json.loads(Path(path).read_text(encoding="utf-8"))


def normalize_dataset_records(payload: object) -> list[dict]:
    """Normalize plain lists and common CKAN API exports into records."""

    if isinstance(payload, list):
        return [item for item in payload if isinstance(item, dict)]

    if not isinstance(payload, dict):
        return []

    result = payload.get("result")
    if isinstance(result, dict):
        if isinstance(result.get("results"), list):
            return [item for item in result["results"] if isinstance(item, dict)]
        if isinstance(result.get("resources"), list):
            return [result]

    if isinstance(result, list):
        return [item for item in result if isinstance(item, dict)]

    if isinstance(payload.get("resources"), list):
        return [payload]

    return []


def assess_records(records: list[dict]) -> list[DatasetAssessment]:
    """Assess a list of dataset metadata records."""

    return [assess_dataset(record) for record in records]


def assess_dataset(record: dict) -> DatasetAssessment:
    """Assess one open-data dataset metadata record."""

    findings: list[Finding] = []
    identifier = str(record.get("id") or record.get("name") or record.get("identifier") or "unknown")
    title = str(record.get("title") or record.get("name") or identifier)
    organization = _organization_name(record)
    resources = record.get("resources") if isinstance(record.get("resources"), list) else []

    _check_license(record, findings)
    _check_description(record, findings)
    _check_organization(organization, findings)
    _check_freshness(record, findings)
    _check_resources(resources, findings)

    score = score_from_severities([finding.severity for finding in findings])
    return DatasetAssessment(
        identifier=identifier,
        title=title,
        organization=organization,
        risk_score=score,
        risk_level=level_from_score(score),
        findings=findings,
    )


def _organization_name(record: dict) -> str | None:
    organization = record.get("organization")
    if isinstance(organization, dict):
        return organization.get("title") or organization.get("name")
    if isinstance(organization, str):
        return organization
    return record.get("publisher") or record.get("owner_org")


def _check_license(record: dict, findings: list[Finding]) -> None:
    license_value = record.get("license_id") or record.get("license_title") or record.get("license")
    if not license_value:
        findings.append(
            Finding(
                code="missing-license",
                severity="medium",
                title="Missing license information",
                detail="The dataset does not expose a clear license field.",
                recommendation="Publish an explicit open-data license in the dataset metadata.",
            )
        )


def _check_description(record: dict, findings: list[Finding]) -> None:
    description = record.get("notes") or record.get("description")
    if not description or len(str(description).strip()) < 20:
        findings.append(
            Finding(
                code="weak-description",
                severity="low",
                title="Missing or weak description",
                detail="The dataset description is missing or too short to support reuse.",
                recommendation="Add a meaningful description, scope, update policy, and reuse context.",
            )
        )


def _check_organization(organization: str | None, findings: list[Finding]) -> None:
    if not organization:
        findings.append(
            Finding(
                code="missing-organization",
                severity="low",
                title="Missing organization ownership",
                detail="The dataset owner or publishing organization is not clear.",
                recommendation="Expose the publishing organization responsible for the dataset.",
            )
        )


def _check_freshness(record: dict, findings: list[Finding]) -> None:
    parsed_date = None
    for key in DATE_KEYS:
        value = record.get(key)
        parsed_date = _parse_date(value) if value else None
        if parsed_date:
            break

    if not parsed_date:
        findings.append(
            Finding(
                code="missing-update-date",
                severity="medium",
                title="Missing update date",
                detail="No reliable creation or update date was found in the dataset metadata.",
                recommendation="Publish metadata_created and metadata_modified values or equivalent fields.",
            )
        )
        return

    age_days = (datetime.now(timezone.utc) - parsed_date).days
    if age_days > 1095:
        severity = "high"
    elif age_days > 730:
        severity = "medium"
    else:
        return

    findings.append(
        Finding(
            code="stale-dataset",
            severity=severity,
            title="Potentially stale dataset",
            detail=f"The most recent metadata date appears to be {age_days} days old.",
            recommendation="Confirm the update policy and refresh the dataset or metadata if maintained.",
        )
    )


def _check_resources(resources: list, findings: list[Finding]) -> None:
    if not resources:
        findings.append(
            Finding(
                code="missing-resources",
                severity="high",
                title="No documented resources",
                detail="The dataset record does not contain resource entries.",
                recommendation="Publish at least one resource URL or documented data endpoint.",
            )
        )
        return

    readable_count = 0
    missing_url_count = 0

    for resource in resources:
        if not isinstance(resource, dict):
            continue
        if is_machine_readable_format(resource.get("format")):
            readable_count += 1
        if not resource.get("url"):
            missing_url_count += 1

    if readable_count == 0:
        findings.append(
            Finding(
                code="no-machine-readable-resource",
                severity="medium",
                title="No machine-readable resource format detected",
                detail="No resource appears to be CSV, JSON, XML, RDF, GeoJSON, Parquet, XLSX, ODS, or API.",
                recommendation="Publish at least one machine-readable resource.",
            )
        )

    if missing_url_count:
        findings.append(
            Finding(
                code="resource-missing-url",
                severity="medium",
                title="Resource URL missing",
                detail=f"{missing_url_count} resource entries do not expose a URL.",
                recommendation="Ensure every resource has a stable URL or endpoint reference.",
            )
        )


def _parse_date(value: object) -> datetime | None:
    if not isinstance(value, str):
        return None

    text = value.strip().replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(text)
    except ValueError:
        return None

    if parsed.tzinfo is None:
        return parsed.replace(tzinfo=timezone.utc)
    return parsed.astimezone(timezone.utc)
