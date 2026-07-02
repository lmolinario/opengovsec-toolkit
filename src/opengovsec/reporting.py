"""Report helpers."""

from __future__ import annotations

from opengovsec.schemas import DatasetAssessment


def render_open_data_report(assessments: list[DatasetAssessment]) -> str:
    lines = ["# OpenGovSec Open Data Report", "", f"Datasets assessed: {len(assessments)}", ""]
    for item in assessments:
        lines.append(f"## {item.title}")
        lines.append(f"Risk level: {item.risk_level}")
        lines.append(f"Risk score: {item.risk_score}")
        lines.append("")
        for finding in item.findings:
            lines.append(f"- {finding.severity}: {finding.title} ({finding.code})")
        lines.append("")
    return "\n".join(lines)
