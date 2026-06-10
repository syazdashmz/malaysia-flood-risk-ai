import json
from pathlib import Path

CONFIG_PATH = Path("configs/kaggle_experimental_baseline.json")
DOC_PATH = Path("docs/KAGGLE_EXPERIMENTAL_BASELINE.md")
REPORT_PATH = Path("reports/kaggle_baseline_profile.md")


def test_kaggle_experimental_baseline_config_exists():
    assert CONFIG_PATH.exists()


def test_kaggle_experimental_baseline_is_marked_experimental_only():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert config["experimental_training_allowed"] is True
    assert config["official_verified_target_source"] is False
    assert config["decision"] == "use_for_experimental_baseline_only"


def test_kaggle_experimental_baseline_targets_are_defined():
    config = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert config["target_columns"] == ["Flood", "Flash_Flood"]
    assert "Rainfall_7day" in config["feature_columns"]
    assert "Is_Monsoon" in config["feature_columns"]


def test_kaggle_experimental_baseline_documentation_exists():
    content = DOC_PATH.read_text(encoding="utf-8")
    report = REPORT_PATH.read_text(encoding="utf-8")

    assert "experimental baseline ML training" in content
    assert "Official verified target source: False" in report
    assert "Flood positive rows" in report
