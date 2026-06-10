"""Benchmark experimental Kaggle flood prediction models.

This script compares several scikit-learn tabular classifiers and selects a
candidate using a flood-aware objective instead of plain accuracy.

The benchmark is experimental only. It does not replace official validation
against EM-DAT, MyWater, DID, or other verified flood event records.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import HistGradientBoostingClassifier, RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder

CONFIG_PATH = Path("configs/kaggle_flood_model_benchmark.json")
RAW_PATH = Path("data/raw/kaggle/malaysia_flood_master.csv")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def safe_float(value: object) -> float | None:
    if value is None:
        return None

    if isinstance(value, float) and np.isnan(value):
        return None

    return round(float(value), 4)


def build_preprocessor(features: pd.DataFrame) -> ColumnTransformer:
    categorical_columns = [
        column for column in features.columns if features[column].dtype == "object"
    ]
    numeric_columns = [column for column in features.columns if column not in categorical_columns]

    numeric_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="median")),
        ],
    )

    categorical_transformer = Pipeline(
        steps=[
            ("imputer", SimpleImputer(strategy="most_frequent")),
            (
                "encoder",
                OneHotEncoder(
                    handle_unknown="ignore",
                    sparse_output=False,
                ),
            ),
        ],
    )

    return ColumnTransformer(
        transformers=[
            ("numeric", numeric_transformer, numeric_columns),
            ("categorical", categorical_transformer, categorical_columns),
        ],
    )


def candidate_models(random_state: int) -> dict[str, object]:
    return {
        "logistic_regression_balanced": LogisticRegression(
            class_weight="balanced",
            max_iter=2000,
            solver="liblinear",
            random_state=random_state,
        ),
        "random_forest_balanced": RandomForestClassifier(
            class_weight="balanced",
            n_estimators=300,
            min_samples_leaf=2,
            random_state=random_state,
            n_jobs=-1,
        ),
        "hist_gradient_boosting": HistGradientBoostingClassifier(
            learning_rate=0.05,
            max_iter=250,
            l2_regularization=0.01,
            random_state=random_state,
        ),
    }


def split_dataset(
    dataset: pd.DataFrame,
    date_column: str,
    train_before: str,
    test_from: str,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    data = dataset.copy()
    data[date_column] = pd.to_datetime(data[date_column], errors="coerce")

    train_mask = data[date_column] < pd.Timestamp(train_before)
    test_mask = data[date_column] >= pd.Timestamp(test_from)

    return data.loc[train_mask].copy(), data.loc[test_mask].copy()


def score_threshold(
    y_true: pd.Series,
    y_score: np.ndarray,
    threshold: float,
    pr_auc: float | None,
    roc_auc: float | None,
    weights: dict[str, float],
) -> dict[str, Any]:
    y_pred = y_score >= threshold

    tn, fp, fn, tp = confusion_matrix(y_true, y_pred, labels=[0, 1]).ravel()
    precision = precision_score(y_true, y_pred, zero_division=0)
    recall = recall_score(y_true, y_pred, zero_division=0)
    f1 = f1_score(y_true, y_pred, zero_division=0)
    accuracy = accuracy_score(y_true, y_pred)

    false_positive_rate = fp / (fp + tn) if (fp + tn) else 0.0

    priority_score = (
        weights["recall"] * recall
        + weights["f1"] * f1
        + weights["pr_auc"] * (pr_auc or 0.0)
        + weights["roc_auc"] * (roc_auc or 0.0)
        - weights["false_positive_rate_penalty"] * false_positive_rate
    )

    return {
        "threshold": safe_float(threshold),
        "accuracy": safe_float(accuracy),
        "precision": safe_float(precision),
        "recall": safe_float(recall),
        "f1": safe_float(f1),
        "pr_auc": safe_float(pr_auc),
        "roc_auc": safe_float(roc_auc),
        "false_positive_rate": safe_float(false_positive_rate),
        "flood_priority_score": safe_float(priority_score),
        "true_negative": int(tn),
        "false_positive": int(fp),
        "false_negative": int(fn),
        "true_positive": int(tp),
        "predicted_positive": int(tp + fp),
    }


def evaluate_model(
    name: str,
    estimator: object,
    x_train: pd.DataFrame,
    y_train: pd.Series,
    x_test: pd.DataFrame,
    y_test: pd.Series,
    weights: dict[str, float],
) -> dict[str, Any]:
    pipeline = Pipeline(
        steps=[
            ("preprocessor", build_preprocessor(x_train)),
            ("classifier", estimator),
        ],
    )

    pipeline.fit(x_train, y_train)

    if hasattr(pipeline, "predict_proba"):
        y_score = pipeline.predict_proba(x_test)[:, 1]
    else:
        decision_scores = pipeline.decision_function(x_test)
        y_score = 1 / (1 + np.exp(-decision_scores))

    try:
        pr_auc = average_precision_score(y_test, y_score)
    except ValueError:
        pr_auc = None

    try:
        roc_auc = roc_auc_score(y_test, y_score)
    except ValueError:
        roc_auc = None

    thresholds = [round(value, 2) for value in np.arange(0.05, 1.0, 0.05)]
    threshold_results = [
        score_threshold(y_test, y_score, threshold, pr_auc, roc_auc, weights)
        for threshold in thresholds
    ]

    best_result = max(
        threshold_results,
        key=lambda item: (
            item["flood_priority_score"] or 0.0,
            item["recall"] or 0.0,
            item["f1"] or 0.0,
        ),
    )

    return {
        "model_name": name,
        "best_threshold": best_result["threshold"],
        "best_result": best_result,
        "threshold_results": threshold_results,
    }


def build_report(
    config: dict[str, Any],
    baseline_config: dict[str, Any],
    results: list[dict[str, Any]],
    best_model: dict[str, Any],
    train_rows: int,
    test_rows: int,
    positive_train_rows: int,
    positive_test_rows: int,
) -> str:
    weights = config["priority_weights"]

    lines = [
        "# Kaggle Flood Model Benchmark Report",
        "",
        "## Guardrail",
        "",
        config["guardrail"],
        "",
        "## Mathematical Selection Objective",
        "",
        "The benchmark does not select by accuracy alone because flood events are imbalanced.",
        "",
        "```text",
        "flood_priority_score =",
        f"  {weights['recall']} * recall",
        f"+ {weights['f1']} * f1",
        f"+ {weights['pr_auc']} * pr_auc",
        f"+ {weights['roc_auc']} * roc_auc",
        f"- {weights['false_positive_rate_penalty']} * false_positive_rate",
        "```",
        "",
        "## Dataset Split",
        "",
        f"- Source ID: `{config['source_id']}`",
        f"- Target column: `{baseline_config['target_column']}`",
        f"- Train rows: {train_rows}",
        f"- Test rows: {test_rows}",
        f"- Train positive rows: {positive_train_rows}",
        f"- Test positive rows: {positive_test_rows}",
        "",
        "## Best Candidate",
        "",
        f"- Model: `{best_model['model_name']}`",
        f"- Threshold: {best_model['best_threshold']}",
        f"- Priority score: {best_model['best_result']['flood_priority_score']}",
        f"- Accuracy: {best_model['best_result']['accuracy']}",
        f"- Precision: {best_model['best_result']['precision']}",
        f"- Recall: {best_model['best_result']['recall']}",
        f"- F1: {best_model['best_result']['f1']}",
        f"- PR-AUC: {best_model['best_result']['pr_auc']}",
        f"- ROC-AUC: {best_model['best_result']['roc_auc']}",
        f"- False positive rate: {best_model['best_result']['false_positive_rate']}",
        "",
        "## Model Comparison",
        "",
        (
            "| Model | Threshold | Priority | Accuracy | Precision | Recall | "
            "F1 | PR-AUC | ROC-AUC | FPR |"
        ),
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]

    for result in sorted(
        results,
        key=lambda item: item["best_result"]["flood_priority_score"] or 0.0,
        reverse=True,
    ):
        best = result["best_result"]
        lines.append(
            "| "
            + " | ".join(
                [
                    f"`{result['model_name']}`",
                    str(result["best_threshold"]),
                    str(best["flood_priority_score"]),
                    str(best["accuracy"]),
                    str(best["precision"]),
                    str(best["recall"]),
                    str(best["f1"]),
                    str(best["pr_auc"]),
                    str(best["roc_auc"]),
                    str(best["false_positive_rate"]),
                ],
            )
            + " |",
        )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            "This benchmark identifies a stronger experimental candidate, but final model",
            "selection still requires validation against official EM-DAT and MyWater/DID",
            "flood event records.",
            "",
        ],
    )

    return "\n".join(lines)


def main() -> None:
    config = load_json(CONFIG_PATH)
    baseline_config = load_json(Path(config["baseline_config_path"]))

    data_path = Path(baseline_config.get("dataset_path", RAW_PATH.as_posix()))

    if not data_path.exists():
        raise SystemExit(f"Missing raw Kaggle dataset: {data_path}")

    dataset = pd.read_csv(data_path)

    feature_columns = baseline_config["feature_columns"]
    target_column = baseline_config["target_column"]
    date_column = baseline_config["date_column"]
    split_config = baseline_config["time_split"]

    train_data, test_data = split_dataset(
        dataset,
        date_column=date_column,
        train_before=split_config["train_before"],
        test_from=split_config["test_from"],
    )

    x_train = train_data[feature_columns]
    y_train = train_data[target_column].astype(int)
    x_test = test_data[feature_columns]
    y_test = test_data[target_column].astype(int)

    weights = config["priority_weights"]
    random_state = int(baseline_config.get("random_state", 42))

    results = [
        evaluate_model(
            name,
            estimator,
            x_train,
            y_train,
            x_test,
            y_test,
            weights,
        )
        for name, estimator in candidate_models(random_state).items()
    ]

    best_model = max(
        results,
        key=lambda item: (
            item["best_result"]["flood_priority_score"] or 0.0,
            item["best_result"]["recall"] or 0.0,
            item["best_result"]["f1"] or 0.0,
        ),
    )

    metrics = {
        "source_id": config["source_id"],
        "training_mode": config["training_mode"],
        "selection_metric": config["selection_metric"],
        "priority_weights": weights,
        "guardrail": config["guardrail"],
        "feature_columns": feature_columns,
        "target_column": target_column,
        "train_rows": int(len(train_data)),
        "test_rows": int(len(test_data)),
        "train_positive_rows": int(y_train.sum()),
        "test_positive_rows": int(y_test.sum()),
        "best_model": best_model,
        "models": results,
    }

    metrics_path = Path(config["metrics_path"])
    report_path = Path(config["report_path"])

    metrics_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.parent.mkdir(parents=True, exist_ok=True)

    metrics_path.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    report_path.write_text(
        build_report(
            config=config,
            baseline_config=baseline_config,
            results=results,
            best_model=best_model,
            train_rows=int(len(train_data)),
            test_rows=int(len(test_data)),
            positive_train_rows=int(y_train.sum()),
            positive_test_rows=int(y_test.sum()),
        ),
        encoding="utf-8",
    )

    best = best_model["best_result"]

    print(f"Generated benchmark metrics: {metrics_path}")
    print(f"Generated benchmark report: {report_path}")
    print(f"Best model: {best_model['model_name']}")
    print(f"Best threshold: {best_model['best_threshold']}")
    print(f"Priority score: {best['flood_priority_score']}")
    print(f"Accuracy: {best['accuracy']}")
    print(f"Precision: {best['precision']}")
    print(f"Recall: {best['recall']}")
    print(f"F1: {best['f1']}")
    print(f"PR-AUC: {best['pr_auc']}")
    print(f"ROC-AUC: {best['roc_auc']}")
    print(f"False positive rate: {best['false_positive_rate']}")


if __name__ == "__main__":
    main()
