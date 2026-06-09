import json
from pathlib import Path

from floodrisk.data.weather_risk import (
    WeatherRiskSummary,
    normalize_weather_signal,
    select_max_weather_signal,
    summarize_weather_features,
    write_weather_risk_summary,
)


def test_normalize_weather_signal_accepts_valid_values():
    assert normalize_weather_signal(" Warning ") == "warning"


def test_normalize_weather_signal_defaults_invalid_values_to_none():
    assert normalize_weather_signal("unknown") == "none"
    assert normalize_weather_signal(None) == "none"


def test_select_max_weather_signal_returns_strongest_signal():
    signal = select_max_weather_signal(["none", "advisory", "warning"])

    assert signal == "warning"


def test_summarize_weather_features_counts_records_and_signals():
    summary = summarize_weather_features(
        [
            {"source_type": "forecast", "weather_signal": "advisory"},
            {"source_type": "warning", "weather_signal": "warning"},
            {"source_type": "warning", "weather_signal": "none"},
        ]
    )

    assert summary.record_count == 3
    assert summary.forecast_count == 1
    assert summary.warning_count == 2
    assert summary.max_weather_signal == "warning"
    assert summary.risk_engine_weather_warning == "warning"
    assert summary.signal_counts["advisory"] == 1


def test_write_weather_risk_summary(tmp_path: Path):
    output_path = tmp_path / "summary.json"
    summary = WeatherRiskSummary(
        record_count=1,
        forecast_count=1,
        warning_count=0,
        max_weather_signal="advisory",
        risk_engine_weather_warning="advisory",
        signal_counts={
            "none": 0,
            "advisory": 1,
            "warning": 0,
            "severe": 0,
        },
    )

    saved_path = write_weather_risk_summary(summary, output_path)
    data = json.loads(saved_path.read_text(encoding="utf-8"))

    assert data["record_count"] == 1
    assert data["risk_engine_weather_warning"] == "advisory"
