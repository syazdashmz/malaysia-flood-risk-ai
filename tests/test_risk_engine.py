from floodrisk.risk_engine import calculate_risk
from floodrisk.schemas import FloodRiskInput


def test_calculate_risk_returns_valid_output():
    data = FloodRiskInput(
        latitude=3.139,
        longitude=101.6869,
        elevation_m=30,
        slope_deg=2,
        river_distance_m=500,
        historical_flood_distance_m=1200,
        rainfall_24h_mm=80,
        rainfall_72h_mm=160,
        water_level_status="warning",
        weather_warning_status="warning",
        land_cover_class="urban",
        population_density_per_km2=7000,
    )

    result = calculate_risk(data)

    assert 0 <= result.risk_score <= 100
    assert result.risk_class in ["Very Low", "Low", "Moderate", "High", "Very High"]
    assert len(result.factors) == 10
    assert result.recommendation
    assert result.disclaimer
