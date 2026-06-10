"""Generate target-source candidate manifest report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "target_source_manifest_report.md"


def main() -> None:
    from floodrisk.ml.target_source_manifest import (
        validate_target_source_manifest,
        write_target_source_manifest_report,
    )

    validation = validate_target_source_manifest(PROJECT_ROOT)
    output_path = write_target_source_manifest_report(validation, REPORT_PATH)

    print(f"Generated target source manifest report: {output_path}")
    print(f"Exists: {validation.exists}")
    print(f"Manifest valid: {validation.is_valid}")
    print(f"Candidate sources: {validation.candidate_count}")
    print(f"Ready candidate sources: {validation.ready_candidate_count}")


if __name__ == "__main__":
    main()
