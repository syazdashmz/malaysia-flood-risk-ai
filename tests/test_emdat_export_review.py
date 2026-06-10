import json
from pathlib import Path

import pandas as pd

from floodrisk.sources.emdat import (
    build_emdat_export_review,
    render_emdat_export_review_report,
    write_emdat_export_review_outputs,
)


def write_emdat_config(project_root: Path, raw_path: str) -> Path:
    config_path = project_root / "configs/emdat_export_intake_plan.json"
    config_path.parent.mkdir(parents=True, exist_ok=True)
    config_path.write_text(
        json.dumps(
            {
                "raw_export_path": raw_path,
                "interim_review_path": (
                    "data/interim/targets/emdat_historical_flood_events_review.csv"
                ),
                "review_report_path": "reports/emdat_export_review.md",
                "review_summary_path": "reports/emdat_export_review_summary.json",
                "processed_target_path": ("data/processed/targets/historical_flood_events.csv"),
                "direct_training_use_allowed": False,
                "target_label_candidate": True,
            }
        ),
        encoding="utf-8",
    )
    return config_path


def write_sample_emdat_workbook(path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    dataframe = pd.DataFrame(
        [
            {
                "DisNo.": "2021-0001-MYS",
                "Country": "Malaysia",
                "Disaster Type": "Flood",
                "Disaster Subtype": "Flash flood",
                "Location": "Selangor",
                "Admin Units": '[{"adm1_name":"Selangor"}]',
                "GADM Admin Units": "",
                "Latitude": 3.1,
                "Longitude": 101.7,
                "Start Year": 2021,
                "Start Month": 12,
                "Start Day": 18,
                "End Year": 2021,
                "End Month": 12,
                "End Day": 20,
                "Total Affected": 1000,
                "Total Deaths": 2,
            },
            {
                "DisNo.": "2021-0002-MYS",
                "Country": "Malaysia",
                "Disaster Type": "Storm",
                "Disaster Subtype": "Convective storm",
                "Location": "Johor",
                "Start Year": 2021,
                "Start Month": 1,
                "Start Day": 1,
            },
            {
                "DisNo.": "2021-0003-IDN",
                "Country": "Indonesia",
                "Disaster Type": "Flood",
                "Disaster Subtype": "Flood (General)",
                "Location": "Jakarta",
                "Start Year": 2021,
                "Start Month": 2,
                "Start Day": 2,
            },
        ]
    )
    dataframe.to_excel(path, sheet_name="EM-DAT Data", index=False)
    return path


def test_build_emdat_export_review_filters_malaysia_flood_rows(tmp_path: Path):
    raw_path = write_sample_emdat_workbook(tmp_path / "data/raw/emdat/export.xlsx")
    write_emdat_config(tmp_path, raw_path.relative_to(tmp_path).as_posix())

    review = build_emdat_export_review(tmp_path)

    assert review.raw_exists is True
    assert review.source_rows == 3
    assert review.malaysia_flood_rows == 1
    assert review.rows_with_lat_lon == 1
    assert review.rows_with_admin_units == 1
    assert review.records[0].event_start_date == "2021-12-18"
    assert review.records[0].flood_occurred == 1
    assert review.ready_for_training is False


def test_build_emdat_export_review_handles_missing_raw_file(tmp_path: Path):
    write_emdat_config(tmp_path, "data/raw/emdat/missing.xlsx")

    review = build_emdat_export_review(tmp_path)

    assert review.raw_exists is False
    assert review.malaysia_flood_rows == 0
    assert review.review_ready is False
    assert review.ready_for_training is False


def test_render_emdat_export_review_report_contains_guardrail(tmp_path: Path):
    raw_path = write_sample_emdat_workbook(tmp_path / "data/raw/emdat/export.xlsx")
    write_emdat_config(tmp_path, raw_path.relative_to(tmp_path).as_posix())
    review = build_emdat_export_review(tmp_path)

    report = render_emdat_export_review_report(review)

    assert "EM-DAT Export Review" in report
    assert "Ready for training: False" in report
    assert "Do not train the official model" in report


def test_write_emdat_export_review_outputs(tmp_path: Path):
    raw_path = write_sample_emdat_workbook(tmp_path / "data/raw/emdat/export.xlsx")
    write_emdat_config(tmp_path, raw_path.relative_to(tmp_path).as_posix())
    review = build_emdat_export_review(tmp_path)

    interim_path, summary_path, report_path = write_emdat_export_review_outputs(
        review,
        project_root=tmp_path,
    )

    assert interim_path.exists()
    assert summary_path.exists()
    assert report_path.exists()
    assert "2021-0001-MYS" in interim_path.read_text(encoding="utf-8")
    assert "EM-DAT Export Review" in report_path.read_text(encoding="utf-8")

    summary = json.loads(summary_path.read_text(encoding="utf-8"))
    assert summary["malaysia_flood_rows"] == 1
    assert "records" not in summary
