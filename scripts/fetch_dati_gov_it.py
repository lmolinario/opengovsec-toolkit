from __future__ import annotations

import argparse

from opengovsec.connectors.dati_gov_it import fetch_open_data, save_json


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", required=True)
    parser.add_argument("--limit", type=int, default=10)
    parser.add_argument("--offset", type=int, default=0)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    data = fetch_open_data(args.query, args.limit, args.offset)
    save_json(data, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
