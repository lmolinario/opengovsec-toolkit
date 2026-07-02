"""Report helpers."""

from __future__ import annotations

import json
from collections import Counter
from dataclasses import asdict

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


def render_open_data_json(assessments: list[DatasetAssessment]) -> str:
    """Render open-data assessments as machine-readable JSON."""

    payload = {
        "summary": {
            "datasets_assessed": len(assessments),
            "risk_levels": _risk_level_counts(assessments),
        },
        "finding_distribution": _finding_counts(assessments),
        "datasets": [asdict(item) for item in assessments],
    }
    return json.dumps(payload, indent=2, ensure_ascii=False)


def _render_summary(assessments: list[DatasetAssessment]) -> list[str]:
    levels = _risk_level_counts(assessments)
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
    counts = _finding_counts(assessments)
    lines = ["## Finding distribution", ""]
    if not counts:
        lines.extend(["No findings detected.", ""])
        return lines

    lines.extend(["| Finding | Count |", "|---|---:|"])
    for code, count in sorted(counts.items()):
        lines.append(f"| `{code}` | {count} |")
    lines.append("")
    return lines


def _risk_level_counts(assessments: list[DatasetAssessment]) -> dict[str, int]:
    levels = Counter(item.risk_level for item in assessments)
    return {level: levels.get(level, 0) for level in RISK_LEVELS}


def _finding_counts(assessments: list[DatasetAssessment]) -> dict[str, int]:
    counts = Counter(
        finding.code
        for item in assessments
        for finding in item.findings
    )
    return dict(sorted(counts.items()))
