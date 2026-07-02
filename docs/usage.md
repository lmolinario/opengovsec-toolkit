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

Write a machine-readable JSON report:

```bash
opengovsec scan-open-data --input examples/sample_datasets.json --output reports/demo_open_data_report.json --format json
```

Open-data reports include a summary section, a finding distribution table, and per-dataset details.

## 2. Check API documentation

Input: a local OpenAPI-like JSON document.

```bash
opengovsec check-api-doc --input examples/sample_openapi.json
```

Write a Markdown report:

```bash
opengovsec check-api-doc --input examples/sample_openapi.json --output reports/demo_api_report.md
```

The API checker is security-documentation oriented. It reviews documented OpenAPI/Swagger signals such as security schemes, security requirements, operation identifiers, documented error responses, contact metadata, and license metadata. It does not perform live service testing and does not certify API security.

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
opengovsec scan-open-data --input data/dati_gov_it_ambiente.json --output reports/dati_gov_it_ambiente_report.json --format json
```

The downloaded JSON can then be reviewed, versioned if appropriate, or used as input for the open-data scanner.

## 5. Build an aggregate demo summary

OpenGovSec JSON reports can be aggregated into a compact CSV file for portfolio summaries, dashboards, or CI artifacts.

```bash
python scripts/build_demo_summary.py \
  reports/dati_gov_it_ambiente_report.json \
  reports/dati_gov_it_sanita_report.json \
  reports/dati_gov_it_trasporti_report.json \
  --output reports/dati_gov_it_demo_summary.csv
```

The resulting CSV summarizes dataset counts, risk-level counts, and finding distributions for each demo query.

## Current design principle

The current version is document-based and non-invasive. It reads local files provided by the user and produces triage-style reports.

No live service assessment is performed by the scanner modules. The dati.gov.it helper only downloads public catalogue metadata.
