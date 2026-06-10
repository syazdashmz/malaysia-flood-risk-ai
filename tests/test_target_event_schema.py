from pathlib import Path

from floodrisk.ml.target_event_schema import (
    REQUIRED_TARGET_EVENT_COLUMNS,
    render_target_event_source_schema_report,
    validate_target_event_source_schema,
)


def write_target_source(path: Path, rows: list[str]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ",".join(REQUIRED_TARGET_EVENT_COLUMNS)
    path.write_text(header + "\n" + "\n".join(rows) + "\n", encoding="utf-8")
    return path


def test_missing_target_event_source_is_not_ready(tmp_path: Path):
    validation = validate_target_event_source_schema(tmp_path)

    assert validation.exists is False
    assert validation.is_schema_valid is False
    assert validation.is_ready_for_target_generation is False
    assert "flood_occurred" in validation.missing_columns


def test_valid_target_event_source_is_ready(tmp_path: Path):
    row = (
        "evt-001,example,https://example.com,open,"
        "2020-01-01,2020-01-02,3.1,101.7,Selangor,Petaling,1,verified,note"
    )
    write_target_source(
        tmp_path / "data/processed/targets/historical_flood_events.csv",
        [row],
    )

    validation = validate_target_event_source_schema(tmp_path)

    assert validation.exists is True
    assert validation.row_count == 1
    assert validation.is_schema_valid is True
    assert validation.is_ready_for_target_generation is True


def test_invalid_target_event_source_rejects_bad_binary_label(tmp_path: Path):
    row = (
        "evt-001,example,https://example.com,open,"
        "2020-01-01,2020-01-02,3.1,101.7,Selangor,Petaling,yes,verified,note"
    )
    write_target_source(
        tmp_path / "data/processed/targets/historical_flood_events.csv",
        [row],
    )

    validation = validate_target_event_source_schema(tmp_path)

    assert validation.is_schema_valid is False
    assert any("flood_occurred must be 0 or 1" in item for item in validation.invalid_rows)


def test_target_event_source_report_contains_decision(tmp_path: Path):
    validation = validate_target_event_source_schema(tmp_path)
    report = render_target_event_source_schema_report(validation)

    assert "Target Event Source Schema Report" in report
    assert "Ready for target generation: False" in report
    assert "not ready for label generation yet" in report


def test_target_event_source_report_uses_portable_relative_path(tmp_path: Path):
    validation = validate_target_event_source_schema(tmp_path)
    report = render_target_event_source_schema_report(validation)

    assert validation.path == "data/processed/targets/historical_flood_events.csv"
    assert str(tmp_path) not in report
    assert "\\" not in validation.path
