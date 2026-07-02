"""API documentation report helpers."""

from __future__ import annotations

from opengovsec.scanners.api_documentation_checker import APIDocumentAssessment


def render_api_report(assessment: APIDocumentAssessment) -> str:
    lines = [
        "# OpenGovSec API Documentation Report",
        "",
        f"API: {assessment.title}",
        f"Version: {assessment.version}",
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
