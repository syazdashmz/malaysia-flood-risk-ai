# Dataset Readiness Report

## Summary

- Checks: 6
- Available: 4
- Missing: 2
- Blocking training: 2
- Ready for ML training: False

## Checks

| Check | Path | Required for Training | Status | Blocks Training |
|---|---|---:|---|---:|
| Sample Malaysia locations | data/samples/sample_malaysia_locations.csv | False | available | False |
| Weather risk signal summary | reports/weather_risk_signal_summary.json | False | available | False |
| Geospatial validation report | reports/geospatial_validation_report.md | False | available | False |
| Project readiness notebook | notebooks/00_project_readiness.ipynb | False | available | False |
| Training dataset design document | docs/TRAINING_DATASET.md | True | missing | True |
| Model-ready training table | data/processed/model_training/training_features.csv | True | missing | True |

## Interpretation

The dataset foundation is not ready for real ML training yet. Training should wait until blocking items are resolved.

## Next Required Training Items

1. Define the training target label.
2. Document feature columns and leakage risks.
3. Create a model-ready training table.
4. Define train/validation split strategy.
5. Only then start baseline ML experiments.
