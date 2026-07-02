# Risk model

The initial OpenGovSec risk model is intentionally simple and explainable.

## Severity weights

| Severity | Weight |
|---|---:|
| info | 0 |
| low | 1 |
| medium | 2 |
| high | 3 |
| critical | 4 |

## Risk level mapping

| Score | Level |
|---:|---|
| 0-2 | low |
| 3-5 | medium |
| 6-8 | high |
| 9+ | critical |

## Open-data finding catalogue

| Code | Severity | Meaning |
|---|---|---|
| `missing-license` | medium | No clear license metadata is present. |
| `weak-description` | low | Description is absent or too short. |
| `missing-organization` | low | Publisher or owner is unclear. |
| `missing-update-date` | medium | No reliable update date is present. |
| `stale-dataset` | medium/high | Metadata appears old. |
| `missing-resources` | high | No documented dataset resources are present. |
| `no-machine-readable-resource` | medium | No declared data file, archive, or service format is present. |
| `resource-missing-locator` | medium | One or more resources lack url, access_url, uri, or distribution_ref. |
| `service-only-resource` | low | Only service-style resources are declared. |

## API documentation finding catalogue

| Code | Severity | Meaning |
|---|---|---|
| `missing-openapi-version` | medium | No OpenAPI or Swagger version field is present. |
| `missing-paths` | high | No documented API paths are present. |
| `missing-servers` | low | No server/base URL declaration is present. |
| `weak-operation-text` | low | One or more operations lack summary or description text. |

## Notes

This model is meant for prioritization and portfolio demonstration. It can be refined with domain-specific weights, policy requirements, and manual validation.

The current modules are document-based and do not perform live service testing.
