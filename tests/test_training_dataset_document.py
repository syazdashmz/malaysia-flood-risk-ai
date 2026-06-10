import re
from pathlib import Path


def test_training_dataset_document_exists():
    assert Path("docs/TRAINING_DATASET.md").exists()


def test_training_dataset_document_defines_target_label():
    content = Path("docs/TRAINING_DATASET.md").read_text(encoding="utf-8")

    assert "flood_occurred" in content
    assert "binary classification" in content


def test_training_dataset_document_defines_training_table_path():
    content = Path("docs/TRAINING_DATASET.md").read_text(encoding="utf-8")

    assert "data/processed/model_training/training_features.csv" in content


def test_training_dataset_document_mentions_leakage_risks():
    content = Path("docs/TRAINING_DATASET.md").read_text(encoding="utf-8")

    assert "Data Leakage Risks" in content
    assert re.search(r"future rainfall", content, re.IGNORECASE)


def test_training_dataset_document_keeps_training_not_started_clear():
    content = Path("docs/TRAINING_DATASET.md").read_text(encoding="utf-8")

    assert "not ready for real AI/ML training yet" in content
    assert "baseline ML training: not started yet" in content
