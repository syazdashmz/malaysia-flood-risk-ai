"""Vector dataset validation utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class VectorDatasetValidation:
    """Validation summary for one vector geospatial dataset."""

    path: str
    exists: bool
    row_count: int
    crs: str | None
    has_crs: bool
    has_geometry: bool
    invalid_geometry_count: int
    empty_geometry_count: int
    error_message: str | None = None

    @property
    def is_valid(self) -> bool:
        """Return True if the vector dataset passes basic validation."""

        return (
            self.exists
            and self.error_message is None
            and self.row_count > 0
            and self.has_crs
            and self.has_geometry
            and self.invalid_geometry_count == 0
            and self.empty_geometry_count == 0
        )

    def as_dict(self) -> dict[str, str | int | bool | None]:
        """Return validation result as a dictionary."""

        return {
            "path": self.path,
            "exists": self.exists,
            "row_count": self.row_count,
            "crs": self.crs,
            "has_crs": self.has_crs,
            "has_geometry": self.has_geometry,
            "invalid_geometry_count": self.invalid_geometry_count,
            "empty_geometry_count": self.empty_geometry_count,
            "error_message": self.error_message,
            "is_valid": self.is_valid,
        }


def validate_vector_dataset(input_path: Path) -> VectorDatasetValidation:
    """Validate a vector geospatial dataset with GeoPandas."""

    if not input_path.exists():
        return VectorDatasetValidation(
            path=str(input_path),
            exists=False,
            row_count=0,
            crs=None,
            has_crs=False,
            has_geometry=False,
            invalid_geometry_count=0,
            empty_geometry_count=0,
            error_message="File does not exist.",
        )

    try:
        import geopandas as gpd

        geodataframe = gpd.read_file(input_path)

        has_geometry = (
            geodataframe.geometry is not None and geodataframe.geometry.name in geodataframe.columns
        )
        crs = geodataframe.crs.to_string() if geodataframe.crs is not None else None

        if not has_geometry:
            return VectorDatasetValidation(
                path=str(input_path),
                exists=True,
                row_count=len(geodataframe),
                crs=crs,
                has_crs=crs is not None,
                has_geometry=False,
                invalid_geometry_count=0,
                empty_geometry_count=0,
                error_message="Dataset has no geometry column.",
            )

        geometry = geodataframe.geometry
        invalid_geometry_count = int((~geometry.is_valid.fillna(False)).sum())
        empty_geometry_count = int(geometry.is_empty.fillna(False).sum())

        return VectorDatasetValidation(
            path=str(input_path),
            exists=True,
            row_count=len(geodataframe),
            crs=crs,
            has_crs=crs is not None,
            has_geometry=has_geometry,
            invalid_geometry_count=invalid_geometry_count,
            empty_geometry_count=empty_geometry_count,
        )
    except Exception as exc:
        return VectorDatasetValidation(
            path=str(input_path),
            exists=True,
            row_count=0,
            crs=None,
            has_crs=False,
            has_geometry=False,
            invalid_geometry_count=0,
            empty_geometry_count=0,
            error_message=str(exc),
        )
