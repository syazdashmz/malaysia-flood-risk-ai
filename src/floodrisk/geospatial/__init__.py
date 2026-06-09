"""Geospatial foundation utilities for Malaysia Flood Risk AI."""

from floodrisk.geospatial.malaysia import (
    MALAYSIA_BOUNDING_BOX,
    GeographicBoundingBox,
    is_within_malaysia_bbox,
    malaysia_bbox_description,
)

__all__ = [
    "GeographicBoundingBox",
    "MALAYSIA_BOUNDING_BOX",
    "is_within_malaysia_bbox",
    "malaysia_bbox_description",
]
