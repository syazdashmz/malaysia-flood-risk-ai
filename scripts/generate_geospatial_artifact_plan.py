"""Generate geospatial artifact planning report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


REPORT_PATH = PROJECT_ROOT / "reports" / "geospatial_artifact_plan.md"


def main() -> None:
    from floodrisk.geospatial.artifacts import (
        check_geospatial_artifacts,
        write_geospatial_artifact_report,
    )

    checks = check_geospatial_artifacts(PROJECT_ROOT)
    output_path = write_geospatial_artifact_report(checks, REPORT_PATH)

    print(f"Generated geospatial artifact plan: {output_path}")

    for check in checks:
        print(f"{check.status}: {check.artifact.relative_path}")


if __name__ == "__main__":
    main()
