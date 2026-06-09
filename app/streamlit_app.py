"""Streamlit web app for Malaysia Flood Risk AI."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.risk_engine import calculate_risk
from floodrisk.schemas import FloodRiskInput


st.set_page_config(
    page_title="Malaysia Flood Risk AI",
    page_icon="🌊",
    layout="wide",
)

st.title("🌊 Malaysia Flood Risk AI")
st.caption(
    "Research MVP for estimating location-based flood risk using transparent "
    "geospatial, rainfall, hydrology, and exposure features."
)

with st.sidebar:
    st.header("About")
    st.write(
        "This prototype estimates flood risk using a transparent scoring engine. "
        "Future versions will integrate real geospatial datasets, rainfall APIs, "
        "water-level stations, and machine-learning models."
    )

    st.warning(
        "Research use only. Always follow official Malaysian flood warnings "
        "and emergency instructions."
    )

st.subheader("Location and flood-risk features")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input("Latitude", value=3.1390, format="%.6f")
    longitude = st.number_input("Longitude", value=101.6869, format="%.6f")
    elevation_m = st.number_input("Elevation (m)", min_value=-20.0, value=30.0)
    slope_deg = st.number_input("Slope (degrees)", min_value=0.0, max_value=90.0, value=2.0)
    river_distance_m = st.number_input("Distance to nearest river (m)", min_value=0.0, value=500.0)

with col2:
    historical_flood_distance_m = st.number_input(
        "Distance to nearest historical flood area (m)",
        min_value=0.0,
        value=1200.0,
    )
    rainfall_24h_mm = st.number_input("Rainfall last 24 hours (mm)", min_value=0.0, value=80.0)
    rainfall_72h_mm = st.number_input("Rainfall last 72 hours (mm)", min_value=0.0, value=160.0)
    population_density_per_km2 = st.number_input(
        "Population density (people/km²)",
        min_value=0.0,
        value=7000.0,
    )

col3, col4, col5 = st.columns(3)

with col3:
    water_level_status = st.selectbox(
        "Water level status",
        ["unknown", "normal", "alert", "warning", "danger"],
        index=3,
    )

with col4:
    weather_warning_status = st.selectbox(
        "Weather warning status",
        ["none", "advisory", "warning", "severe"],
        index=2,
    )

with col5:
    land_cover_class = st.selectbox(
        "Land cover class",
        [
            "unknown",
            "urban",
            "built_up",
            "water",
            "wetland",
            "cropland",
            "agriculture",
            "grassland",
            "forest",
            "bare",
        ],
        index=1,
    )

payload = FloodRiskInput(
    latitude=latitude,
    longitude=longitude,
    elevation_m=elevation_m,
    slope_deg=slope_deg,
    river_distance_m=river_distance_m,
    historical_flood_distance_m=historical_flood_distance_m,
    rainfall_24h_mm=rainfall_24h_mm,
    rainfall_72h_mm=rainfall_72h_mm,
    water_level_status=water_level_status,
    weather_warning_status=weather_warning_status,
    land_cover_class=land_cover_class,
    population_density_per_km2=population_density_per_km2,
)

result = calculate_risk(payload)

st.divider()

metric_col1, metric_col2, metric_col3 = st.columns(3)

with metric_col1:
    st.metric("Risk Score", f"{result.risk_score:.2f} / 100")

with metric_col2:
    st.metric("Risk Class", result.risk_class)

with metric_col3:
    st.metric("Confidence", result.confidence)

if result.risk_class in ["High", "Very High"]:
    st.error(result.recommendation)
elif result.risk_class == "Moderate":
    st.warning(result.recommendation)
else:
    st.success(result.recommendation)

st.subheader("Top risk factors")

factors_df = pd.DataFrame(
    [
        {
            "Factor": factor.name,
            "Score": factor.score,
            "Explanation": factor.explanation,
        }
        for factor in result.factors
    ]
)

st.dataframe(factors_df, use_container_width=True, hide_index=True)

st.bar_chart(
    factors_df.set_index("Factor")["Score"],
    use_container_width=True,
)

st.subheader("Location preview")

map_df = pd.DataFrame(
    {
        "lat": [latitude],
        "lon": [longitude],
    }
)

st.map(map_df, latitude="lat", longitude="lon", zoom=10)

with st.expander("JSON output"):
    st.json(result.model_dump())

st.caption(result.disclaimer)
