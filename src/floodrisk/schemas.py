"""Shared data schemas for Malaysia Flood Risk AI."""

from typing import Literal

from pydantic import BaseModel, Field, model_validator

from floodrisk.data.validation import (
    is_coordinate_in_malaysia_bbox,
    malaysia_coordinate_error,
)


WaterLevelStatus = Literal["unknown", "normal", "alert", "warning", "danger"]
WeatherWarningStatus = Literal["none", "advisory", "warning", "severe"]


class FloodRiskInput(BaseModel):
    """Input features for transparent rule-based flood risk scoring."""

    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    elevation_m: float = Field(..., ge=-20, le=5000)
    slope_deg: float = Field(..., ge=0, le=90)
    river_distance_m: float = Field(..., ge=0)
    historical_flood_distance_m: float = Field(..., ge=0)

    rainfall_24h_mm: float = Field(default=0, ge=0)
    rainfall_72h_mm: float = Field(default=0, ge=0)

    water_level_status: WaterLevelStatus = "unknown"
    weather_warning_status: WeatherWarningStatus = "none"

    land_cover_class: str = "unknown"
    population_density_per_km2: float = Field(default=0, ge=0)

    @model_validator(mode="after")
    def validate_malaysia_coordinate(self) -> "FloodRiskInput":
        if not is_coordinate_in_malaysia_bbox(self.latitude, self.longitude):
            raise ValueError(malaysia_coordinate_error(self.latitude, self.longitude))
        return self


class RiskFactor(BaseModel):
    name: str
    score: float = Field(..., ge=0, le=1)
    explanation: str


class FloodRiskOutput(BaseModel):
    risk_score: float = Field(..., ge=0, le=100)
    risk_class: str
    confidence: str
    factors: list[RiskFactor]
    recommendation: str
    disclaimer: str
