from opengovsec.scanners.repository_readiness_checker import assess_repository_metadata, load_repository_file


def test_sample_repository_metadata_is_supply_chain_ready():
    assessment = assess_repository_metadata(load_repository_file("examples/sample_repository_metadata.json"))

    assert assessment.risk_score == 0
    assert assessment.risk_level == "low"
    assert assessment.findings == []


def test_weak_sample_repository_metadata_produces_supply_chain_findings():
    assessment = assess_repository_metadata(load_repository_file("examples/sample_repository_metadata_weak.json"))
    codes = {finding.code for finding in assessment.findings}

    assert "missing-license" in codes
    assert "missing-readme" in codes
    assert "missing-dependency-manifest" in codes
    assert "missing-ci" in codes
    assert "missing-community-docs" in codes
    assert "missing-security-policy" in codes
    assert "missing-dependency-update-config" in codes
    assert "missing-release-metadata" in codes
    assert "missing-sbom" in codes
    assert "stale-repository" in codes
