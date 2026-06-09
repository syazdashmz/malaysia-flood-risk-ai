import json
from pathlib import Path

from floodrisk.geospatial.vector import validate_vector_dataset


def write_geojson(path: Path, geometry: dict) -> Path:
    payload = {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {"name": "sample"},
                "geometry": geometry,
            }
        ],
    }
    path.write_text(json.dumps(payload), encoding="utf-8")
    return path


def test_validate_vector_dataset_reports_missing_file(tmp_path: Path):
    validation = validate_vector_dataset(tmp_path / "missing.geojson")

    assert validation.exists is False
    assert validation.is_valid is False
    assert validation.error_message == "File does not exist."


def test_validate_vector_dataset_accepts_valid_geojson(tmp_path: Path):
    path = write_geojson(
        tmp_path / "valid.geojson",
        {
            "type": "Point",
            "coordinates": [101.6869, 3.139],
        },
    )

    validation = validate_vector_dataset(path)

    assert validation.exists is True
    assert validation.row_count == 1
    assert validation.has_geometry is True
    assert validation.has_crs is True
    assert validation.invalid_geometry_count == 0
    assert validation.empty_geometry_count == 0
    assert validation.is_valid is True


def test_validate_vector_dataset_detects_invalid_geometry(tmp_path: Path):
    path = write_geojson(
        tmp_path / "invalid.geojson",
        {
            "type": "Polygon",
            "coordinates": [
                [
                    [0, 0],
                    [1, 1],
                    [1, 0],
                    [0, 1],
                    [0, 0],
                ]
            ],
        },
    )

    validation = validate_vector_dataset(path)

    assert validation.exists is True
    assert validation.row_count == 1
    assert validation.invalid_geometry_count == 1
    assert validation.is_valid is False


def test_vector_dataset_validation_as_dict(tmp_path: Path):
    validation = validate_vector_dataset(tmp_path / "missing.geojson")
    data = validation.as_dict()

    assert data["exists"] is False
    assert data["is_valid"] is False
    assert data["path"].endswith("missing.geojson")
