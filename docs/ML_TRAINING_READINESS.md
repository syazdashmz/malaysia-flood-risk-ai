# ML Training Readiness Workflow

This document explains the current supervised ML readiness status for the
Malaysia flood risk AI project.

## Current Decision

Real supervised ML training remains blocked.

The project has enough assets for initial EDA, but it does not yet have a
verified model-ready training table with a trusted `flood_occurred` target label.

## Current Readiness Gates

| Gate | Status |
|---|---|
| Target label source plan | Available |
| Feature table generation plan | Available |
| Feature table builder dry run | Available |
| Training table schema validation | Available |
| Combined ML training readiness gate | Available |
| Real model-ready training table | Missing |
| Verified `flood_occurred` target label | Missing |

## Current Blockers

The current ML training readiness gate reports these blockers:

1. No verified target label source is ready for real training.
2. Feature table builder is not allowed to create a real training table yet.
3. Model-ready training table schema is not valid yet.
4. Model-ready training table has no rows yet.

## Regenerate All ML Readiness Reports

Run:

    .\scripts\run_ml_readiness_suite.ps1

This regenerates:

- `reports/target_label_source_plan.md`
- `reports/target_label_source_evaluation.md`
- `reports/target_event_source_schema_report.md`
- `reports/feature_table_plan.md`
- `reports/feature_table_builder_dry_run.md`
- `reports/training_table_schema_report.md`
- `reports/dataset_readiness_report.md`
- `reports/ml_training_readiness_report.md`

## Training Guardrail

The rule-based `risk_score` must not be used as the real target label.

It may be used only for:

- demos
- transparent scoring explanations
- weak-supervision experiments clearly marked as proxy or synthetic

Real supervised ML training can start only after a verified historical flood
label source is integrated, aligned by location and time, and validated against
the required training-table schema.
