"""Display latest local weather risk summary status."""

from __future__ import annotations

import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))


SUMMARY_PATH = PROJECT_ROOT / "reports" / "weather_risk_signal_summary.json"


def main() -> None:
    from floodrisk.data.weather_summary import build_weather_summary_status

    status = build_weather_summary_status(SUMMARY_PATH)

    print(json.dumps(status, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
