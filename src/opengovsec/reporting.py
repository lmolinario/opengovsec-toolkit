"""Report helpers."""

from __future__ import annotations

from collections import Counter

from opengovsec.schemas import DatasetAssessment

RISK_LEVELS = ("low", "medium", "high", "critical")


def render_open_data_report(assessments: list[DatasetAssessment]) -> str:
    lines = ["# OpenGovSec Open Data Report", ""]
    lines.extend(_render_summary(assessments))
    lines.extend(_render_finding_distribution(assessments))
    lines.append("## Dataset details")
    lines.append("")

    for item in assessments:
        lines.append(f"### {item.title}")
        lines.append(f"Risk level: {item.risk_level}")
        lines.append(f"Risk score: {item.risk_score}")
        lines.append("")
        if not item.findings:
            lines.append("No findings detected.")
        for finding in item.findings:
            lines.append(f"- {finding.severity}: {finding.title} ({finding.code})")
        lines.append("")
    return "\n".join(lines)


def _render_summary(assessments: list[DatasetAssessment]) -> list[str]:
    levels = Counter(item.risk_level for item in assessments)
    lines = [
        "## Summary",
        "",
        f"- Datasets assessed: {len(assessments)}",
    ]
    for level in RISK_LEVELS:
        lines.append(f"- {level.title()} risk: {levels.get(level, 0)}")
    lines.append("")
    return lines


def _render_finding_distribution(assessments: list[DatasetAssessment]) -> list[str]:
    counts = Counter(
        finding.code
        for item in assessments
        for finding in item.findings
    )
    lines = ["## Finding distribution", ""]
    if not counts:
        lines.extend(["No findings detected.", ""])
        return lines

    lines.extend(["| Finding | Count |", "|---|---:|"])
    for code, count in sorted(counts.items()):
        lines.append(f"| `{code}` | {count} |")
    lines.append("")
    return lines
