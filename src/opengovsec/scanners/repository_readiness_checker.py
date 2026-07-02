"""Passive repository readiness checker."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from opengovsec.schemas import Finding
from opengovsec.scoring import level_from_score, score_from_severities


@dataclass
class RepositoryAssessment:
    name: str
    risk_score: int
    risk_level: str
    findings: list[Finding] = field(default_factory=list)


def load_repository_file(path: str) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def assess_repository_metadata(metadata: dict) -> RepositoryAssessment:
    findings: list[Finding] = []
    name = str(metadata.get("name") or metadata.get("full_name") or "unknown-repository")
    files = set(str(item).lower() for item in metadata.get("files", []) if isinstance(item, str))
    last_activity_days = metadata.get("last_activity_days")

    if not metadata.get("license"):
        findings.append(Finding("missing-license", "medium", "Missing license", "No repository license was declared.", "Declare a clear license."))

    if "readme.md" not in files:
        findings.append(Finding("missing-readme", "medium", "Missing README", "No README.md file was declared.", "Add a clear README with purpose and usage."))

    if not any(item in files for item in {"requirements.txt", "pyproject.toml", "package.json", "pom.xml", "build.gradle"}):
        findings.append(Finding("missing-dependency-manifest", "medium", "Missing dependency manifest", "No common dependency manifest was declared.", "Declare dependencies using the standard manifest for the stack."))

    if not any(item.startswith(".github/workflows/") for item in files):
        findings.append(Finding("missing-ci", "low", "Missing CI workflow", "No GitHub Actions workflow was declared.", "Add basic test automation."))

    if not any(item in files for item in {"code_of_conduct.md", "contributing.md"}):
        findings.append(Finding("missing-community-docs", "low", "Missing community documentation", "No contribution or conduct file was declared.", "Add contribution guidance for reuse."))

    if isinstance(last_activity_days, int) and last_activity_days > 365:
        findings.append(Finding("stale-repository", "high", "Repository appears stale", f"Last activity is declared as {last_activity_days} days ago.", "Confirm maintenance status or archive the repository."))

    score = score_from_severities([finding.severity for finding in findings])
    return RepositoryAssessment(name, score, level_from_score(score), findings)
