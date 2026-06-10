import json
from pathlib import Path

CONFIG_PATH = Path("configs/emdat_target_source_review.json")
DOC_PATH = Path("docs/EMDAT_TARGET_SOURCE_REVIEW.md")
REPORT_PATH = Path("reports/emdat_target_source_review.md")


def test_emdat_target_source_review_config_exists():
    assert CONFIG_PATH.exists()


def test_emdat_is_candidate_but_not_training_approved():
    review = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert review["source_id"] == "emdat"
    assert review["target_label_candidate"] is True
    assert review["direct_training_use_allowed"] is False
    assert review["candidate_target_column"] == "flood_occurred"


def test_emdat_review_requires_location_and_date_checks():
    review = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))
    steps = " ".join(review["required_review_steps"])

    assert "event date fields" in steps
    assert "location granularity" in steps
    assert "historical_flood_events.csv" in steps


def test_emdat_review_document_blocks_training():
    content = DOC_PATH.read_text(encoding="utf-8")

    assert "must not be used directly for supervised ML training" in content
    assert "data/processed/targets/historical_flood_events.csv" in content
    assert "Review EM-DAT next" in content


def test_emdat_review_report_exists_and_keeps_readiness_blocked():
    content = REPORT_PATH.read_text(encoding="utf-8")

    assert "Direct training use allowed now: False" in content
    assert "real_ml_training_ready" in content
    assert "verified target source" in content
