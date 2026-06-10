from pathlib import Path

from floodrisk.ml.feature_table_builder import (
    build_feature_table_preview,
    render_feature_table_builder_report,
    write_feature_table_builder_report,
)
from floodrisk.ml.training_schema import TARGET_COLUMN


def write_sample_locations(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(
        "\n".join(
            [
                "location_name,state,latitude,longitude,elevation_m,weather_warning_status",
                "A,Selangor,3.1,101.7,20,warning",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return path


def test_feature_table_preview_reads_sample_source(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")

    preview = build_feature_table_preview(tmp_path)

    assert preview.source_exists is True
    assert preview.source_row_count == 1
    assert "latitude" in preview.mapped_training_columns


def test_feature_table_preview_blocks_real_output_without_target(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")

    preview = build_feature_table_preview(tmp_path, output_allowed=True)

    assert preview.target_available is False
    assert TARGET_COLUMN in preview.missing_training_columns
    assert preview.can_create_real_training_table is False


def test_feature_table_preview_does_not_create_training_table(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")

    preview = build_feature_table_preview(tmp_path)

    assert Path(preview.output_path).exists() is False


def test_render_feature_table_builder_report_contains_guardrail(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")
    preview = build_feature_table_preview(tmp_path)

    report = render_feature_table_builder_report(preview)

    assert "Feature Table Builder Dry-Run Report" in report
    assert "Can create real training table: False" in report
    assert "Do not create the real training table yet" in report


def test_write_feature_table_builder_report(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")
    preview = build_feature_table_preview(tmp_path)
    output_path = tmp_path / "feature_table_builder_dry_run.md"

    saved_path = write_feature_table_builder_report(preview, output_path)

    assert saved_path.exists()
    assert "Feature Table Builder Dry-Run Report" in saved_path.read_text(encoding="utf-8")
