"""Generate dataset readiness report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "dataset_readiness_report.md"


def main() -> None:
    from floodrisk.notebooks.readiness import (
        build_dataset_readiness_summary,
        write_dataset_readiness_report,
    )

    summary = build_dataset_readiness_summary(PROJECT_ROOT)
    output_path = write_dataset_readiness_report(summary, REPORT_PATH)

    print(f"Generated dataset readiness report: {output_path}")
    print(f"Checks: {summary.check_count}")
    print(f"Available: {summary.available_count}")
    print(f"Missing: {summary.missing_count}")
    print(f"Blocking training: {summary.blocking_count}")
    print(f"Ready for ML training: {summary.ready_for_training}")


if __name__ == "__main__":
    main()
