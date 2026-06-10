import json
from pathlib import Path

CONFIG_PATH = Path("configs/kaggle_flood_baseline_training.json")
REPORT_PATH = Path("reports/kaggle_flood_baseline_training_report.md")
METRICS_PATH = Path("reports/kaggle_flood_baseline_training_metrics.json")


def test_kaggle_flood_baseline_training_config_exists():
    assert CONFIG_PATH.exists()


def test_kaggle_flood_baseline_uses_no_target_leakage_features():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert config["target_column"] == "Flood"
    assert "Flood" not in config["feature_columns"]
    assert "Flash_Flood" not in config["feature_columns"]
    assert set(config["excluded_columns"]) == {"Flood", "Flash_Flood"}


def test_kaggle_flood_baseline_uses_temporal_split():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert config["time_split"]["train_before"] == "2024-01-01"
    assert config["time_split"]["test_from"] == "2024-01-01"


def test_kaggle_flood_baseline_training_outputs_exist():
    assert REPORT_PATH.exists()
    assert METRICS_PATH.exists()


def test_kaggle_flood_baseline_metrics_are_valid():
    metrics = json.loads(METRICS_PATH.read_text(encoding="utf-8"))

    assert metrics["training_mode"] == "experimental_baseline"
    assert metrics["target_column"] == "Flood"
    assert metrics["train_rows"] > 0
    assert metrics["test_rows"] > 0
    assert metrics["test_positive_rows"] > 0
    assert 0 <= metrics["f1"] <= 1
    assert 0 <= metrics["recall"] <= 1
    assert 0 <= metrics["precision"] <= 1
