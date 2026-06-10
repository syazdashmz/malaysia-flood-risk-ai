from pathlib import Path

CONFIG_PATH = Path("configs/kaggle_flood_model_benchmark.json")
SCRIPT_PATH = Path("scripts/benchmark_kaggle_flood_models.py")


def test_kaggle_flood_model_benchmark_config_exists():
    assert CONFIG_PATH.exists()


def test_kaggle_flood_model_benchmark_script_exists():
    assert SCRIPT_PATH.exists()


def test_kaggle_flood_model_benchmark_uses_flood_priority_score():
    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "flood_priority_score" in content
    assert "false_positive_rate" in content
    assert "average_precision_score" in content
    assert "roc_auc_score" in content


def test_kaggle_flood_model_benchmark_compares_multiple_models():
    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "LogisticRegression" in content
    assert "RandomForestClassifier" in content
    assert "HistGradientBoostingClassifier" in content


def test_kaggle_flood_model_benchmark_has_raw_dataset_fallback():
    content = SCRIPT_PATH.read_text(encoding="utf-8")

    assert "data/raw/kaggle/malaysia_flood_master.csv" in content
    assert "baseline_config.get" in content
