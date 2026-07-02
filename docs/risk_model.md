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

## Dataset risk level

| Score | Level |
|---:|---|
| 0-2 | low |
| 3-5 | medium |
| 6-8 | high |
| 9+ | critical |

## Current finding catalogue

| Code | Severity | Meaning |
|---|---|---|
| `missing-license` | medium | No clear license metadata is present. |
| `weak-description` | low | Description is absent or too short. |
| `missing-organization` | low | Publisher or owner is unclear. |
| `missing-update-date` | medium | No reliable update date is present. |
| `stale-dataset` | medium/high | Metadata appears old. |
| `missing-resources` | high | No documented dataset resources are present. |
| `no-machine-readable-resource` | medium | No declared machine-readable format is present. |
| `resource-missing-url` | medium | One or more resources lack a URL field. |

## Notes

This model is meant for prioritization and portfolio demonstration. It can be refined with domain-specific weights, policy requirements, and manual validation.
