"""Command-line interface."""

from __future__ import annotations

import argparse
from pathlib import Path

from opengovsec.reporting import render_open_data_report
from opengovsec.scanners.open_data_scanner import assess_records, load_json_file, normalize_dataset_records


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="opengovsec")
    parser.add_argument("scan_open_data", nargs="?", help="Use: scan-open-data")
    parser.add_argument("--input", required=True)
    parser.add_argument("--output")
    args = parser.parse_args(argv)

    data = load_json_file(args.input)
    records = normalize_dataset_records(data)
    report = render_open_data_report(assess_records(records))

    if args.output:
        path = Path(args.output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
    else:
        print(report)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
