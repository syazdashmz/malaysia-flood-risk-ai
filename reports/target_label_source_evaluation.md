# Target Label Source Evaluation

## Summary

- Target column: `flood_occurred`
- Candidate sources: 5
- Ready candidate sources: 0
- Real training target ready: False

## Evaluation Criteria

| Criterion | Required | Description |
|---|---:|---|
| Verified authority | True | Source must come from a trusted or documented authority. |
| Historical event coverage | True | Source must represent past flood occurrence events. |
| Binary target mapping | True | Source must be mappable to flood_occurred as 0 or 1. |
| Location alignment | True | Source must align to latitude, longitude, state, or district. |
| Time alignment | True | Source must align to observation_date. |
| License documented | True | Usage permissions must be documented before training use. |
| Leakage free | True | Target must not be derived from the rule-based risk score. |

## Candidate Scorecard

| Candidate | Type | Available | Allowed | Ready | verified_authority | historical_event_coverage | binary_mapping | location_alignment | time_alignment | license_documented | leakage_free | Notes |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Verified historical flood event records | preferred | False | True | False | False | False | False | False | False | False | True | Preferred source type, but no verified event file is integrated yet. |
| Historical flood extent polygons | acceptable | False | True | False | False | True | False | False | False | False | True | Usable only if event dates, coverage, and licensing are verified. |
| Official flood incident reports | acceptable | False | True | False | False | True | False | False | False | False | True | Usable only after structured location and date fields are available. |
| Rule-based risk score | rejected_for_real_training | True | False | False | False | False | True | False | False | False | False | Rejected because it leaks the scoring logic into the target label. |
| Current sample demo dataset | rejected_for_real_training | True | False | False | False | False | False | True | False | False | True | Useful for demos and EDA, but not verified historical ground truth. |

## Decision

No target-label source is ready for real supervised ML training yet.

Next practical action:

Find or prepare a verified historical flood occurrence source with location, date, licensing, and binary target mapping.
