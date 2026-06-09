"""Geospatial validation helpers for Malaysia Flood Risk AI."""

from __future__ import annotations

from floodrisk.geospatial.malaysia import (
    MALAYSIA_BOUNDING_BOX,
    is_within_malaysia_bbox,
    malaysia_bbox_description,
)

MALAYSIA_MIN_LAT = MALAYSIA_BOUNDING_BOX.min_lat
MALAYSIA_MAX_LAT = MALAYSIA_BOUNDING_BOX.max_lat
MALAYSIA_MIN_LON = MALAYSIA_BOUNDING_BOX.min_lon
MALAYSIA_MAX_LON = MALAYSIA_BOUNDING_BOX.max_lon


def is_coordinate_in_malaysia_bbox(latitude: float, longitude: float) -> bool:
    """Return True if coordinate is within a broad Malaysia bounding box."""

    return is_within_malaysia_bbox(latitude, longitude)


def malaysia_coordinate_error(latitude: float, longitude: float) -> str:
    """Return a readable validation error for coordinates outside Malaysia."""

    return (
        "Coordinate appears to be outside Malaysia. "
        f"Received latitude={latitude}, longitude={longitude}. "
        f"Expected {malaysia_bbox_description()}."
    )
