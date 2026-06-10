"""Utilities for using live weather API feature rows inside the app."""

from __future__ import annotations

import json
from collections.abc import Mapping
from datetime import date
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_FORECAST_FEATURE_PATH = (
    PROJECT_ROOT / "data" / "processed" / "data_gov_my" / "weather_forecast_ml_features.json"
)
DEFAULT_WARNING_FEATURE_PATH = (
    PROJECT_ROOT / "data" / "processed" / "data_gov_my" / "weather_warning_ml_features.json"
)


def load_live_weather_feature_rows(path: Path) -> list[dict[str, Any]]:
    """Load generated live weather feature rows if available."""
    if not path.exists():
        return []

    payload = json.loads(path.read_text(encoding="utf-8"))

    if not isinstance(payload, list):
        return []

    return [dict(row) for row in payload if isinstance(row, Mapping)]


def normalize_region_name(value: Any) -> str:
    """Normalize region names for matching state/federal territory forecasts."""
    normalized = str(value or "").strip().lower()

    replacements = {
        "w.p.": "",
        "wp": "",
        "wilayah persekutuan": "",
        "pulau": "pulau",
    }

    for old, new in replacements.items():
        normalized = normalized.replace(old, new)

    return " ".join(normalized.replace(".", " ").split())


def parse_forecast_date(value: Any) -> date | None:
    """Parse forecast date safely."""
    if value is None:
        return None

    try:
        return date.fromisoformat(str(value)[:10])
    except ValueError:
        return None


def select_forecast_for_region(
    forecast_rows: list[dict[str, Any]],
    region_name: str,
    selected_date: date | None = None,
) -> dict[str, Any] | None:
    """Select the best forecast feature row for a region and optional date."""
    normalized_region = normalize_region_name(region_name)

    candidates = [
        row
        for row in forecast_rows
        if normalize_region_name(row.get("location_name")) == normalized_region
    ]

    if not candidates:
        return None

    if selected_date is not None:
        same_date_candidates = [
            row
            for row in candidates
            if parse_forecast_date(row.get("forecast_date")) == selected_date
        ]
        if same_date_candidates:
            return same_date_candidates[0]

    dated_candidates = [
        row for row in candidates if parse_forecast_date(row.get("forecast_date")) is not None
    ]

    if dated_candidates:
        return max(
            dated_candidates,
            key=lambda row: parse_forecast_date(row.get("forecast_date")) or date.min,
        )

    return candidates[0]


def highest_warning_severity(
    warning_rows: list[dict[str, Any]],
) -> int:
    """Return highest available warning severity from warning feature rows."""
    severities = []

    for row in warning_rows:
        value = row.get("warning_severity_score")
        try:
            severities.append(int(value))
        except (TypeError, ValueError):
            continue

    return max(severities, default=0)


def weather_warning_status_from_signal(
    *,
    max_period_rain_score: int,
    has_thunderstorm_forecast: int,
    warning_severity_score: int,
) -> str:
    """Map live weather feature values to the app risk-engine warning categories."""
    if warning_severity_score >= 3:
        return "severe"

    if max_period_rain_score >= 3 or warning_severity_score >= 2:
        return "warning"

    if max_period_rain_score >= 1 or has_thunderstorm_forecast or warning_severity_score >= 1:
        return "advisory"

    return "none"


def summarize_live_weather_signal(
    *,
    region_name: str,
    forecast_rows: list[dict[str, Any]],
    warning_rows: list[dict[str, Any]],
    selected_date: date | None = None,
) -> dict[str, Any]:
    """Summarize live weather features for one region into app-ready signals."""
    forecast = select_forecast_for_region(
        forecast_rows,
        region_name=region_name,
        selected_date=selected_date,
    )
    warning_severity_score = highest_warning_severity(warning_rows)

    if forecast is None:
        return {
            "available": False,
            "region_name": region_name,
            "weather_warning_status": "none",
            "warning_severity_score": warning_severity_score,
            "warning_feature_rows": len(warning_rows),
            "note": (
                "No matching live forecast feature row is available for this region. "
                "Run scripts/fetch_live_weather_features.py to refresh local live data."
            ),
        }

    max_period_rain_score = int(forecast.get("max_period_rain_score") or 0)
    has_thunderstorm = int(forecast.get("has_thunderstorm_forecast") or 0)

    return {
        "available": True,
        "region_name": region_name,
        "matched_location_name": forecast.get("location_name"),
        "forecast_date": forecast.get("forecast_date"),
        "summary_forecast": forecast.get("summary_forecast"),
        "summary_when": forecast.get("summary_when"),
        "max_period_rain_score": max_period_rain_score,
        "has_thunderstorm_forecast": has_thunderstorm,
        "warning_severity_score": warning_severity_score,
        "warning_feature_rows": len(warning_rows),
        "weather_warning_status": weather_warning_status_from_signal(
            max_period_rain_score=max_period_rain_score,
            has_thunderstorm_forecast=has_thunderstorm,
            warning_severity_score=warning_severity_score,
        ),
        "note": (
            "Forecast signal is matched by region. Warning severity is currently "
            "treated as a national/latest warning signal until warning areas are "
            "matched to districts/states."
        ),
    }
