# ML Training Readiness Gate

## Summary

- Target column: `flood_occurred`
- Target ready: False
- Allowed target sources: 3
- Ready target sources: 0
- Target event source exists: False
- Target event source rows: 0
- Target event source schema valid: False
- Target event source ready: False
- Feature source exists: True
- Feature source rows: 6
- Mapped feature columns: 13
- Missing feature columns: 4
- Feature builder can create training table: False
- Training table exists: False
- Training table schema valid: False
- Training table has rows: False
- Training table ready: False
- Real ML training ready: False

## Blockers

- No verified target label source is ready for real training.
- Historical flood event target source is not ready for label generation yet.
- Feature table builder is not allowed to create a real training table yet.
- Model-ready training table schema is not valid yet.
- Model-ready training table has no rows yet.

## Missing Feature Columns

- observation_id
- observation_date
- district
- flood_occurred

## Decision

Real supervised ML training must remain blocked until all gates are clear.
