"""Training table schema contract and validation utilities."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class TrainingTableColumn:
    """Expected model-training table column."""

    name: str
    dtype: str
    role: str
    required: bool
    description: str

    def as_dict(self) -> dict[str, str | bool]:
        """Return column metadata as a dictionary."""

        return asdict(self)


TRAINING_TABLE_COLUMNS = (
    TrainingTableColumn(
        name="observation_id",
        dtype="string",
        role="identifier",
        required=True,
        description="Unique row identifier.",
    ),
    TrainingTableColumn(
        name="latitude",
        dtype="float",
        role="feature",
        required=True,
        description="Observation latitude.",
    ),
    TrainingTableColumn(
        name="longitude",
        dtype="float",
        role="feature",
        required=True,
        description="Observation longitude.",
    ),
    TrainingTableColumn(
        name="observation_date",
        dtype="date",
        role="time",
        required=True,
        description="Observation date.",
    ),
    TrainingTableColumn(
        name="state",
        dtype="string",
        role="feature",
        required=True,
        description="Administrative state.",
    ),
    TrainingTableColumn(
        name="district",
        dtype="string",
        role="feature",
        required=True,
        description="Administrative district.",
    ),
    TrainingTableColumn(
        name="elevation_m",
        dtype="float",
        role="feature",
        required=True,
        description="Terrain elevation in meters.",
    ),
    TrainingTableColumn(
        name="slope_deg",
        dtype="float",
        role="feature",
        required=True,
        description="Terrain slope in degrees.",
    ),
    TrainingTableColumn(
        name="river_distance_m",
        dtype="float",
        role="feature",
        required=True,
        description="Distance to nearest river in meters.",
    ),
    TrainingTableColumn(
        name="historical_flood_distance_m",
        dtype="float",
        role="feature",
        required=True,
        description="Distance to nearest known historical flood area in meters.",
    ),
    TrainingTableColumn(
        name="rainfall_24h_mm",
        dtype="float",
        role="feature",
        required=True,
        description="Rainfall over previous 24 hours.",
    ),
    TrainingTableColumn(
        name="rainfall_72h_mm",
        dtype="float",
        role="feature",
        required=True,
        description="Rainfall over previous 72 hours.",
    ),
    TrainingTableColumn(
        name="water_level_status",
        dtype="string",
        role="feature",
        required=True,
        description="Hydrology warning/status category.",
    ),
    TrainingTableColumn(
        name="weather_warning_status",
        dtype="string",
        role="feature",
        required=True,
        description="Weather warning category.",
    ),
    TrainingTableColumn(
        name="land_cover_class",
        dtype="string",
        role="feature",
        required=True,
        description="Land cover category.",
    ),
    TrainingTableColumn(
        name="population_density_per_km2",
        dtype="float",
        role="feature",
        required=True,
        description="Population density per square kilometer.",
    ),
    TrainingTableColumn(
        name="flood_occurred",
        dtype="integer",
        role="target",
        required=True,
        description="Preferred binary target label.",
    ),
)

TARGET_COLUMN = "flood_occurred"
REQUIRED_TRAINING_COLUMNS = tuple(
    column.name for column in TRAINING_TABLE_COLUMNS if column.required
)
KNOWN_TRAINING_COLUMNS = tuple(column.name for column in TRAINING_TABLE_COLUMNS)


@dataclass(frozen=True)
class TrainingTableSchemaValidation:
    """Training table schema validation result."""

    path: str
    exists: bool
    valid_csv: bool
    row_count: int
    columns: list[str]
    missing_required_columns: list[str]
    extra_columns: list[str]
    target_column_present: bool
    error_message: str | None = None

    @property
    def has_rows(self) -> bool:
        """Return True if the table has at least one data row."""

        return self.row_count > 0

    @property
    def is_schema_valid(self) -> bool:
        """Return True if required schema is present."""

        return (
            self.exists
            and self.valid_csv
            and not self.missing_required_columns
            and self.target_column_present
            and self.error_message is None
        )

    @property
    def is_training_ready(self) -> bool:
        """Return True if the table is structurally ready for baseline training."""

        return self.is_schema_valid and self.has_rows

    def as_dict(self) -> dict[str, str | int | bool | list[str] | None]:
        """Return validation result as a dictionary."""

        data = asdict(self)
        data["has_rows"] = self.has_rows
        data["is_schema_valid"] = self.is_schema_valid
        data["is_training_ready"] = self.is_training_ready
        return data


def validate_training_table_schema(path: Path) -> TrainingTableSchemaValidation:
    """Validate expected model-training CSV table schema."""

    if not path.exists():
        return TrainingTableSchemaValidation(
            path=str(path),
            exists=False,
            valid_csv=False,
            row_count=0,
            columns=[],
            missing_required_columns=list(REQUIRED_TRAINING_COLUMNS),
            extra_columns=[],
            target_column_present=False,
            error_message="Training table does not exist.",
        )

    try:
        with path.open("r", encoding="utf-8", newline="") as file:
            reader = csv.DictReader(file)
            columns = list(reader.fieldnames or [])
            row_count = sum(1 for _ in reader)
    except csv.Error as exc:
        return TrainingTableSchemaValidation(
            path=str(path),
            exists=True,
            valid_csv=False,
            row_count=0,
            columns=[],
            missing_required_columns=list(REQUIRED_TRAINING_COLUMNS),
            extra_columns=[],
            target_column_present=False,
            error_message=str(exc),
        )

    missing_required_columns = [
        column for column in REQUIRED_TRAINING_COLUMNS if column not in columns
    ]
    extra_columns = [column for column in columns if column not in KNOWN_TRAINING_COLUMNS]

    return TrainingTableSchemaValidation(
        path=str(path),
        exists=True,
        valid_csv=True,
        row_count=row_count,
        columns=columns,
        missing_required_columns=missing_required_columns,
        extra_columns=extra_columns,
        target_column_present=TARGET_COLUMN in columns,
    )


def render_training_table_schema_report(
    validation: TrainingTableSchemaValidation,
) -> str:
    """Render training table schema validation as Markdown."""

    lines = [
        "# Training Table Schema Report",
        "",
        "## Summary",
        "",
        f"- Exists: {validation.exists}",
        f"- Valid CSV: {validation.valid_csv}",
        f"- Row count: {validation.row_count}",
        f"- Required columns: {len(REQUIRED_TRAINING_COLUMNS)}",
        f"- Missing required columns: {len(validation.missing_required_columns)}",
        f"- Target column present: {validation.target_column_present}",
        f"- Schema valid: {validation.is_schema_valid}",
        f"- Training ready: {validation.is_training_ready}",
        "",
        "## Expected Columns",
        "",
        "| Column | Type | Role | Required | Description |",
        "|---|---|---|---:|---|",
    ]

    for column in TRAINING_TABLE_COLUMNS:
        lines.append(
            "| "
            f"{column.name} | "
            f"{column.dtype} | "
            f"{column.role} | "
            f"{column.required} | "
            f"{column.description} |"
        )

    lines.extend(
        [
            "",
            "## Observed Columns",
            "",
        ]
    )

    if validation.columns:
        for column in validation.columns:
            lines.append(f"- {column}")
    else:
        lines.append("No columns were found.")

    lines.extend(
        [
            "",
            "## Missing Required Columns",
            "",
        ]
    )

    if validation.missing_required_columns:
        for column in validation.missing_required_columns:
            lines.append(f"- {column}")
    else:
        lines.append("No required columns are missing.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
        ]
    )

    if validation.is_training_ready:
        lines.append("The training table is structurally ready for baseline ML training.")
    else:
        lines.append(
            "The training table is not ready for baseline ML training yet. "
            "This is expected until a real model-ready feature table is created."
        )

    return "\n".join(lines).rstrip() + "\n"


def write_training_table_schema_report(
    validation: TrainingTableSchemaValidation,
    output_path: Path,
) -> Path:
    """Write training table schema validation report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_training_table_schema_report(validation),
        encoding="utf-8",
    )
    return output_path
