"""Load generated weather risk summaries for app/API integration."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

DEFAULT_WEATHER_WARNING = "none"
VALID_RISK_ENGINE_WEATHER_WARNINGS = {
    "none",
    "advisory",
    "warning",
    "severe",
}


def normalize_risk_engine_weather_warning(value: str | None) -> str:
    """Normalize a risk-engine-compatible weather warning value."""

    normalized = (value or "").strip().lower()

    if normalized in VALID_RISK_ENGINE_WEATHER_WARNINGS:
        return normalized

    return DEFAULT_WEATHER_WARNING


def load_weather_summary(summary_path: Path) -> dict[str, Any]:
    """Load weather risk summary JSON from disk."""

    if not summary_path.exists():
        return {}

    data = json.loads(summary_path.read_text(encoding="utf-8"))

    if isinstance(data, dict):
        return data

    return {}


def load_risk_engine_weather_warning(summary_path: Path) -> str:
    """Load the latest weather warning signal for risk-engine input."""

    summary = load_weather_summary(summary_path)

    return normalize_risk_engine_weather_warning(
        str(summary.get("risk_engine_weather_warning", DEFAULT_WEATHER_WARNING))
    )


def build_weather_summary_status(summary_path: Path) -> dict[str, Any]:
    """Build a compact weather summary status payload."""

    summary = load_weather_summary(summary_path)
    weather_warning = load_risk_engine_weather_warning(summary_path)

    return {
        "available": bool(summary),
        "risk_engine_weather_warning": weather_warning,
        "record_count": summary.get("record_count", 0),
        "forecast_count": summary.get("forecast_count", 0),
        "warning_count": summary.get("warning_count", 0),
        "signal_counts": summary.get("signal_counts", {}),
    }
