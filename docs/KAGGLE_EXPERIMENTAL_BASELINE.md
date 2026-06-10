# Kaggle Experimental Baseline Dataset

This dataset is used for fast experimental baseline ML training.

## Source

- Source ID: `kaggle_malaysia_flood_master`
- Source type: third-party Kaggle dataset
- Raw local path: `data/raw/kaggle/malaysia_flood_master.csv`

## Intended Use

Use this dataset for:

- exploratory baseline training
- feature pipeline testing
- model evaluation workflow setup
- early portfolio demonstration

## Guardrail

This dataset is not treated as the final official verified Malaysia flood target
source. EM-DAT and MyWater remain the official-source validation track.

## Target Columns

- `Flood`
- `Flash_Flood`

## Feature Columns

- `Temperature_C`
- `Humidity_pct`
- `Wind_Speed_ms`
- `Rainfall_3day`
- `Rainfall_7day`
- `Rainfall_14day`
- `Rainfall_cumsum7`
- `Month`
- `Is_Monsoon`

## Decision

Allowed for experimental baseline ML training only.

## Training Command

Run the full experimental AI pipeline:

    .\scripts\run_experimental_ai_pipeline.ps1

Or train only the model artifact:

    python scripts\train_kaggle_flood_baseline.py

## Local Model Outputs

- `models/kaggle_flood_baseline.joblib`
- `models/kaggle_flood_baseline_metadata.json`

Model binaries are local artifacts and are not committed to Git.

## API Integration

Run the API:

    .\scripts\run_api.ps1

Open:

    http://127.0.0.1:8000/docs

Experimental endpoints:

- `GET /experimental/flood/model/status`
- `POST /experimental/flood/predict`
