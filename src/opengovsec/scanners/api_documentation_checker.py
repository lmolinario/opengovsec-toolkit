"""Passive API documentation checker."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path

from opengovsec.schemas import Finding
from opengovsec.scoring import level_from_score, score_from_severities


@dataclass
class APIDocumentAssessment:
    title: str
    version: str
    risk_score: int
    risk_level: str
    findings: list[Finding] = field(default_factory=list)


def load_api_file(path: str) -> dict:
    payload = json.loads(Path(path).read_text(encoding="utf-8"))
    return payload if isinstance(payload, dict) else {}


def assess_api_document(document: dict) -> APIDocumentAssessment:
    findings: list[Finding] = []
    info = document.get("info") if isinstance(document.get("info"), dict) else {}
    title = str(info.get("title") or "unknown-api")
    version = str(info.get("version") or "unknown")

    if not document.get("openapi") and not document.get("swagger"):
        findings.append(Finding("missing-openapi-version", "medium", "Missing OpenAPI version", "No openapi or swagger field was found.", "Declare the specification version."))

    paths = document.get("paths") if isinstance(document.get("paths"), dict) else {}
    if not paths:
        findings.append(Finding("missing-paths", "high", "Missing paths", "No documented paths were found.", "Document available paths and operations."))

    servers = document.get("servers") if isinstance(document.get("servers"), list) else []
    if not servers:
        findings.append(Finding("missing-servers", "low", "Missing server declaration", "No server list was declared.", "Declare base URLs in the documentation."))

    undocumented = _count_operations_without_text(paths)
    if undocumented:
        findings.append(Finding("weak-operation-text", "low", "Weak operation text", f"{undocumented} operations have no summary or description.", "Add summaries and descriptions to operations."))

    score = score_from_severities([finding.severity for finding in findings])
    return APIDocumentAssessment(title, version, score, level_from_score(score), findings)


def _count_operations_without_text(paths: dict) -> int:
    methods = {"get", "post", "put", "patch", "delete", "head", "options"}
    count = 0
    for path_item in paths.values():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in methods or not isinstance(operation, dict):
                continue
            if not operation.get("summary") and not operation.get("description"):
                count += 1
    return count
