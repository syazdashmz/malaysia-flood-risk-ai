# v0.4.0 Milestone — Notebook and ML Readiness Foundation

This milestone establishes a reproducible notebook, EDA, and ML-readiness
foundation for the Malaysia flood risk AI project.

## Milestone Decision

The project is ready for initial notebook-based EDA.

The project is not ready for real supervised ML training yet.

## Delivered Capabilities

### Notebook Foundation

- Added project readiness notebook.
- Added initial data catalog EDA notebook.
- Added notebook structure checks.
- Added notebook validation reports.
- Added notebook smoke execution checks.
- Ensured committed notebooks remain clean, without saved outputs or execution counts.

### Data Catalog and EDA Foundation

- Added notebook data catalog.
- Cataloged sample, weather, geospatial, dataset-readiness, notebook, EDA, and ML-readiness reports.
- Added initial EDA report generator.
- Confirmed current assets are sufficient for initial EDA.

### ML Readiness Foundation

- Added training dataset design.
- Added training table schema validator.
- Added feature table generation plan.
- Added feature table builder dry-run.
- Added target label source plan.
- Added combined ML training readiness gate.
- Added complete ML readiness suite runner.

## Current ML Training Status

Real supervised ML training remains blocked.

Current blockers:

1. No verified target label source is ready for real training.
2. Feature table builder is not allowed to create a real training table yet.
3. Model-ready training table schema is not valid yet.
4. Model-ready training table has no rows yet.

## Guardrails

- The rule-based `risk_score` must not be used as the real training target.
- The future `flood_occurred` target must come from a verified historical flood source.
- A real training table must be schema-valid, non-empty, documented, and aligned by location and time.
- Baseline ML experiments should wait until the readiness gate is clear.

## Main Reports

- `reports/notebook_data_catalog_report.md`
- `reports/notebook_validation_report.md`
- `reports/notebook_execution_report.md`
- `reports/initial_eda_report.md`
- `reports/feature_table_plan.md`
- `reports/feature_table_builder_dry_run.md`
- `reports/target_label_source_plan.md`
- `reports/training_table_schema_report.md`
- `reports/dataset_readiness_report.md`
- `reports/ml_training_readiness_report.md`

## Main Commands

Run notebook checks:

    .\scripts\run_notebook_checks.ps1
    .\scripts\run_notebook_smoke_tests.ps1
    .\scripts\run_notebook_data_catalog.ps1

Run EDA report:

    .\scripts\run_initial_eda_report.ps1

Run complete ML readiness suite:

    .\scripts\run_ml_readiness_suite.ps1

## Next Milestone Direction

The next practical milestone is to integrate or prepare a verified historical
flood label source, then generate a real model-ready training table.
