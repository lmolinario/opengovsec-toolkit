"""Repository readiness report helpers."""

from __future__ import annotations

from opengovsec.scanners.repository_readiness_checker import RepositoryAssessment


def render_repository_report(assessment: RepositoryAssessment) -> str:
    lines = [
        "# OpenGovSec Repository Readiness Report",
        "",
        f"Repository: {assessment.name}",
        f"Risk level: {assessment.risk_level}",
        f"Risk score: {assessment.risk_score}",
        "",
        "## Findings",
        "",
    ]
    if not assessment.findings:
        lines.append("No findings detected.")
    for finding in assessment.findings:
        lines.append(f"- {finding.severity}: {finding.title} ({finding.code})")
    lines.append("")
    return "\n".join(lines)
