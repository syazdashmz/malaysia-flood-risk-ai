"""Malaysia-specific geospatial constants and helpers."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class GeographicBoundingBox:
    """Simple latitude/longitude bounding box."""

    min_lat: float
    max_lat: float
    min_lon: float
    max_lon: float
    label: str

    def contains(self, latitude: float, longitude: float) -> bool:
        """Return True if the coordinate is inside the bounding box."""

        return (
            self.min_lat <= latitude <= self.max_lat and self.min_lon <= longitude <= self.max_lon
        )

    def as_dict(self) -> dict[str, float | str]:
        """Return the bounding box as a dictionary."""

        return asdict(self)

    def description(self) -> str:
        """Return a readable bounding box description."""

        return (
            f"{self.label} bounding box: latitude roughly between "
            f"{self.min_lat} and {self.max_lat}, longitude roughly between "
            f"{self.min_lon} and {self.max_lon}"
        )


MALAYSIA_BOUNDING_BOX = GeographicBoundingBox(
    min_lat=-1.5,
    max_lat=7.5,
    min_lon=99.0,
    max_lon=120.0,
    label="Malaysia",
)


def is_within_malaysia_bbox(latitude: float, longitude: float) -> bool:
    """Return True if coordinate is within the broad Malaysia bounding box."""

    return MALAYSIA_BOUNDING_BOX.contains(latitude, longitude)


def malaysia_bbox_description() -> str:
    """Return a readable Malaysia bounding box description."""

    return MALAYSIA_BOUNDING_BOX.description()
