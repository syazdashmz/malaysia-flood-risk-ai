"""Generate initial EDA report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "initial_eda_report.md"


def main() -> None:
    from floodrisk.notebooks.eda import (
        build_initial_eda_summary,
        write_initial_eda_report,
    )

    summary = build_initial_eda_summary(PROJECT_ROOT)
    output_path = write_initial_eda_report(summary, REPORT_PATH)

    print(f"Generated initial EDA report: {output_path}")
    print(f"Sample locations available: {summary.sample_locations_exists}")
    print(f"Sample location rows: {summary.sample_locations_row_count}")
    print(f"Weather summary available: {summary.weather_summary_exists}")
    print(f"Ready for initial EDA: {summary.catalog_ready_for_eda}")
    print(f"Ready for real ML training: {summary.dataset_ready_for_training}")


if __name__ == "__main__":
    main()
