from opengovsec.scanners.api_documentation_checker import assess_api_document


def test_good_api_document_has_low_score():
    document = {
        "openapi": "3.0.3",
        "info": {"title": "Demo API", "version": "1.0.0"},
        "servers": [{"url": "https://api.example.invalid"}],
        "paths": {"/items": {"get": {"summary": "List items"}}},
    }
    assessment = assess_api_document(document)
    assert assessment.title == "Demo API"
    assert assessment.risk_level == "low"


def test_incomplete_api_document_has_findings():
    assessment = assess_api_document({"info": {"title": "Incomplete API"}})
    codes = {finding.code for finding in assessment.findings}
    assert "missing-openapi-version" in codes
    assert "missing-paths" in codes
    assert assessment.risk_score > 0
