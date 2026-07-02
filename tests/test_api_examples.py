from opengovsec.scanners.api_documentation_checker import assess_api_document, load_api_file


def test_sample_openapi_is_security_documentation_complete():
    assessment = assess_api_document(load_api_file("examples/sample_openapi.json"))

    assert assessment.risk_score == 0
    assert assessment.risk_level == "low"
    assert assessment.findings == []


def test_weak_sample_openapi_produces_security_documentation_findings():
    assessment = assess_api_document(load_api_file("examples/sample_openapi_weak.json"))
    codes = {finding.code for finding in assessment.findings}

    assert "missing-servers" in codes
    assert "missing-security-schemes" in codes
    assert "weak-operation-text" in codes
    assert "missing-operation-id" in codes
    assert "missing-error-responses" in codes
    assert "missing-contact-metadata" in codes
    assert "missing-license-metadata" in codes
