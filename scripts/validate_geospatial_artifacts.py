"""Run geospatial artifact and vector validation checks."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


REPORT_PATH = PROJECT_ROOT / "reports" / "geospatial_validation_report.md"


def main() -> None:
    from floodrisk.geospatial.validation_report import (
        build_geospatial_validation_summary,
        write_geospatial_validation_report,
    )

    summary = build_geospatial_validation_summary(PROJECT_ROOT)
    output_path = write_geospatial_validation_report(summary, REPORT_PATH)

    print(f"Generated geospatial validation report: {output_path}")
    print(f"Planned artifacts: {summary.planned_artifact_count}")
    print(f"Available artifacts: {summary.available_artifact_count}")
    print(f"Missing artifacts: {summary.missing_artifact_count}")
    print(f"Valid vector datasets: {summary.valid_vector_count}")


if __name__ == "__main__":
    main()
