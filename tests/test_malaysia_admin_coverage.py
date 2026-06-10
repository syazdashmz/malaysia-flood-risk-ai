from pathlib import Path

from floodrisk.sources.malaysia_admin import (
    EXPECTED_REGION_NAMES,
    get_covered_region_names,
    load_malaysia_admin_coverage,
    validate_malaysia_admin_coverage,
)

COVERAGE_PATH = Path("data/reference/malaysia_admin_coverage.json")


def test_malaysia_admin_coverage_file_exists():
    assert COVERAGE_PATH.exists()


def test_malaysia_admin_coverage_has_all_regions():
    coverage = load_malaysia_admin_coverage(COVERAGE_PATH)
    region_names = {region["name"] for region in coverage["regions"]}

    assert coverage["country"] == "Malaysia"
    assert coverage["total_regions"] == 16
    assert region_names == EXPECTED_REGION_NAMES


def test_malaysia_admin_coverage_has_13_states_and_3_federal_territories():
    validation = validate_malaysia_admin_coverage(COVERAGE_PATH)

    assert validation["state_count"] == 13
    assert validation["federal_territory_count"] == 3
    assert validation["missing_regions"] == []
    assert validation["extra_regions"] == []
    assert validation["is_complete"] is True


def test_malaysia_admin_coverage_has_coordinates_and_hazard_context():
    coverage = load_malaysia_admin_coverage(COVERAGE_PATH)

    for region in coverage["regions"]:
        assert isinstance(region["latitude"], float)
        assert isinstance(region["longitude"], float)
        assert region["priority_hazards"]
        assert region["region_group"] in {
            "Peninsular Malaysia",
            "East Malaysia",
        }


def test_get_covered_region_names_returns_sorted_names():
    names = get_covered_region_names(COVERAGE_PATH)

    assert names == sorted(EXPECTED_REGION_NAMES)
    assert "Selangor" in names
    assert "Sabah" in names
    assert "Sarawak" in names
    assert "Putrajaya" in names
