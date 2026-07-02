"""Passive API documentation checker."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from opengovsec.schemas import Finding
from opengovsec.scoring import level_from_score, score_from_severities

HTTP_METHODS = {"get", "post", "put", "patch", "delete", "head", "options"}
ERROR_STATUS_CODES = {"400", "401", "403", "404", "409", "422", "429", "500", "502", "503", "504", "default"}


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

    security_schemes = _security_schemes(document)
    if not security_schemes:
        findings.append(Finding("missing-security-schemes", "medium", "Missing security schemes", "No reusable security schemes were declared in components.securitySchemes or securityDefinitions.", "Document authentication and authorization mechanisms, such as bearer tokens, OAuth2, API keys, or mutual TLS where applicable."))

    if security_schemes and not _has_declared_security(document, paths):
        findings.append(Finding("missing-security-requirements", "medium", "Missing security requirements", "Security schemes exist but no global or operation-level security requirements were declared.", "Apply documented security requirements globally or on each protected operation."))

    undocumented = _count_operations_without_text(paths)
    if undocumented:
        findings.append(Finding("weak-operation-text", "low", "Weak operation text", f"{undocumented} operations have no summary or description.", "Add summaries and descriptions to operations."))

    missing_operation_ids = _count_operations_missing_operation_id(paths)
    if missing_operation_ids:
        findings.append(Finding("missing-operation-id", "low", "Missing operationId", f"{missing_operation_ids} operations have no operationId.", "Add stable operationId values to support traceability, client generation, testing, and audit review."))

    missing_error_responses = _count_operations_missing_error_responses(paths)
    if missing_error_responses:
        findings.append(Finding("missing-error-responses", "low", "Missing documented error responses", f"{missing_error_responses} operations do not document any common error response.", "Document expected error responses such as 400, 401, 403, 404, 429, 5xx, or default."))

    if not _has_contact_metadata(info):
        findings.append(Finding("missing-contact-metadata", "low", "Missing contact metadata", "The API info block does not declare contact information.", "Add a contact object or equivalent support reference for API consumers and governance review."))

    if not _has_license_metadata(info):
        findings.append(Finding("missing-license-metadata", "low", "Missing license metadata", "The API info block does not declare license information.", "Add license metadata where applicable to clarify reuse and documentation terms."))

    score = score_from_severities([finding.severity for finding in findings])
    return APIDocumentAssessment(title, version, score, level_from_score(score), findings)


def _operations(paths: dict) -> list[dict[str, Any]]:
    operations: list[dict[str, Any]] = []
    for path_item in paths.values():
        if not isinstance(path_item, dict):
            continue
        for method, operation in path_item.items():
            if method.lower() not in HTTP_METHODS or not isinstance(operation, dict):
                continue
            operations.append(operation)
    return operations


def _count_operations_without_text(paths: dict) -> int:
    count = 0
    for operation in _operations(paths):
        if not operation.get("summary") and not operation.get("description"):
            count += 1
    return count


def _count_operations_missing_operation_id(paths: dict) -> int:
    return sum(1 for operation in _operations(paths) if not operation.get("operationId"))


def _count_operations_missing_error_responses(paths: dict) -> int:
    count = 0
    for operation in _operations(paths):
        responses = operation.get("responses") if isinstance(operation.get("responses"), dict) else {}
        documented_codes = {str(code).lower() for code in responses}
        if not documented_codes.intersection(ERROR_STATUS_CODES):
            count += 1
    return count


def _security_schemes(document: dict) -> dict:
    components = document.get("components") if isinstance(document.get("components"), dict) else {}
    schemes = components.get("securitySchemes") if isinstance(components.get("securitySchemes"), dict) else {}
    if schemes:
        return schemes
    legacy = document.get("securityDefinitions") if isinstance(document.get("securityDefinitions"), dict) else {}
    return legacy


def _has_declared_security(document: dict, paths: dict) -> bool:
    if isinstance(document.get("security"), list) and document.get("security"):
        return True
    return any(isinstance(operation.get("security"), list) for operation in _operations(paths))


def _has_contact_metadata(info: dict) -> bool:
    contact = info.get("contact")
    return isinstance(contact, dict) and any(contact.get(key) for key in ("name", "email", "url"))


def _has_license_metadata(info: dict) -> bool:
    license_info = info.get("license")
    return isinstance(license_info, dict) and any(license_info.get(key) for key in ("name", "url", "identifier"))
