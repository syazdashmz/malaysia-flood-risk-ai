from pathlib import Path

from floodrisk.ml.training_readiness import (
    build_ml_training_readiness_summary,
    render_ml_training_readiness_report,
    write_ml_training_readiness_report,
)


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


def test_ml_training_readiness_blocks_without_target_and_training_table(
    tmp_path: Path,
):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")

    summary = build_ml_training_readiness_summary(tmp_path)

    assert summary.target_ready is False
    assert summary.training_table_ready is False
    assert summary.real_ml_training_ready is False
    assert summary.blockers


def test_ml_training_readiness_reports_feature_preview_details(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")

    summary = build_ml_training_readiness_summary(tmp_path)

    assert summary.feature_source_exists is True
    assert summary.feature_source_rows == 1
    assert summary.mapped_feature_columns >= 1
    assert "flood_occurred" in summary.missing_feature_columns


def test_render_ml_training_readiness_report(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")
    summary = build_ml_training_readiness_summary(tmp_path)

    report = render_ml_training_readiness_report(summary)

    assert "ML Training Readiness Gate" in report
    assert "Real ML training ready: False" in report
    assert "Real supervised ML training must remain blocked" in report


def test_write_ml_training_readiness_report(tmp_path: Path):
    write_sample_locations(tmp_path / "data/samples/sample_malaysia_locations.csv")
    summary = build_ml_training_readiness_summary(tmp_path)
    output_path = tmp_path / "ml_training_readiness_report.md"

    saved_path = write_ml_training_readiness_report(summary, output_path)

    assert saved_path.exists()
    assert "ML Training Readiness Gate" in saved_path.read_text(encoding="utf-8")
