# OpenGovSec Toolkit

[![CI](https://github.com/lmolinario/opengovsec-toolkit/actions/workflows/ci.yml/badge.svg)](https://github.com/lmolinario/opengovsec-toolkit/actions/workflows/ci.yml)

OpenGovSec Toolkit is an open-source cybersecurity and digital-governance toolkit for assessing public-sector open data, API documentation, metadata quality, and software supply-chain exposure.

The project focuses on practical, reproducible, and transparent checks for public-sector digital ecosystems, with an initial focus on Italian public-administration resources such as open-data catalogues, interoperability documentation, and reusable open-source software.

Current milestone: `v0.1.0` portfolio-ready MVP.

Project page: https://lmolinario.github.io/opengovsec/

Release notes: [`docs/releases/v0.1.0.md`](docs/releases/v0.1.0.md)

## Goals

- Assess open-data metadata quality and operational risk.
- Check API documentation and interoperability readiness.
- Evaluate repository reuse readiness in public-sector open-source projects.
- Produce clear reports for technical, governance, and compliance audiences.
- Support portfolio, research, and professional development in cybersecurity, data governance, and public-sector digital transformation.

## Current status

Early-stage but usable prototype.

Implemented:

- Open Data Risk Scanner.
- API Security Documentation Checker.
- Repository Readiness / Supply-Chain Readiness Checker.
- Public dati.gov.it metadata helper.
- Markdown, JSON, and CSV report generation with summary and finding distribution.
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

Generate a machine-readable JSON report:

```bash
opengovsec scan-open-data --input examples/sample_datasets.json --output reports/demo_open_data_report.json --format json
```

### Public dati.gov.it metadata example

```bash
mkdir -p data reports
python scripts/fetch_dati_gov_it.py --query ambiente --limit 20 --output data/dati_gov_it_ambiente.json
opengovsec scan-open-data --input data/dati_gov_it_ambiente.json --output reports/dati_gov_it_ambiente_report_v4.md
opengovsec scan-open-data --input data/dati_gov_it_ambiente.json --output reports/dati_gov_it_ambiente_report.json --format json
```

The helper downloads public catalogue metadata only. The scanner remains document-based and does not probe live services.

### API security documentation check

Run the security-complete demo document:

```bash
opengovsec check-api-doc --input examples/sample_openapi.json --output reports/demo_api_good_report.md
```

Run the intentionally weak demo document:

```bash
opengovsec check-api-doc --input examples/sample_openapi_weak.json --output reports/demo_api_weak_report.md
```

The API checker reviews documented OpenAPI/Swagger signals such as security schemes, security requirements, operation identifiers, error responses, contact metadata, and license metadata. It does not perform live service testing and does not certify API security.

### Repository supply-chain readiness check

Run the supply-chain-ready demo metadata:

```bash
opengovsec check-repository --input examples/sample_repository_metadata.json --output reports/demo_repository_good_report.md
```

Run the intentionally weak demo metadata:

```bash
opengovsec check-repository --input examples/sample_repository_metadata_weak.json --output reports/demo_repository_weak_report.md
```

The repository checker reviews declared repository metadata and file inventory signals such as license, README, dependency manifests, lockfiles, CI, security policy, dependency update configuration, release metadata, SBOM declaration, and activity metadata. It does not inspect source code, resolve dependencies, or certify software supply-chain security.

## Demo reports

OpenGovSec includes reproducible demo reports generated from public CKAN metadata downloaded from dati.gov.it.

| Query | Source data | Markdown report | JSON report | Summary |
|---|---|---|---|---|
| ambiente | [`data/dati_gov_it_ambiente.json`](data/dati_gov_it_ambiente.json) | [`reports/dati_gov_it_ambiente_report_v4.md`](reports/dati_gov_it_ambiente_report_v4.md) | [`reports/dati_gov_it_ambiente_report.json`](reports/dati_gov_it_ambiente_report.json) | 20 datasets, all low risk; service and catalogue-style resources identified. |
| sanita | [`data/dati_gov_it_sanita.json`](data/dati_gov_it_sanita.json) | [`reports/dati_gov_it_sanita_report.md`](reports/dati_gov_it_sanita_report.md) | [`reports/dati_gov_it_sanita_report.json`](reports/dati_gov_it_sanita_report.json) | 20 datasets, all low risk; weak descriptions are the main finding. |
| trasporti | [`data/dati_gov_it_trasporti.json`](data/dati_gov_it_trasporti.json) | [`reports/dati_gov_it_trasporti_report.md`](reports/dati_gov_it_trasporti_report.md) | [`reports/dati_gov_it_trasporti_report.json`](reports/dati_gov_it_trasporti_report.json) | 20 datasets, all low risk; service-style resources are the main finding. |

Aggregate demo summary: [`reports/dati_gov_it_demo_summary.csv`](reports/dati_gov_it_demo_summary.csv).

### API and repository demo reports

| Module | Input | Report | Result |
|---|---|---|---|
| API documentation | [`examples/sample_openapi.json`](examples/sample_openapi.json) | [`reports/demo_api_good_report.md`](reports/demo_api_good_report.md) | low risk, no findings |
| API documentation | [`examples/sample_openapi_weak.json`](examples/sample_openapi_weak.json) | [`reports/demo_api_weak_report.md`](reports/demo_api_weak_report.md) | high risk, security-documentation findings |
| Repository readiness | [`examples/sample_repository_metadata.json`](examples/sample_repository_metadata.json) | [`reports/demo_repository_good_report.md`](reports/demo_repository_good_report.md) | low risk, no findings |
| Repository readiness | [`examples/sample_repository_metadata_weak.json`](examples/sample_repository_metadata_weak.json) | [`reports/demo_repository_weak_report.md`](reports/demo_repository_weak_report.md) | critical risk, supply-chain-readiness findings |

These examples are intended to demonstrate the full workflow:

```text
public catalogue metadata -> local JSON -> passive scanner -> Markdown/JSON report -> CSV summary
OpenAPI or repository metadata -> passive documentation/readiness checker -> good/weak Markdown reports
```

## Modules

### 1. Open Data Risk Scanner

Analyzes public open-data metadata and declared resources from local JSON exports or CKAN-like responses.

Initial checks:

- dataset freshness;
- license availability;
- metadata completeness;
- machine-readable formats;
- declared resource locators;
- service-style and catalogue-style resource declarations;
- organizational ownership;
- risk scoring.

### 2. API Security Documentation Checker

Evaluates local OpenAPI-like JSON documents using passive documentation checks.

Initial checks:

- OpenAPI or Swagger version declaration;
- documented paths and server declaration;
- documented authentication or authorization schemes;
- declared security requirements;
- operation identifiers and operation text;
- documented error responses;
- contact and license metadata;
- risk scoring.

### 3. Repository Readiness / Supply-Chain Readiness Checker

Evaluates local repository metadata declarations for reuse, maintainability, and lightweight supply-chain readiness signals.

Initial checks:

- license declaration;
- README presence;
- dependency manifest and lockfile presence;
- CI workflow declaration;
- contribution/community documentation;
- security policy declaration;
- dependency update configuration;
- release or tag metadata;
- SBOM declaration;
- declared repository activity;
- risk scoring.

## Intended use

This toolkit is designed for passive, non-invasive analysis of public information, metadata, documentation, and openly available repositories.

The scanner modules read local files and public catalogue metadata and produce triage-style governance reports.

## Project documentation

- [`docs/methodology.md`](docs/methodology.md)
- [`docs/risk_model.md`](docs/risk_model.md)
- [`docs/roadmap.md`](docs/roadmap.md)
- [`docs/usage.md`](docs/usage.md)
- [`docs/releases/v0.1.0.md`](docs/releases/v0.1.0.md)

## License

MIT License.
