"""Geospatial validation report utilities."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from floodrisk.geospatial.artifacts import (
    GeospatialArtifactCheck,
    check_geospatial_artifacts,
)
from floodrisk.geospatial.vector import (
    VectorDatasetValidation,
    validate_vector_dataset,
)


@dataclass(frozen=True)
class GeospatialValidationSummary:
    """Summary of geospatial artifact and vector validation checks."""

    artifact_checks: list[GeospatialArtifactCheck]
    vector_validations: list[VectorDatasetValidation]

    @property
    def planned_artifact_count(self) -> int:
        """Return total planned geospatial artifacts."""

        return len(self.artifact_checks)

    @property
    def available_artifact_count(self) -> int:
        """Return number of available geospatial artifacts."""

        return sum(1 for check in self.artifact_checks if check.exists)

    @property
    def missing_artifact_count(self) -> int:
        """Return number of missing planned geospatial artifacts."""

        return sum(1 for check in self.artifact_checks if not check.exists)

    @property
    def valid_vector_count(self) -> int:
        """Return number of valid vector artifacts."""

        return sum(1 for validation in self.vector_validations if validation.is_valid)

    @property
    def has_available_boundary_data(self) -> bool:
        """Return True if at least one planned boundary artifact is available."""

        return self.available_artifact_count > 0

    def as_dict(self) -> dict[str, int | bool | list[dict]]:
        """Return summary as a dictionary."""

        return {
            "planned_artifact_count": self.planned_artifact_count,
            "available_artifact_count": self.available_artifact_count,
            "missing_artifact_count": self.missing_artifact_count,
            "valid_vector_count": self.valid_vector_count,
            "has_available_boundary_data": self.has_available_boundary_data,
            "artifact_checks": [check.as_dict() for check in self.artifact_checks],
            "vector_validations": [validation.as_dict() for validation in self.vector_validations],
        }


def build_geospatial_validation_summary(
    project_root: Path,
) -> GeospatialValidationSummary:
    """Build geospatial validation summary for planned artifacts."""

    artifact_checks = check_geospatial_artifacts(project_root)
    vector_validations = [
        validate_vector_dataset(project_root / check.artifact.relative_path)
        for check in artifact_checks
        if check.exists
    ]

    return GeospatialValidationSummary(
        artifact_checks=artifact_checks,
        vector_validations=vector_validations,
    )


def render_geospatial_validation_report(
    summary: GeospatialValidationSummary,
) -> str:
    """Render geospatial validation summary as Markdown."""

    lines = [
        "# Geospatial Validation Report",
        "",
        "## Summary",
        "",
        f"- Planned artifacts: {summary.planned_artifact_count}",
        f"- Available artifacts: {summary.available_artifact_count}",
        f"- Missing artifacts: {summary.missing_artifact_count}",
        f"- Valid vector datasets: {summary.valid_vector_count}",
        (f"- Has available boundary data: {summary.has_available_boundary_data}"),
        "",
        "## Artifact Checks",
        "",
        "| Dataset ID | Path | Status |",
        "|---|---|---|",
    ]

    for check in summary.artifact_checks:
        lines.append(
            f"| {check.artifact.dataset_id} | {check.artifact.relative_path} | {check.status} |"
        )

    lines.extend(
        [
            "",
            "## Vector Dataset Validations",
            "",
        ]
    )

    if not summary.vector_validations:
        lines.append(
            "No vector datasets were validated because no planned artifacts are available yet."
        )
    else:
        lines.extend(
            [
                "| Path | Rows | CRS | Invalid Geometry | Empty Geometry | Valid |",
                "|---|---:|---|---:|---:|---|",
            ]
        )

        for validation in summary.vector_validations:
            lines.append(
                "| "
                f"{validation.path} | "
                f"{validation.row_count} | "
                f"{validation.crs} | "
                f"{validation.invalid_geometry_count} | "
                f"{validation.empty_geometry_count} | "
                f"{validation.is_valid} |"
            )

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "A missing planned artifact is expected until an authoritative "
                "boundary dataset has been selected, verified, and added locally."
            ),
            "",
            (
                "A valid vector dataset requires existing data, non-empty rows, "
                "CRS metadata, geometry, and no invalid or empty geometries."
            ),
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_geospatial_validation_report(
    summary: GeospatialValidationSummary,
    output_path: Path,
) -> Path:
    """Write geospatial validation report to Markdown."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_geospatial_validation_report(summary),
        encoding="utf-8",
    )
    return output_path
