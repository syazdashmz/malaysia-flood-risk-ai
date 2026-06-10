# Notebook Data Catalog Report

## Summary

- Assets cataloged: 9
- Available assets: 8
- Explorable assets: 8
- Missing assets: 1
- Blocking EDA assets: 0
- Ready for initial EDA: True

## Assets

| Asset | Category | Path | Required for EDA | Status | Rows | Size Bytes |
|---|---|---|---:|---|---:|---:|
| Sample Malaysia locations | sample | data/samples/sample_malaysia_locations.csv | True | explorable | 6 | 904 |
| Weather risk signal summary | weather | reports/weather_risk_signal_summary.json | True | explorable | - | 253 |
| Weather pipeline validation report | weather | reports/weather_pipeline_validation.md | False | explorable | - | 538 |
| Geospatial artifact plan | geospatial | reports/geospatial_artifact_plan.md | False | explorable | - | 992 |
| Geospatial validation report | geospatial | reports/geospatial_validation_report.md | True | explorable | - | 978 |
| Dataset readiness report | readiness | reports/dataset_readiness_report.md | True | explorable | - | 1456 |
| Training table schema report | ml_readiness | reports/training_table_schema_report.md | True | explorable | - | 2210 |
| Notebook environment report | notebook | reports/notebook_environment_report.md | True | explorable | - | 1116 |
| Model-ready training table | ml_training | data/processed/model_training/training_features.csv | False | missing | - | 0 |

## Interpretation

The available assets are enough to start initial notebook-based EDA.

## Training Note

A model-ready training table is cataloged but not required for initial EDA. Real ML training should still wait until the training table is schema-valid, non-empty, and documented.
