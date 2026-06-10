from __future__ import annotations

import json
from pathlib import Path

import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

RAW_PATH = Path("data/raw/kaggle/malaysia_flood_master.csv")
CONFIG_PATH = Path("configs/kaggle_flood_baseline_training.json")
REPORT_PATH = Path("reports/kaggle_flood_baseline_training_report.md")
METRICS_PATH = Path("reports/kaggle_flood_baseline_training_metrics.json")


def safe_float(value: object) -> float | None:
    if value is None:
        return None
    return round(float(value), 4)


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

    target_column = config["target_column"]
    feature_columns = config["feature_columns"]
    train_before = pd.Timestamp(config["time_split"]["train_before"])
    test_from = pd.Timestamp(config["time_split"]["test_from"])

    df[target_column] = df[target_column].astype(int)

    train_df = df[df[config["date_column"]] < train_before].copy()
    test_df = df[df[config["date_column"]] >= test_from].copy()

    if train_df.empty or test_df.empty:
        raise SystemExit("Temporal split produced an empty train or test set.")

    if train_df[target_column].nunique() < 2:
        raise SystemExit("Training split does not contain both target classes.")

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

    y_pred = pipeline.predict(x_test)
    y_score = pipeline.predict_proba(x_test)[:, 1]

    labels = [0, 1]
    tn, fp, fn, tp = confusion_matrix(y_test, y_pred, labels=labels).ravel()

    roc_auc = None
    if y_test.nunique() > 1:
        roc_auc = roc_auc_score(y_test, y_score)

    metrics = {
        "source_id": config["source_id"],
        "training_mode": config["training_mode"],
        "model": config["model"],
        "target_column": target_column,
        "feature_columns": feature_columns,
        "excluded_columns": config["excluded_columns"],
        "train_before": config["time_split"]["train_before"],
        "test_from": config["time_split"]["test_from"],
        "total_rows": int(len(df)),
        "train_rows": int(len(train_df)),
        "test_rows": int(len(test_df)),
        "train_positive_rows": int(y_train.sum()),
        "test_positive_rows": int(y_test.sum()),
        "test_predicted_positive_rows": int(y_pred.sum()),
        "accuracy": safe_float(accuracy_score(y_test, y_pred)),
        "precision": safe_float(
            precision_score(y_test, y_pred, zero_division=0),
        ),
        "recall": safe_float(recall_score(y_test, y_pred, zero_division=0)),
        "f1": safe_float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": safe_float(roc_auc) if roc_auc is not None else None,
        "confusion_matrix": {
            "true_negative": int(tn),
            "false_positive": int(fp),
            "false_negative": int(fn),
            "true_positive": int(tp),
        },
        "guardrail": config["guardrail"],
    }

    METRICS_PATH.parent.mkdir(parents=True, exist_ok=True)
    METRICS_PATH.write_text(
        json.dumps(metrics, indent=2),
        encoding="utf-8",
    )

    report = [
        "# Kaggle Flood Baseline Training Report",
        "",
        "## Summary",
        "",
        "- Training mode: experimental baseline",
        "- Official verified target source: False",
        f"- Model: `{metrics['model']}`",
        f"- Target column: `{metrics['target_column']}`",
        f"- Total rows: {metrics['total_rows']}",
        f"- Train rows: {metrics['train_rows']}",
        f"- Test rows: {metrics['test_rows']}",
        f"- Train positive rows: {metrics['train_positive_rows']}",
        f"- Test positive rows: {metrics['test_positive_rows']}",
        "",
        "## Temporal Split",
        "",
        f"- Train before: `{metrics['train_before']}`",
        f"- Test from: `{metrics['test_from']}`",
        "",
        "## Features",
        "",
    ]

    report.extend(f"- `{column}`" for column in feature_columns)

    report.extend(
        [
            "",
            "## Excluded Columns",
            "",
        ],
    )
    report.extend(f"- `{column}`" for column in config["excluded_columns"])

    report.extend(
        [
            "",
            "## Metrics",
            "",
            f"- Accuracy: {metrics['accuracy']}",
            f"- Precision: {metrics['precision']}",
            f"- Recall: {metrics['recall']}",
            f"- F1: {metrics['f1']}",
            f"- ROC AUC: {metrics['roc_auc']}",
            "",
            "## Confusion Matrix",
            "",
            f"- True negative: {tn}",
            f"- False positive: {fp}",
            f"- False negative: {fn}",
            f"- True positive: {tp}",
            "",
            "## Guardrail",
            "",
            metrics["guardrail"],
            "",
        ],
    )

    REPORT_PATH.write_text("\n".join(report), encoding="utf-8")

    print(f"Generated training metrics: {METRICS_PATH}")
    print(f"Generated training report: {REPORT_PATH}")
    print(f"Accuracy: {metrics['accuracy']}")
    print(f"Precision: {metrics['precision']}")
    print(f"Recall: {metrics['recall']}")
    print(f"F1: {metrics['f1']}")
    print(f"ROC AUC: {metrics['roc_auc']}")


if __name__ == "__main__":
    main()
