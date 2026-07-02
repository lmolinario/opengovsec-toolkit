from opengovsec.scanners.api_documentation_checker import assess_api_document


def test_good_api_document_has_low_score():
    document = {
        "openapi": "3.0.3",
        "info": {
            "title": "Demo API",
            "version": "1.0.0",
            "contact": {"name": "API support", "email": "support@example.invalid"},
            "license": {"name": "CC-BY-4.0"},
        },
        "servers": [{"url": "https://api.example.invalid"}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer"}
            }
        },
        "security": [{"bearerAuth": []}],
        "paths": {
            "/items": {
                "get": {
                    "summary": "List items",
                    "operationId": "listItems",
                    "responses": {
                        "200": {"description": "OK"},
                        "401": {"description": "Unauthorized"},
                    },
                }
            }
        },
    }
    assessment = assess_api_document(document)
    assert assessment.title == "Demo API"
    assert assessment.risk_level == "low"
    assert assessment.risk_score == 0


def test_incomplete_api_document_has_findings():
    assessment = assess_api_document({"info": {"title": "Incomplete API"}})
    codes = {finding.code for finding in assessment.findings}
    assert "missing-openapi-version" in codes
    assert "missing-paths" in codes
    assert "missing-security-schemes" in codes
    assert assessment.risk_score > 0


def test_security_schemes_without_requirements_are_reported():
    document = {
        "openapi": "3.0.3",
        "info": {
            "title": "Security Scheme Only API",
            "version": "1.0.0",
            "contact": {"name": "API support"},
            "license": {"name": "CC-BY-4.0"},
        },
        "servers": [{"url": "https://api.example.invalid"}],
        "components": {
            "securitySchemes": {
                "bearerAuth": {"type": "http", "scheme": "bearer"}
            }
        },
        "paths": {
            "/items": {
                "get": {
                    "summary": "List items",
                    "operationId": "listItems",
                    "responses": {"200": {"description": "OK"}, "403": {"description": "Forbidden"}},
                }
            }
        },
    }

    codes = {finding.code for finding in assess_api_document(document).findings}

    assert "missing-security-requirements" in codes
    assert "missing-security-schemes" not in codes


def test_operations_without_traceability_and_error_responses_are_reported():
    document = {
        "openapi": "3.0.3",
        "info": {"title": "Weak Operations API", "version": "1.0.0"},
        "servers": [{"url": "https://api.example.invalid"}],
        "paths": {
            "/items": {
                "get": {
                    "summary": "List items",
                    "responses": {"200": {"description": "OK"}},
                }
            }
        },
    }

    codes = {finding.code for finding in assess_api_document(document).findings}

    assert "missing-operation-id" in codes
    assert "missing-error-responses" in codes
    assert "missing-contact-metadata" in codes
    assert "missing-license-metadata" in codes
