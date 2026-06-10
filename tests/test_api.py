from api.main import app
from fastapi.testclient import TestClient

client = TestClient(app)


def test_health_endpoint():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_weather_summary_endpoint():
    response = client.get("/weather/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is True
    assert data["risk_engine_weather_warning"] in [
        "none",
        "advisory",
        "warning",
        "severe",
    ]
    assert "record_count" in data
    assert "signal_counts" in data


def test_geospatial_summary_endpoint():
    response = client.get("/geospatial/summary")

    assert response.status_code == 200

    data = response.json()

    assert data["available"] is True
    assert data["planned_artifact_count"] == 3
    assert data["available_artifact_count"] == 0
    assert data["missing_artifact_count"] == 3
    assert data["valid_vector_count"] == 0
    assert data["has_available_boundary_data"] is False
    assert len(data["artifact_statuses"]) == 3
    assert data["artifact_statuses"][0]["dataset_id"] == "malaysia_admin_boundary"


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
