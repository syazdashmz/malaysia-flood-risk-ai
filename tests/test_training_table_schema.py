from pathlib import Path

from floodrisk.ml.training_schema import (
    REQUIRED_TRAINING_COLUMNS,
    TARGET_COLUMN,
    TRAINING_TABLE_COLUMNS,
    render_training_table_schema_report,
    validate_training_table_schema,
    write_training_table_schema_report,
)


def write_training_csv(path: Path, columns: tuple[str, ...]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ",".join(columns)
    row = ",".join("1" for _ in columns)
    path.write_text(f"{header}\n{row}\n", encoding="utf-8")
    return path


def test_training_schema_includes_target_column():
    column_names = [column.name for column in TRAINING_TABLE_COLUMNS]

    assert TARGET_COLUMN == "flood_occurred"
    assert TARGET_COLUMN in column_names
    assert TARGET_COLUMN in REQUIRED_TRAINING_COLUMNS


def test_validate_training_table_schema_reports_missing_file(tmp_path: Path):
    validation = validate_training_table_schema(tmp_path / "missing.csv")

    assert validation.exists is False
    assert validation.is_schema_valid is False
    assert validation.is_training_ready is False
    assert TARGET_COLUMN in validation.missing_required_columns


def test_validate_training_table_schema_accepts_valid_table(tmp_path: Path):
    path = write_training_csv(tmp_path / "training_features.csv", REQUIRED_TRAINING_COLUMNS)

    validation = validate_training_table_schema(path)

    assert validation.exists is True
    assert validation.is_schema_valid is True
    assert validation.has_rows is True
    assert validation.is_training_ready is True


def test_validate_training_table_schema_detects_missing_target(tmp_path: Path):
    columns = tuple(column for column in REQUIRED_TRAINING_COLUMNS if column != TARGET_COLUMN)
    path = write_training_csv(tmp_path / "training_features.csv", columns)

    validation = validate_training_table_schema(path)

    assert validation.target_column_present is False
    assert TARGET_COLUMN in validation.missing_required_columns
    assert validation.is_training_ready is False


def test_render_training_table_schema_report(tmp_path: Path):
    validation = validate_training_table_schema(tmp_path / "missing.csv")
    report = render_training_table_schema_report(validation)

    assert "Training Table Schema Report" in report
    assert "Training ready: False" in report
    assert TARGET_COLUMN in report


def test_write_training_table_schema_report(tmp_path: Path):
    validation = validate_training_table_schema(tmp_path / "missing.csv")
    output_path = tmp_path / "training_table_schema_report.md"

    saved_path = write_training_table_schema_report(validation, output_path)

    assert saved_path.exists()
    assert "Training Table Schema Report" in saved_path.read_text(encoding="utf-8")
