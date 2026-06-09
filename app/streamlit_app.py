"""Streamlit web app for Malaysia Flood Risk AI."""

from __future__ import annotations

import sys
from pathlib import Path

import pandas as pd
import streamlit as st
from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "samples" / "sample_malaysia_locations.csv"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.risk_engine import calculate_risk
from floodrisk.schemas import FloodRiskInput


def load_sample_locations() -> pd.DataFrame:
    if SAMPLE_DATA_PATH.exists():
        return pd.read_csv(SAMPLE_DATA_PATH)
    return pd.DataFrame()


def get_sample_value(row: pd.Series | None, column: str, default):
    if row is None:
        return default
    value = row.get(column, default)
    if pd.isna(value):
        return default
    return value


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

samples_df = load_sample_locations()

st.subheader("Sample location preset")

selected_sample_row = None

if samples_df.empty:
    st.info("No sample dataset found. Using manual input mode.")
    selected_sample_name = "Custom manual input"
else:
    sample_options = ["Custom manual input"] + samples_df["location_name"].tolist()
    selected_sample_name = st.selectbox("Choose a sample Malaysia location", sample_options)

    if selected_sample_name != "Custom manual input":
        selected_sample_row = samples_df.loc[
            samples_df["location_name"] == selected_sample_name
        ].iloc[0]
        st.info(
            f"Loaded sample preset: {selected_sample_row['location_name']}, "
            f"{selected_sample_row['state']}"
        )

widget_suffix = selected_sample_name.replace(" ", "_").replace(",", "").lower()

st.subheader("Location and flood-risk features")

col1, col2 = st.columns(2)

with col1:
    latitude = st.number_input(
        "Latitude",
        value=float(get_sample_value(selected_sample_row, "latitude", 3.1390)),
        format="%.6f",
        key=f"latitude_{widget_suffix}",
    )
    longitude = st.number_input(
        "Longitude",
        value=float(get_sample_value(selected_sample_row, "longitude", 101.6869)),
        format="%.6f",
        key=f"longitude_{widget_suffix}",
    )
    elevation_m = st.number_input(
        "Elevation (m)",
        min_value=-20.0,
        value=float(get_sample_value(selected_sample_row, "elevation_m", 30.0)),
        key=f"elevation_{widget_suffix}",
    )
    slope_deg = st.number_input(
        "Slope (degrees)",
        min_value=0.0,
        max_value=90.0,
        value=float(get_sample_value(selected_sample_row, "slope_deg", 2.0)),
        key=f"slope_{widget_suffix}",
    )
    river_distance_m = st.number_input(
        "Distance to nearest river (m)",
        min_value=0.0,
        value=float(get_sample_value(selected_sample_row, "river_distance_m", 500.0)),
        key=f"river_distance_{widget_suffix}",
    )

with col2:
    historical_flood_distance_m = st.number_input(
        "Distance to nearest historical flood area (m)",
        min_value=0.0,
        value=float(get_sample_value(selected_sample_row, "historical_flood_distance_m", 1200.0)),
        key=f"historical_flood_distance_{widget_suffix}",
    )
    rainfall_24h_mm = st.number_input(
        "Rainfall last 24 hours (mm)",
        min_value=0.0,
        value=float(get_sample_value(selected_sample_row, "rainfall_24h_mm", 80.0)),
        key=f"rainfall_24h_{widget_suffix}",
    )
    rainfall_72h_mm = st.number_input(
        "Rainfall last 72 hours (mm)",
        min_value=0.0,
        value=float(get_sample_value(selected_sample_row, "rainfall_72h_mm", 160.0)),
        key=f"rainfall_72h_{widget_suffix}",
    )
    population_density_per_km2 = st.number_input(
        "Population density (people/km²)",
        min_value=0.0,
        value=float(get_sample_value(selected_sample_row, "population_density_per_km2", 7000.0)),
        key=f"population_density_{widget_suffix}",
    )

col3, col4, col5 = st.columns(3)

water_level_options = ["unknown", "normal", "alert", "warning", "danger"]
weather_warning_options = ["none", "advisory", "warning", "severe"]
land_cover_options = [
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
]

default_water_status = str(get_sample_value(selected_sample_row, "water_level_status", "warning"))
default_weather_status = str(get_sample_value(selected_sample_row, "weather_warning_status", "warning"))
default_land_cover = str(get_sample_value(selected_sample_row, "land_cover_class", "urban"))

with col3:
    water_level_status = st.selectbox(
        "Water level status",
        water_level_options,
        index=water_level_options.index(default_water_status)
        if default_water_status in water_level_options
        else 0,
        key=f"water_level_{widget_suffix}",
    )

with col4:
    weather_warning_status = st.selectbox(
        "Weather warning status",
        weather_warning_options,
        index=weather_warning_options.index(default_weather_status)
        if default_weather_status in weather_warning_options
        else 0,
        key=f"weather_warning_{widget_suffix}",
    )

with col5:
    land_cover_class = st.selectbox(
        "Land cover class",
        land_cover_options,
        index=land_cover_options.index(default_land_cover)
        if default_land_cover in land_cover_options
        else 0,
        key=f"land_cover_{widget_suffix}",
    )

try:
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
except ValidationError as error:
    st.error("Invalid input. Please make sure the coordinate is inside Malaysia.")
    with st.expander("Validation details"):
        st.json(error.errors())
    st.stop()

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

st.dataframe(factors_df, width="stretch", hide_index=True)

st.bar_chart(
    factors_df.set_index("Factor")["Score"],
    width="stretch",
)

st.subheader("Location preview")

map_df = pd.DataFrame(
    {
        "lat": [latitude],
        "lon": [longitude],
    }
)

st.map(map_df, latitude="lat", longitude="lon", zoom=10)

if not samples_df.empty:
    with st.expander("View sample demo dataset"):
        st.dataframe(samples_df, width="stretch", hide_index=True)

with st.expander("JSON output"):
    st.json(result.model_dump())

st.caption(result.disclaimer)
