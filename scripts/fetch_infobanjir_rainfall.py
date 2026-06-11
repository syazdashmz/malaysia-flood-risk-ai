"""Fetch Public InfoBanjir rainfall records."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_DIR = PROJECT_ROOT / "src"

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from floodrisk.data.infobanjir_rainfall import (  # noqa: E402
    fetch_rainfall_records_for_state,
    rainfall_records_to_dicts,
    save_json,
    summarize_rainfall_records,
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Fetch Public InfoBanjir rainfall records.")
    parser.add_argument("--state-code", required=True, help="InfoBanjir state code.")
    parser.add_argument("--state-name", required=True, help="Human-readable state name.")
    parser.add_argument(
        "--output",
        default="data/processed/infobanjir/rainfall_latest.json",
        help="Output JSON file path.",
    )
    parser.add_argument(
        "--summary-output",
        default="reports/infobanjir_rainfall_summary.json",
        help="Summary JSON file path.",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=30,
        help="HTTP request timeout in seconds.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    records = fetch_rainfall_records_for_state(
        state_code=args.state_code,
        state_name=args.state_name,
        timeout_seconds=args.timeout_seconds,
    )

    output_path = save_json(
        rainfall_records_to_dicts(records),
        Path(args.output),
    )
    summary_path = save_json(
        summarize_rainfall_records(records),
        Path(args.summary_output),
    )

    print(f"Saved {len(records)} rainfall records to {output_path}")
    print(f"Saved rainfall summary to {summary_path}")
    print(summarize_rainfall_records(records))


if __name__ == "__main__":
    main()
