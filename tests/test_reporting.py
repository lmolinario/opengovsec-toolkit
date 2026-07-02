from opengovsec.reporting import render_open_data_report
from opengovsec.schemas import DatasetAssessment, Finding


def test_open_data_report_contains_summary_and_distribution():
    assessments = [
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

    report = render_open_data_report(assessments)

    assert "## Summary" in report
    assert "- Datasets assessed: 2" in report
    assert "- Low risk: 2" in report
    assert "## Finding distribution" in report
    assert "| `weak-description` | 1 |" in report
    assert "## Dataset details" in report
    assert "### Dataset A" in report
    assert "No findings detected." in report
