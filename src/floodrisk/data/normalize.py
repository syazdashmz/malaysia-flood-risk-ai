"""Generic JSON normalization helpers for data acquisition pipelines."""

from __future__ import annotations

import csv
import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any


def extract_records(data: Any) -> list[Any]:
    """Extract records from common JSON API response shapes."""

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        for key in ("data", "results", "records", "items"):
            value = data.get(key)
            if isinstance(value, list):
                return value

        return [data]

    return [{"value": data}]


def flatten_mapping(
    mapping: Mapping[str, Any],
    *,
    parent_key: str = "",
    separator: str = ".",
) -> dict[str, Any]:
    """Flatten nested dictionaries into a single-level dictionary."""

    flattened: dict[str, Any] = {}

    for key, value in mapping.items():
        new_key = f"{parent_key}{separator}{key}" if parent_key else str(key)

        if isinstance(value, Mapping):
            flattened.update(
                flatten_mapping(
                    value,
                    parent_key=new_key,
                    separator=separator,
                )
            )
        elif isinstance(value, list):
            flattened[new_key] = json.dumps(value, ensure_ascii=False)
        else:
            flattened[new_key] = value

    return flattened


def normalize_record(record: Any) -> dict[str, Any]:
    """Normalize one JSON record into a flat dictionary."""

    if isinstance(record, Mapping):
        return flatten_mapping(record)

    return {"value": record}


def load_json_records(input_path: Path) -> list[Any]:
    """Load records from a JSON file."""

    data = json.loads(input_path.read_text(encoding="utf-8"))
    return extract_records(data)


def write_records_csv(records: list[Any], output_path: Path) -> Path:
    """Write normalized JSON records to CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    normalized_records = [normalize_record(record) for record in records]
    fieldnames = sorted(
        {field for record in normalized_records for field in record},
    )

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(normalized_records)

    return output_path
