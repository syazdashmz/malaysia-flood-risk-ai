"""Create a lightweight profile report for normalized weather samples."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


INTERIM_WEATHER_DIR = PROJECT_ROOT / "data" / "interim" / "weather"
REPORT_PATH = PROJECT_ROOT / "reports" / "weather_sample_profile.md"


def main() -> None:
    from floodrisk.data.profile import profile_csv, write_profiles_markdown

    input_paths = sorted(INTERIM_WEATHER_DIR.glob("*.csv"))

    if not input_paths:
        msg = (
            "No normalized weather CSV files found. Run scripts/normalize_weather_samples.py first."
        )
        raise FileNotFoundError(msg)

    profiles = [profile_csv(input_path) for input_path in input_paths]
    output_path = write_profiles_markdown(
        profiles,
        REPORT_PATH,
        title="Weather Sample Data Quality Profile",
    )

    print(f"Generated weather profile report: {output_path}")


if __name__ == "__main__":
    main()
