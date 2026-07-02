"""Connector for the public dati.gov.it CKAN API."""

from __future__ import annotations

import json
from pathlib import Path
from urllib.parse import urlencode
from urllib.request import Request, urlopen

BASE_URL = "https://www.dati.gov.it/opendata/api/3/action"
USER_AGENT = "opengovsec-toolkit/0.1"


def build_package_search_url(query: str, limit: int = 10, offset: int = 0) -> str:
    """Build a CKAN package_search URL for dati.gov.it."""

    safe_limit = max(1, min(limit, 100))
    safe_offset = max(0, offset)
    params = urlencode({"q": query, "rows": safe_limit, "start": safe_offset})
    return f"{BASE_URL}/package_search?{params}"


def fetch_open_data(query: str, limit: int = 10, offset: int = 0, timeout: int = 20) -> dict:
    """Fetch open-data metadata from dati.gov.it using package_search."""

    url = build_package_search_url(query=query, limit=limit, offset=offset)
    request = Request(url, headers={"User-Agent": USER_AGENT})
    with urlopen(request, timeout=timeout) as response:  # nosec: public metadata endpoint
        payload = response.read().decode("utf-8")
    data = json.loads(payload)
    return data if isinstance(data, dict) else {}


def save_json(data: dict, output_path: str) -> None:
    """Save JSON data to disk."""

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
