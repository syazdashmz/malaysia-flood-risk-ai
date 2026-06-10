from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAW_PATH = Path("data/raw/kaggle/malaysia_flood_master.csv")
CONFIG_PATH = Path("configs/kaggle_flood_baseline_training.json")
REPORT_PATH = Path("reports/kaggle_flood_threshold_tuning_report.md")
METRICS_PATH = Path("reports/kaggle_flood_threshold_tuning_metrics.json")


def metric_row(y_true, y_score, threshold: float) -> dict:
    y_pred = (y_score >= threshold).astype(int)
    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()

    return {
        "threshold": round(float(threshold), 2),
        "precision": round(float(precision_score(y_true, y_pred, zero_division=0)), 4),
        "recall": round(float(recall_score(y_true, y_pred, zero_division=0)), 4),
        "f1": round(float(f1_score(y_true, y_pred, zero_division=0)), 4),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
        "predicted_positive": int(y_pred.sum()),
    }


def main() -> None:
    if not RAW_PATH.exists():
        raise SystemExit(f"Missing raw Kaggle dataset: {RAW_PATH}")

    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    df = pd.read_csv(RAW_PATH)
    df[config["date_column"]] = pd.to_datetime(
        df[config["date_column"]],
        errors="coerce",
    )
    df = df.dropna(subset=[config["date_column"]]).copy()
    df[config["target_column"]] = df[config["target_column"]].astype(int)

    train_before = pd.Timestamp(config["time_split"]["train_before"])
    test_from = pd.Timestamp(config["time_split"]["test_from"])

    train_df = df[df[config["date_column"]] < train_before].copy()
    test_df = df[df[config["date_column"]] >= test_from].copy()

    feature_columns = config["feature_columns"]
    target_column = config["target_column"]

    x_train = train_df[feature_columns]
    y_train = train_df[target_column]
    x_test = test_df[feature_columns]
    y_test = test_df[target_column]

    numeric_features = [column for column in feature_columns if column != "City"]
    categorical_features = ["City"]

    preprocessor = ColumnTransformer(
        transformers=[
            (
                "numeric",
                Pipeline(
                    steps=[
                        ("imputer", SimpleImputer(strategy="median")),
                        ("scaler", StandardScaler()),
                    ],
                ),
                numeric_features,
            ),
            (
                "categorical",
                OneHotEncoder(handle_unknown="ignore"),
                categorical_features,
            ),
        ],
    )

    model = LogisticRegression(
        class_weight="balanced",
        max_iter=1000,
        solver="liblinear",
        random_state=42,
    )

    pipeline = Pipeline(
        steps=[
            ("preprocessor", preprocessor),
            ("model", model),
        ],
    )

    pipeline.fit(x_train, y_train)
    y_score = pipeline.predict_proba(x_test)[:, 1]

    thresholds = [round(i / 100, 2) for i in range(5, 96, 5)]
    rows = [metric_row(y_test, y_score, threshold) for threshold in thresholds]

    best_f1 = max(rows, key=lambda row: row["f1"])
    high_recall_candidates = [row for row in rows if row["recall"] >= 0.95]
    best_high_recall = max(
        high_recall_candidates,
        key=lambda row: (row["precision"], row["f1"]),
    )

    high_precision_candidates = [row for row in rows if row["precision"] >= 0.5]
    best_high_precision = (
        max(high_precision_candidates, key=lambda row: row["recall"])
        if high_precision_candidates
        else None
    )

    payload = {
        "source_id": config["source_id"],
        "training_mode": "experimental_threshold_tuning",
        "target_column": target_column,
        "test_rows": int(len(test_df)),
        "test_positive_rows": int(y_test.sum()),
        "best_f1": best_f1,
        "best_high_recall": best_high_recall,
        "best_high_precision": best_high_precision,
        "thresholds": rows,
        "guardrail": config["guardrail"],
    }

    METRICS_PATH.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    report = [
        "# Kaggle Flood Threshold Tuning Report",
        "",
        "## Summary",
        "",
        "- Training mode: experimental threshold tuning",
        "- Official verified target source: False",
        f"- Target column: `{target_column}`",
        f"- Test rows: {len(test_df)}",
        f"- Test positive rows: {int(y_test.sum())}",
        "",
        "## Recommended Thresholds",
        "",
        "### Best F1",
        "",
        f"- Threshold: {best_f1['threshold']}",
        f"- Precision: {best_f1['precision']}",
        f"- Recall: {best_f1['recall']}",
        f"- F1: {best_f1['f1']}",
        f"- False positives: {best_f1['false_positive']}",
        f"- False negatives: {best_f1['false_negative']}",
        "",
        "### High Recall Flood Warning",
        "",
        f"- Threshold: {best_high_recall['threshold']}",
        f"- Precision: {best_high_recall['precision']}",
        f"- Recall: {best_high_recall['recall']}",
        f"- F1: {best_high_recall['f1']}",
        f"- False positives: {best_high_recall['false_positive']}",
        f"- False negatives: {best_high_recall['false_negative']}",
        "",
    ]

    if best_high_precision:
        report.extend(
            [
                "### Higher Precision Candidate",
                "",
                f"- Threshold: {best_high_precision['threshold']}",
                f"- Precision: {best_high_precision['precision']}",
                f"- Recall: {best_high_precision['recall']}",
                f"- F1: {best_high_precision['f1']}",
                f"- False positives: {best_high_precision['false_positive']}",
                f"- False negatives: {best_high_precision['false_negative']}",
                "",
            ],
        )

    report.extend(
        [
            "## Threshold Table",
            "",
            "| Threshold | Precision | Recall | F1 | FP | FN | TP | TN |",
            "|---:|---:|---:|---:|---:|---:|---:|---:|",
        ],
    )

    for row in rows:
        report.append(
            f"| {row['threshold']} | {row['precision']} | {row['recall']} | "
            f"{row['f1']} | {row['false_positive']} | {row['false_negative']} | "
            f"{row['true_positive']} | {row['true_negative']} |",
        )

    report.extend(
        [
            "",
            "## Guardrail",
            "",
            config["guardrail"],
            "",
        ],
    )

    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"Generated threshold metrics: {METRICS_PATH}")
    print(f"Generated threshold report: {REPORT_PATH}")
    print("Best F1:", best_f1)
    print("Best high recall:", best_high_recall)
    print("Best high precision:", best_high_precision)


if __name__ == "__main__":
    main()
