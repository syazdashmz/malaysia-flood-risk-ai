"""Initial EDA report utilities."""

from __future__ import annotations

import csv
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from statistics import mean
from typing import Any

from floodrisk.notebooks.catalog import build_notebook_data_catalog
from floodrisk.notebooks.readiness import build_dataset_readiness_summary


@dataclass(frozen=True)
class CsvNumericProfile:
    """Numeric profile for one CSV column."""

    column: str
    count: int
    minimum: float
    maximum: float
    mean_value: float

    def as_dict(self) -> dict[str, str | int | float]:
        """Return profile as a dictionary."""

        return asdict(self)


@dataclass(frozen=True)
class InitialEdaSummary:
    """Initial EDA summary for current project assets."""

    sample_locations_exists: bool
    sample_locations_row_count: int
    sample_locations_columns: list[str]
    sample_numeric_profiles: list[CsvNumericProfile]
    weather_summary_exists: bool
    weather_summary_keys: list[str]
    weather_signal_counts: dict[str, Any]
    catalog_ready_for_eda: bool
    dataset_ready_for_training: bool

    def as_dict(self) -> dict[str, Any]:
        """Return summary as a dictionary."""

        return {
            "sample_locations_exists": self.sample_locations_exists,
            "sample_locations_row_count": self.sample_locations_row_count,
            "sample_locations_columns": self.sample_locations_columns,
            "sample_numeric_profiles": [
                profile.as_dict() for profile in self.sample_numeric_profiles
            ],
            "weather_summary_exists": self.weather_summary_exists,
            "weather_summary_keys": self.weather_summary_keys,
            "weather_signal_counts": self.weather_signal_counts,
            "catalog_ready_for_eda": self.catalog_ready_for_eda,
            "dataset_ready_for_training": self.dataset_ready_for_training,
        }


def _read_csv_rows(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    """Read CSV columns and rows."""

    if not path.exists():
        return [], []

    with path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        return list(reader.fieldnames or []), list(reader)


def _try_float(value: str | None) -> float | None:
    """Parse a float value when possible."""

    if value is None or value.strip() == "":
        return None

    try:
        return float(value)
    except ValueError:
        return None


def _numeric_profiles(
    rows: list[dict[str, str]],
    columns: list[str],
) -> list[CsvNumericProfile]:
    """Build numeric profiles for parseable CSV columns."""

    profiles: list[CsvNumericProfile] = []

    for column in columns:
        values = [parsed for row in rows if (parsed := _try_float(row.get(column))) is not None]

        if not values:
            continue

        profiles.append(
            CsvNumericProfile(
                column=column,
                count=len(values),
                minimum=min(values),
                maximum=max(values),
                mean_value=mean(values),
            )
        )

    return profiles


def _read_json(path: Path) -> dict[str, Any]:
    """Read JSON object when available."""

    if not path.exists():
        return {}

    data = json.loads(path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return data

    return {}


def build_initial_eda_summary(project_root: Path) -> InitialEdaSummary:
    """Build initial EDA summary from currently available assets."""

    sample_locations_path = project_root / "data" / "samples" / "sample_malaysia_locations.csv"
    weather_summary_path = project_root / "reports" / "weather_risk_signal_summary.json"

    sample_columns, sample_rows = _read_csv_rows(sample_locations_path)
    weather_summary = _read_json(weather_summary_path)

    catalog_summary = build_notebook_data_catalog(project_root)
    dataset_summary = build_dataset_readiness_summary(project_root)

    signal_counts = weather_summary.get("signal_counts", {})

    return InitialEdaSummary(
        sample_locations_exists=sample_locations_path.exists(),
        sample_locations_row_count=len(sample_rows),
        sample_locations_columns=sample_columns,
        sample_numeric_profiles=_numeric_profiles(sample_rows, sample_columns),
        weather_summary_exists=weather_summary_path.exists(),
        weather_summary_keys=sorted(weather_summary.keys()),
        weather_signal_counts=signal_counts if isinstance(signal_counts, dict) else {},
        catalog_ready_for_eda=catalog_summary.ready_for_eda,
        dataset_ready_for_training=dataset_summary.ready_for_training,
    )


def render_initial_eda_report(summary: InitialEdaSummary) -> str:
    """Render initial EDA summary as Markdown."""

    lines = [
        "# Initial EDA Report",
        "",
        "## Summary",
        "",
        f"- Sample locations available: {summary.sample_locations_exists}",
        f"- Sample location rows: {summary.sample_locations_row_count}",
        f"- Weather summary available: {summary.weather_summary_exists}",
        f"- Ready for initial EDA: {summary.catalog_ready_for_eda}",
        f"- Ready for real ML training: {summary.dataset_ready_for_training}",
        "",
        "## Sample Location Columns",
        "",
    ]

    if summary.sample_locations_columns:
        for column in summary.sample_locations_columns:
            lines.append(f"- {column}")
    else:
        lines.append("No sample location columns were found.")

    lines.extend(
        [
            "",
            "## Numeric Profiles",
            "",
            "| Column | Count | Min | Max | Mean |",
            "|---|---:|---:|---:|---:|",
        ]
    )

    if summary.sample_numeric_profiles:
        for profile in summary.sample_numeric_profiles:
            lines.append(
                "| "
                f"{profile.column} | "
                f"{profile.count} | "
                f"{profile.minimum:.4f} | "
                f"{profile.maximum:.4f} | "
                f"{profile.mean_value:.4f} |"
            )
    else:
        lines.append("| - | 0 | - | - | - |")

    lines.extend(
        [
            "",
            "## Weather Summary Keys",
            "",
        ]
    )

    if summary.weather_summary_keys:
        for key in summary.weather_summary_keys:
            lines.append(f"- {key}")
    else:
        lines.append("No weather summary keys were found.")

    lines.extend(
        [
            "",
            "## Weather Signal Counts",
            "",
        ]
    )

    if summary.weather_signal_counts:
        for key, value in summary.weather_signal_counts.items():
            lines.append(f"- {key}: {value}")
    else:
        lines.append("No weather signal counts were found.")

    lines.extend(
        [
            "",
            "## Interpretation",
            "",
            (
                "The current assets are suitable for initial notebook-based EDA. "
                "They are not sufficient for real ML training yet because the "
                "model-ready training table is still missing."
            ),
            "",
            "## Next EDA Direction",
            "",
            "1. Inspect sample location distribution.",
            "2. Review weather signal counts.",
            "3. Compare readiness reports.",
            "4. Define the first model-ready feature table generation plan.",
            "5. Keep real training blocked until validated target labels exist.",
        ]
    )

    return "\n".join(lines).rstrip() + "\n"


def write_initial_eda_report(
    summary: InitialEdaSummary,
    output_path: Path,
) -> Path:
    """Write initial EDA report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(render_initial_eda_report(summary), encoding="utf-8")
    return output_path
