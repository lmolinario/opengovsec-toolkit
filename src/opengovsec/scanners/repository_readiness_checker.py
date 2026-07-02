"""Passive repository readiness checker."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from opengovsec.schemas import Finding
from opengovsec.scoring import level_from_score, score_from_severities

DEPENDENCY_MANIFESTS = {
    "requirements.txt",
    "pyproject.toml",
    "package.json",
    "pom.xml",
    "build.gradle",
    "go.mod",
    "cargo.toml",
}
LOCKFILES = {
    "poetry.lock",
    "uv.lock",
    "pdm.lock",
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "go.sum",
    "cargo.lock",
    "gradle.lockfile",
}
COMMUNITY_DOCS = {"code_of_conduct.md", "contributing.md"}
SECURITY_POLICY_FILES = {"security.md", ".github/security.md", "docs/security.md"}
DEPENDENCY_UPDATE_FILES = {
    ".github/dependabot.yml",
    ".github/dependabot.yaml",
    "renovate.json",
    ".renovaterc",
    ".renovaterc.json",
}
SBOM_FILES = {"sbom.json", "sbom.spdx.json", "bom.json", "cyclonedx.json"}


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
    releases_count = metadata.get("releases_count")
    tags_count = metadata.get("tags_count")
    has_sbom = bool(metadata.get("has_sbom")) or bool(files.intersection(SBOM_FILES))

    if not metadata.get("license"):
        findings.append(Finding("missing-license", "medium", "Missing license", "No repository license was declared.", "Declare a clear license."))

    if "readme.md" not in files:
        findings.append(Finding("missing-readme", "medium", "Missing README", "No README.md file was declared.", "Add a clear README with purpose and usage."))

    has_dependency_manifest = bool(files.intersection(DEPENDENCY_MANIFESTS))
    if not has_dependency_manifest:
        findings.append(Finding("missing-dependency-manifest", "medium", "Missing dependency manifest", "No common dependency manifest was declared.", "Declare dependencies using the standard manifest for the stack."))

    if has_dependency_manifest and not files.intersection(LOCKFILES):
        findings.append(Finding("missing-lockfile", "low", "Missing dependency lockfile", "A dependency manifest exists but no common lockfile was declared.", "Add a lockfile where appropriate to support reproducible builds and dependency review."))

    if not any(item.startswith(".github/workflows/") for item in files):
        findings.append(Finding("missing-ci", "low", "Missing CI workflow", "No GitHub Actions workflow was declared.", "Add basic test automation."))

    if not files.intersection(COMMUNITY_DOCS):
        findings.append(Finding("missing-community-docs", "low", "Missing community documentation", "No contribution or conduct file was declared.", "Add contribution guidance for reuse."))

    if not files.intersection(SECURITY_POLICY_FILES):
        findings.append(Finding("missing-security-policy", "medium", "Missing security policy", "No SECURITY.md file was declared.", "Add a security policy describing how vulnerabilities should be reported and handled."))

    if not files.intersection(DEPENDENCY_UPDATE_FILES):
        findings.append(Finding("missing-dependency-update-config", "low", "Missing dependency update configuration", "No Dependabot or Renovate configuration was declared.", "Add automated dependency update configuration where appropriate."))

    if not _has_release_metadata(releases_count, tags_count):
        findings.append(Finding("missing-release-metadata", "low", "Missing release metadata", "No releases or tags were declared in the repository metadata.", "Use releases or tags to support version traceability and reuse."))

    if not has_sbom:
        findings.append(Finding("missing-sbom", "low", "Missing SBOM declaration", "No SBOM file or has_sbom flag was declared.", "Consider publishing an SBOM for reusable or production-oriented software."))

    if isinstance(last_activity_days, int) and last_activity_days > 365:
        findings.append(Finding("stale-repository", "high", "Repository appears stale", f"Last activity is declared as {last_activity_days} days ago.", "Confirm maintenance status or archive the repository."))

    score = score_from_severities([finding.severity for finding in findings])
    return RepositoryAssessment(name, score, level_from_score(score), findings)


def _has_release_metadata(releases_count: object, tags_count: object) -> bool:
    return any(isinstance(value, int) and value > 0 for value in (releases_count, tags_count))
