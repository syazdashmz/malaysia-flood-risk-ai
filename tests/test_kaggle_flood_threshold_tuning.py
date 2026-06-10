import json
from pathlib import Path

REPORT_PATH = Path("reports/kaggle_flood_threshold_tuning_report.md")
METRICS_PATH = Path("reports/kaggle_flood_threshold_tuning_metrics.json")


def test_kaggle_flood_threshold_tuning_outputs_exist():
    assert REPORT_PATH.exists()
    assert METRICS_PATH.exists()


def test_kaggle_flood_threshold_tuning_has_recommendations():
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))

    assert metrics["training_mode"] == "experimental_threshold_tuning"
    assert metrics["target_column"] == "Flood"
    assert metrics["best_f1"]["threshold"] > 0
    assert metrics["best_high_recall"]["recall"] >= 0.95
    assert len(metrics["thresholds"]) >= 10


def test_kaggle_flood_threshold_tuning_report_has_table():
    report = REPORT_PATH.read_text(encoding="utf-8")

    assert "Best F1" in report
    assert "High Recall Flood Warning" in report
    assert "| Threshold | Precision | Recall | F1 | FP | FN | TP | TN |" in report
