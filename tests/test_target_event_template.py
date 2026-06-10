from pathlib import Path

from floodrisk.ml.target_event_schema import REQUIRED_TARGET_EVENT_COLUMNS


def test_historical_flood_events_template_exists():
    path = Path("templates/targets/historical_flood_events_template.csv")

    assert path.exists()


def test_historical_flood_events_template_matches_required_columns():
    path = Path("templates/targets/historical_flood_events_template.csv")
    header = path.read_text(encoding="utf-8").splitlines()[0].split(",")

    assert header == REQUIRED_TARGET_EVENT_COLUMNS


def test_target_event_source_template_documentation_exists():
    path = Path("docs/TARGET_EVENT_SOURCE_TEMPLATE.md")
    content = path.read_text(encoding="utf-8")

    assert "historical_flood_events_template.csv" in content
    assert "flood_occurred" in content
    assert "Do not derive `flood_occurred` from the rule-based `risk_score`" in content
