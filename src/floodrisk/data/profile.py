"""Lightweight CSV profiling utilities for data quality checks."""

from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class CsvProfile:
    """Basic profile for one CSV file."""

    file_name: str
    row_count: int
    column_count: int
    columns: list[str]
    missing_counts: dict[str, int]


def profile_csv(input_path: Path) -> CsvProfile:
    """Profile a CSV file."""

    with input_path.open("r", encoding="utf-8", newline="") as file:
        reader = csv.DictReader(file)
        rows = list(reader)

    columns = reader.fieldnames or []
    missing_counts = {column: 0 for column in columns}

    for row in rows:
        for column in columns:
            value = row.get(column)
            if value is None or value == "":
                missing_counts[column] += 1

    return CsvProfile(
        file_name=input_path.name,
        row_count=len(rows),
        column_count=len(columns),
        columns=columns,
        missing_counts=missing_counts,
    )


def render_profiles_markdown(
    profiles: list[CsvProfile],
    *,
    title: str = "Data Quality Profile",
) -> str:
    """Render CSV profiles as a Markdown report."""

    lines = [
        f"# {title}",
        "",
        "This report is generated from local interim CSV files.",
        "",
    ]

    for profile in profiles:
        lines.extend(
            [
                f"## {profile.file_name}",
                "",
                f"- Rows: {profile.row_count}",
                f"- Columns: {profile.column_count}",
                "",
                "### Columns",
                "",
            ]
        )

        for column in profile.columns:
            missing = profile.missing_counts[column]
            lines.append(f"- {column} — missing values: {missing}")

        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def write_profiles_markdown(
    profiles: list[CsvProfile],
    output_path: Path,
    *,
    title: str = "Data Quality Profile",
) -> Path:
    """Write CSV profiles to a Markdown report."""

    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        render_profiles_markdown(profiles, title=title),
        encoding="utf-8",
    )
    return output_path
