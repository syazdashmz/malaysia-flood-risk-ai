"""Generate ReliefWeb discovery plan report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "reliefweb_discovery_plan.md"


def main() -> None:
    from floodrisk.sources.reliefweb import (
        build_reliefweb_discovery_plan,
        write_reliefweb_discovery_plan_report,
    )

    plan = build_reliefweb_discovery_plan(PROJECT_ROOT)
    output_path = write_reliefweb_discovery_plan_report(plan, REPORT_PATH)

    print(f"Generated ReliefWeb discovery plan report: {output_path}")
    print(f"Source ID: {plan.source_id}")
    print(f"Query count: {plan.query_count}")
    print(f"Direct training use allowed: {plan.direct_training_use_allowed}")


if __name__ == "__main__":
    main()
