"""Generate target label source plan report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "target_label_source_plan.md"


def main() -> None:
    from floodrisk.ml.target_label_plan import (
        build_target_label_source_plan,
        write_target_label_source_plan_report,
    )

    plan = build_target_label_source_plan()
    output_path = write_target_label_source_plan_report(plan, REPORT_PATH)

    print(f"Generated target label source plan report: {output_path}")
    print(f"Target column: {plan.target_column}")
    print(f"Requirements: {plan.requirement_count}")
    print(f"Candidate sources: {plan.candidate_count}")
    print(f"Sources ready now for real training: {plan.ready_candidate_count}")
    print(f"Real training target ready: {plan.real_training_target_ready}")


if __name__ == "__main__":
    main()
