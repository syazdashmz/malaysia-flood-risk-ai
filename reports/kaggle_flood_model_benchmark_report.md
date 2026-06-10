# Kaggle Flood Model Benchmark Report

## Guardrail

Experimental proxy model benchmark only. Do not present as an official verified flood warning model.

## Mathematical Selection Objective

The benchmark does not select by accuracy alone because flood events are imbalanced.

```text
flood_priority_score =
  0.5 * recall
+ 0.25 * f1
+ 0.15 * pr_auc
+ 0.1 * roc_auc
- 0.1 * false_positive_rate
```

## Dataset Split

- Source ID: `kaggle_malaysia_flood_master`
- Target column: `Flood`
- Train rows: 40800
- Test rows: 6567
- Train positive rows: 489
- Test positive rows: 187

## Best Candidate

- Model: `logistic_regression_balanced`
- Threshold: 0.8
- Priority score: 0.8113
- Accuracy: 0.9569
- Precision: 0.3938
- Recall: 0.9519
- F1: 0.5571
- PR-AUC: 0.6779
- ROC-AUC: 0.9868
- False positive rate: 0.0429

## Model Comparison

| Model | Threshold | Priority | Accuracy | Precision | Recall | F1 | PR-AUC | ROC-AUC | FPR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| `logistic_regression_balanced` | 0.8 | 0.8113 | 0.9569 | 0.3938 | 0.9519 | 0.5571 | 0.6779 | 0.9868 | 0.0429 |
| `hist_gradient_boosting` | 0.05 | 0.7843 | 0.9519 | 0.3665 | 0.9465 | 0.5284 | 0.5678 | 0.9854 | 0.048 |
| `random_forest_balanced` | 0.15 | 0.7831 | 0.9414 | 0.3238 | 0.9733 | 0.486 | 0.5501 | 0.9841 | 0.0596 |

## Interpretation

This benchmark identifies a stronger experimental candidate, but final model
selection still requires validation against official EM-DAT and MyWater/DID
flood event records.
