import json
from pathlib import Path

from floodrisk.geospatial.validation_report import (
    build_geospatial_validation_summary,
    render_geospatial_validation_report,
    write_geospatial_validation_report,
)


def write_geojson(path: Path) -> Path:
    payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "sample"},
                "geometry": {
                    "type": "Point",
                    "coordinates": [101.6869, 3.139],
                },
            }
        ],
    }
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_build_geospatial_validation_summary_reports_missing_artifacts(tmp_path: Path):
    summary = build_geospatial_validation_summary(tmp_path)

    assert summary.planned_artifact_count == 3
    assert summary.available_artifact_count == 0
    assert summary.missing_artifact_count == 3
    assert summary.valid_vector_count == 0
    assert summary.has_available_boundary_data is False


def test_build_geospatial_validation_summary_validates_existing_artifact(
    tmp_path: Path,
):
    write_geojson(tmp_path / "data/external/geospatial/malaysia_admin_boundary.geojson")

    summary = build_geospatial_validation_summary(tmp_path)

    assert summary.available_artifact_count == 1
    assert summary.missing_artifact_count == 2
    assert summary.valid_vector_count == 1
    assert summary.has_available_boundary_data is True


def test_render_geospatial_validation_report_handles_missing_artifacts(
    tmp_path: Path,
):
    summary = build_geospatial_validation_summary(tmp_path)
    report = render_geospatial_validation_report(summary)

    assert "Geospatial Validation Report" in report
    assert "planned_missing" in report
    assert "No vector datasets were validated" in report


def test_write_geospatial_validation_report(tmp_path: Path):
    summary = build_geospatial_validation_summary(tmp_path)
    output_path = tmp_path / "geospatial_validation_report.md"

    saved_path = write_geospatial_validation_report(summary, output_path)

    assert saved_path.exists()
    assert "Geospatial Validation Report" in saved_path.read_text(encoding="utf-8")


def test_geospatial_validation_summary_as_dict(tmp_path: Path):
    summary = build_geospatial_validation_summary(tmp_path)
    data = summary.as_dict()

    assert data["planned_artifact_count"] == 3
    assert data["available_artifact_count"] == 0
    assert isinstance(data["artifact_checks"], list)
