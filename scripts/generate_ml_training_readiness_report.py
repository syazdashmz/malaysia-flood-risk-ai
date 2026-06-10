"""Generate combined ML training readiness gate report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "ml_training_readiness_report.md"


def main() -> None:
    from floodrisk.ml.training_readiness import (
        build_ml_training_readiness_summary,
        write_ml_training_readiness_report,
    )

    summary = build_ml_training_readiness_summary(PROJECT_ROOT)
    output_path = write_ml_training_readiness_report(summary, REPORT_PATH)

    print(f"Generated ML training readiness report: {output_path}")
    print(f"Target ready: {summary.target_ready}")
    print(f"Training table ready: {summary.training_table_ready}")
    print(f"Real ML training ready: {summary.real_ml_training_ready}")
    print(f"Blockers: {len(summary.blockers)}")


if __name__ == "__main__":
    main()
