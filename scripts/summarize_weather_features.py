"""Summarize local weather feature records for risk-engine use."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


FEATURE_PATH = PROJECT_ROOT / "data" / "processed" / "weather" / "weather_sample_features.csv"
REPORT_PATH = PROJECT_ROOT / "reports" / "weather_risk_signal_summary.json"


def main() -> None:
    from floodrisk.data.weather_risk import (
        summarize_weather_feature_file,
        write_weather_risk_summary,
    )

    if not FEATURE_PATH.exists():
        msg = "Weather feature table not found. Run scripts/build_weather_features.py first."
        raise FileNotFoundError(msg)

    summary = summarize_weather_feature_file(FEATURE_PATH)
    output_path = write_weather_risk_summary(summary, REPORT_PATH)

    print(f"Generated weather risk summary: {output_path}")
    print(f"Risk engine weather warning: {summary.risk_engine_weather_warning}")


if __name__ == "__main__":
    main()
