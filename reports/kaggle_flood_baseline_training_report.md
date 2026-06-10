# Kaggle Flood Baseline Training Report

## Summary

- Training mode: experimental baseline
- Official verified target source: False
- Model: `logistic_regression_balanced`
- Target column: `Flood`
- Total rows: 47367
- Train rows: 40800
- Test rows: 6567
- Train positive rows: 489
- Test positive rows: 187

## Temporal Split

- Train before: `2024-01-01`
- Test from: `2024-01-01`

## Features

- `City`
- `Temperature_C`
- `Humidity_pct`
- `Wind_Speed_ms`
- `Rainfall_3day`
- `Rainfall_7day`
- `Rainfall_14day`
- `Rainfall_cumsum7`
- `Month`
- `Is_Monsoon`

## Excluded Columns

- `Flood`
- `Flash_Flood`

## Metrics

- Accuracy: 0.9202
- Precision: 0.2623
- Recall: 0.9947
- F1: 0.4152
- ROC AUC: 0.9871

## Confusion Matrix

- True negative: 5857
- False positive: 523
- False negative: 1
- True positive: 186

## Guardrail

Experimental proxy baseline only. Do not present as final official verified flood model.
