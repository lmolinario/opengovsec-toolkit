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


def test_access_url_and_distribution_format_are_recognized():
    assessment = assess_dataset(
        {
            "id": "x",
            "title": "CSV dataset",
            "notes": "A sufficiently descriptive open data record for testing.",
            "license_id": "CC-BY-4.0",
            "metadata_modified": "2026-06-01T00:00:00+00:00",
            "organization": {"title": "Demo organization"},
            "resources": [
                {
                    "access_url": "https://example.invalid/data.csv",
                    "distribution_format": "CSV",
                }
            ],
        }
    )
    codes = {finding.code for finding in assessment.findings}
    assert "resource-missing-locator" not in codes
    assert "no-machine-readable-resource" not in codes


def test_service_resource_is_reported_as_service_only():
    assessment = assess_dataset(
        {
            "id": "x",
            "title": "Map service dataset",
            "notes": "A sufficiently descriptive geospatial service record for testing.",
            "license_id": "CC-BY-4.0",
            "metadata_modified": "2026-06-01T00:00:00+00:00",
            "organization": {"title": "Demo organization"},
            "resources": [
                {
                    "uri": "https://example.invalid/wms",
                    "distribution_format": "MAP_SRVC",
                }
            ],
        }
    )
    codes = {finding.code for finding in assessment.findings}
    assert "service-only-resource" in codes
    assert "resource-missing-locator" not in codes


def test_service_format_can_be_inferred_from_distribution_ref():
    assessment = assess_dataset(
        {
            "id": "x",
            "title": "RNDT service dataset",
            "notes": "A sufficiently descriptive RNDT-style service record for testing.",
            "license_id": "CC-BY-4.0",
            "metadata_modified": "2026-06-01T00:00:00+00:00",
            "organization": {"title": "Demo organization"},
            "resources": [
                {
                    "format": "",
                    "url": "",
                    "uri": "https://geodati.gov.it/resource/distribution/example/WMS_SRVC-123",
                    "distribution_ref": "https://geodati.gov.it/resource/distribution/example/WMS_SRVC-123",
                }
            ],
        }
    )
    codes = {finding.code for finding in assessment.findings}
    assert "service-only-resource" in codes
    assert "resource-missing-locator" not in codes
    assert "no-machine-readable-resource" not in codes
