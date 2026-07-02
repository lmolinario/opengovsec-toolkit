from __future__ import annotations

import argparse
from pathlib import Path

from opengovsec.api_reporting import render_api_report
from opengovsec.reporting import render_open_data_report
from opengovsec.repository_reporting import render_repository_report
from opengovsec.scanners.api_documentation_checker import assess_api_document, load_api_file
from opengovsec.scanners.open_data_scanner import assess_records, load_json_file, normalize_dataset_records
from opengovsec.scanners.repository_readiness_checker import assess_repository_metadata, load_repository_file


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="opengovsec")
    sub = parser.add_subparsers(dest="command", required=True)

    a = sub.add_parser("scan-open-data")
    a.add_argument("--input", required=True)
    a.add_argument("--output")

    b = sub.add_parser("check-api-doc")
    b.add_argument("--input", required=True)
    b.add_argument("--output")

    c = sub.add_parser("check-repository")
    c.add_argument("--input", required=True)
    c.add_argument("--output")
    return parser


def emit(text: str, output: str | None) -> None:
    if not output:
        print(text)
        return
    path = Path(output)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    if args.command == "scan-open-data":
        data = load_json_file(args.input)
        records = normalize_dataset_records(data)
        emit(render_open_data_report(assess_records(records)), args.output)
        return 0
    if args.command == "check-api-doc":
        emit(render_api_report(assess_api_document(load_api_file(args.input))), args.output)
        return 0
    if args.command == "check-repository":
        emit(render_repository_report(assess_repository_metadata(load_repository_file(args.input))), args.output)
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
