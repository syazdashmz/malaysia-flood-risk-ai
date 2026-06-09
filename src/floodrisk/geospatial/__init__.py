"""Geospatial foundation utilities for Malaysia Flood Risk AI."""

from floodrisk.geospatial.malaysia import (
    MALAYSIA_BOUNDING_BOX,
    GeographicBoundingBox,
    is_within_malaysia_bbox,
    malaysia_bbox_description,
)
from floodrisk.geospatial.vector import (
    VectorDatasetValidation,
    validate_vector_dataset,
)

__all__ = [
    "GeographicBoundingBox",
    "MALAYSIA_BOUNDING_BOX",
    "VectorDatasetValidation",
    "is_within_malaysia_bbox",
    "malaysia_bbox_description",
    "validate_vector_dataset",
]
