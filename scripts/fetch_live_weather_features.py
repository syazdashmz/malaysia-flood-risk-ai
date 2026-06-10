"""Fetch live weather data and transform it into ML-ready feature rows."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.data.weather_client import (  # noqa: E402
    fetch_weather_forecast_by_category,
    fetch_weather_warnings,
    forecast_records_to_ml_feature_rows,
    save_json,
    weather_warning_records_to_ml_feature_rows,
)

RAW_OUTPUT_DIR = PROJECT_ROOT / "data" / "raw" / "data_gov_my"
PROCESSED_OUTPUT_DIR = PROJECT_ROOT / "data" / "processed" / "data_gov_my"
REPORT_OUTPUT_DIR = PROJECT_ROOT / "reports"


def build_summary(
    *,
    forecast_payload: Any,
    forecast_features: list[dict[str, Any]],
    warning_payload: Any,
    warning_features: list[dict[str, Any]],
    category: str,
) -> dict[str, Any]:
    """Build a lightweight extraction summary."""
    return {
        "source_id": "data_gov_my_weather",
        "extracted_at_utc": datetime.now(UTC).isoformat(),
        "forecast_location_category": category,
        "raw_forecast_records": len(forecast_payload)
        if isinstance(forecast_payload, list)
        else None,
        "forecast_feature_rows": len(forecast_features),
        "raw_warning_records": len(warning_payload) if isinstance(warning_payload, list) else None,
        "warning_feature_rows": len(warning_features),
        "forecast_feature_path": str(PROCESSED_OUTPUT_DIR / "weather_forecast_ml_features.json"),
        "warning_feature_path": str(PROCESSED_OUTPUT_DIR / "weather_warning_ml_features.json"),
    }


def parse_args() -> argparse.Namespace:
    """Parse CLI arguments."""
    parser = argparse.ArgumentParser(
        description=(
            "Fetch live Data.gov.my weather data and transform it into ML-ready feature rows."
        )
    )
    parser.add_argument(
        "--category",
        default="state",
        choices=["state", "district", "town", "division", "recreation_centre"],
        help="Weather location category to fetch for forecast records.",
    )
    parser.add_argument(
        "--forecast-limit",
        type=int,
        default=100,
        help="Maximum number of forecast records to fetch.",
    )
    parser.add_argument(
        "--warning-limit",
        type=int,
        default=100,
        help="Maximum number of warning records to fetch.",
    )
    return parser.parse_args()


def main() -> int:
    """Run live weather extraction."""
    args = parse_args()

    forecast_payload = fetch_weather_forecast_by_category(
        args.category,
        limit=args.forecast_limit,
    )
    warning_payload = fetch_weather_warnings(limit=args.warning_limit)

    forecast_features = forecast_records_to_ml_feature_rows(forecast_payload)
    warning_features = weather_warning_records_to_ml_feature_rows(warning_payload)

    raw_forecast_path = RAW_OUTPUT_DIR / "weather_forecast_latest.json"
    raw_warning_path = RAW_OUTPUT_DIR / "weather_warning_latest.json"
    forecast_feature_path = PROCESSED_OUTPUT_DIR / "weather_forecast_ml_features.json"
    warning_feature_path = PROCESSED_OUTPUT_DIR / "weather_warning_ml_features.json"
    summary_path = REPORT_OUTPUT_DIR / "live_weather_feature_summary.json"

    save_json(forecast_payload, raw_forecast_path)
    save_json(warning_payload, raw_warning_path)
    save_json(forecast_features, forecast_feature_path)
    save_json(warning_features, warning_feature_path)

    summary = build_summary(
        forecast_payload=forecast_payload,
        forecast_features=forecast_features,
        warning_payload=warning_payload,
        warning_features=warning_features,
        category=args.category,
    )
    save_json(summary, summary_path)

    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
