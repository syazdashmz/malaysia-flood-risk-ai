"""Create a small sample Malaysia flood-risk dataset.

This sample dataset is used only for local testing, demos, and app/API validation.
It is not a real trained research dataset.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from floodrisk.risk_engine import calculate_risk
from floodrisk.schemas import FloodRiskInput


PROJECT_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_PATH = PROJECT_ROOT / "data" / "samples" / "sample_malaysia_locations.csv"


SAMPLE_LOCATIONS = [
    {
        "location_name": "Kuala Lumpur City Centre",
        "state": "Kuala Lumpur",
        "latitude": 3.1579,
        "longitude": 101.7123,
        "elevation_m": 35,
        "slope_deg": 2,
        "river_distance_m": 450,
        "historical_flood_distance_m": 1200,
        "rainfall_24h_mm": 80,
        "rainfall_72h_mm": 160,
        "water_level_status": "warning",
        "weather_warning_status": "warning",
        "land_cover_class": "urban",
        "population_density_per_km2": 7500,
    },
    {
        "location_name": "Shah Alam",
        "state": "Selangor",
        "latitude": 3.0738,
        "longitude": 101.5183,
        "elevation_m": 25,
        "slope_deg": 1.5,
        "river_distance_m": 700,
        "historical_flood_distance_m": 900,
        "rainfall_24h_mm": 95,
        "rainfall_72h_mm": 190,
        "water_level_status": "warning",
        "weather_warning_status": "warning",
        "land_cover_class": "urban",
        "population_density_per_km2": 4200,
    },
    {
        "location_name": "Kota Bharu",
        "state": "Kelantan",
        "latitude": 6.1254,
        "longitude": 102.2381,
        "elevation_m": 8,
        "slope_deg": 0.8,
        "river_distance_m": 350,
        "historical_flood_distance_m": 500,
        "rainfall_24h_mm": 120,
        "rainfall_72h_mm": 260,
        "water_level_status": "danger",
        "weather_warning_status": "severe",
        "land_cover_class": "urban",
        "population_density_per_km2": 1800,
    },
    {
        "location_name": "Kuantan",
        "state": "Pahang",
        "latitude": 3.8077,
        "longitude": 103.3260,
        "elevation_m": 15,
        "slope_deg": 1.2,
        "river_distance_m": 600,
        "historical_flood_distance_m": 800,
        "rainfall_24h_mm": 110,
        "rainfall_72h_mm": 240,
        "water_level_status": "warning",
        "weather_warning_status": "warning",
        "land_cover_class": "built_up",
        "population_density_per_km2": 900,
    },
    {
        "location_name": "Cyberjaya",
        "state": "Selangor",
        "latitude": 2.9225,
        "longitude": 101.6550,
        "elevation_m": 45,
        "slope_deg": 3,
        "river_distance_m": 1800,
        "historical_flood_distance_m": 3500,
        "rainfall_24h_mm": 45,
        "rainfall_72h_mm": 90,
        "water_level_status": "normal",
        "weather_warning_status": "advisory",
        "land_cover_class": "urban",
        "population_density_per_km2": 1400,
    },
    {
        "location_name": "Cameron Highlands",
        "state": "Pahang",
        "latitude": 4.4721,
        "longitude": 101.3801,
        "elevation_m": 1450,
        "slope_deg": 18,
        "river_distance_m": 2500,
        "historical_flood_distance_m": 9000,
        "rainfall_24h_mm": 25,
        "rainfall_72h_mm": 70,
        "water_level_status": "normal",
        "weather_warning_status": "none",
        "land_cover_class": "forest",
        "population_density_per_km2": 120,
    },
]


def build_sample_dataset() -> pd.DataFrame:
    rows = []

    for row in SAMPLE_LOCATIONS:
        risk_input = FloodRiskInput(
            latitude=row["latitude"],
            longitude=row["longitude"],
            elevation_m=row["elevation_m"],
            slope_deg=row["slope_deg"],
            river_distance_m=row["river_distance_m"],
            historical_flood_distance_m=row["historical_flood_distance_m"],
            rainfall_24h_mm=row["rainfall_24h_mm"],
            rainfall_72h_mm=row["rainfall_72h_mm"],
            water_level_status=row["water_level_status"],
            weather_warning_status=row["weather_warning_status"],
            land_cover_class=row["land_cover_class"],
            population_density_per_km2=row["population_density_per_km2"],
        )

        result = calculate_risk(risk_input)

        rows.append(
            {
                **row,
                "risk_score": result.risk_score,
                "risk_class": result.risk_class,
                "confidence": result.confidence,
            }
        )

    return pd.DataFrame(rows)


def save_sample_dataset(output_path: Path = OUTPUT_PATH) -> Path:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataset = build_sample_dataset()
    dataset.to_csv(output_path, index=False)
    return output_path


if __name__ == "__main__":
    path = save_sample_dataset()
    print(f"Sample dataset saved to: {path}")
