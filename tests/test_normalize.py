import csv
from pathlib import Path

from floodrisk.data.normalize import (
    extract_records,
    flatten_mapping,
    load_json_records,
    write_records_csv,
)


def test_extract_records_from_list():
    records = extract_records([{"id": 1}, {"id": 2}])

    assert records == [{"id": 1}, {"id": 2}]


def test_extract_records_from_data_key():
    records = extract_records({"data": [{"id": 1}]})

    assert records == [{"id": 1}]


def test_flatten_mapping_handles_nested_values():
    flattened = flatten_mapping(
        {
            "location": {
                "name": "Kuala Lumpur",
                "state": "Kuala Lumpur",
            },
            "warnings": ["heavy_rain"],
        }
    )

    assert flattened["location.name"] == "Kuala Lumpur"
    assert flattened["location.state"] == "Kuala Lumpur"
    assert flattened["warnings"] == '["heavy_rain"]'


def test_write_records_csv(tmp_path: Path):
    output_path = tmp_path / "records.csv"

    write_records_csv(
        [
            {"location": {"name": "Kuala Lumpur"}, "value": 1},
            {"location": {"name": "Shah Alam"}, "value": 2},
        ],
        output_path,
    )

    with output_path.open("r", encoding="utf-8", newline="") as file:
        rows = list(csv.DictReader(file))

    assert rows[0]["location.name"] == "Kuala Lumpur"
    assert rows[1]["value"] == "2"


def test_load_json_records(tmp_path: Path):
    input_path = tmp_path / "records.json"
    input_path.write_text('{"data": [{"id": 1}]}', encoding="utf-8")

    records = load_json_records(input_path)

    assert records == [{"id": 1}]
