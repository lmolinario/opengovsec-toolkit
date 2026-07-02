from opengovsec.scoring import is_machine_readable_format, level_from_score, score_from_severities


def test_score_mapping():
    assert score_from_severities(["low", "medium", "high"]) == 6
    assert level_from_score(0) == "low"
    assert level_from_score(3) == "medium"
    assert level_from_score(6) == "high"
    assert level_from_score(9) == "critical"


def test_format_mapping():
    assert is_machine_readable_format("CSV") is True
    assert is_machine_readable_format("json") is True
    assert is_machine_readable_format("PDF") is False
