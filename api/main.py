"""FastAPI backend for Malaysia Flood Risk AI."""

from pathlib import Path
from typing import Any

from fastapi import FastAPI, HTTPException

from floodrisk.data.weather_summary import build_weather_summary_status
from floodrisk.geospatial.summary import load_geospatial_summary
from floodrisk.ml.experimental_flood_model import (
    load_experimental_model_status,
    predict_experimental_flood,
)
from floodrisk.risk_engine import calculate_risk
from floodrisk.schemas import (
    ExperimentalFloodPredictionInput,
    ExperimentalFloodPredictionOutput,
    FloodRiskInput,
    FloodRiskOutput,
)
from floodrisk.version import __version__

PROJECT_ROOT = Path(__file__).resolve().parents[1]
WEATHER_SUMMARY_PATH = PROJECT_ROOT / "reports" / "weather_risk_signal_summary.json"


app = FastAPI(
    title="Malaysia Flood Risk AI API",
    description=(
        "Research API for estimating Malaysia flood risk using transparent "
        "geospatial, rainfall, hydrology, and exposure features."
    ),
    version=__version__,
)


@app.get("/")
def root() -> dict[str, str]:
    return {
        "name": "Malaysia Flood Risk AI API",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/weather/summary")
def weather_summary() -> dict[str, Any]:
    return build_weather_summary_status(WEATHER_SUMMARY_PATH)


@app.get("/geospatial/summary")
def geospatial_summary() -> dict[str, Any]:
    return load_geospatial_summary(PROJECT_ROOT)


@app.get("/experimental/flood/model/status")
def experimental_flood_model_status() -> dict[str, Any]:
    return load_experimental_model_status(PROJECT_ROOT).as_dict()


@app.post("/experimental/flood/predict", response_model=ExperimentalFloodPredictionOutput)
def experimental_flood_predict(
    payload: ExperimentalFloodPredictionInput,
) -> ExperimentalFloodPredictionOutput:
    try:
        return predict_experimental_flood(payload, PROJECT_ROOT)
    except FileNotFoundError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc


@app.post("/predict", response_model=FloodRiskOutput)
def predict(payload: FloodRiskInput) -> FloodRiskOutput:
    return calculate_risk(payload)
