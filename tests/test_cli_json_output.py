import json

from opengovsec.cli import main


def test_scan_open_data_json_output(tmp_path):
    input_path = tmp_path / "datasets.json"
    output_path = tmp_path / "report.json"
    input_path.write_text(
        json.dumps([{"id": "dataset-1", "title": "Dataset 1"}]),
        encoding="utf-8",
    )

    exit_code = main(
        [
            "scan-open-data",
            "--input",
            str(input_path),
            "--output",
            str(output_path),
            "--format",
            "json",
        ]
    )

    assert exit_code == 0
    payload = json.loads(output_path.read_text(encoding="utf-8"))
    assert payload["summary"]["datasets_assessed"] == 1
    assert payload["datasets"][0]["identifier"] == "dataset-1"
