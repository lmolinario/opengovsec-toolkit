# OpenGovSec Toolkit

OpenGovSec Toolkit is an open-source cybersecurity and digital-governance toolkit for assessing public-sector open data, APIs, metadata quality, and software supply-chain exposure.

The project focuses on practical, reproducible and transparent checks for public-sector digital ecosystems, with an initial focus on Italian public administration resources such as open-data catalogues, interoperability APIs and reusable open-source software.

## Goals

- Assess open-data metadata quality and operational risk.
- Check API documentation and basic security posture.
- Evaluate software supply-chain exposure in public-sector open-source projects.
- Produce clear reports for technical, governance and compliance audiences.
- Support portfolio, research and professional development in cybersecurity, data governance and public-sector digital transformation.

## Modules

### 1. Open Data Risk Scanner

Analyzes public open-data metadata and resources.

Initial checks:

- dataset freshness;
- license availability;
- metadata completeness;
- resource reachability;
- machine-readable formats;
- broken links;
- organizational ownership;
- risk scoring.

### 2. API Security Checker

Evaluates public API documentation and basic security signals.

Initial checks:

- HTTPS usage;
- OpenAPI availability;
- endpoint reachability;
- authentication declaration;
- security headers;
- API versioning;
- error handling;
- OWASP API Security mapping.

### 3. Software Supply-Chain Radar

Assesses open-source software repositories used or published in public-sector contexts.

Initial checks:

- license;
- last activity;
- dependency files;
- CI/CD presence;
- Dockerfile presence;
- security policy;
- SBOM readiness;
- issue and maintenance signals.

## Status

Early-stage project. The repository is being initialized.

## Intended Use

This toolkit is designed for passive, non-invasive analysis of public information, metadata, documentation and openly available repositories.

It is not intended for unauthorized security testing, exploitation, vulnerability scanning against live systems, or intrusive assessment activities.

## License

MIT License.
