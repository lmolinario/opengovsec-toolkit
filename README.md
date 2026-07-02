# OpenGovSec Toolkit

OpenGovSec Toolkit is an open-source cybersecurity and digital-governance toolkit for assessing public-sector open data, API documentation, metadata quality, and software supply-chain exposure.

The project focuses on practical, reproducible, and transparent checks for public-sector digital ecosystems, with an initial focus on Italian public-administration resources such as open-data catalogues, interoperability documentation, and reusable open-source software.

## Goals

- Assess open-data metadata quality and operational risk.
- Check API documentation and interoperability readiness.
- Evaluate software supply-chain exposure in public-sector open-source projects.
- Produce clear reports for technical, governance, and compliance audiences.
- Support portfolio, research, and professional development in cybersecurity, data governance, and public-sector digital transformation.

## Current status

Early-stage but usable prototype.

Implemented:

- Open Data Risk Scanner.
- API Documentation Checker.
- Markdown report generation.
- Python package configuration.
- CLI entry point.
- Sample input files.
- Unit tests.
- GitHub Actions CI.

## Installation

```bash
git clone https://github.com/lmolinario/opengovsec-toolkit.git
cd opengovsec-toolkit
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

Windows PowerShell:

```powershell
git clone https://github.com/lmolinario/opengovsec-toolkit.git
cd opengovsec-toolkit
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -e .[dev]
```

## Usage

### Open-data metadata scan

```bash
opengovsec scan-open-data --input examples/sample_datasets.json
```

Generate a Markdown report:

```bash
opengovsec scan-open-data --input examples/sample_datasets.json --output reports/demo_open_data_report.md
```

### API documentation check

```bash
opengovsec check-api-doc --input examples/sample_openapi.json
```

Generate a Markdown report:

```bash
opengovsec check-api-doc --input examples/sample_openapi.json --output reports/demo_api_report.md
```

## Modules

### 1. Open Data Risk Scanner

Analyzes public open-data metadata and declared resources from local JSON exports or CKAN-like responses.

Initial checks:

- dataset freshness;
- license availability;
- metadata completeness;
- machine-readable formats;
- declared resource URLs;
- organizational ownership;
- risk scoring.

### 2. API Documentation Checker

Evaluates local OpenAPI-like JSON documents using passive documentation checks.

Initial checks:

- OpenAPI or Swagger version declaration;
- documented paths;
- server declaration;
- operation summaries or descriptions;
- risk scoring.

### 3. Software Supply-Chain Radar

Planned module for assessing open-source software repositories used or published in public-sector contexts.

Planned checks:

- license;
- last activity;
- dependency files;
- CI/CD presence;
- Dockerfile presence;
- security policy;
- SBOM readiness;
- issue and maintenance signals.

## Intended use

This toolkit is designed for passive, non-invasive analysis of public information, metadata, documentation, and openly available repositories.

It is not intended for unauthorized security testing, exploitation, vulnerability scanning against live systems, or intrusive assessment activities.

## Project documentation

- [`docs/methodology.md`](docs/methodology.md)
- [`docs/risk_model.md`](docs/risk_model.md)
- [`docs/roadmap.md`](docs/roadmap.md)

## License

MIT License.
