"""Feature table builder dry-run utilities.

This module intentionally avoids writing a real model-training table.
It only previews which training-table columns can be populated from
currently available sample assets.
"""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

from floodrisk.ml.training_schema import REQUIRED_TRAINING_COLUMNS, TARGET_COLUMN

SAMPLE_TO_TRAINING_COLUMN_MAP = {
    "latitude": "latitude",
    "longitude": "longitude",
    "state": "state",
    "elevation_m": "elevation_m",
    "slope_deg": "slope_deg",
    "river_distance_m": "river_distance_m",
    "historical_flood_distance_m": "historical_flood_distance_m",
    "rainfall_24h_mm": "rainfall_24h_mm",
    "rainfall_72h_mm": "rainfall_72h_mm",
    "water_level_status": "water_level_status",
    "weather_warning_status": "weather_warning_status",
    "land_cover_class": "land_cover_class",
    "population_density_per_km2": "population_density_per_km2",
}


@dataclass(frozen=True)
class FeatureTableBuildPreview:
    """Dry-run preview for future feature table generation."""

    source_path: str
    source_exists: bool
    source_row_count: int
    source_columns: list[str]
    mapped_training_columns: list[str]
    missing_training_columns: list[str]
    target_available: bool
    output_allowed: bool
    output_path: str

    @property
    def can_create_real_training_table(self) -> bool:
        """Return True only when the verified target is available."""

        return self.output_allowed and self.target_available

    def as_dict(self) -> dict[str, Any]:
        """Return dry-run preview as a dictionary."""

        data = asdict(self)
        data["can_create_real_training_table"] = self.can_create_real_training_table
        return data


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read CSV columns and rows."""

    if not path.exists():
        return [], []

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def build_feature_table_preview(
    project_root: Path,
    *,
    output_allowed: bool = False,
) -> FeatureTableBuildPreview:
    """Build a dry-run preview for the future feature table."""

    source_path = project_root / "data" / "samples" / "sample_malaysia_locations.csv"
    output_path = project_root / "data" / "processed" / "model_training" / "training_features.csv"

    source_columns, source_rows = _read_csv(source_path)
    source_column_set = set(source_columns)

    mapped_training_columns = sorted(
        training_column
        for sample_column, training_column in SAMPLE_TO_TRAINING_COLUMN_MAP.items()
        if sample_column in source_column_set
    )

    missing_training_columns = [
        column for column in REQUIRED_TRAINING_COLUMNS if column not in mapped_training_columns
    ]

    target_available = TARGET_COLUMN in mapped_training_columns

    return FeatureTableBuildPreview(
        source_path=str(source_path),
        source_exists=source_path.exists(),
        source_row_count=len(source_rows),
        source_columns=source_columns,
        mapped_training_columns=mapped_training_columns,
        missing_training_columns=missing_training_columns,
        target_available=target_available,
        output_allowed=output_allowed,
        output_path=str(output_path),
    )


def render_feature_table_builder_report(preview: FeatureTableBuildPreview) -> str:
    """Render feature table builder dry-run report."""

    lines = [
        "# Feature Table Builder Dry-Run Report",
        "",
        "## Summary",
        "",
        f"- Source exists: {preview.source_exists}",
        f"- Source rows: {preview.source_row_count}",
        f"- Source columns: {len(preview.source_columns)}",
        f"- Mapped training columns: {len(preview.mapped_training_columns)}",
        f"- Missing training columns: {len(preview.missing_training_columns)}",
        f"- Target available: {preview.target_available}",
        f"- Output allowed: {preview.output_allowed}",
        f"- Can create real training table: {preview.can_create_real_training_table}",
        "",
        "## Source",
        "",
        f"- Source path: `{preview.source_path}`",
        f"- Planned output path: `{preview.output_path}`",
        "",
        "## Mapped Training Columns",
        "",
    ]

    if preview.mapped_training_columns:
        for column in preview.mapped_training_columns:
            lines.append(f"- {column}")
    else:
        lines.append("No training columns can be mapped from the source.")

    lines.extend(
        [
            "",
            "## Missing Training Columns",
            "",
        ]
    )

    if preview.missing_training_columns:
        for column in preview.missing_training_columns:
            lines.append(f"- {column}")
    else:
        lines.append("No required training columns are missing.")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            (
                "This dry run must not create `training_features.csv` until the "
                "verified `flood_occurred` target label is available."
            ),
            "",
            "Current decision:",
            "",
            "    Do not create the real training table yet.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_feature_table_builder_report(
    preview: FeatureTableBuildPreview,
    output_path: Path,
) -> Path:
    """Write feature table builder dry-run report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_feature_table_builder_report(preview),
        encoding="utf-8",
    )
    return output_path
