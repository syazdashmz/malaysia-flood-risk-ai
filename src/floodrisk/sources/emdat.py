"""Controlled EM-DAT export review utilities.

The review output is an interim source-review artifact. It is not the final
`historical_flood_events.csv` target label table.
"""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from datetime import date
from pathlib import Path
from typing import Any

import pandas as pd

EMDAT_CONFIG_PATH = Path("configs/emdat_export_intake_plan.json")
DEFAULT_INTERIM_REVIEW_PATH = Path("data/interim/targets/emdat_historical_flood_events_review.csv")
DEFAULT_REVIEW_REPORT_PATH = Path("reports/emdat_export_review.md")
DEFAULT_REVIEW_SUMMARY_PATH = Path("reports/emdat_export_review_summary.json")


@dataclass(frozen=True)
class EmdatReviewRecord:
    """One normalized EM-DAT row prepared for human review."""

    event_id: str
    country: str
    disaster_type: str
    disaster_subtype: str
    event_start_date: str
    event_end_date: str
    location: str
    admin_units: str
    gadm_admin_units: str
    latitude: str
    longitude: str
    total_affected: str
    total_deaths: str
    flood_occurred: int
    review_status: str
    review_notes: str

    @property
    def has_lat_lon(self) -> bool:
        """Return whether latitude and longitude are present."""

        return bool(self.latitude and self.longitude)

    @property
    def has_admin_units(self) -> bool:
        """Return whether any administrative-unit mapping is present."""

        return bool(self.admin_units or self.gadm_admin_units)

    @property
    def has_usable_start_date(self) -> bool:
        """Return whether event_start_date is populated."""

        return bool(self.event_start_date)

    def as_dict(self) -> dict[str, str | int]:
        """Return record as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class EmdatExportReview:
    """Summary for an EM-DAT export review run."""

    raw_path: str
    raw_exists: bool
    source_rows: int
    malaysia_flood_rows: int
    rows_with_location: int
    rows_with_lat_lon: int
    rows_with_admin_units: int
    rows_with_usable_start_date: int
    interim_review_path: str
    processed_target_path: str
    direct_training_use_allowed: bool
    target_label_candidate: bool
    records: list[EmdatReviewRecord]

    @property
    def review_ready(self) -> bool:
        """Return whether the export produced rows ready for human review."""

        return self.raw_exists and self.malaysia_flood_rows > 0

    @property
    def ready_for_training(self) -> bool:
        """Return whether this review output can be used for training."""

        return False

    def as_dict(self) -> dict[str, Any]:
        """Return review summary as JSON-serializable data."""

        data = asdict(self)
        data["review_ready"] = self.review_ready
        data["ready_for_training"] = self.ready_for_training
        return data

    def summary_dict(self) -> dict[str, Any]:
        """Return compact review metadata without row-level records."""

        data = self.as_dict()
        data.pop("records", None)
        return data


def _clean(value: object) -> str:
    """Return a stable string for source cell values."""

    if value is None:
        return ""

    try:
        if pd.isna(value):
            return ""
    except TypeError:
        pass

    if isinstance(value, float) and value.is_integer():
        return str(int(value))

    return str(value).strip()


def _int_value(value: object) -> int | None:
    """Parse a source value as integer when possible."""

    cleaned = _clean(value)

    if not cleaned:
        return None

    try:
        return int(float(cleaned))
    except ValueError:
        return None


def _iso_date_from_parts(year: object, month: object, day: object) -> str:
    """Build ISO date from EM-DAT year/month/day fields when complete."""

    year_value = _int_value(year)
    month_value = _int_value(month)
    day_value = _int_value(day)

    if year_value is None or month_value is None or day_value is None:
        return ""

    try:
        return date(year_value, month_value, day_value).isoformat()
    except ValueError:
        return ""


def load_emdat_export(raw_path: Path) -> pd.DataFrame:
    """Load an EM-DAT export from CSV or XLSX."""

    if raw_path.suffix.lower() in {".xlsx", ".xls"}:
        return pd.read_excel(raw_path, sheet_name="EM-DAT Data")

    if raw_path.suffix.lower() == ".csv":
        return pd.read_csv(raw_path)

    msg = f"Unsupported EM-DAT export format: {raw_path.suffix}"
    raise ValueError(msg)


def _review_status(row: pd.Series) -> str:
    """Return current review status for one normalized EM-DAT row."""

    has_lat_lon = bool(_clean(row.get("Latitude")) and _clean(row.get("Longitude")))
    has_admin_units = bool(_clean(row.get("Admin Units")) or _clean(row.get("GADM Admin Units")))

    if has_lat_lon:
        return "coordinate_review_required"

    if has_admin_units:
        return "admin_unit_review_required"

    return "location_text_review_required"


def _review_notes(row: pd.Series) -> str:
    """Return review notes for one EM-DAT row."""

    notes = [
        "Review license, location granularity, and date mapping before target use.",
    ]

    if not _clean(row.get("Latitude")) or not _clean(row.get("Longitude")):
        notes.append("Coordinate fields are incomplete.")

    if _clean(row.get("Admin Units")) or _clean(row.get("GADM Admin Units")):
        notes.append("Administrative unit fields may support state/district mapping.")

    return " ".join(notes)


def _normalize_record(row: pd.Series) -> EmdatReviewRecord:
    """Normalize one EM-DAT source row for review."""

    return EmdatReviewRecord(
        event_id=_clean(row.get("DisNo.")),
        country=_clean(row.get("Country")),
        disaster_type=_clean(row.get("Disaster Type")),
        disaster_subtype=_clean(row.get("Disaster Subtype")),
        event_start_date=_iso_date_from_parts(
            row.get("Start Year"),
            row.get("Start Month"),
            row.get("Start Day"),
        ),
        event_end_date=_iso_date_from_parts(
            row.get("End Year"),
            row.get("End Month"),
            row.get("End Day"),
        ),
        location=_clean(row.get("Location")),
        admin_units=_clean(row.get("Admin Units")),
        gadm_admin_units=_clean(row.get("GADM Admin Units")),
        latitude=_clean(row.get("Latitude")),
        longitude=_clean(row.get("Longitude")),
        total_affected=_clean(row.get("Total Affected")),
        total_deaths=_clean(row.get("Total Deaths")),
        flood_occurred=1,
        review_status=_review_status(row),
        review_notes=_review_notes(row),
    )


def _filtered_malaysia_flood_rows(dataframe: pd.DataFrame) -> pd.DataFrame:
    """Return Malaysia flood rows from an EM-DAT export."""

    country = dataframe.get("Country", pd.Series("", index=dataframe.index)).astype(str).str.strip()
    disaster_type = (
        dataframe.get("Disaster Type", pd.Series("", index=dataframe.index)).astype(str).str.strip()
    )

    return dataframe[(country == "Malaysia") & (disaster_type == "Flood")].copy()


def build_emdat_export_review(project_root: Path) -> EmdatExportReview:
    """Build a controlled EM-DAT export review summary."""

    config_path = project_root / EMDAT_CONFIG_PATH
    config = json.loads(config_path.read_text(encoding="utf-8"))

    raw_relative_path = Path(str(config["raw_export_path"]))
    raw_path = project_root / raw_relative_path
    interim_relative_path = Path(
        str(config.get("interim_review_path", DEFAULT_INTERIM_REVIEW_PATH.as_posix()))
    )
    processed_target_path = str(config["processed_target_path"])

    if not raw_path.exists():
        return EmdatExportReview(
            raw_path=raw_relative_path.as_posix(),
            raw_exists=False,
            source_rows=0,
            malaysia_flood_rows=0,
            rows_with_location=0,
            rows_with_lat_lon=0,
            rows_with_admin_units=0,
            rows_with_usable_start_date=0,
            interim_review_path=interim_relative_path.as_posix(),
            processed_target_path=processed_target_path,
            direct_training_use_allowed=bool(config["direct_training_use_allowed"]),
            target_label_candidate=bool(config["target_label_candidate"]),
            records=[],
        )

    dataframe = load_emdat_export(raw_path)
    filtered = _filtered_malaysia_flood_rows(dataframe)
    records = [_normalize_record(row) for _, row in filtered.iterrows()]

    return EmdatExportReview(
        raw_path=raw_relative_path.as_posix(),
        raw_exists=True,
        source_rows=len(dataframe),
        malaysia_flood_rows=len(records),
        rows_with_location=sum(1 for record in records if record.location),
        rows_with_lat_lon=sum(1 for record in records if record.has_lat_lon),
        rows_with_admin_units=sum(1 for record in records if record.has_admin_units),
        rows_with_usable_start_date=sum(1 for record in records if record.has_usable_start_date),
        interim_review_path=interim_relative_path.as_posix(),
        processed_target_path=processed_target_path,
        direct_training_use_allowed=bool(config["direct_training_use_allowed"]),
        target_label_candidate=bool(config["target_label_candidate"]),
        records=records,
    )


def write_emdat_review_csv(review: EmdatExportReview, output_path: Path) -> Path:
    """Write normalized EM-DAT review rows to CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = list(EmdatReviewRecord.__dataclass_fields__)

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(record.as_dict() for record in review.records)

    return output_path


