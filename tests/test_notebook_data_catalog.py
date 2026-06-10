from pathlib import Path

from floodrisk.ml.training_schema import REQUIRED_TRAINING_COLUMNS
from floodrisk.notebooks.catalog import (
    build_notebook_data_catalog,
    list_notebook_data_assets,
    render_notebook_data_catalog_report,
    write_notebook_data_catalog_report,
)


def write_text(path: Path, content: str = "x") -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def write_training_csv(path: Path, columns: tuple[str, ...]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    header = ",".join(columns)
    row = ",".join("1" for _ in columns)
    path.write_text(f"{header}\n{row}\n", encoding="utf-8")
    return path


def test_list_notebook_data_assets_contains_required_eda_assets():
    assets = list_notebook_data_assets()
    required_assets = [asset for asset in assets if asset.required_for_eda]

    assert len(assets) >= 9
    assert len(required_assets) >= 6


def test_build_notebook_data_catalog_reports_missing_assets(tmp_path: Path):
    summary = build_notebook_data_catalog(tmp_path)

    assert summary.asset_count >= 9
    assert summary.available_count == 0
    assert summary.ready_for_eda is False


def test_build_notebook_data_catalog_reports_ready_for_initial_eda(tmp_path: Path):
    required_paths = [
        "data/samples/sample_malaysia_locations.csv",
        "reports/weather_risk_signal_summary.json",
        "reports/geospatial_validation_report.md",
        "reports/dataset_readiness_report.md",
        "reports/training_table_schema_report.md",
        "reports/notebook_environment_report.md",
    ]

    for relative_path in required_paths:
        if relative_path.endswith(".csv"):
            write_text(tmp_path / relative_path, "id,value\n1,2\n")
        else:
            write_text(tmp_path / relative_path)

    summary = build_notebook_data_catalog(tmp_path)

    assert summary.blocking_eda_count == 0
    assert summary.ready_for_eda is True


def test_build_notebook_data_catalog_treats_invalid_training_table_as_not_explorable(
    tmp_path: Path,
):
    write_text(
        tmp_path / "data/processed/model_training/training_features.csv",
        "target\n0\n",
    )

    summary = build_notebook_data_catalog(tmp_path)
    training_entry = next(
        entry for entry in summary.entries if entry.asset.asset_id == "model_training_table"
    )

    assert training_entry.exists is True
    assert training_entry.explorable is False
    assert training_entry.status == "available_not_explorable"


def test_build_notebook_data_catalog_accepts_schema_valid_training_table(
    tmp_path: Path,
):
    write_training_csv(
        tmp_path / "data/processed/model_training/training_features.csv",
        REQUIRED_TRAINING_COLUMNS,
    )

    summary = build_notebook_data_catalog(tmp_path)
    training_entry = next(
        entry for entry in summary.entries if entry.asset.asset_id == "model_training_table"
    )

    assert training_entry.exists is True
    assert training_entry.explorable is True


def test_render_notebook_data_catalog_report(tmp_path: Path):
    summary = build_notebook_data_catalog(tmp_path)
    report = render_notebook_data_catalog_report(summary)

    assert "Notebook Data Catalog Report" in report
    assert "Ready for initial EDA" in report
    assert "Model-ready training table" in report


def test_write_notebook_data_catalog_report(tmp_path: Path):
    summary = build_notebook_data_catalog(tmp_path)
    output_path = tmp_path / "notebook_data_catalog_report.md"

    saved_path = write_notebook_data_catalog_report(summary, output_path)

    assert saved_path.exists()
    assert "Notebook Data Catalog Report" in saved_path.read_text(encoding="utf-8")
