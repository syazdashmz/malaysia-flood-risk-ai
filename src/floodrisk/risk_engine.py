"""Transparent flood-risk scoring engine.

This is the first MVP risk engine. It is intentionally explainable and simple.
Later, this will become the baseline compared against ML models.
"""

from __future__ import annotations

from floodrisk.schemas import FloodRiskInput, FloodRiskOutput, RiskFactor

LAND_COVER_RISK = {
    "urban": 0.75,
    "built_up": 0.75,
    "water": 0.90,
    "wetland": 0.85,
    "cropland": 0.55,
    "agriculture": 0.55,
    "grassland": 0.40,
    "forest": 0.25,
    "bare": 0.45,
    "unknown": 0.50,
}

WATER_LEVEL_RISK = {
    "unknown": 0.30,
    "normal": 0.10,
    "alert": 0.45,
    "warning": 0.75,
    "danger": 1.00,
}

WEATHER_WARNING_RISK = {
    "none": 0.10,
    "advisory": 0.40,
    "warning": 0.75,
    "severe": 1.00,
}


def clamp(value: float, minimum: float = 0.0, maximum: float = 1.0) -> float:
    return max(minimum, min(value, maximum))


def normalize_positive(value: float, high_value: float) -> float:
    return clamp(value / high_value)


def normalize_inverse_distance(distance_m: float, high_distance_m: float) -> float:
    return clamp(1.0 - (distance_m / high_distance_m))


def classify_risk(score: float) -> str:
    if score < 20:
        return "Very Low"
    if score < 40:
        return "Low"
    if score < 60:
        return "Moderate"
    if score < 80:
        return "High"
    return "Very High"


def confidence_level(data: FloodRiskInput) -> str:
    dynamic_signals = [
        data.rainfall_24h_mm > 0,
        data.rainfall_72h_mm > 0,
        data.water_level_status != "unknown",
        data.weather_warning_status != "none",
    ]
    count = sum(dynamic_signals)

    if count >= 3:
        return "High"
    if count >= 1:
        return "Medium"
    return "Low"


def recommendation_for(risk_class: str) -> str:
    recommendations = {
        "Very Low": "Flood risk appears very low. Continue normal monitoring.",
        "Low": "Flood risk appears low. Stay aware of local weather updates.",
        "Moderate": "Monitor weather and nearby river conditions. Prepare basic precautions.",
        "High": "Prepare for possible flooding. Avoid low-lying roads and monitor official alerts.",
        "Very High": "Take immediate precautions. Follow official flood warnings and evacuation guidance.",
    }
    return recommendations[risk_class]


def calculate_risk(data: FloodRiskInput) -> FloodRiskOutput:
    elevation_risk = clamp(1.0 - (data.elevation_m / 300.0))
    slope_risk = clamp(1.0 - (data.slope_deg / 15.0))
    river_risk = normalize_inverse_distance(data.river_distance_m, 5000.0)
    historical_risk = normalize_inverse_distance(data.historical_flood_distance_m, 10000.0)
    rainfall_24h_risk = normalize_positive(data.rainfall_24h_mm, 150.0)
    rainfall_72h_risk = normalize_positive(data.rainfall_72h_mm, 300.0)
    water_level_risk = WATER_LEVEL_RISK[data.water_level_status]
    weather_warning_risk = WEATHER_WARNING_RISK[data.weather_warning_status]
    land_cover_risk = LAND_COVER_RISK.get(data.land_cover_class.lower(), LAND_COVER_RISK["unknown"])
    exposure_risk = normalize_positive(data.population_density_per_km2, 8000.0)

    weighted_score = (
        elevation_risk * 0.12
        + slope_risk * 0.08
        + river_risk * 0.14
        + historical_risk * 0.12
        + rainfall_24h_risk * 0.16
        + rainfall_72h_risk * 0.10
        + water_level_risk * 0.12
        + weather_warning_risk * 0.08
        + land_cover_risk * 0.05
        + exposure_risk * 0.03
    )

    risk_score = round(weighted_score * 100, 2)
    risk_class = classify_risk(risk_score)

    factors = [
        RiskFactor(
            name="Elevation",
            score=round(elevation_risk, 3),
            explanation=f"Lower elevation increases flood susceptibility. Input: {data.elevation_m} m.",
        ),
        RiskFactor(
            name="Slope",
            score=round(slope_risk, 3),
            explanation=f"Flatter areas drain slower. Input slope: {data.slope_deg} degrees.",
        ),
        RiskFactor(
            name="River proximity",
            score=round(river_risk, 3),
            explanation=f"Closer distance to rivers increases flood exposure. Input: {data.river_distance_m} m.",
        ),
        RiskFactor(
            name="Historical flood proximity",
            score=round(historical_risk, 3),
            explanation=(
                "Nearby historical flood locations indicate recurring local susceptibility. "
                f"Input: {data.historical_flood_distance_m} m."
            ),
        ),
        RiskFactor(
            name="24-hour rainfall",
            score=round(rainfall_24h_risk, 3),
            explanation=f"Higher recent rainfall increases near-term flood hazard. Input: {data.rainfall_24h_mm} mm.",
        ),
        RiskFactor(
            name="72-hour rainfall",
            score=round(rainfall_72h_risk, 3),
            explanation=f"Accumulated rainfall can saturate soil and drainage systems. Input: {data.rainfall_72h_mm} mm.",
        ),
        RiskFactor(
            name="Water level status",
            score=round(water_level_risk, 3),
            explanation=f"Official or nearby water-level status: {data.water_level_status}.",
        ),
        RiskFactor(
            name="Weather warning",
            score=round(weather_warning_risk, 3),
            explanation=f"Weather warning status: {data.weather_warning_status}.",
        ),
        RiskFactor(
            name="Land cover",
            score=round(land_cover_risk, 3),
            explanation=f"Land cover affects runoff and drainage. Input: {data.land_cover_class}.",
        ),
        RiskFactor(
            name="Population exposure",
            score=round(exposure_risk, 3),
            explanation=(
                "Higher population density increases potential impact. "
                f"Input: {data.population_density_per_km2} people/km²."
            ),
        ),
    ]

    factors = sorted(factors, key=lambda factor: factor.score, reverse=True)

    return FloodRiskOutput(
        risk_score=risk_score,
        risk_class=risk_class,
        confidence=confidence_level(data),
        factors=factors,
        recommendation=recommendation_for(risk_class),
        disclaimer=(
            "This result is for research and public awareness only. "
            "Always follow official Malaysian flood warnings and emergency instructions."
        ),
    )
