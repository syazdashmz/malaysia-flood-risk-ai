"""Malaysia administrative coverage reference helpers."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

PROJECT_ROOT = Path(__file__).resolve().parents[3]
COVERAGE_PATH = PROJECT_ROOT / "data" / "reference" / "malaysia_admin_coverage.json"

EXPECTED_REGION_NAMES = {
    "Johor",
    "Kedah",
    "Kelantan",
    "Melaka",
    "Negeri Sembilan",
    "Pahang",
    "Perak",
    "Perlis",
    "Pulau Pinang",
    "Sabah",
    "Sarawak",
    "Selangor",
    "Terengganu",
    "Kuala Lumpur",
    "Labuan",
    "Putrajaya",
}


def load_malaysia_admin_coverage(path: Path = COVERAGE_PATH) -> dict[str, Any]:
    """Load Malaysia state and federal territory coverage metadata."""
    return json.loads(path.read_text(encoding="utf-8"))


def get_covered_region_names(path: Path = COVERAGE_PATH) -> list[str]:
    """Return sorted Malaysia region names covered by the project."""
    coverage = load_malaysia_admin_coverage(path)
    return sorted(region["name"] for region in coverage["regions"])


def validate_malaysia_admin_coverage(path: Path = COVERAGE_PATH) -> dict[str, Any]:
    """Validate that all top-level Malaysian regions are represented."""
    coverage = load_malaysia_admin_coverage(path)
    region_names = set(get_covered_region_names(path))

    missing_regions = sorted(EXPECTED_REGION_NAMES - region_names)
    extra_regions = sorted(region_names - EXPECTED_REGION_NAMES)

    state_count = sum(region["type"] == "state" for region in coverage["regions"])
    federal_territory_count = sum(
        region["type"] == "federal_territory" for region in coverage["regions"]
    )

    return {
        "country": coverage["country"],
        "coverage_level": coverage["coverage_level"],
        "total_regions": len(region_names),
        "state_count": state_count,
        "federal_territory_count": federal_territory_count,
        "missing_regions": missing_regions,
        "extra_regions": extra_regions,
        "is_complete": not missing_regions
        and not extra_regions
        and state_count == 13
        and federal_territory_count == 3,
    }
