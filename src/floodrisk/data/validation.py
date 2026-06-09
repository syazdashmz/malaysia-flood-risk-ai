"""Geospatial validation helpers for Malaysia Flood Risk AI."""

from __future__ import annotations


MALAYSIA_MIN_LAT = -1.5
MALAYSIA_MAX_LAT = 7.5
MALAYSIA_MIN_LON = 99.0
MALAYSIA_MAX_LON = 120.0


def is_coordinate_in_malaysia_bbox(latitude: float, longitude: float) -> bool:
    """Return True if coordinate is within a broad Malaysia bounding box."""

    return (
        MALAYSIA_MIN_LAT <= latitude <= MALAYSIA_MAX_LAT
        and MALAYSIA_MIN_LON <= longitude <= MALAYSIA_MAX_LON
    )


def malaysia_coordinate_error(latitude: float, longitude: float) -> str:
    """Return a readable validation error for coordinates outside Malaysia."""

    return (
        "Coordinate appears to be outside Malaysia. "
        f"Received latitude={latitude}, longitude={longitude}. "
        "Expected latitude roughly between -1.5 and 7.5, "
        "and longitude roughly between 99 and 120."
    )
