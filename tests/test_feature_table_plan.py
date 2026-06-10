from pathlib import Path

from floodrisk.ml.feature_table_plan import (
    build_feature_table_plan,
    render_feature_table_plan_report,
    write_feature_table_plan_report,
)
from floodrisk.ml.training_schema import REQUIRED_TRAINING_COLUMNS, TARGET_COLUMN


def test_feature_table_plan_covers_required_training_columns():
    plan_items = build_feature_table_plan()
    planned_columns = {item.column for item in plan_items}

    assert set(REQUIRED_TRAINING_COLUMNS) == planned_columns


def test_feature_table_plan_keeps_target_not_ready():
    plan_items = build_feature_table_plan()
    target_item = next(item for item in plan_items if item.column == TARGET_COLUMN)

    assert target_item.role == "target"
    assert target_item.ready_now is False
    assert "verified historical flood source" in target_item.derivation_note


def test_feature_table_plan_has_some_current_proxy_sources():
    plan_items = build_feature_table_plan()
    ready_items = [item for item in plan_items if item.ready_now]

    assert ready_items
    assert any(item.column == "latitude" for item in ready_items)
    assert any(item.column == "weather_warning_status" for item in ready_items)


def test_render_feature_table_plan_report_blocks_real_training():
    report = render_feature_table_plan_report(build_feature_table_plan())

    assert "Feature Table Generation Plan" in report
    assert "Real ML training allowed now: False" in report
    assert "flood_occurred" in report


def test_write_feature_table_plan_report(tmp_path: Path):
    output_path = tmp_path / "feature_table_plan.md"
    saved_path = write_feature_table_plan_report(
        build_feature_table_plan(),
        output_path,
    )

    assert saved_path.exists()
    assert "Feature Table Generation Plan" in saved_path.read_text(encoding="utf-8")
