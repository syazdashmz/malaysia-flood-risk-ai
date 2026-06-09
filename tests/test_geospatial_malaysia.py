from floodrisk.geospatial.malaysia import (
    MALAYSIA_BOUNDING_BOX,
    GeographicBoundingBox,
    is_within_malaysia_bbox,
    malaysia_bbox_description,
)


def test_geographic_bounding_box_contains_coordinate():
    bbox = GeographicBoundingBox(
        min_lat=0,
        max_lat=5,
        min_lon=100,
        max_lon=105,
        label="Test",
    )

    assert bbox.contains(3, 102)
    assert not bbox.contains(6, 102)


def test_malaysia_bounding_box_contains_kuala_lumpur():
    assert MALAYSIA_BOUNDING_BOX.contains(3.139, 101.6869)


def test_malaysia_bounding_box_rejects_far_outside_coordinate():
    assert not is_within_malaysia_bbox(49.3198, 6.3722)


def test_malaysia_bounding_box_exports_expected_values():
    data = MALAYSIA_BOUNDING_BOX.as_dict()

    assert data["min_lat"] == -1.5
    assert data["max_lat"] == 7.5
    assert data["min_lon"] == 99.0
    assert data["max_lon"] == 120.0
    assert data["label"] == "Malaysia"


def test_malaysia_bbox_description_is_readable():
    description = malaysia_bbox_description()

    assert "Malaysia bounding box" in description
    assert "latitude" in description
    assert "longitude" in description
