"""Run live metadata-only ReliefWeb discovery."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

JSON_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "interim" / "source_discovery" / "reliefweb_metadata.json"
)
REPORT_OUTPUT_PATH = PROJECT_ROOT / "reports" / "reliefweb_metadata_discovery_report.md"


def main() -> None:
    from floodrisk.sources.reliefweb import (
        discover_reliefweb_metadata,
        write_reliefweb_metadata_discovery_outputs,
    )

    result = discover_reliefweb_metadata(PROJECT_ROOT)
    json_path, report_path = write_reliefweb_metadata_discovery_outputs(
        result,
        json_output_path=JSON_OUTPUT_PATH,
        report_output_path=REPORT_OUTPUT_PATH,
    )

    print(f"Generated ReliefWeb metadata JSON: {json_path}")
    print(f"Generated ReliefWeb metadata report: {report_path}")
    print(f"Report metadata records: {result.report_count}")
    print(f"Successful: {result.is_successful}")
    print(f"Direct training use allowed: {result.direct_training_use_allowed}")


if __name__ == "__main__":
    main()
