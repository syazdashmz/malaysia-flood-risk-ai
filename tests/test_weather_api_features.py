from pathlib import Path

import pytest

from floodrisk.data.weather_client import (
    build_location_category_filter,
    forecast_record_to_ml_features,
    forecast_records_to_ml_feature_rows,
    score_forecast_phrase,
    weather_warning_record_to_ml_features,
)


def test_build_location_category_filter_supports_state_and_district():
    assert build_location_category_filter("state") == "St@location__location_id"
    assert build_location_category_filter("district") == "Ds@location__location_id"


def test_build_location_category_filter_rejects_unknown_category():
    with pytest.raises(ValueError, match="Unsupported weather location category"):
        build_location_category_filter("kampung")


def test_score_forecast_phrase_maps_rain_and_thunderstorm_terms():
    assert score_forecast_phrase("Tiada hujan") == 0
    assert score_forecast_phrase("Hujan di satu dua tempat") == 1
    assert score_forecast_phrase("Hujan di beberapa tempat") == 2
    assert score_forecast_phrase("Ribut petir di beberapa tempat") == 3


def test_forecast_record_to_ml_features_scores_daily_forecast():
    record = {
        "location": {
            "location_id": "St001",
            "location_name": "Johor",
        },
        "date": "2026-06-11",
        "morning_forecast": "Tiada hujan",
        "afternoon_forecast": "Ribut petir di beberapa tempat",
        "night_forecast": "Hujan di satu dua tempat",
        "summary_forecast": "Ribut petir di beberapa tempat",
        "summary_when": "Petang",
        "min_temp": 24,
        "max_temp": 32,
    }

    features = forecast_record_to_ml_features(record)

    assert features["source_id"] == "data_gov_my_weather_forecast"
    assert features["location_id"] == "St001"
    assert features["location_name"] == "Johor"
    assert features["forecast_date"] == "2026-06-11"
    assert features["morning_rain_score"] == 0
    assert features["afternoon_rain_score"] == 3
    assert features["night_rain_score"] == 1
    assert features["max_period_rain_score"] == 3
    assert features["has_rain_forecast"] == 1
    assert features["has_thunderstorm_forecast"] == 1
    assert features["temp_range_c"] == 8


def test_forecast_records_to_ml_feature_rows_accepts_list_payload():
    payload = [
        {
            "location": {"location_id": "St014", "location_name": "Selangor"},
            "date": "2026-06-11",
            "summary_forecast": "Hujan",
            "min_temp": 25,
            "max_temp": 33,
        }
    ]

    rows = forecast_records_to_ml_feature_rows(payload)

    assert len(rows) == 1
    assert rows[0]["location_name"] == "Selangor"
    assert rows[0]["summary_rain_score"] == 2


def test_weather_warning_record_to_ml_features_scores_warning_text():
    record = {
        "warning_issue": {
            "issued": "2026-06-11T08:00:00",
            "title_bm": "Amaran Hujan Berterusan",
            "title_en": "Continuous Rain Warning",
        },
        "valid_from": "2026-06-11T08:00:00",
        "valid_to": "2026-06-12T08:00:00",
        "heading_en": "Continuous Rain Warning",
        "text_en": "Heavy rain may cause flood-prone areas to be affected.",
        "instruction_en": "Follow official instructions.",
    }

    features = weather_warning_record_to_ml_features(record)

    assert features["source_id"] == "data_gov_my_weather_warning"
    assert features["has_weather_warning"] == 1
    assert features["warning_severity_score"] == 3
    assert features["warning_title_en"] == "Continuous Rain Warning"


def test_live_weather_feature_script_exists():
    script_path = Path("scripts/fetch_live_weather_features.py")
    content = script_path.read_text(encoding="utf-8")

    assert script_path.exists()
    assert "fetch_weather_forecast_by_category" in content
    assert "forecast_records_to_ml_feature_rows" in content
    assert "weather_warning_records_to_ml_feature_rows" in content
