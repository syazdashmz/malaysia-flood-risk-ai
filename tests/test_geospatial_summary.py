from pathlib import Path

from floodrisk.geospatial.summary import load_geospatial_summary


def test_load_geospatial_summary_reports_missing_artifacts(tmp_path: Path):
    summary = load_geospatial_summary(tmp_path)

    assert summary["available"] is True
    assert summary["planned_artifact_count"] == 3
    assert summary["available_artifact_count"] == 0
    assert summary["missing_artifact_count"] == 3
    assert summary["valid_vector_count"] == 0
    assert summary["has_available_boundary_data"] is False


def test_load_geospatial_summary_includes_artifact_statuses(tmp_path: Path):
    summary = load_geospatial_summary(tmp_path)

    statuses = summary["artifact_statuses"]

    assert len(statuses) == 3
    assert statuses[0]["dataset_id"] == "malaysia_admin_boundary"
    assert statuses[0]["status"] == "planned_missing"
    assert statuses[0]["required_for_mvp"] is False


def test_load_geospatial_summary_detects_available_artifact(tmp_path: Path):
    artifact_path = (
        tmp_path / "data" / "external" / "geospatial" / "malaysia_admin_boundary.geojson"
    )
    artifact_path.parent.mkdir(parents=True, exist_ok=True)
    artifact_path.write_text(
        """
        {
          "type": "FeatureCollection",
          "features": [
            {
              "type": "Feature",
              "properties": {"name": "sample"},
              "geometry": {
                "type": "Point",
                "coordinates": [101.6869, 3.139]
              }
            }
          ]
        }
        """,
        encoding="utf-8",
    )

    summary = load_geospatial_summary(tmp_path)

    assert summary["available_artifact_count"] == 1
    assert summary["missing_artifact_count"] == 2
    assert summary["valid_vector_count"] == 1
    assert summary["has_available_boundary_data"] is True
