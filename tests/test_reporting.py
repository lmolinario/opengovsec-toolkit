import json

from opengovsec.reporting import render_open_data_json, render_open_data_report
from opengovsec.schemas import DatasetAssessment, Finding


def _sample_assessments():
    return [
        DatasetAssessment(
            identifier="a",
            title="Dataset A",
            organization="Org",
            risk_score=1,
            risk_level="low",
            findings=[
                Finding(
                    code="weak-description",
                    severity="low",
                    title="Weak description",
                    detail="Short description.",
                    recommendation="Improve description.",
                )
            ],
        ),
        DatasetAssessment(
            identifier="b",
            title="Dataset B",
            organization="Org",
            risk_score=0,
            risk_level="low",
            findings=[],
        ),
    ]


def test_open_data_report_contains_summary_and_distribution():
    report = render_open_data_report(_sample_assessments())

    assert "## Summary" in report
    assert "- Datasets assessed: 2" in report
    assert "- Low risk: 2" in report
    assert "## Finding distribution" in report
    assert "| `weak-description` | 1 |" in report
    assert "## Dataset details" in report
    assert "### Dataset A" in report
    assert "No findings detected." in report


def test_open_data_json_contains_summary_distribution_and_datasets():
    payload = json.loads(render_open_data_json(_sample_assessments()))

    assert payload["summary"]["datasets_assessed"] == 2
    assert payload["summary"]["risk_levels"] == {
        "low": 2,
        "medium": 0,
        "high": 0,
        "critical": 0,
    }
    assert payload["finding_distribution"] == {"weak-description": 1}
    assert payload["datasets"][0]["identifier"] == "a"
    assert payload["datasets"][0]["findings"][0]["code"] == "weak-description"
