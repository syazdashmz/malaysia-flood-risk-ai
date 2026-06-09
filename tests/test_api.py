from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_predict_endpoint():
    payload = {
        "latitude": 3.139,
        "longitude": 101.6869,
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

    response = client.post("/predict", json=payload)

    assert response.status_code == 200
    data = response.json()
    assert 0 <= data["risk_score"] <= 100
    assert data["risk_class"] in ["Very Low", "Low", "Moderate", "High", "Very High"]
    assert len(data["factors"]) == 10


def test_predict_endpoint_rejects_coordinate_outside_malaysia():
    payload = {
        "latitude": 49.3198,
        "longitude": 6.3722,
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

    response = client.post("/predict", json=payload)

    assert response.status_code == 422
