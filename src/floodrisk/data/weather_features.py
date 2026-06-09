"""Feature extraction helpers for weather-related flood-risk signals."""

from __future__ import annotations

import csv
from pathlib import Path

NO_RISK_TERMS = (
    "no advisory",
    "no weather advisory",
    "no active advisory",
    "no warning",
    "no weather warning",
    "no active warning",
    "no rain",
    "no thunderstorm",
    "no thunderstorms",
    "fair weather",
    "clear weather",
    "tiada amaran",
    "tiada sebarang amaran",
    "tiada hujan",
    "tiada ribut petir",
    "cerah",
)

SEVERE_TERMS = (
    "severe",
    "danger",
    "bahaya",
    "red",
)

WARNING_TERMS = (
    "warning",
    "amaran",
    "heavy rain",
    "continuous rain",
    "continuous heavy rain",
    "hujan lebat",
    "lebat berterusan",
)

ADVISORY_TERMS = (
    "advisory",
    "alert",
    "waspada",
    "rain",
    "hujan",
    "shower",
    "showers",
    "thunderstorm",
    "thunderstorms",
    "ribut petir",
)


def remove_no_risk_terms(text: str) -> str:
    """Remove explicit no-risk phrases before positive signal matching."""

    normalized = text

    for term in NO_RISK_TERMS:
        normalized = normalized.replace(term, " ")

    return " ".join(normalized.split())


def classify_weather_signal(*texts: str | None) -> str:
    """Classify weather text into MVP risk-engine warning categories."""

    combined_text = " ".join(text or "" for text in texts).lower()
    risk_text = remove_no_risk_terms(combined_text)

    if any(term in risk_text for term in SEVERE_TERMS):
        return "severe"

    if any(term in risk_text for term in WARNING_TERMS):
        return "warning"

    if any(term in risk_text for term in ADVISORY_TERMS):
        return "advisory"

    return "none"


def load_csv_records(input_path: Path) -> list[dict[str, str]]:
    """Load CSV records as dictionaries."""

    with input_path.open("r", encoding="utf-8", newline="") as file:
        return list(csv.DictReader(file))


def build_forecast_feature_records(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build weather feature rows from normalized forecast records."""

    feature_rows: list[dict[str, str]] = []

    for record in records:
        summary_forecast = record.get("summary_forecast", "")
        morning_forecast = record.get("morning_forecast", "")
        afternoon_forecast = record.get("afternoon_forecast", "")
        night_forecast = record.get("night_forecast", "")

        feature_rows.append(
            {
                "source_type": "forecast",
                "location_id": record.get("location.location_id", ""),
                "location_name": record.get("location.location_name", ""),
                "date": record.get("date", ""),
                "weather_signal": classify_weather_signal(
                    summary_forecast,
                    morning_forecast,
                    afternoon_forecast,
                    night_forecast,
                ),
                "summary": summary_forecast,
                "valid_from": "",
                "valid_to": "",
            }
        )

    return feature_rows


def build_warning_feature_records(records: list[dict[str, str]]) -> list[dict[str, str]]:
    """Build weather feature rows from normalized warning records."""

    feature_rows: list[dict[str, str]] = []

    for record in records:
        title_en = record.get("warning_issue.title_en", "")
        heading_en = record.get("heading_en", "")
        text_en = record.get("text_en", "")

        feature_rows.append(
            {
                "source_type": "warning",
                "location_id": "",
                "location_name": "",
                "date": record.get("warning_issue.issued", ""),
                "weather_signal": classify_weather_signal(title_en, heading_en, text_en),
                "summary": heading_en or title_en,
                "valid_from": record.get("valid_from", ""),
                "valid_to": record.get("valid_to", ""),
            }
        )

    return feature_rows


def write_feature_records(records: list[dict[str, str]], output_path: Path) -> Path:
    """Write weather feature records to CSV."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "source_type",
        "location_id",
        "location_name",
        "date",
        "weather_signal",
        "summary",
        "valid_from",
        "valid_to",
    ]

    with output_path.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)

    return output_path
