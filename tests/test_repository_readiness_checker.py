from opengovsec.scanners.repository_readiness_checker import assess_repository_metadata


def test_complete_repository_metadata_has_low_score():
    metadata = {
        "name": "demo",
        "license": "MIT",
        "last_activity_days": 10,
        "releases_count": 2,
        "tags_count": 4,
        "has_sbom": True,
        "files": [
            "README.md",
            "SECURITY.md",
            "pyproject.toml",
            "uv.lock",
            ".github/workflows/ci.yml",
            ".github/dependabot.yml",
            "CONTRIBUTING.md",
            "sbom.spdx.json",
        ],
    }
    assessment = assess_repository_metadata(metadata)
    assert assessment.name == "demo"
    assert assessment.risk_level == "low"
    assert assessment.risk_score == 0


def test_incomplete_repository_metadata_has_findings():
    assessment = assess_repository_metadata({"name": "demo", "files": []})
    codes = {finding.code for finding in assessment.findings}
    assert "missing-license" in codes
    assert "missing-readme" in codes
    assert "missing-dependency-manifest" in codes
    assert "missing-security-policy" in codes
    assert assessment.risk_score > 0


def test_repository_with_manifest_but_without_lockfile_is_reported():
    assessment = assess_repository_metadata(
        {
            "name": "demo",
            "license": "MIT",
            "releases_count": 1,
            "has_sbom": True,
            "files": [
                "README.md",
                "SECURITY.md",
                "pyproject.toml",
                ".github/workflows/ci.yml",
                ".github/dependabot.yml",
                "CONTRIBUTING.md",
            ],
        }
    )
    codes = {finding.code for finding in assessment.findings}
    assert "missing-lockfile" in codes


def test_stale_repository_is_high_risk_signal():
    assessment = assess_repository_metadata({"name": "demo", "last_activity_days": 540, "files": []})
    codes = {finding.code for finding in assessment.findings}
    assert "stale-repository" in codes
    assert assessment.risk_level in {"high", "critical"}
