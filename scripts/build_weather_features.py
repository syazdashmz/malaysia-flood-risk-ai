"""Build weather feature table from local normalized weather samples."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


INTERIM_WEATHER_DIR = PROJECT_ROOT / "data" / "interim" / "weather"
OUTPUT_PATH = PROJECT_ROOT / "data" / "processed" / "weather" / "weather_sample_features.csv"


def main() -> None:
    from floodrisk.data.weather_features import (
        build_forecast_feature_records,
        build_warning_feature_records,
        load_csv_records,
        write_feature_records,
    )

    forecast_path = INTERIM_WEATHER_DIR / "weather_forecast_sample_flat.csv"
    warning_path = INTERIM_WEATHER_DIR / "weather_warning_sample_flat.csv"

    if not forecast_path.exists() or not warning_path.exists():
        msg = (
            "Normalized weather samples not found. Run scripts/normalize_weather_samples.py first."
        )
        raise FileNotFoundError(msg)

    forecast_records = load_csv_records(forecast_path)
    warning_records = load_csv_records(warning_path)

    feature_records = [
        *build_forecast_feature_records(forecast_records),
        *build_warning_feature_records(warning_records),
    ]

    output_path = write_feature_records(feature_records, OUTPUT_PATH)

    print(f"Generated weather feature table: {output_path}")
    print(f"Rows: {len(feature_records)}")


if __name__ == "__main__":
    main()
