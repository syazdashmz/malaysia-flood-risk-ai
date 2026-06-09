from pathlib import Path

from floodrisk.data.manifest import (
    DataSourceRecord,
    append_manifest_record,
    current_utc_date,
    load_manifest_records,
    upsert_manifest_record,
)


def build_record(
    *,
    known_limitations: str = "Example limitation",
) -> DataSourceRecord:
    return DataSourceRecord(
        dataset_name="Example Dataset",
        source_organization="Example Organization",
        source_url="https://example.com/data",
        access_date="2026-06-10",
        license_or_usage="Example usage notes",
        raw_path="data/raw/example/example.csv",
        processing_script="scripts/example.py",
        known_limitations=known_limitations,
        notes={"country": "Malaysia"},
    )


def test_current_utc_date_returns_iso_date():
    date_value = current_utc_date()

    assert len(date_value) == 10
    assert date_value.count("-") == 2


def test_manifest_record_round_trip(tmp_path: Path):
    manifest_path = tmp_path / "manifest.jsonl"

    record = build_record()

    append_manifest_record(record, manifest_path)
    records = load_manifest_records(manifest_path)

    assert records == [record]


def test_upsert_manifest_record_replaces_existing_record(tmp_path: Path):
    manifest_path = tmp_path / "manifest.jsonl"

    first_record = build_record(known_limitations="Old limitation")
    second_record = build_record(known_limitations="New limitation")

    upsert_manifest_record(first_record, manifest_path)
    upsert_manifest_record(second_record, manifest_path)

    records = load_manifest_records(manifest_path)

    assert len(records) == 1
    assert records[0].known_limitations == "New limitation"
