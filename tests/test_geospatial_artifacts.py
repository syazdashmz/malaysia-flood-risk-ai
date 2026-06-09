from pathlib import Path

from floodrisk.geospatial.artifacts import (
    check_geospatial_artifacts,
    list_geospatial_artifacts,
    render_geospatial_artifact_report,
    write_geospatial_artifact_report,
)


def test_list_geospatial_artifacts_returns_planned_artifacts():
    artifacts = list_geospatial_artifacts()

    assert len(artifacts) == 3
    assert artifacts[0].dataset_id == "malaysia_admin_boundary"


def test_check_geospatial_artifacts_marks_missing_files(tmp_path: Path):
    checks = check_geospatial_artifacts(tmp_path)

    assert checks
    assert checks[0].exists is False
    assert checks[0].status == "planned_missing"


def test_check_geospatial_artifacts_detects_existing_file(tmp_path: Path):
    artifact = list_geospatial_artifacts()[0]
    artifact_path = tmp_path / artifact.relative_path
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text("{}", encoding="utf-8")

    checks = check_geospatial_artifacts(tmp_path)

    assert checks[0].exists is True
    assert checks[0].status == "available"


def test_render_geospatial_artifact_report_contains_expected_paths(tmp_path: Path):
    checks = check_geospatial_artifacts(tmp_path)

    report = render_geospatial_artifact_report(checks)

    assert "Geospatial Artifact Plan" in report
    assert "malaysia_admin_boundary.geojson" in report
    assert "planned_missing" in report


def test_write_geospatial_artifact_report(tmp_path: Path):
    checks = check_geospatial_artifacts(tmp_path)
    output_path = tmp_path / "report.md"

    saved_path = write_geospatial_artifact_report(checks, output_path)

    assert saved_path.exists()
    assert "Geospatial Artifact Plan" in saved_path.read_text(encoding="utf-8")
