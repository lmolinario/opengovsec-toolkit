from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path

RISK_LEVELS = ("low", "medium", "high", "critical")


def infer_query_name(path: Path) -> str:
    name = path.stem
    if name.startswith("dati_gov_it_"):
        name = name.removeprefix("dati_gov_it_")
    if name.endswith("_report"):
        name = name.removesuffix("_report")
    return name


def format_findings(distribution: dict[str, int]) -> str:
    if not distribution:
        return ""
    return "; ".join(f"{code}={count}" for code, count in sorted(distribution.items()))


def build_rows(report_paths: list[Path]) -> list[dict[str, str | int]]:
    rows: list[dict[str, str | int]] = []
    for report_path in report_paths:
        payload = json.loads(report_path.read_text(encoding="utf-8"))
        summary = payload.get("summary", {})
        risk_levels = summary.get("risk_levels", {})
        finding_distribution = payload.get("finding_distribution", {})
        row: dict[str, str | int] = {
            "query": infer_query_name(report_path),
            "datasets_assessed": int(summary.get("datasets_assessed", 0)),
            "finding_distribution": format_findings(finding_distribution),
            "json_report": str(report_path),
        }
        for level in RISK_LEVELS:
            row[f"{level}_risk"] = int(risk_levels.get(level, 0))
        rows.append(row)
    return rows


def write_csv(rows: list[dict[str, str | int]], output_path: Path) -> None:
    fieldnames = [
        "query",
        "datasets_assessed",
        "low_risk",
        "medium_risk",
        "high_risk",
        "critical_risk",
        "finding_distribution",
        "json_report",
    ]
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a CSV summary from OpenGovSec JSON reports.")
    parser.add_argument("reports", nargs="+", help="Input JSON report paths.")
    parser.add_argument("--output", required=True, help="Output CSV path.")
    args = parser.parse_args()

    rows = build_rows([Path(path) for path in args.reports])
    write_csv(rows, Path(args.output))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
