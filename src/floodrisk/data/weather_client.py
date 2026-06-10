"""Client utilities for Malaysia weather data from data.gov.my."""

from __future__ import annotations

import json
from collections.abc import Mapping
from pathlib import Path
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from floodrisk.version import __version__

BASE_WEATHER_URL = "https://api.data.gov.my/weather"
USER_AGENT = f"malaysia-flood-risk-ai/{__version__}"

LOCATION_CATEGORY_PREFIXES = {
    "state": "St",
    "recreation_centre": "Rc",
    "district": "Ds",
    "town": "Tn",
    "division": "Dv",
}

FORECAST_RISK_SCORES = {
    "berjerebu": 0,
    "tiada hujan": 0,
    "hujan": 2,
    "hujan di satu dua tempat": 1,
    "hujan di satu dua tempat di kawasan pantai": 1,
    "hujan di satu dua tempat di kawasan pedalaman": 1,
    "hujan di beberapa tempat": 2,
    "ribut petir": 3,
    "ribut petir di satu dua tempat": 2,
    "ribut petir di satu dua tempat di kawasan pantai": 2,
    "ribut petir di satu dua tempat di kawasan pedalaman": 2,
    "ribut petir di beberapa tempat": 3,
    "ribut petir di beberapa tempat di kawasan pedalaman": 3,
}


def build_weather_url(endpoint: str, params: dict[str, Any] | None = None) -> str:
    """Build a data.gov.my weather API URL."""

    endpoint = endpoint.strip("/")

    if endpoint not in {"forecast", "warning"}:
        msg = f"Unsupported weather endpoint: {endpoint}"
        raise ValueError(msg)

    url = f"{BASE_WEATHER_URL}/{endpoint}"

    if not params:
        return url

    return f"{url}?{urlencode(params)}"


def build_location_category_filter(category: str) -> str:
    """Build a data.gov.my nested-field filter for weather location category."""
    normalized_category = category.strip().lower().replace(" ", "_").replace("-", "_")

    if normalized_category not in LOCATION_CATEGORY_PREFIXES:
        supported = ", ".join(sorted(LOCATION_CATEGORY_PREFIXES))
        msg = f"Unsupported weather location category: {category}. Supported: {supported}"
        raise ValueError(msg)

    return f"{LOCATION_CATEGORY_PREFIXES[normalized_category]}@location__location_id"


def fetch_json(url: str, timeout_seconds: int = 30) -> Any:
    """Fetch JSON from a URL."""

    request = Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )

    with urlopen(request, timeout=timeout_seconds) as response:
        body = response.read().decode("utf-8")

    return json.loads(body)


def fetch_weather_forecast(
    *,
    limit: int = 100,
    contains: str | None = None,
    location_category: str | None = None,
    timeout_seconds: int = 30,
) -> Any:
    """Fetch 7-day general weather forecast records."""

    params: dict[str, Any] = {"limit": limit}

    if contains:
        params["contains"] = contains
    elif location_category:
        params["contains"] = build_location_category_filter(location_category)

    url = build_weather_url("forecast", params)
    return fetch_json(url, timeout_seconds=timeout_seconds)


def fetch_weather_forecast_by_category(
    category: str,
    *,
    limit: int = 100,
    timeout_seconds: int = 30,
) -> Any:
    """Fetch forecast records for a known data.gov.my weather location category."""
    return fetch_weather_forecast(
        limit=limit,
        location_category=category,
        timeout_seconds=timeout_seconds,
    )


def fetch_weather_warnings(
    *,
    limit: int = 100,
    timeout_seconds: int = 30,
) -> Any:
    """Fetch active or recent weather warning records."""

    url = build_weather_url("warning", {"limit": limit})
    return fetch_json(url, timeout_seconds=timeout_seconds)


