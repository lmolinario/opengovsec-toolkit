"""Shared data structures for OpenGovSec Toolkit."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Finding:
    """A single assessment finding."""

    code: str
    severity: str
    title: str
    detail: str
    recommendation: str


@dataclass
class DatasetAssessment:
    """Assessment result for one open-data dataset record."""

    identifier: str
    title: str
    organization: str | None
    risk_score: int
    risk_level: str
    findings: list[Finding] = field(default_factory=list)

    @property
    def finding_count(self) -> int:
        return len(self.findings)
