# Roadmap

## v0.1.0 - Portfolio-ready MVP

Status: completed.

This milestone freezes the first public, portfolio-ready version of OpenGovSec Toolkit.

Delivered scope:

- Python package structure and CLI entry point.
- Passive Open Data Risk Scanner.
- Passive API Security Documentation Checker.
- Passive Repository Readiness / Supply-Chain Readiness Checker.
- Public dati.gov.it metadata helper.
- Real dati.gov.it demo inputs for `ambiente`, `sanita`, and `trasporti`.
- Markdown reports for human review.
- JSON reports for machine-readable output.
- CSV aggregate summary for portfolio/dashboard use.
- Good/weak API documentation examples and reports.
- Good/weak repository metadata examples and reports.
- Explainable risk model.
- Methodology documentation.
- Usage documentation.
- Unit tests and GitHub Actions CI across Python 3.10, 3.11, and 3.12.
- Public project page: `https://lmolinario.github.io/opengovsec/`.

## v0.2.0 - PDND/API documentation readiness

Planned direction: specialize the API checker toward public-sector API documentation readiness.

Candidate checks:

- stronger OpenAPI completeness checks;
- authentication and authorization documentation signals;
- versioning and lifecycle metadata;
- documented error model;
- rate-limit and quota documentation;
- contact, owner, and service metadata;
- optional mapping to public-sector API governance requirements;
- dedicated API JSON output, matching the open-data JSON report pattern.

## v0.3.0 - PA software supply-chain radar

Planned direction: extend repository metadata checks into a broader public-administration supply-chain readiness radar.

Candidate checks:

- dependency manifests and lockfiles;
- CI/CD declaration;
- security policy;
- Dependabot/Renovate configuration;
- release and tag traceability;
- SBOM declaration;
- maintenance activity signals;
- reusable project metadata;
- optional scoring profiles for public-sector open-source reuse.

## v0.4.0 - Dashboard and deployment layer

Planned direction: add a lightweight local dashboard and optional deployment layer.

Candidate features:

- local dashboard for report exploration;
- HTML report generation;
- Dockerfile or docker-compose workflow;
- aggregate trend view;
- exportable portfolio screenshots;
- optional FastAPI backend only if it adds clear value.

## Design principles

- Passive first: avoid intrusive scanning and live probing.
- Explainable scoring: every risk score must map to visible findings.
- Reproducible outputs: examples should be runnable from local files.
- Portfolio value: every module should include input examples, tests, and reports.
- No overclaiming: the toolkit supports triage and governance review; it does not certify security or compliance.
