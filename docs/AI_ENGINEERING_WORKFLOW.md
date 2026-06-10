# AI Engineering Workflow

## Goal

Build a Malaysia flood prediction system that moves from research data to a
tested AI model, API, and web demo without mixing experimental labels with
official verified labels.

## Current Decision

- Transparent rule-based risk engine: production demo baseline.
- Kaggle flood dataset: experimental AI baseline only.
- EM-DAT export: candidate official target source, still under review.
- Real official supervised ML model: blocked until target labels are verified.

## Professional Development Flow

1. Gather data.
2. Record source, license, access date, and limitations.
3. Store raw data under `data/raw/`.
4. Clean and normalize into `data/interim/`.
5. Build model-ready tables under `data/processed/`.
6. Validate schema and target leakage.
7. Train experimental or official model.
8. Tune threshold for flood-warning behavior.
9. Save model artifact and metadata under `models/`.
10. Test API, model code, reports, and notebooks.
11. Serve predictions through FastAPI/Uvicorn.
12. Keep Streamlit as a readable public demo.
13. Commit and push clean changes to GitHub.

## Data Organization

| Folder | Purpose |
|---|---|
| `data/raw/` | Original downloaded files. Do not edit manually. |
| `data/interim/` | Normalized or reviewed intermediate data. |
| `data/processed/` | Clean tables ready for training or validation. |
| `data/external/` | Third-party reference files. |
| `data/samples/` | Small committed demo datasets. |
| `reports/` | Lightweight metrics, validation reports, and model notes. |
| `models/` | Local model artifacts. Binaries stay ignored by Git. |

## Experimental AI Pipeline

Run:

```powershell
.\scripts\run_experimental_ai_pipeline.ps1
```

This runs:

1. Kaggle dataset profile.
2. Logistic Regression flood baseline training.
3. Threshold tuning.
4. Focused API and ML tests.

Outputs:

- `reports/kaggle_baseline_profile.md`
- `reports/kaggle_flood_baseline_training_report.md`
- `reports/kaggle_flood_baseline_training_metrics.json`
- `reports/kaggle_flood_threshold_tuning_report.md`
- `reports/kaggle_flood_threshold_tuning_metrics.json`
- `models/kaggle_flood_baseline.joblib`
- `models/kaggle_flood_baseline_metadata.json`

Guardrail:

The Kaggle model is experimental. Do not present it as the final official
Malaysia flood model.

## API Flow

Run:

```powershell
.\scripts\run_api.ps1
```

Open:

```text
http://127.0.0.1:8000/docs
```

Core endpoints:

- `GET /health`
- `POST /predict`
- `GET /weather/summary`
- `GET /geospatial/summary`

Experimental AI endpoints:

- `GET /experimental/flood/model/status`
- `POST /experimental/flood/predict`

## Training Readiness Flow

Run:

```powershell
.\scripts\run_ml_readiness_suite.ps1
```

Real supervised ML training can start only when:

- a verified target source is ready
- `data/processed/targets/historical_flood_events.csv` exists
- target event schema validation passes
- `data/processed/model_training/training_features.csv` exists
- training table schema validation passes
- the table has rows
- target leakage checks pass

## EM-DAT Intake Flow

Current local artifact:

```text
data/raw/emdat/emdat_public_export.xlsx
```

Review command:

```powershell
.\scripts\run_emdat_export_review.ps1
```

Current review flow:

1. Convert workbook rows into an interim review table.
2. Keep only Malaysia flood records.
3. Build ISO start and end dates.
4. Extract state/district candidates from admin-unit fields.
5. Review license and attribution.
6. Map only verified rows into `historical_flood_events.csv`.

Review outputs:

- `data/interim/targets/emdat_historical_flood_events_review.csv`
- `reports/emdat_export_review.md`
- `reports/emdat_export_review_summary.json`

Do not copy EM-DAT rows into the final target table until the review passes.

## Quality Gate

Run:

```powershell
.\scripts\run_quality.ps1
```

Expected checks:

- Ruff lint
- Ruff format check
- Pytest

## GitHub Flow

Use a clean branch for each milestone:

```powershell
git checkout -b codex/experimental-ai-pipeline
git status
git add .
git commit -m "Add experimental AI flood prediction pipeline"
git push -u origin codex/experimental-ai-pipeline
```

Then open a draft pull request and review:

- changed code
- generated reports
- test results
- model/data guardrails
