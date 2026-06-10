"""Schema validation for a future verified historical flood target source."""

from __future__ import annotations

import csv
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

TARGET_EVENT_SOURCE_PATH = Path("data/processed/targets/historical_flood_events.csv")

REQUIRED_TARGET_EVENT_COLUMNS = [
    "event_id",
    "source_name",
    "source_url",
    "license_name",
    "event_start_date",
    "event_end_date",
    "latitude",
    "longitude",
    "state",
    "district",
    "flood_occurred",
    "verification_status",
    "notes",
]

ALLOWED_VERIFICATION_STATUSES = {"verified", "reviewed"}
ALLOWED_BINARY_VALUES = {"0", "1"}


@dataclass(frozen=True)
class TargetEventSourceValidation:
    """Validation result for future historical flood event target source."""

    path: str
    exists: bool
    row_count: int
    columns: list[str]
    missing_columns: list[str]
    extra_columns: list[str]
    invalid_rows: list[str]

    @property
    def has_rows(self) -> bool:
        """Return whether the source has at least one row."""

        return self.row_count > 0

    @property
    def is_schema_valid(self) -> bool:
        """Return whether required columns are present and rows are valid."""

        return self.exists and not self.missing_columns and not self.invalid_rows

    @property
    def is_ready_for_target_generation(self) -> bool:
        """Return whether this source can generate flood_occurred labels."""

        return self.is_schema_valid and self.has_rows

    def as_dict(self) -> dict[str, Any]:
        """Return validation result as a dictionary."""

        data = asdict(self)
        data["has_rows"] = self.has_rows
        data["is_schema_valid"] = self.is_schema_valid
        data["is_ready_for_target_generation"] = self.is_ready_for_target_generation
        return data


def _parse_date(value: str) -> bool:
    """Return True if value is blank or ISO date."""

    if not value:
        return True

    try:
        date.fromisoformat(value)
    except ValueError:
        return False

    return True


def _parse_float(value: str) -> float | None:
    """Parse a float, returning None on failure."""

    try:
        return float(value)
    except ValueError:
        return None


def _is_malaysia_coordinate(latitude: float, longitude: float) -> bool:
    """Return whether coordinate is inside a broad Malaysia bounding box."""

    return -1.5 <= latitude <= 7.5 and 99.0 <= longitude <= 120.0


def _validate_row(row: dict[str, str], row_number: int) -> list[str]:
    """Validate one target source row."""

    issues: list[str] = []

    event_id = row.get("event_id", "").strip()
    if not event_id:
        issues.append(f"row {row_number}: event_id is required")

    if row.get("flood_occurred", "").strip() not in ALLOWED_BINARY_VALUES:
        issues.append(f"row {row_number}: flood_occurred must be 0 or 1")

    status = row.get("verification_status", "").strip().lower()
    if status not in ALLOWED_VERIFICATION_STATUSES:
        issues.append(f"row {row_number}: verification_status must be verified or reviewed")

    if not _parse_date(row.get("event_start_date", "").strip()):
        issues.append(f"row {row_number}: event_start_date must be ISO date")

    if not _parse_date(row.get("event_end_date", "").strip()):
        issues.append(f"row {row_number}: event_end_date must be ISO date or blank")

    latitude = _parse_float(row.get("latitude", "").strip())
    longitude = _parse_float(row.get("longitude", "").strip())

    if latitude is None:
        issues.append(f"row {row_number}: latitude must be numeric")

    if longitude is None:
        issues.append(f"row {row_number}: longitude must be numeric")

    if (
        latitude is not None
        and longitude is not None
        and not _is_malaysia_coordinate(latitude, longitude)
    ):
        issues.append(f"row {row_number}: coordinate must be within Malaysia bounds")

    return issues


def validate_target_event_source_schema(
    project_root: Path,
    relative_path: Path = TARGET_EVENT_SOURCE_PATH,
) -> TargetEventSourceValidation:
    """Validate future historical flood event target source."""

    path = project_root / relative_path

    if not path.exists():
        return TargetEventSourceValidation(
            path=str(path),
            exists=False,
            row_count=0,
            columns=[],
            missing_columns=REQUIRED_TARGET_EVENT_COLUMNS.copy(),
            extra_columns=[],
            invalid_rows=[],
        )

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        columns = list(reader.fieldnames or [])
        rows = list(reader)

    missing_columns = [column for column in REQUIRED_TARGET_EVENT_COLUMNS if column not in columns]
    extra_columns = [column for column in columns if column not in REQUIRED_TARGET_EVENT_COLUMNS]

    invalid_rows: list[str] = []

    if not missing_columns:
        for index, row in enumerate(rows, start=2):
            invalid_rows.extend(_validate_row(row, index))

    return TargetEventSourceValidation(
        path=str(path),
        exists=True,
        row_count=len(rows),
        columns=columns,
        missing_columns=missing_columns,
        extra_columns=extra_columns,
        invalid_rows=invalid_rows,
    )


def render_target_event_source_schema_report(
    validation: TargetEventSourceValidation,
) -> str:
    """Render target event source schema report."""

    lines = [
        "# Target Event Source Schema Report",
        "",
        "## Summary",
        "",
        f"- Path: `{validation.path}`",
        f"- Exists: {validation.exists}",
        f"- Rows: {validation.row_count}",
        f"- Columns: {len(validation.columns)}",
        f"- Missing columns: {len(validation.missing_columns)}",
        f"- Extra columns: {len(validation.extra_columns)}",
        f"- Invalid row issues: {len(validation.invalid_rows)}",
        f"- Schema valid: {validation.is_schema_valid}",
        f"- Ready for target generation: {validation.is_ready_for_target_generation}",
        "",
        "## Required Columns",
        "",
    ]

    for column in REQUIRED_TARGET_EVENT_COLUMNS:
        lines.append(f"- {column}")

    lines.extend(["", "## Missing Columns", ""])

    if validation.missing_columns:
        for column in validation.missing_columns:
            lines.append(f"- {column}")
    else:
        lines.append("No required columns are missing.")

    lines.extend(["", "## Invalid Row Issues", ""])

    if validation.invalid_rows:
        for issue in validation.invalid_rows:
            lines.append(f"- {issue}")
    else:
        lines.append("No row-level issues found.")

    lines.extend(
        [
            "",
            "## Decision",
            "",
        ]
    )

    if validation.is_ready_for_target_generation:
        lines.append("The target event source can be used for label generation.")
    else:
        lines.append("The target event source is not ready for label generation yet.")

    return "\n".join(lines).rstrip() + "\n"


def write_target_event_source_schema_report(
    validation: TargetEventSourceValidation,
    output_path: Path,
) -> Path:
    """Write target event source schema report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_target_event_source_schema_report(validation),
        encoding="utf-8",
    )
    return output_path
