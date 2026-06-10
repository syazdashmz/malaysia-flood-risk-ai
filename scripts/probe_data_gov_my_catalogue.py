"""Run sample-only data.gov.my catalogue candidate probe."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

JSON_OUTPUT_PATH = (
    PROJECT_ROOT / "data" / "interim" / "source_discovery" / "data_gov_my_catalogue_probe.json"
)
REPORT_OUTPUT_PATH = PROJECT_ROOT / "reports" / "data_gov_my_catalogue_probe_report.md"


def main() -> None:
    from floodrisk.sources.data_gov_my import (
        probe_data_gov_my_catalogue_candidates,
        write_data_gov_my_catalogue_probe_outputs,
    )

    summary = probe_data_gov_my_catalogue_candidates(PROJECT_ROOT)
    json_path, report_path = write_data_gov_my_catalogue_probe_outputs(
        summary,
        json_output_path=JSON_OUTPUT_PATH,
        report_output_path=REPORT_OUTPUT_PATH,
    )

    print(f"Generated data.gov.my catalogue probe JSON: {json_path}")
    print(f"Generated data.gov.my catalogue probe report: {report_path}")
    print(f"Candidate datasets: {summary.candidate_count}")
    print(f"Successful probes: {summary.successful_probes}")
    print(f"Failed probes: {summary.failed_probes}")
    print(f"Direct training use allowed: {summary.direct_training_use_allowed}")


if __name__ == "__main__":
    main()
