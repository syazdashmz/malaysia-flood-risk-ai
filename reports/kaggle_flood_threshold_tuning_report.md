# Kaggle Flood Threshold Tuning Report

## Summary

- Training mode: experimental threshold tuning
- Official verified target source: False
- Target column: `Flood`
- Test rows: 6567
- Test positive rows: 187

## Recommended Thresholds

### Best F1

- Threshold: 0.95
- Precision: 0.4716
- Recall: 0.8877
- F1: 0.616
- False positives: 186
- False negatives: 21

### High Recall Flood Warning

- Threshold: 0.75
- Precision: 0.3475
- Recall: 0.9626
- F1: 0.5106
- False positives: 338
- False negatives: 7

## Threshold Table

| Threshold | Precision | Recall | F1 | FP | FN | TP | TN |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0.05 | 0.0971 | 1.0 | 0.177 | 1739 | 0 | 187 | 4641 |
| 0.1 | 0.1273 | 1.0 | 0.2258 | 1282 | 0 | 187 | 5098 |
| 0.15 | 0.1501 | 1.0 | 0.261 | 1059 | 0 | 187 | 5321 |
| 0.2 | 0.1711 | 1.0 | 0.2922 | 906 | 0 | 187 | 5474 |
| 0.25 | 0.1889 | 1.0 | 0.3178 | 803 | 0 | 187 | 5577 |
| 0.3 | 0.2022 | 1.0 | 0.3363 | 738 | 0 | 187 | 5642 |
| 0.35 | 0.2167 | 1.0 | 0.3562 | 676 | 0 | 187 | 5704 |
| 0.4 | 0.232 | 1.0 | 0.3766 | 619 | 0 | 187 | 5761 |
| 0.45 | 0.2487 | 0.9947 | 0.3979 | 562 | 1 | 186 | 5818 |
| 0.5 | 0.2623 | 0.9947 | 0.4152 | 523 | 1 | 186 | 5857 |
| 0.55 | 0.2776 | 0.9947 | 0.4341 | 484 | 1 | 186 | 5896 |
| 0.6 | 0.2946 | 0.9893 | 0.454 | 443 | 2 | 185 | 5937 |
| 0.65 | 0.3091 | 0.9786 | 0.4698 | 409 | 4 | 183 | 5971 |
| 0.7 | 0.3249 | 0.9626 | 0.4858 | 374 | 7 | 180 | 6006 |
| 0.75 | 0.3475 | 0.9626 | 0.5106 | 338 | 7 | 180 | 6042 |
| 0.8 | 0.3649 | 0.9465 | 0.5268 | 308 | 10 | 177 | 6072 |
| 0.85 | 0.3929 | 0.9412 | 0.5543 | 272 | 11 | 176 | 6108 |
| 0.9 | 0.4237 | 0.9358 | 0.5833 | 238 | 12 | 175 | 6142 |
| 0.95 | 0.4716 | 0.8877 | 0.616 | 186 | 21 | 166 | 6194 |

## Guardrail

Experimental proxy baseline only. Do not present as final official verified flood model.
