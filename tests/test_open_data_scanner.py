from opengovsec.scanners.open_data_scanner import assess_dataset, normalize_dataset_records


def test_normalize_plain_list():
    records = normalize_dataset_records([{"id": "a"}, {"id": "b"}])
    assert len(records) == 2


def test_normalize_ckan_response():
    payload = {"result": {"results": [{"id": "a"}]}}
    records = normalize_dataset_records(payload)
    assert records == [{"id": "a"}]


def test_assess_dataset_with_missing_metadata():
    assessment = assess_dataset({"id": "x", "title": "Dataset X"})
    codes = {finding.code for finding in assessment.findings}
    assert "missing-license" in codes
    assert "missing-resources" in codes
    assert assessment.risk_score > 0
