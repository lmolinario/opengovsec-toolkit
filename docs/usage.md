# Usage

OpenGovSec Toolkit currently provides three passive commands and one public metadata helper script.

## 1. Scan open-data metadata

Input: a local JSON file containing either a list of dataset records or a CKAN-like response.

```bash
opengovsec scan-open-data --input examples/sample_datasets.json
```

Write a Markdown report:

```bash
opengovsec scan-open-data --input examples/sample_datasets.json --output reports/demo_open_data_report.md
```

## 2. Check API documentation

Input: a local OpenAPI-like JSON document.

```bash
opengovsec check-api-doc --input examples/sample_openapi.json
```

Write a Markdown report:

```bash
opengovsec check-api-doc --input examples/sample_openapi.json --output reports/demo_api_report.md
```

## 3. Check repository readiness

Input: a local JSON file that declares basic repository metadata.

```bash
opengovsec check-repository --input examples/sample_repository_metadata.json
```

Write a Markdown report:

```bash
opengovsec check-repository --input examples/sample_repository_metadata.json --output reports/demo_repository_report.md
```

## 4. Fetch metadata from dati.gov.it

The helper script downloads public CKAN metadata into a local JSON file.

```bash
mkdir -p data reports
python scripts/fetch_dati_gov_it.py --query ambiente --limit 20 --output data/dati_gov_it_ambiente.json
opengovsec scan-open-data --input data/dati_gov_it_ambiente.json --output reports/dati_gov_it_ambiente_report.md
```

The downloaded JSON can then be reviewed, versioned if appropriate, or used as input for the open-data scanner.

## Current design principle

The current version is document-based and non-invasive. It reads local files provided by the user and produces triage-style reports.

No live service assessment is performed by the scanner modules. The dati.gov.it helper only downloads public catalogue metadata.
