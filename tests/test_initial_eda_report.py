from pathlib import Path

from floodrisk.notebooks.eda import (
    build_initial_eda_summary,
    render_initial_eda_report,
    write_initial_eda_report,
)


def write_text(path: Path, content: str) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def prepare_required_assets(tmp_path: Path) -> None:
    write_text(
        tmp_path / "data/samples/sample_malaysia_locations.csv",
        "name,latitude,longitude,risk_score\nA,3.1,101.7,40\nB,5.2,100.4,70\n",
    )
    write_text(
        tmp_path / "reports/weather_risk_signal_summary.json",
        '{"signal_counts":{"none":1,"warning":2},"record_count":3}',
    )
    write_text(tmp_path / "reports/geospatial_validation_report.md", "# Geo\n")
    write_text(tmp_path / "reports/dataset_readiness_report.md", "# Dataset\n")
    write_text(tmp_path / "reports/training_table_schema_report.md", "# Schema\n")
    write_text(tmp_path / "reports/notebook_environment_report.md", "# Env\n")


def test_build_initial_eda_summary_profiles_available_assets(tmp_path: Path):
    prepare_required_assets(tmp_path)

    summary = build_initial_eda_summary(tmp_path)

    assert summary.sample_locations_exists is True
    assert summary.sample_locations_row_count == 2
    assert "latitude" in summary.sample_locations_columns
    assert summary.weather_summary_exists is True
    assert summary.weather_signal_counts["warning"] == 2


def test_build_initial_eda_summary_reports_training_not_ready(tmp_path: Path):
    prepare_required_assets(tmp_path)

    summary = build_initial_eda_summary(tmp_path)

    assert summary.catalog_ready_for_eda is True
    assert summary.dataset_ready_for_training is False


def test_render_initial_eda_report(tmp_path: Path):
    prepare_required_assets(tmp_path)
    summary = build_initial_eda_summary(tmp_path)

    report = render_initial_eda_report(summary)

    assert "Initial EDA Report" in report
    assert "Ready for initial EDA: True" in report
    assert "Ready for real ML training: False" in report


def test_write_initial_eda_report(tmp_path: Path):
    prepare_required_assets(tmp_path)
    summary = build_initial_eda_summary(tmp_path)
    output_path = tmp_path / "initial_eda_report.md"

    saved_path = write_initial_eda_report(summary, output_path)

    assert saved_path.exists()
    assert "Initial EDA Report" in saved_path.read_text(encoding="utf-8")
