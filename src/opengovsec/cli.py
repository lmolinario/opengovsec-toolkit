"""Command-line interface for OpenGovSec Toolkit."""

from __future__ import annotations

import argparse
from pathlib import Path

from opengovsec.api_reporting import render_api_report
from opengovsec.reporting import render_open_data_report
from opengovsec.scanners.api_documentation_checker import assess_api_document, load_api_file
from opengovsec.scanners.open_data_scanner import assess_records, load_json_file, normalize_dataset_records


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="opengovsec",
        description="Passive public-sector digital governance toolkit.",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    open_data = subparsers.add_parser(
        "scan-open-data",
        help="Assess local open-data metadata exported as JSON.",
    )
    open_data.add_argument("--input", required=True, help="Local JSON input file.")
    open_data.add_argument("--output", help="Optional Markdown output path.")

    api_doc = subparsers.add_parser(
        "check-api-doc",
        help="Assess a local OpenAPI-like JSON document.",
    )
    api_doc.add_argument("--input", required=True, help="Local OpenAPI JSON input file.")
    api_doc.add_argument("--output", help="Optional Markdown output path.")

    return parser


def _write_or_print(report: str, output: str | None) -> None:
    if output:
        path = Path(output)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(report, encoding="utf-8")
    else:
        print(report)


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "scan-open-data":
        data = load_json_file(args.input)
        records = normalize_dataset_records(data)
        report = render_open_data_report(assess_records(records))
        _write_or_print(report, args.output)
        return 0

    if args.command == "check-api-doc":
        document = load_api_file(args.input)
        report = render_api_report(assess_api_document(document))
        _write_or_print(report, args.output)
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
