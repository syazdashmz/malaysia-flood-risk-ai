"""Normalize locally downloaded weather API samples.

Raw JSON files remain ignored by Git.
The generated CSV files are local working artifacts for inspection.
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.data.normalize import load_json_records, write_records_csv  # noqa: E402


RAW_WEATHER_DIR = PROJECT_ROOT / "data" / "raw" / "weather"
INTERIM_WEATHER_DIR = PROJECT_ROOT / "data" / "interim" / "weather"


def normalize_weather_sample(input_path: Path, output_path: Path) -> int:
    records = load_json_records(input_path)
    write_records_csv(records, output_path)
    return len(records)


def main() -> None:
    targets = [
        (
            RAW_WEATHER_DIR / "weather_forecast_sample.json",
            INTERIM_WEATHER_DIR / "weather_forecast_sample_flat.csv",
        ),
        (
            RAW_WEATHER_DIR / "weather_warning_sample.json",
            INTERIM_WEATHER_DIR / "weather_warning_sample_flat.csv",
        ),
    ]

    for input_path, output_path in targets:
        record_count = normalize_weather_sample(input_path, output_path)
        print(f"Normalized {record_count} records: {output_path}")


if __name__ == "__main__":
    main()
