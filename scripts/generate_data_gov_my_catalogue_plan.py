"""Generate data.gov.my catalogue candidate plan report."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

REPORT_PATH = PROJECT_ROOT / "reports" / "data_gov_my_catalogue_plan.md"


def main() -> None:
    from floodrisk.sources.data_gov_my import (
        build_data_gov_my_catalogue_plan,
        write_data_gov_my_catalogue_plan_report,
    )

    plan = build_data_gov_my_catalogue_plan(PROJECT_ROOT)
    output_path = write_data_gov_my_catalogue_plan_report(plan, REPORT_PATH)

    print(f"Generated data.gov.my catalogue plan report: {output_path}")
    print(f"Source ID: {plan.source_id}")
    print(f"Candidate datasets: {plan.candidate_count}")
    print(f"Target-label candidates: {plan.target_label_candidate_count}")
    print(f"Direct training use allowed: {plan.direct_training_use_allowed}")


if __name__ == "__main__":
    main()
