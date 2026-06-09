"""Fetch small weather samples from Malaysia's official Open API.

This script downloads small sample files only.

It is intended for Phase 2 data acquisition testing, not full dataset ingestion.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.data.manifest import (  # noqa: E402
    DataSourceRecord,
    append_manifest_record,
    current_utc_date,
)
from floodrisk.data.weather_client import (  # noqa: E402
    fetch_weather_forecast,
    fetch_weather_warnings,
    save_json,
)

RAW_WEATHER_DIR = PROJECT_ROOT / "data" / "raw" / "weather"
STRUCTURED_MANIFEST_PATH = PROJECT_ROOT / "data" / "raw" / "manifest.jsonl"

LICENSE_OR_USAGE = (
    "Public API sample for research and portfolio use. "
    "Confirm official terms before production use."
)


def main() -> None:
    access_date = current_utc_date()

    forecast_data = fetch_weather_forecast(limit=3)
    forecast_path = save_json(
        forecast_data,
        RAW_WEATHER_DIR / "weather_forecast_sample.json",
    )

    warning_data = fetch_weather_warnings(limit=3)
    warning_path = save_json(
        warning_data,
        RAW_WEATHER_DIR / "weather_warning_sample.json",
    )

    append_manifest_record(
        DataSourceRecord(
            dataset_name="MET Malaysia 7-day weather forecast sample",
            source_organization="MET Malaysia via data.gov.my",
            source_url="https://api.data.gov.my/weather/forecast",
            access_date=access_date,
            license_or_usage=LICENSE_OR_USAGE,
            raw_path=str(forecast_path.relative_to(PROJECT_ROOT)),
            processing_script="scripts/fetch_weather_sample.py",
            known_limitations=(
                "Small API sample only; not a complete historical or modelling dataset."
            ),
            notes={"limit": 3, "api": "data.gov.my weather forecast"},
        ),
        STRUCTURED_MANIFEST_PATH,
    )

    append_manifest_record(
        DataSourceRecord(
            dataset_name="MET Malaysia weather warning sample",
            source_organization="MET Malaysia via data.gov.my",
            source_url="https://api.data.gov.my/weather/warning",
            access_date=access_date,
            license_or_usage=LICENSE_OR_USAGE,
            raw_path=str(warning_path.relative_to(PROJECT_ROOT)),
            processing_script="scripts/fetch_weather_sample.py",
            known_limitations="Small API sample only; warning data updates when required.",
            notes={"limit": 3, "api": "data.gov.my weather warning"},
        ),
        STRUCTURED_MANIFEST_PATH,
    )

    print(f"Saved forecast sample: {forecast_path}")
    print(f"Saved warning sample: {warning_path}")
    print(f"Updated manifest: {STRUCTURED_MANIFEST_PATH}")


if __name__ == "__main__":
    main()
