"""Load geospatial validation summary for apps and APIs."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from floodrisk.geospatial.validation_report import (
    build_geospatial_validation_summary,
)

DEFAULT_PROJECT_ROOT = Path(__file__).resolve().parents[3]


def load_geospatial_summary(
    project_root: Path = DEFAULT_PROJECT_ROOT,
) -> dict[str, Any]:
    """Load current geospatial readiness summary."""

    summary = build_geospatial_validation_summary(project_root)

    return {
        "available": True,
        "planned_artifact_count": summary.planned_artifact_count,
        "available_artifact_count": summary.available_artifact_count,
        "missing_artifact_count": summary.missing_artifact_count,
        "valid_vector_count": summary.valid_vector_count,
        "has_available_boundary_data": summary.has_available_boundary_data,
        "artifact_statuses": [
            {
                "dataset_id": check.artifact.dataset_id,
                "relative_path": check.artifact.relative_path,
                "status": check.status,
                "required_for_mvp": check.artifact.required_for_mvp,
            }
            for check in summary.artifact_checks
        ],
    }