def save_json(data: Any, output_path: Path) -> Path:
    """Save JSON data to disk."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    output_path.write_text(
        json.dumps(data, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return output_path


def as_record_list(payload: Any) -> list[Mapping[str, Any]]:
    """Convert a direct-list or wrapped API payload into records."""
    if isinstance(payload, list):
        return [record for record in payload if isinstance(record, Mapping)]

    if isinstance(payload, Mapping) and isinstance(payload.get("data"), list):
        return [record for record in payload["data"] if isinstance(record, Mapping)]

    return []


def normalize_forecast_text(value: Any) -> str:
    """Normalize Bahasa Melayu weather forecast text."""
    if value is None:
        return ""

    return str(value).strip().lower()


def score_forecast_phrase(value: Any) -> int:
    """Convert official forecast phrase into a simple ML-ready rain risk score."""
    normalized_value = normalize_forecast_text(value)

    if not normalized_value:
        return 0

    if normalized_value in FORECAST_RISK_SCORES:
        return FORECAST_RISK_SCORES[normalized_value]

    if "ribut petir" in normalized_value:
        if "beberapa tempat" in normalized_value:
            return 3
        return 2

    if "hujan" in normalized_value:
        if "beberapa tempat" in normalized_value:
            return 2
        return 1

    return 0


def has_thunderstorm_forecast(*values: Any) -> int:
    """Return 1 when any forecast period mentions thunderstorms."""
    return int(any("ribut petir" in normalize_forecast_text(value) for value in values))


def safe_float(value: Any) -> float | None:
    """Convert API numeric values safely."""
    if value is None or value == "":
        return None

    try:
        return float(value)
    except (TypeError, ValueError):
        return None


def forecast_record_to_ml_features(record: Mapping[str, Any]) -> dict[str, Any]:
    """Transform one forecast record into ML-ready weather features."""
    location = record.get("location", {})
    if not isinstance(location, Mapping):
        location = {}

    morning_forecast = record.get("morning_forecast")
    afternoon_forecast = record.get("afternoon_forecast")
    night_forecast = record.get("night_forecast")
    summary_forecast = record.get("summary_forecast")

    morning_score = score_forecast_phrase(morning_forecast)
    afternoon_score = score_forecast_phrase(afternoon_forecast)
    night_score = score_forecast_phrase(night_forecast)
    summary_score = score_forecast_phrase(summary_forecast)

    min_temp_c = safe_float(record.get("min_temp"))
    max_temp_c = safe_float(record.get("max_temp"))

    temp_range_c = None
    if min_temp_c is not None and max_temp_c is not None:
        temp_range_c = max_temp_c - min_temp_c

    max_period_score = max(morning_score, afternoon_score, night_score, summary_score)

    return {
        "source_id": "data_gov_my_weather_forecast",
        "location_id": location.get("location_id"),
        "location_name": location.get("location_name"),
        "forecast_date": record.get("date"),
        "morning_forecast": morning_forecast,
        "afternoon_forecast": afternoon_forecast,
        "night_forecast": night_forecast,
        "summary_forecast": summary_forecast,
        "summary_when": record.get("summary_when"),
        "morning_rain_score": morning_score,
        "afternoon_rain_score": afternoon_score,
        "night_rain_score": night_score,
        "summary_rain_score": summary_score,
        "max_period_rain_score": max_period_score,
        "has_rain_forecast": int(max_period_score > 0),
        "has_thunderstorm_forecast": has_thunderstorm_forecast(
            morning_forecast,
            afternoon_forecast,
            night_forecast,
            summary_forecast,
        ),
        "min_temp_c": min_temp_c,
        "max_temp_c": max_temp_c,
        "temp_range_c": temp_range_c,
    }


def forecast_records_to_ml_feature_rows(payload: Any) -> list[dict[str, Any]]:
    """Transform forecast API payload into ML-ready weather feature rows."""
    return [forecast_record_to_ml_features(record) for record in as_record_list(payload)]


def infer_warning_severity_score(record: Mapping[str, Any]) -> int:
    """Infer simple weather-warning severity score from warning text."""
    warning_issue = record.get("warning_issue", {})
    if not isinstance(warning_issue, Mapping):
        warning_issue = {}

    text_values = [
        warning_issue.get("title_bm"),
        warning_issue.get("title_en"),
        record.get("heading_bm"),
        record.get("heading_en"),
        record.get("text_bm"),
        record.get("text_en"),
        record.get("instruction_bm"),
        record.get("instruction_en"),
    ]
    combined_text = " ".join(str(value).lower() for value in text_values if value)

    if not combined_text:
        return 0

    if any(
        term in combined_text
        for term in [
            "bahaya",
            "danger",
            "severe",
            "hujan berterusan",
            "continuous rain",
            "heavy rain",
            "banjir",
            "flood",
        ]
    ):
        return 3

    if any(
        term in combined_text for term in ["amaran", "warning", "ribut", "thunderstorm", "kategori"]
    ):
        return 2

    if any(term in combined_text for term in ["advisory", "alert", "waspada"]):
        return 1

    return 1


def weather_warning_record_to_ml_features(
    record: Mapping[str, Any],
) -> dict[str, Any]:
    """Transform one warning record into ML-ready weather-warning features."""
    warning_issue = record.get("warning_issue", {})
    if not isinstance(warning_issue, Mapping):
        warning_issue = {}

    return {
        "source_id": "data_gov_my_weather_warning",
        "warning_issued_at": warning_issue.get("issued"),
        "warning_title_bm": warning_issue.get("title_bm"),
        "warning_title_en": warning_issue.get("title_en"),
        "valid_from": record.get("valid_from"),
        "valid_to": record.get("valid_to"),
        "heading_bm": record.get("heading_bm"),
        "heading_en": record.get("heading_en"),
        "text_bm": record.get("text_bm"),
        "text_en": record.get("text_en"),
        "instruction_bm": record.get("instruction_bm"),
        "instruction_en": record.get("instruction_en"),
        "has_weather_warning": 1,
        "warning_severity_score": infer_warning_severity_score(record),
    }


def weather_warning_records_to_ml_feature_rows(
    payload: Any,
) -> list[dict[str, Any]]:
    """Transform weather warning payload into ML-ready warning feature rows."""
    return [weather_warning_record_to_ml_features(record) for record in as_record_list(payload)]
