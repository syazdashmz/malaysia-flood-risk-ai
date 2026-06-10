"""Utilities for parsing MyWater/DID exported spreadsheet tables."""

from __future__ import annotations

import json
import re
from collections.abc import Iterable
from dataclasses import asdict, dataclass
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_MYWATER_RAW_DIR = PROJECT_ROOT / "data" / "raw" / "mywater"
DEFAULT_MYWATER_PROCESSED_DIR = PROJECT_ROOT / "data" / "processed" / "mywater"


MYWATER_SOURCE_PATTERNS = {
    "flood_location_cause": "Summary List of Location and Cause of Flood",
    "flood_monitoring_station_status": "Summary Status List of Flood Monitoring Station",
    "operation_modes_by_year": "Total Operation Modes By Year",
    "zone_by_status": "Total Zone By Status",
}


@dataclass(frozen=True)
class MyWaterTableProfile:
    """Metadata profile for one parsed MyWater/DID table."""

    source_file: str
    source_kind: str
    sheet_name: str
    row_count: int
    column_count: int
    columns: list[str]


class SimpleHTMLTableParser(HTMLParser):
    """Small no-dependency parser for simple HTML table exports."""

    def __init__(self) -> None:
        super().__init__()
        self.tables: list[list[list[str]]] = []
        self._current_table: list[list[str]] | None = None
        self._current_row: list[str] | None = None
        self._current_cell: list[str] | None = None

    def handle_starttag(
        self,
        tag: str,
        attrs: list[tuple[str, str | None]],
    ) -> None:
        del attrs

        normalized_tag = tag.lower()

        if normalized_tag == "table":
            self._current_table = []
        elif normalized_tag == "tr" and self._current_table is not None:
            self._current_row = []
        elif normalized_tag in {"td", "th"} and self._current_row is not None:
            self._current_cell = []

    def handle_data(self, data: str) -> None:
        if self._current_cell is not None:
            self._current_cell.append(data)

    def handle_endtag(self, tag: str) -> None:
        normalized_tag = tag.lower()

        if normalized_tag in {"td", "th"} and self._current_cell is not None:
            cell_text = " ".join("".join(self._current_cell).split())
            if self._current_row is not None:
                self._current_row.append(cell_text)
            self._current_cell = None

        elif normalized_tag == "tr" and self._current_row is not None:
            if any(cell for cell in self._current_row) and self._current_table is not None:
                self._current_table.append(self._current_row)
            self._current_row = None

        elif normalized_tag == "table" and self._current_table is not None:
            if self._current_table:
                self.tables.append(self._current_table)
            self._current_table = None


def normalize_mywater_column_name(value: Any) -> str:
    """Normalize exported table column names into stable snake_case."""
    text = str(value or "").strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text)
    text = re.sub(r"_+", "_", text).strip("_")
    return text or "unnamed_column"


def classify_mywater_file(path: Path) -> str:
    """Classify a MyWater/DID export by filename."""
    filename = path.name.lower()

    for source_kind, pattern in MYWATER_SOURCE_PATTERNS.items():
        if pattern.lower() in filename:
            return source_kind

    return "unknown_mywater_export"


def clean_mywater_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Clean one parsed spreadsheet table."""
    cleaned = df.copy()
    cleaned = cleaned.dropna(how="all")
    cleaned = cleaned.dropna(axis=1, how="all")

    cleaned.columns = [normalize_mywater_column_name(column) for column in cleaned.columns]

    return cleaned.reset_index(drop=True)


def dataframe_from_html_rows(rows: list[list[str]]) -> pd.DataFrame:
    """Convert simple parsed HTML table rows into a dataframe."""
    if not rows:
        return pd.DataFrame()

    header = rows[0]
    body = rows[1:]

    if not body:
        return pd.DataFrame(columns=header)

    width = len(header)
    normalized_body = []

    for row in body:
        padded_row = row[:width] + [""] * max(width - len(row), 0)
        normalized_body.append(padded_row)

    return pd.DataFrame(normalized_body, columns=header)


def read_html_tables_without_optional_dependencies(path: Path) -> list[pd.DataFrame]:
    """Read simple HTML tables without requiring lxml/html5lib."""
    parser = SimpleHTMLTableParser()
    parser.feed(path.read_text(encoding="utf-8", errors="ignore"))

    return [dataframe_from_html_rows(table_rows) for table_rows in parser.tables]


def read_mywater_export_tables(path: Path) -> dict[str, pd.DataFrame]:
    """Read tables from an XLS/XLSX/HTML-style MyWater export."""
    try:
        sheets = pd.read_excel(path, sheet_name=None)
        return {
            str(sheet_name): cleaned_table
            for sheet_name, sheet_df in sheets.items()
            if not (cleaned_table := clean_mywater_dataframe(sheet_df)).empty
        }
    except Exception:
        html_tables = read_html_tables_without_optional_dependencies(path)
        return {
            f"html_table_{index + 1}": cleaned_table
            for index, table in enumerate(html_tables)
            if not (cleaned_table := clean_mywater_dataframe(table)).empty
        }


def discover_mywater_files(raw_dir: Path = DEFAULT_MYWATER_RAW_DIR) -> list[Path]:
    """Discover MyWater/DID spreadsheet exports."""
    if not raw_dir.exists():
        return []

    candidates: list[Path] = []

    for suffix in ("*.xls", "*.xlsx", "*.html", "*.htm"):
        candidates.extend(raw_dir.glob(suffix))

    return sorted(candidates)


def profile_mywater_file(path: Path) -> list[MyWaterTableProfile]:
    """Build table profiles for one MyWater/DID export."""
    source_kind = classify_mywater_file(path)
    tables = read_mywater_export_tables(path)

    profiles = []

    for sheet_name, table in tables.items():
        profiles.append(
            MyWaterTableProfile(
                source_file=path.name,
                source_kind=source_kind,
                sheet_name=sheet_name,
                row_count=int(len(table)),
                column_count=int(len(table.columns)),
                columns=[str(column) for column in table.columns],
            )
        )

    return profiles


def profile_mywater_sources(
    files: Iterable[Path],
) -> list[MyWaterTableProfile]:
    """Build table profiles for many MyWater/DID exports."""
    profiles: list[MyWaterTableProfile] = []

    for path in files:
        profiles.extend(profile_mywater_file(path))

    return profiles


def save_mywater_profiles(
    profiles: list[MyWaterTableProfile],
    output_path: Path,
) -> Path:
    """Save parsed MyWater/DID table profiles."""
    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(
            [asdict(profile) for profile in profiles],
            ensure_ascii=False,
            indent=2,
        ),
        encoding="utf-8",
    )

    return output_path


def summarize_mywater_profiles(
    profiles: list[MyWaterTableProfile],
) -> dict[str, Any]:
    """Summarize parsed MyWater/DID table profiles."""
    source_files = sorted({profile.source_file for profile in profiles})
    source_kinds = sorted({profile.source_kind for profile in profiles})

    return {
        "source_id": "mywater_did_exports",
        "source_file_count": len(source_files),
        "table_count": len(profiles),
        "source_files": source_files,
        "source_kinds": source_kinds,
        "total_rows": sum(profile.row_count for profile in profiles),
    }
