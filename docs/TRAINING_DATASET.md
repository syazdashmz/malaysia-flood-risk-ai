# Training Dataset Design

## Purpose

This document defines the planned training dataset structure for future baseline ML experiments.

The project is not ready for real AI/ML training yet.

This document exists to prevent premature training on unclear labels, unstable features, or leaky data.

## Current Status

Current training readiness:

- target label design: documented
- model-ready training table: not created yet
- real historical flood labels: not added yet
- baseline ML training: not started yet

## Target Label Strategy

The preferred future target label is:

    flood_occurred

Meaning:

    Whether a flood event occurred for a location and time window.

Expected type:

    binary classification

Expected values:

| Value | Meaning |
|---:|---|
| 0 | No known flood event |
| 1 | Flood event occurred |

## Alternative Labels

If a reliable binary event label is not available, possible future alternatives are:

| Candidate Label | Task Type | Notes |
|---|---|---|
| flood_risk_class | multiclass classification | Requires trusted labeled classes |
| flood_incident_count | regression/count modeling | Requires event count data by area/time |
| risk_score_proxy | regression | Should only be used as a proxy, not true supervised flood prediction |

## Important Rule

The transparent rule-based risk score should not be treated as a true ground-truth label.

It may be useful for:

- sanity checks
- weak supervision experiments
- demo-only proxy experiments
- comparing model behavior against rule-based output

It should not be presented as real flood prediction training unless clearly marked as synthetic/proxy learning.

## Planned Training Table

Planned file path:

    data/processed/model_training/training_features.csv

Expected grain:

    one row per location-time observation

Minimum planned columns:

| Column | Type | Purpose |
|---|---|---|
| observation_id | string | Unique row ID |
| latitude | float | Location coordinate |
| longitude | float | Location coordinate |
| observation_date | date | Date of observation |
| state | string | Future administrative boundary attribute |
| district | string | Future administrative boundary attribute |
| elevation_m | float | Terrain feature |
| slope_deg | float | Terrain feature |
| river_distance_m | float | Hydrology/geospatial feature |
| historical_flood_distance_m | float | Historical proximity feature |
| rainfall_24h_mm | float | Short-term rainfall feature |
| rainfall_72h_mm | float | Multi-day rainfall feature |
| water_level_status | string | Hydrology status feature |
| weather_warning_status | string | Weather warning feature |
| land_cover_class | string | Surface/exposure feature |
| population_density_per_km2 | float | Exposure feature |
| flood_occurred | int | Preferred future target label |

## Feature Groups

### Geospatial Features

Planned geospatial features:

- latitude
- longitude
- state
- district
- elevation
- slope
- river distance
- land cover
- administrative boundary attributes

### Weather Features

Planned weather features:

- rainfall over 24 hours
- rainfall over 72 hours
- weather warning status
- forecast signal category
- warning signal category

### Hydrology Features

Planned hydrology features:

- water level status
- river proximity
- flood-prone area indicators if available

### Exposure Features

Planned exposure features:

- population density
- urban/rural proxy
- land cover class

## Data Leakage Risks

The following must be avoided before training:

| Leakage Risk | Why It Matters |
|---|---|
| Using future rainfall after the target event | Gives the model information it would not have at prediction time |
| Using post-event reports as input features | Leaks the answer into the feature table |
| Using rule-based risk score as a true label | Trains the model to imitate the rules, not real flood events |
| Random splits across time-sensitive data | Can leak future patterns into training |
| Duplicated nearby observations across train/test | Can inflate evaluation scores |

## Recommended Split Strategy

Preferred split order:

1. temporal split by date
2. geographic holdout by state or district
3. final random split only for non-temporal sanity checks

Initial baseline recommendation:

    train on older observations, validate on newer observations

Reason:

    Flood prediction is time-sensitive, so evaluation should approximate future prediction.

## Baseline Model Plan

First baseline candidates:

| Model | Reason |
|---|---|
| Logistic Regression | Simple, interpretable binary baseline |
| Random Forest | Handles nonlinear feature interactions |
| XGBoost | Strong tabular baseline after data quality is stable |
| LightGBM | Efficient tabular baseline after data quality is stable |

The first baseline should prioritize interpretability over maximum score.

## Evaluation Metrics

For binary flood occurrence:

| Metric | Purpose |
|---|---|
| Precision | Avoid too many false flood alarms |
| Recall | Capture real flood events |
| F1 score | Balance precision and recall |
| ROC AUC | Ranking quality |
| PR AUC | Better for imbalanced flood events |
| Confusion matrix | Practical error analysis |

## Minimum Requirements Before Training

Real baseline ML training can start only after:

- this document exists
- the model-ready training table exists
- target label source is documented
- feature columns are stable
- leakage risks are reviewed
- train/validation split is defined
- dataset readiness report says training blockers are resolved

## Current Decision

The project should continue with notebook-based exploration first.

Real AI/ML training should wait until:

    data/processed/model_training/training_features.csv

exists and contains a documented target label.

## Training Table Schema Validation

Validate the planned model-training table schema with:

    .\scripts\run_training_schema_check.ps1

This generates:

    reports/training_table_schema_report.md

The validator checks:

- whether the training table exists
- required feature columns
- target label column
- row count
- schema validity
- whether the table is structurally ready for baseline training

Current expected result:

    Training ready: False

This remains false until a real model-ready training table is created.

## Feature Table Generation Plan

Generate the feature table plan with:

    .\scripts\run_feature_table_plan.ps1

This generates:

    reports/feature_table_plan.md

The plan maps each required training-table column to:

- source category
- planned source
- derivation note
- current readiness

Real ML training remains blocked until the target label comes from a verified historical flood source.

## Feature Table Builder Dry Run

Generate the feature table builder dry-run report with:

    .\scripts\run_feature_table_builder_dry_run.ps1

This generates:

    reports/feature_table_builder_dry_run.md

The dry run inspects available sample data and maps currently available columns to the future training-table schema.

It does not create:

    data/processed/model_training/training_features.csv

The real training table remains blocked until a verified `flood_occurred` target label is available.

## Target Label Source Plan

Generate the target label source plan with:

    .\scripts\run_target_label_source_plan.ps1

This generates:

    reports/target_label_source_plan.md

The plan defines requirements for the future `flood_occurred` target label, including:

- verified historical source
- location alignment
- time alignment
- binary target mapping
- no rule-based risk-score leakage

Real supervised ML training remains blocked until an allowed target label source is integrated.

## ML Training Readiness Gate

Generate the combined ML training readiness gate with:

    .\scripts\run_ml_training_readiness.ps1

This generates:

    reports/ml_training_readiness_report.md

The gate combines:

- target label source readiness
- feature table builder readiness
- training table schema readiness
- training table row availability

Real supervised ML training can start only when all gates are clear.

## ML Training Readiness Workflow

See:

    docs/ML_TRAINING_READINESS.md

Run the complete ML readiness suite with:

    .\scripts\run_ml_readiness_suite.ps1

This workflow regenerates all target-label, feature-table, schema, dataset,
and combined ML training readiness reports.
