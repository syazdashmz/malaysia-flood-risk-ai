"""Generate target-label source evaluation report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "target_label_source_evaluation.md"


def main() -> None:
    from floodrisk.ml.target_source_evaluation import (
        build_target_source_evaluation_summary,
        write_target_source_evaluation_report,
    )

    summary = build_target_source_evaluation_summary()
    output_path = write_target_source_evaluation_report(summary, REPORT_PATH)

    print(f"Generated target source evaluation report: {output_path}")
    print(f"Target column: {summary.target_column}")
    print(f"Candidate sources: {summary.candidate_count}")
    print(f"Ready candidate sources: {summary.ready_candidate_count}")
    print(f"Real training target ready: {summary.real_training_target_ready}")


if __name__ == "__main__":
    main()
