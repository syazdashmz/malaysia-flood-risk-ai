import json
from pathlib import Path

from floodrisk.data.weather_summary import (
    build_weather_summary_status,
    load_risk_engine_weather_warning,
    load_weather_summary,
    normalize_risk_engine_weather_warning,
)


def test_normalize_risk_engine_weather_warning_accepts_valid_values():
    assert normalize_risk_engine_weather_warning(" Warning ") == "warning"


def test_normalize_risk_engine_weather_warning_defaults_invalid_values():
    assert normalize_risk_engine_weather_warning("unknown") == "none"
    assert normalize_risk_engine_weather_warning(None) == "none"


def test_load_weather_summary_returns_empty_dict_when_missing(tmp_path: Path):
    summary = load_weather_summary(tmp_path / "missing.json")

    assert summary == {}


def test_load_risk_engine_weather_warning_reads_summary(tmp_path: Path):
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(
        json.dumps({"risk_engine_weather_warning": "severe"}),
        encoding="utf-8",
    )

    warning = load_risk_engine_weather_warning(summary_path)

    assert warning == "severe"


def test_build_weather_summary_status(tmp_path: Path):
    summary_path = tmp_path / "summary.json"
    summary_path.write_text(
        json.dumps(
            {
                "risk_engine_weather_warning": "warning",
                "record_count": 6,
                "forecast_count": 3,
                "warning_count": 3,
                "signal_counts": {
                    "none": 0,
                    "advisory": 4,
                    "warning": 2,
                    "severe": 0,
                },
            }
        ),
        encoding="utf-8",
    )

    status = build_weather_summary_status(summary_path)

    assert status["available"] is True
    assert status["risk_engine_weather_warning"] == "warning"
    assert status["record_count"] == 6
    assert status["signal_counts"]["warning"] == 2
