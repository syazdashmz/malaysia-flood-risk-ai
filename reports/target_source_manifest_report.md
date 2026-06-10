# Target Source Candidate Manifest Report

## Summary

- Path: `configs/target_source_candidates.json`
- Exists: True
- Manifest valid: True
- Candidate sources: 4
- Ready candidate sources: 0
- Has ready candidate: False

## Invalid Entries

No invalid entries found.

## Candidate Sources

| Source | Type | License | Status | Allowed | Ready | Notes |
|---|---|---|---|---:|---:|---|
| Verified historical flood event records | preferred | pending_review | planned | True | False | Preferred future source type. Not ready until authority, license, location, and date fields are verified. |
| Historical flood extent polygons | acceptable | pending_review | planned | True | False | Useful if event dates, polygon quality, CRS, and licensing are verified. |
| Official flood incident reports | acceptable | pending_review | planned | True | False | Needs structured extraction if the source is not already tabular. |
| Rule-based risk score | rejected | verified | rejected | False | False | Rejected because it would leak the rule-based scoring logic into the target label. |

## Decision

No target source candidate is ready for real training yet.
