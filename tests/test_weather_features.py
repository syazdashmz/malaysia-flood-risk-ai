import csv
from pathlib import Path

from floodrisk.data.weather_features import (
    build_forecast_feature_records,
    build_warning_feature_records,
    classify_weather_signal,
    load_csv_records,
    write_feature_records,
)


def test_classify_weather_signal_detects_severe():
    status = classify_weather_signal("Severe thunderstorm warning")

    assert status == "severe"


def test_classify_weather_signal_detects_warning():
    status = classify_weather_signal("Continuous heavy rain warning")

    assert status == "warning"


def test_classify_weather_signal_detects_advisory():
    status = classify_weather_signal("Afternoon thunderstorms")

    assert status == "advisory"


def test_classify_weather_signal_defaults_to_none():
    status = classify_weather_signal("Fair weather")

    assert status == "none"


def test_build_forecast_feature_records():
    records = [
        {
            "location.location_id": "St001",
            "location.location_name": "Kuala Lumpur",
            "date": "2026-06-10",
            "summary_forecast": "Thunderstorms",
            "morning_forecast": "No rain",
            "afternoon_forecast": "Thunderstorms",
            "night_forecast": "No rain",
        }
    ]

    features = build_forecast_feature_records(records)

    assert features[0]["source_type"] == "forecast"
    assert features[0]["location_name"] == "Kuala Lumpur"
    assert features[0]["weather_signal"] == "advisory"


def test_build_warning_feature_records():
    records = [
        {
            "warning_issue.title_en": "Warning",
            "heading_en": "Continuous Heavy Rain Warning",
            "text_en": "Heavy rain is expected.",
            "warning_issue.issued": "2026-06-10T00:00:00",
            "valid_from": "2026-06-10T00:00:00",
            "valid_to": "2026-06-10T12:00:00",
        }
    ]

    features = build_warning_feature_records(records)

    assert features[0]["source_type"] == "warning"
    assert features[0]["weather_signal"] == "warning"
    assert features[0]["summary"] == "Continuous Heavy Rain Warning"


def test_write_and_load_feature_records(tmp_path: Path):
    output_path = tmp_path / "features.csv"

    write_feature_records(
        [
            {
                "source_type": "forecast",
                "location_id": "St001",
                "location_name": "Kuala Lumpur",
                "date": "2026-06-10",
                "weather_signal": "advisory",
                "summary": "Thunderstorms",
                "valid_from": "",
                "valid_to": "",
            }
        ],
        output_path,
    )

    rows = load_csv_records(output_path)

    assert rows[0]["location_name"] == "Kuala Lumpur"
    assert rows[0]["weather_signal"] == "advisory"

    with output_path.open("r", encoding="utf-8", newline="") as file:
        header = next(csv.reader(file))

    assert header[0] == "source_type"
