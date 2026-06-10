import json
from pathlib import Path

CONFIG_PATH = Path("configs/emdat_export_intake_plan.json")
DOC_PATH = Path("docs/EMDAT_EXPORT_INTAKE.md")
REPORT_PATH = Path("reports/emdat_export_intake_plan.md")


def test_emdat_export_intake_plan_config_exists():
    assert CONFIG_PATH.exists()


def test_emdat_export_intake_paths_are_defined():
    plan = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert plan["raw_export_path"] == "data/raw/emdat/emdat_public_export.xlsx"
    assert (
        plan["interim_review_path"]
        == "data/interim/targets/emdat_historical_flood_events_review.csv"
    )
    assert plan["review_report_path"] == "reports/emdat_export_review.md"
    assert plan["review_summary_path"] == "reports/emdat_export_review_summary.json"
    assert plan["processed_target_path"] == "data/processed/targets/historical_flood_events.csv"


def test_emdat_export_intake_requires_malaysia_flood_filter():
    plan = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert plan["required_filter"]["country"] == "Malaysia"
    assert plan["required_filter"]["disaster_type"] == "Flood"


def test_emdat_export_intake_keeps_training_blocked():
    plan = json.loads(CONFIG_PATH.read_text(encoding="utf-8"))

    assert plan["target_label_candidate"] is True
    assert plan["direct_training_use_allowed"] is False
    assert "target leakage risk is checked before training" in plan["approval_requirements"]


def test_emdat_export_intake_documentation_exists():
    content = DOC_PATH.read_text(encoding="utf-8")
    report = REPORT_PATH.read_text(encoding="utf-8")

    assert "data/raw/emdat/emdat_public_export.xlsx" in content
    assert "not an approved training source" in content
    assert "Direct training use allowed now: False" in report
