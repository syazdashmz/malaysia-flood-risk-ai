from pathlib import Path


def test_data_acquisition_plan_exists():
    path = Path("docs/DATA_ACQUISITION_PLAN.md")

    assert path.exists()


def test_data_acquisition_plan_mentions_target_output():
    content = Path("docs/DATA_ACQUISITION_PLAN.md").read_text(encoding="utf-8")

    assert "data/processed/targets/historical_flood_events.csv" in content
    assert "flood_occurred" in content
    assert "run_ml_readiness_suite.ps1" in content


def test_data_source_review_checklist_exists():
    path = Path("docs/DATA_SOURCE_REVIEW_CHECKLIST.md")

    assert path.exists()


def test_data_source_review_checklist_blocks_risk_score_leakage():
    content = Path("docs/DATA_SOURCE_REVIEW_CHECKLIST.md").read_text(encoding="utf-8")

    assert "risk_score" in content
    assert "Source does not depend on project `risk_score`" in content
