from datetime import date
from pathlib import Path

from floodrisk.data.live_weather_features import (
    highest_warning_severity,
    load_live_weather_feature_rows,
    normalize_region_name,
    select_forecast_for_region,
    summarize_live_weather_signal,
    weather_warning_status_from_signal,
)


def test_normalize_region_name_handles_federal_territory_prefixes():
    assert normalize_region_name("W.P. Kuala Lumpur") == "kuala lumpur"
    assert normalize_region_name("WP Putrajaya") == "putrajaya"
    assert normalize_region_name("Selangor") == "selangor"


def test_select_forecast_for_region_prefers_selected_date():
    rows = [
        {
            "location_name": "Selangor",
            "forecast_date": "2026-06-10",
            "max_period_rain_score": 1,
        },
        {
            "location_name": "Selangor",
            "forecast_date": "2026-06-11",
            "max_period_rain_score": 3,
        },
    ]

    selected = select_forecast_for_region(
        rows,
        region_name="Selangor",
        selected_date=date(2026, 6, 11),
    )

    assert selected is not None
    assert selected["max_period_rain_score"] == 3


def test_select_forecast_for_region_falls_back_to_latest_date():
    rows = [
        {"location_name": "Johor", "forecast_date": "2026-06-10"},
        {"location_name": "Johor", "forecast_date": "2026-06-12"},
    ]

    selected = select_forecast_for_region(rows, region_name="Johor")

    assert selected is not None
    assert selected["forecast_date"] == "2026-06-12"


def test_highest_warning_severity_returns_max_score():
    rows = [
        {"warning_severity_score": 1},
        {"warning_severity_score": 3},
        {"warning_severity_score": 2},
    ]

    assert highest_warning_severity(rows) == 3


def test_weather_warning_status_from_signal_maps_to_risk_engine_status():
    assert (
        weather_warning_status_from_signal(
            max_period_rain_score=0,
            has_thunderstorm_forecast=0,
            warning_severity_score=0,
        )
        == "none"
    )
    assert (
        weather_warning_status_from_signal(
            max_period_rain_score=1,
            has_thunderstorm_forecast=0,
            warning_severity_score=0,
        )
        == "advisory"
    )
    assert (
        weather_warning_status_from_signal(
            max_period_rain_score=3,
            has_thunderstorm_forecast=1,
            warning_severity_score=0,
        )
        == "warning"
    )
    assert (
        weather_warning_status_from_signal(
            max_period_rain_score=1,
            has_thunderstorm_forecast=1,
            warning_severity_score=3,
        )
        == "severe"
    )


def test_summarize_live_weather_signal_returns_app_ready_signal():
    forecast_rows = [
        {
            "location_name": "Pahang",
            "forecast_date": "2026-06-11",
            "summary_forecast": "Ribut petir di beberapa tempat",
            "summary_when": "Petang",
            "max_period_rain_score": 3,
            "has_thunderstorm_forecast": 1,
        }
    ]
    warning_rows = [{"warning_severity_score": 2}]

    signal = summarize_live_weather_signal(
        region_name="Pahang",
        forecast_rows=forecast_rows,
        warning_rows=warning_rows,
        selected_date=date(2026, 6, 11),
    )

    assert signal["available"] is True
    assert signal["matched_location_name"] == "Pahang"
    assert signal["weather_warning_status"] == "warning"
    assert signal["warning_feature_rows"] == 1


def test_load_live_weather_feature_rows_returns_empty_for_missing_file(tmp_path):
    missing_path = tmp_path / "missing.json"

    assert load_live_weather_feature_rows(missing_path) == []


def test_load_live_weather_feature_rows_loads_list_payload(tmp_path):
    feature_path = tmp_path / "features.json"
    feature_path.write_text('[{"location_name": "Johor"}]', encoding="utf-8")

    assert load_live_weather_feature_rows(feature_path) == [{"location_name": "Johor"}]


def test_live_weather_feature_module_paths_are_project_relative():
    module_path = Path("src/floodrisk/data/live_weather_features.py")
    content = module_path.read_text(encoding="utf-8")

    assert "data_gov_my" in content
    assert "weather_forecast_ml_features.json" in content
    assert "weather_warning_ml_features.json" in content
