"""Utilities for recording raw data acquisition metadata."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class DataSourceRecord:
    """Metadata record for one acquired dataset."""

    dataset_name: str
    source_organization: str
    source_url: str
    access_date: str
    license_or_usage: str
    raw_path: str
    processing_script: str
    known_limitations: str
    notes: dict[str, Any] = field(default_factory=dict)


def current_utc_date() -> str:
    """Return the current UTC date in ISO format."""

    return datetime.now(UTC).date().isoformat()


def append_manifest_record(record: DataSourceRecord, manifest_path: Path) -> Path:
    """Append one data source record to a JSON Lines manifest."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True))
        file.write("\n")

    return manifest_path


def load_manifest_records(manifest_path: Path) -> list[DataSourceRecord]:
    """Load data source records from a JSON Lines manifest."""

    if not manifest_path.exists():
        return []

    records: list[DataSourceRecord] = []

    with manifest_path.open("r", encoding="utf-8") as file:
        for line in file:
            stripped_line = line.strip()
            if not stripped_line:
                continue

            data = json.loads(stripped_line)
            records.append(DataSourceRecord(**data))

    return records
