from pathlib import Path

from floodrisk.data.manifest import (
    DataSourceRecord,
    append_manifest_record,
    current_utc_date,
    load_manifest_records,
)


def test_current_utc_date_returns_iso_date():
    date_value = current_utc_date()

    assert len(date_value) == 10
    assert date_value.count("-") == 2


def test_manifest_record_round_trip(tmp_path: Path):
    manifest_path = tmp_path / "manifest.jsonl"

    record = DataSourceRecord(
        dataset_name="Example Dataset",
        source_organization="Example Organization",
        source_url="https://example.com/data",
        access_date="2026-06-10",
        license_or_usage="Example usage notes",
        raw_path="data/raw/example/example.csv",
        processing_script="scripts/example.py",
        known_limitations="Example limitation",
        notes={"country": "Malaysia"},
    )

    append_manifest_record(record, manifest_path)
    records = load_manifest_records(manifest_path)

    assert records == [record]
