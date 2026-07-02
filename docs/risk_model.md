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
| `no-machine-readable-resource` | medium | No declared data file, archive, service, or catalogue-style resource is present. |
| `resource-missing-locator` | medium | One or more resources lack url, access_url, uri, or distribution_ref. |
| `service-only-resource` | low | Only service-style resources are declared. |
| `catalogue-record-resource` | low | Only catalogue-style metadata resources are declared. |

## API documentation finding catalogue

The API documentation checker is a passive documentation review. It does not certify API security and does not perform live testing. It highlights missing or weak documentation signals that are relevant for API governance, interoperability review, and security-oriented documentation hygiene.

| Code | Severity | Meaning |
|---|---|---|
| `missing-openapi-version` | medium | No OpenAPI or Swagger version field is present. |
| `missing-paths` | high | No documented API paths are present. |
| `missing-servers` | low | No server/base URL declaration is present. |
| `missing-security-schemes` | medium | No reusable authentication or authorization scheme is documented. |
| `missing-security-requirements` | medium | Security schemes exist but are not applied globally or at operation level. |
| `weak-operation-text` | low | One or more operations lack summary or description text. |
| `missing-operation-id` | low | One or more operations lack stable operationId values. |
| `missing-error-responses` | low | One or more operations do not document common error responses. |
| `missing-contact-metadata` | low | The API info block does not include contact metadata. |
| `missing-license-metadata` | low | The API info block does not include license metadata. |

## Notes

This model is meant for prioritization and portfolio demonstration. It can be refined with domain-specific weights, policy requirements, and manual validation.

The current modules are document-based and do not perform live service testing.
