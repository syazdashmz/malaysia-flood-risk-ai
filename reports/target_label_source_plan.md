# Target Label Source Plan

## Summary

- Target column: `flood_occurred`
- Requirements: 5
- Candidate sources: 5
- Sources allowed for real training: 3
- Sources ready now for real training: 0
- Real training target ready: False

## Target Label Requirements

| Requirement | Required | Description |
|---|---:|---|
| Binary flood occurrence label | True | The preferred target must map to flood_occurred as 0 or 1. |
| Verified historical source | True | The label must come from a verified historical flood source. |
| Location alignment | True | The label must align with latitude, longitude, state, or district. |
| Time alignment | True | The label must align with observation_date for temporal splitting. |
| No risk-score leakage | True | The target must not be derived from the rule-based risk score. |

## Candidate Sources

| Candidate | Type | Allowed for Real Training | Ready Now | Reason |
|---|---|---:|---:|---|
| Verified historical flood event records | preferred | True | False | Preferred option, but no verified event dataset is integrated yet. |
| Historical flood extent polygons | acceptable | True | False | Usable if event dates and polygon coverage are verified. |
| Official flood incident reports | acceptable | True | False | Usable if locations, dates, and event definitions are structured. |
| Rule-based risk score | rejected_for_real_training | False | True | Rejected as ground truth because it would leak engineered scoring logic. |
| Current sample demo dataset | rejected_for_real_training | False | True | Useful for demos and EDA, but not verified as historical ground truth. |

## Training Guardrail

Do not start real supervised ML training until at least one allowed target label source is integrated and ready.

Current decision:

    Real supervised ML training remains blocked.
