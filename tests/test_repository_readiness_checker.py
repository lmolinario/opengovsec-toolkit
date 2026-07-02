from opengovsec.scanners.repository_readiness_checker import assess_repository_metadata


def test_complete_repository_metadata_has_low_score():
    metadata = {
        "name": "demo",
        "license": "MIT",
        "last_activity_days": 10,
        "files": ["README.md", "pyproject.toml", ".github/workflows/ci.yml", "CONTRIBUTING.md"],
    }
    assessment = assess_repository_metadata(metadata)
    assert assessment.name == "demo"
    assert assessment.risk_level == "low"


def test_incomplete_repository_metadata_has_findings():
    assessment = assess_repository_metadata({"name": "demo", "files": []})
    codes = {finding.code for finding in assessment.findings}
    assert "missing-license" in codes
    assert "missing-readme" in codes
    assert assessment.risk_score > 0
