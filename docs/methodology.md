# Methodology

OpenGovSec Toolkit starts from a conservative principle: public-sector digital risk can often be assessed from public metadata, documentation, and repository signals before any technical interaction with live services is considered.

The first module, Open Data Risk Scanner, evaluates dataset records using passive metadata checks.

## Assessment scope

The initial scanner reviews:

- license fields;
- dataset description quality;
- publishing organization;
- metadata creation or update date;
- declared resources;
- resource formats;
- resource URL presence.

## Out of scope for the initial version

The initial version does not perform live endpoint checks. It does not test external systems. It only reads local JSON metadata supplied by the user.

## Risk model

Each finding has a severity:

- info: 0 points;
- low: 1 point;
- medium: 2 points;
- high: 3 points;
- critical: 4 points.

The dataset score is the sum of finding weights. The score is mapped to a qualitative level:

- 0-2: low;
- 3-5: medium;
- 6-8: high;
- 9 or more: critical.

## Interpretation

The score is not a legal or compliance certification. It is a practical triage indicator useful for prioritizing manual review and remediation.