def render_emdat_export_review_report(review: EmdatExportReview) -> str:
    """Render an EM-DAT export review report."""

    lines = [
        "# EM-DAT Export Review",
        "",
        "## Summary",
        "",
        f"- Raw export path: `{review.raw_path}`",
        f"- Raw export exists: {review.raw_exists}",
        f"- Source rows: {review.source_rows}",
        f"- Malaysia flood rows: {review.malaysia_flood_rows}",
        f"- Rows with location text: {review.rows_with_location}",
        f"- Rows with latitude/longitude: {review.rows_with_lat_lon}",
        f"- Rows with admin units: {review.rows_with_admin_units}",
        f"- Rows with usable start date: {review.rows_with_usable_start_date}",
        f"- Review ready: {review.review_ready}",
        f"- Ready for training: {review.ready_for_training}",
        f"- Direct training use allowed: {review.direct_training_use_allowed}",
        f"- Target-label candidate: {review.target_label_candidate}",
        "",
        "## Output",
        "",
        f"- Interim review table: `{review.interim_review_path}`",
        f"- Final processed target table: `{review.processed_target_path}`",
        "",
        "## Review Status Counts",
        "",
    ]

    status_counts: dict[str, int] = {}
    for record in review.records:
        status_counts[record.review_status] = status_counts.get(record.review_status, 0) + 1

    if status_counts:
        for status, count in sorted(status_counts.items()):
            lines.append(f"- {status}: {count}")
    else:
        lines.append("No review rows were produced.")

    lines.extend(
        [
            "",
            "## Guardrail",
            "",
            (
                "This review table is not the final supervised ML target table. "
                "Do not train the official model from EM-DAT rows until license, "
                "location granularity, date mapping, schema mapping, and leakage "
                "checks pass."
            ),
            "",
            "## Next Actions",
            "",
            "1. Review EM-DAT license and attribution requirements.",
            "2. Confirm state/district mapping from admin-unit fields.",
            "3. Decide which rows can map to verified `historical_flood_events.csv` records.",
            "4. Keep real official ML training blocked until target-source validation passes.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_emdat_export_review_outputs(
    review: EmdatExportReview,
    *,
    project_root: Path,
) -> tuple[Path, Path, Path]:
    """Write EM-DAT review CSV, summary JSON, and Markdown report."""

    config = json.loads((project_root / EMDAT_CONFIG_PATH).read_text(encoding="utf-8"))
    interim_path = project_root / Path(
        str(config.get("interim_review_path", DEFAULT_INTERIM_REVIEW_PATH.as_posix()))
    )
    summary_path = project_root / Path(
        str(config.get("review_summary_path", DEFAULT_REVIEW_SUMMARY_PATH.as_posix()))
    )
    report_path = project_root / Path(
        str(config.get("review_report_path", DEFAULT_REVIEW_REPORT_PATH.as_posix()))
    )

    write_emdat_review_csv(review, interim_path)

    summary_path.parent.mkdir(parents=True, exist_ok=True)
    summary_path.write_text(
        json.dumps(review.summary_dict(), indent=2) + "\n",
        encoding="utf-8",
    )

    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        render_emdat_export_review_report(review),
        encoding="utf-8",
    )

    return interim_path, summary_path, report_path
