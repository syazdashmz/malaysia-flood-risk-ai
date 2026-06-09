"""FastAPI backend for Malaysia Flood Risk AI."""

from fastapi import FastAPI

from floodrisk.risk_engine import calculate_risk
from floodrisk.schemas import FloodRiskInput, FloodRiskOutput

app = FastAPI(
    title="Malaysia Flood Risk AI API",
    description=(
        "Research API for estimating Malaysia flood risk using transparent "
        "geospatial, rainfall, hydrology, and exposure features."
    ),
    version="0.1.0",
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


@app.post("/predict", response_model=FloodRiskOutput)
def predict(payload: FloodRiskInput) -> FloodRiskOutput:
    return calculate_risk(payload)
