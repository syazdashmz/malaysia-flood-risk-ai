import json
from pathlib import Path

REGISTRY_PATH = Path("data/reference/infobanjir_state_sources.json")


def load_registry():
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8"))


def test_infobanjir_state_source_registry_exists():
    assert REGISTRY_PATH.exists()


def test_infobanjir_state_source_registry_has_16_project_regions():
    registry = load_registry()

    assert registry["source_id"] == "public_infobanjir_state_sources"
    assert len(registry["regions"]) == 16


def test_infobanjir_state_source_registry_has_16_public_station_regions():
    registry = load_registry()

    available_regions = [
        region for region in registry["regions"] if region["station_data_available"]
    ]

    assert len(available_regions) == 16
    assert all(region["water_level_url"] for region in available_regions)
    assert all(region["rainfall_url"] for region in available_regions)


def test_infobanjir_state_source_registry_corrects_pulau_pinang_code():
    registry = load_registry()

    pulau_pinang = next(
        region for region in registry["regions"] if region["name"] == "Pulau Pinang"
    )

    assert pulau_pinang["code"] == "PNG"
    assert "state=PNG" in pulau_pinang["water_level_url"]
    assert "state=PNG" in pulau_pinang["rainfall_url"]


def test_infobanjir_state_source_registry_marks_putrajaya_code_from_site():
    registry = load_registry()

    putrajaya = next(region for region in registry["regions"] if region["name"] == "Putrajaya")

    assert putrajaya["station_data_available"] is True
    assert putrajaya["code"] == "PTJ"
    assert "state=PTJ" in putrajaya["water_level_url"]
    assert "state=PTJ" in putrajaya["rainfall_url"]
