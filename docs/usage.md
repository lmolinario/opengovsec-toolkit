# Usage

OpenGovSec Toolkit currently provides three passive commands.

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

## Current design principle

The current version is document-based and non-invasive. It reads local files provided by the user and produces triage-style reports.

No live service assessment is performed by the initial modules.
