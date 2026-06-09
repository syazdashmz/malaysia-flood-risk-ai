import pytest
from pydantic import ValidationError

from floodrisk.data.validation import is_coordinate_in_malaysia_bbox
from floodrisk.schemas import FloodRiskInput


def valid_payload(latitude: float = 3.139, longitude: float = 101.6869) -> dict:
    return {
        "latitude": latitude,
        "longitude": longitude,
        "elevation_m": 30,
        "slope_deg": 2,
        "river_distance_m": 500,
        "historical_flood_distance_m": 1200,
        "rainfall_24h_mm": 80,
        "rainfall_72h_mm": 160,
        "water_level_status": "warning",
        "weather_warning_status": "warning",
        "land_cover_class": "urban",
        "population_density_per_km2": 7000,
    }


def test_malaysia_coordinate_bbox_accepts_kuala_lumpur():
    assert is_coordinate_in_malaysia_bbox(3.139, 101.6869)


def test_malaysia_coordinate_bbox_rejects_outside_location():
    assert not is_coordinate_in_malaysia_bbox(49.3198, 6.3722)


def test_flood_risk_input_rejects_coordinate_outside_malaysia():
    with pytest.raises(ValidationError):
        FloodRiskInput(**valid_payload(latitude=49.3198, longitude=6.3722))
