"""Geospatial data source registry."""

from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass(frozen=True)
class GeospatialDataSource:
    """Metadata for a planned or available geospatial dataset."""

    dataset_id: str
    name: str
    source_type: str
    expected_format: str
    status: str
    description: str
    license_note: str

    def as_dict(self) -> dict[str, str]:
        """Return source metadata as a dictionary."""

        return asdict(self)


GEOSPATIAL_DATA_SOURCES = [
    GeospatialDataSource(
        dataset_id="malaysia_admin_boundary",
        name="Malaysia Administrative Boundary",
        source_type="administrative_boundary",
        expected_format="GeoJSON or Shapefile",
        status="planned",
        description=(
            "Administrative boundary polygons for Malaysia, intended for "
            "point-in-boundary validation and location-aware joins."
        ),
        license_note="License and redistribution rules must be verified before use.",
    ),
    GeospatialDataSource(
        dataset_id="malaysia_state_boundary",
        name="Malaysia State Boundary",
        source_type="administrative_boundary",
        expected_format="GeoJSON or Shapefile",
        status="planned",
        description=(
            "State-level boundary polygons for state-aware flood risk grouping "
            "and dashboard filtering."
        ),
        license_note="License and redistribution rules must be verified before use.",
    ),
    GeospatialDataSource(
        dataset_id="malaysia_district_boundary",
        name="Malaysia District Boundary",
        source_type="administrative_boundary",
        expected_format="GeoJSON or Shapefile",
        status="planned",
        description=(
            "District-level boundary polygons for more precise local risk "
            "aggregation and weather/geospatial joins."
        ),
        license_note="License and redistribution rules must be verified before use.",
    ),
]


def list_geospatial_data_sources() -> list[GeospatialDataSource]:
    """Return all registered geospatial data sources."""

    return GEOSPATIAL_DATA_SOURCES.copy()


def get_geospatial_data_source(dataset_id: str) -> GeospatialDataSource:
    """Return one geospatial data source by dataset id."""

    for source in GEOSPATIAL_DATA_SOURCES:
        if source.dataset_id == dataset_id:
            return source

    msg = f"Unknown geospatial dataset id: {dataset_id}"
    raise KeyError(msg)


def list_geospatial_data_source_dicts() -> list[dict[str, str]]:
    """Return all geospatial data sources as dictionaries."""

    return [source.as_dict() for source in GEOSPATIAL_DATA_SOURCES]
