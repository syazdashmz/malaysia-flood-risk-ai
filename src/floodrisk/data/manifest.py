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


def record_identity(record: DataSourceRecord) -> tuple[str, str, str]:
    """Return the stable identity for one data source record."""

    return (
        record.dataset_name,
        record.source_url,
        record.raw_path,
    )


def append_manifest_record(record: DataSourceRecord, manifest_path: Path) -> Path:
    """Append one data source record to a JSON Lines manifest."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    with manifest_path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True))
        file.write("\n")

    return manifest_path


def save_manifest_records(records: list[DataSourceRecord], manifest_path: Path) -> Path:
    """Save manifest records to a JSON Lines manifest."""

    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    lines = [json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) for record in records]

    manifest_path.write_text(
        "\n".join(lines) + ("\n" if lines else ""),
        encoding="utf-8",
    )

    return manifest_path


def upsert_manifest_record(record: DataSourceRecord, manifest_path: Path) -> Path:
    """Insert or replace a manifest record using its stable identity."""

    existing_records = load_manifest_records(manifest_path)
    target_identity = record_identity(record)

    updated_records: list[DataSourceRecord] = []
    replaced = False

    for existing_record in existing_records:
        if record_identity(existing_record) == target_identity:
            if not replaced:
                updated_records.append(record)
                replaced = True
            continue

        updated_records.append(existing_record)

    if not replaced:
        updated_records.append(record)

    return save_manifest_records(updated_records, manifest_path)


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
