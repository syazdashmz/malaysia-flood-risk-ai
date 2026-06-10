"""Streamlit web app for Malaysia Flood Risk AI."""

from __future__ import annotations

import json
import sys
from datetime import date
from pathlib import Path
from typing import Any, cast
from urllib.error import URLError
from urllib.request import Request, urlopen

import pandas as pd
import streamlit as st
from pydantic import ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SRC_PATH = PROJECT_ROOT / "src"
SAMPLE_DATA_PATH = PROJECT_ROOT / "data" / "samples" / "sample_malaysia_locations.csv"
WEATHER_SUMMARY_PATH = PROJECT_ROOT / "reports" / "weather_risk_signal_summary.json"
TRAINING_METRICS_PATH = PROJECT_ROOT / "reports" / "kaggle_flood_baseline_training_metrics.json"
THRESHOLD_METRICS_PATH = PROJECT_ROOT / "reports" / "kaggle_flood_threshold_tuning_metrics.json"
BENCHMARK_METRICS_PATH = PROJECT_ROOT / "reports" / "kaggle_flood_model_benchmark_metrics.json"

if str(SRC_PATH) not in sys.path:
    sys.path.insert(0, str(SRC_PATH))

from floodrisk.risk_engine import calculate_risk  # noqa: E402
from floodrisk.schemas import (  # noqa: E402
    FloodRiskInput,
    WaterLevelStatus,
    WeatherWarningStatus,
)
from floodrisk.sources.malaysia_admin import load_malaysia_admin_coverage  # noqa: E402


def load_weather_summary_status() -> dict[str, Any]:
    from floodrisk.data.weather_summary import build_weather_summary_status

    return build_weather_summary_status(WEATHER_SUMMARY_PATH)


def load_geospatial_summary_status() -> dict[str, Any]:
    from floodrisk.geospatial.summary import load_geospatial_summary

    return load_geospatial_summary(PROJECT_ROOT)


def load_experimental_model_status() -> dict[str, Any]:
    from floodrisk.ml.experimental_flood_model import load_experimental_model_status

    return load_experimental_model_status(PROJECT_ROOT).as_dict()


def load_sample_locations() -> pd.DataFrame:
    if SAMPLE_DATA_PATH.exists():
        return pd.read_csv(SAMPLE_DATA_PATH)
    return pd.DataFrame()


def load_admin_regions_df() -> pd.DataFrame:
    coverage = load_malaysia_admin_coverage()

    rows = []
    for region in coverage["regions"]:
        rows.append(
            {
                "location_name": (
                    f"{region['name']} overview ({region['capital_or_admin_centre']})"
                ),
                "state": region["name"],
                "latitude": region["latitude"],
                "longitude": region["longitude"],
                "elevation_m": 30.0,
                "slope_deg": 2.0,
                "river_distance_m": 750.0,
                "historical_flood_distance_m": 1500.0,
                "rainfall_24h_mm": 60.0,
                "rainfall_72h_mm": 120.0,
                "water_level_status": "unknown",
                "weather_warning_status": "advisory",
                "land_cover_class": "urban",
                "population_density_per_km2": 3000.0,
                "source_type": "admin_region_fallback",
                "region_group": region["region_group"],
                "priority_hazards": ", ".join(region["priority_hazards"]),
            }
        )

    return pd.DataFrame(rows)


def build_public_location_catalog(
    samples_df: pd.DataFrame,
    admin_regions_df: pd.DataFrame,
) -> pd.DataFrame:
    catalog_parts = []

    if not admin_regions_df.empty:
        catalog_parts.append(admin_regions_df)

    if not samples_df.empty:
        enriched_samples = samples_df.copy()
        enriched_samples["source_type"] = "sample_location"
        enriched_samples["region_group"] = "Sample location"
        enriched_samples["priority_hazards"] = "sample-specific flood risk profile"
        catalog_parts.append(enriched_samples)

    if not catalog_parts:
        return pd.DataFrame()

    return pd.concat(catalog_parts, ignore_index=True)


def load_json_report(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {"available": False, "path": str(path.relative_to(PROJECT_ROOT))}

    return {
        "available": True,
        "path": str(path.relative_to(PROJECT_ROOT)),
        "data": json.loads(path.read_text(encoding="utf-8")),
    }


def get_sample_value(row: pd.Series | None, column: str, default: Any) -> Any:
    if row is None:
        return default

    value = row.get(column, default)
    if pd.isna(value):
        return default

    return value


def option_index(options: list[str], value: str) -> int:
    if value in options:
        return options.index(value)
    return 0


def metric_percent(value: Any) -> str:
    if value is None:
        return "n/a"
    return f"{float(value) * 100:.2f}%"


def api_get_json(url: str) -> dict[str, Any]:
    with urlopen(url, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def api_post_json(url: str, payload: dict[str, Any]) -> dict[str, Any]:
    body = json.dumps(payload).encode("utf-8")
    request = Request(
        url,
        data=body,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urlopen(request, timeout=5) as response:
        return json.loads(response.read().decode("utf-8"))


def resolve_weather_status(
    selected_sample_row: pd.Series | None,
    weather_summary_status: dict[str, Any],
    use_latest_weather_signal: bool,
) -> str:
    sample_default = str(get_sample_value(selected_sample_row, "weather_warning_status", "warning"))

    if use_latest_weather_signal and weather_summary_status.get("available"):
        return str(
            weather_summary_status.get(
                "risk_engine_weather_warning",
                sample_default,
            )
        )

    return sample_default


def build_risk_input_from_sample(
    selected_sample_row: pd.Series | None,
    weather_summary_status: dict[str, Any],
    use_latest_weather_signal: bool,
) -> FloodRiskInput:
    water_level_status = str(get_sample_value(selected_sample_row, "water_level_status", "warning"))
    weather_warning_status = resolve_weather_status(
        selected_sample_row,
        weather_summary_status,
        use_latest_weather_signal,
    )

    return FloodRiskInput(
        latitude=float(get_sample_value(selected_sample_row, "latitude", 3.1390)),
        longitude=float(get_sample_value(selected_sample_row, "longitude", 101.6869)),
        elevation_m=float(get_sample_value(selected_sample_row, "elevation_m", 30.0)),
        slope_deg=float(get_sample_value(selected_sample_row, "slope_deg", 2.0)),
        river_distance_m=float(get_sample_value(selected_sample_row, "river_distance_m", 500.0)),
        historical_flood_distance_m=float(
            get_sample_value(selected_sample_row, "historical_flood_distance_m", 1200.0)
        ),
        rainfall_24h_mm=float(get_sample_value(selected_sample_row, "rainfall_24h_mm", 80.0)),
        rainfall_72h_mm=float(get_sample_value(selected_sample_row, "rainfall_72h_mm", 160.0)),
        water_level_status=cast(WaterLevelStatus, water_level_status),
        weather_warning_status=cast(WeatherWarningStatus, weather_warning_status),
        land_cover_class=str(get_sample_value(selected_sample_row, "land_cover_class", "urban")),
        population_density_per_km2=float(
            get_sample_value(selected_sample_row, "population_density_per_km2", 7000.0)
        ),
    )


def render_risk_summary(payload: FloodRiskInput, selected_date: date | Any) -> None:
    result = calculate_risk(payload)

    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

    with metric_col1:
        st.metric("Flood risk", result.risk_class)

    with metric_col2:
        st.metric("Risk score", f"{result.risk_score:.2f} / 100")

    with metric_col3:
        st.metric("Confidence", result.confidence)

    with metric_col4:
        st.metric("Selected date", str(selected_date))

    if result.risk_class in ["High", "Very High"]:
        st.error(result.recommendation)
    elif result.risk_class == "Moderate":
        st.warning(result.recommendation)
    else:
        st.success(result.recommendation)

    st.subheader("Plain-language explanation")
    top_factors = sorted(result.factors, key=lambda factor: factor.score, reverse=True)[:3]

    for factor in top_factors:
        st.write(f"- **{factor.name}** — {factor.explanation}")

    st.subheader("Location map")
    map_df = pd.DataFrame(
        {
            "lat": [payload.latitude],
            "lon": [payload.longitude],
        }
    )
    st.map(map_df, latitude="lat", longitude="lon", zoom=10)

    context_col1, context_col2, context_col3 = st.columns(3)

    with context_col1:
        st.metric("Nearest river distance", f"{payload.river_distance_m:,.0f} m")
        st.metric(
            "Historical flood area distance",
            f"{payload.historical_flood_distance_m:,.0f} m",
        )

    with context_col2:
        st.metric("Rainfall last 24h", f"{payload.rainfall_24h_mm:,.1f} mm")
        st.metric("Rainfall last 72h", f"{payload.rainfall_72h_mm:,.1f} mm")

    with context_col3:
        st.metric("Water level status", str(payload.water_level_status))
        st.metric("Weather warning status", str(payload.weather_warning_status))

    with st.expander("Technical factor table"):
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
        st.bar_chart(factors_df.set_index("Factor")["Score"], width="stretch")

    with st.expander("JSON result"):
        st.json(result.model_dump())

    st.caption(result.disclaimer)


def render_public_checker(
    samples_df: pd.DataFrame,
    admin_regions_df: pd.DataFrame,
    weather_summary_status: dict[str, Any],
) -> None:
    st.header("Flood Risk Checker")
    st.caption(
        "Designed for normal users: choose a place and date, then review the "
        "risk result, map marker, and simple explanation."
    )

    public_locations_df = build_public_location_catalog(samples_df, admin_regions_df)

    if public_locations_df.empty:
        st.info(
            "No Malaysia coverage or sample location dataset found yet. "
            "Use Advanced Manual Mode for now."
        )
        return

    state_options = ["All states"] + sorted(public_locations_df["state"].dropna().unique())
    selected_state = st.selectbox("State / federal territory", state_options)

    filtered_df = public_locations_df
    if selected_state != "All states":
        filtered_df = public_locations_df[public_locations_df["state"] == selected_state]

    location_options = filtered_df["location_name"].dropna().tolist()
    selected_location = st.selectbox("Area / sample location", location_options)

    selected_sample_row = filtered_df.loc[filtered_df["location_name"] == selected_location].iloc[0]

    input_col1, input_col2 = st.columns(2)

    with input_col1:
        selected_date = st.date_input("Date to check", value=date.today())

    with input_col2:
        risk_view = st.radio(
            "Risk view",
            [
                "Today / latest available estimate",
                "Past / historical-style estimate",
            ],
            horizontal=True,
        )

    use_latest_weather_signal = risk_view == "Today / latest available estimate"

    st.info(
        f"Checking **{selected_location}, {selected_sample_row['state']}** for **{selected_date}**."
    )

    source_type = str(get_sample_value(selected_sample_row, "source_type", "unknown"))

    if source_type == "admin_region_fallback":
        st.warning(
            "This is a Malaysia-wide regional fallback profile. It provides coverage "
            "for every state and federal territory, but detailed district, river, "
            "station, and date-specific data still need to be connected."
        )

    with st.expander("Selected area coverage details"):
        st.write(f"- **Source type:** {source_type}")
        st.write(
            f"- **Region group:** {get_sample_value(selected_sample_row, 'region_group', 'n/a')}"
        )
        st.write(
            f"- **Priority hazards:** "
            f"{get_sample_value(selected_sample_row, 'priority_hazards', 'n/a')}"
        )

    if risk_view == "Past / historical-style estimate":
        st.warning(
            "Historical date mode currently uses the selected area's stored sample "
            "risk profile. A future version should fetch date-specific rainfall, "
            "river, and official flood records."
        )

    payload = build_risk_input_from_sample(
        selected_sample_row,
        weather_summary_status,
        use_latest_weather_signal,
    )
    render_risk_summary(payload, selected_date)

    with st.expander("What this version uses"):
        st.write(
            "- Malaysia-wide state and federal territory coverage registry.\n"
            "- Sample location values where available.\n"
            "- Regional fallback profiles where detailed local data is not ready yet.\n"
            "- Local weather pipeline summary when available.\n"
            "- Transparent rule-based risk scoring.\n"
            "- Experimental AI model reports in the Research Dashboard."
        )

    with st.expander("What future versions should add"):
        st.write(
            "- District-level location coverage.\n"
            "- Live rainfall and water-level station data.\n"
            "- Official river/station overlays on the map.\n"
            "- Date-specific historical flood lookup.\n"
            "- Official MyWater/DID and EM-DAT validation matching."
        )


def render_training_metrics(training_report: dict[str, Any]) -> None:
    if not training_report.get("available"):
        st.info("Training metrics report not found. Run the experimental AI pipeline.")
        return

    metrics = training_report["data"]
    cols = st.columns(5)

    cols[0].metric("Accuracy", metric_percent(metrics.get("accuracy")))
    cols[1].metric("Precision", metric_percent(metrics.get("precision")))
    cols[2].metric("Recall", metric_percent(metrics.get("recall")))
    cols[3].metric("F1", metric_percent(metrics.get("f1")))
    cols[4].metric("ROC-AUC", metric_percent(metrics.get("roc_auc")))

    st.caption(f"Loaded from `{training_report['path']}`")


def render_threshold_metrics(threshold_report: dict[str, Any]) -> None:
    if not threshold_report.get("available"):
        st.info("Threshold tuning report not found. Run the experimental AI pipeline.")
        return

    metrics = threshold_report["data"]
    rows = []

    for key, label in [
        ("best_f1", "Best F1"),
        ("best_high_recall", "Best high recall"),
        ("best_high_precision", "Best high precision"),
    ]:
        value = metrics.get(key)
        if value:
            rows.append(
                {
                    "Strategy": label,
                    "Threshold": value.get("threshold"),
                    "Precision": value.get("precision"),
                    "Recall": value.get("recall"),
                    "F1": value.get("f1"),
                    "False positives": value.get("false_positive"),
                    "False negatives": value.get("false_negative"),
                }
            )

    if rows:
        threshold_df = pd.DataFrame(rows)
        st.dataframe(threshold_df, width="stretch", hide_index=True)
        st.bar_chart(
            threshold_df.set_index("Strategy")[["Precision", "Recall", "F1"]],
            width="stretch",
        )

    st.caption(f"Loaded from `{threshold_report['path']}`")


def render_benchmark_metrics(benchmark_report: dict[str, Any]) -> None:
    if not benchmark_report.get("available"):
        st.info("Benchmark report not found. Run scripts/benchmark_kaggle_flood_models.py.")
        return

    metrics = benchmark_report["data"]
    best_model = metrics.get("best_model", {})
    best_result = best_model.get("best_result", {})

    cols = st.columns(5)
    cols[0].metric("Best model", str(best_model.get("model_name", "n/a")))
    cols[1].metric("Threshold", str(best_model.get("best_threshold", "n/a")))
    cols[2].metric("Priority score", str(best_result.get("flood_priority_score", "n/a")))
    cols[3].metric("Recall", metric_percent(best_result.get("recall")))
    cols[4].metric("F1", metric_percent(best_result.get("f1")))

    comparison_rows = []
    for model in metrics.get("models", []):
        result = model.get("best_result", {})
        comparison_rows.append(
            {
                "Model": model.get("model_name"),
                "Threshold": model.get("best_threshold"),
                "Priority": result.get("flood_priority_score"),
                "Accuracy": result.get("accuracy"),
                "Precision": result.get("precision"),
                "Recall": result.get("recall"),
                "F1": result.get("f1"),
                "PR-AUC": result.get("pr_auc"),
                "ROC-AUC": result.get("roc_auc"),
                "FPR": result.get("false_positive_rate"),
            }
        )

    if comparison_rows:
        benchmark_df = pd.DataFrame(comparison_rows)
        st.dataframe(benchmark_df, width="stretch", hide_index=True)
        st.bar_chart(
            benchmark_df.set_index("Model")[["Priority", "Recall", "F1", "Precision"]],
            width="stretch",
        )

    st.caption(f"Loaded from `{benchmark_report['path']}`")


def render_api_test_panel() -> None:
    base_url = st.text_input(
        "FastAPI base URL",
        value="http://127.0.0.1:8000",
        help="Start the API first with scripts/run_api.ps1.",
    ).rstrip("/")

    col_a, col_b = st.columns(2)

    with col_a:
        if st.button("Check API model status"):
            try:
                st.json(api_get_json(f"{base_url}/experimental/flood/model/status"))
            except (URLError, TimeoutError, OSError) as error:
                st.error(f"Could not reach the API server: {error}")

    with col_b:
        if st.button("Run sample API prediction"):
            sample_payload = {
                "city": "Kuala Lumpur",
                "temperature_c": 27.5,
                "humidity_pct": 88,
                "wind_speed_ms": 3.2,
                "rainfall_3day_mm": 95,
                "rainfall_7day_mm": 180,
                "rainfall_14day_mm": 260,
                "rainfall_cumsum7_mm": 180,
                "month": 12,
                "is_monsoon": 1,
            }

            try:
                prediction = api_post_json(
                    f"{base_url}/experimental/flood/predict",
                    sample_payload,
                )
                st.json(prediction)

                probability = prediction.get("flood_probability")
                if probability is not None:
                    st.progress(float(probability))
                    st.metric("Flood probability", metric_percent(probability))
            except (URLError, TimeoutError, OSError) as error:
                st.error(f"Could not reach the API server: {error}")


def render_research_dashboard(
    training_metrics_status: dict[str, Any],
    threshold_metrics_status: dict[str, Any],
    benchmark_metrics_status: dict[str, Any],
) -> None:
    st.header("Research Dashboard")
    st.caption(
        "Detailed model, threshold, benchmark, and API testing section for "
        "researchers and developers."
    )

    dashboard_tab1, dashboard_tab2, dashboard_tab3, dashboard_tab4 = st.tabs(
        [
            "Training metrics",
            "Threshold tuning",
            "Model benchmark",
            "API test panel",
        ]
    )

    with dashboard_tab1:
        render_training_metrics(training_metrics_status)

    with dashboard_tab2:
        render_threshold_metrics(threshold_metrics_status)

    with dashboard_tab3:
        render_benchmark_metrics(benchmark_metrics_status)

    with dashboard_tab4:
        render_api_test_panel()


def render_advanced_manual_mode(
    weather_summary_status: dict[str, Any],
    samples_df: pd.DataFrame,
) -> None:
    st.header("Advanced Manual Mode")
    st.caption(
        "For researchers and developers who want to override all technical "
        "geospatial, rainfall, hydrology, and exposure inputs manually."
    )

    selected_sample_row = None

    if samples_df.empty:
        st.info("No sample dataset found. Using manual input mode.")
        selected_sample_name = "Custom manual input"
    else:
        sample_options = ["Custom manual input"] + samples_df["location_name"].tolist()
        selected_sample_name = st.selectbox(
            "Optional sample preset",
            sample_options,
            key="advanced_sample_preset",
        )

        if selected_sample_name != "Custom manual input":
            selected_sample_row = samples_df.loc[
                samples_df["location_name"] == selected_sample_name
            ].iloc[0]
            st.info(
                f"Loaded sample preset: {selected_sample_row['location_name']}, "
                f"{selected_sample_row['state']}"
            )

    widget_suffix = selected_sample_name.replace(" ", "_").replace(",", "").lower()

    col1, col2 = st.columns(2)

    with col1:
        latitude = st.number_input(
            "Latitude",
            value=float(get_sample_value(selected_sample_row, "latitude", 3.1390)),
            format="%.6f",
            key=f"advanced_latitude_{widget_suffix}",
        )
        longitude = st.number_input(
            "Longitude",
            value=float(get_sample_value(selected_sample_row, "longitude", 101.6869)),
            format="%.6f",
            key=f"advanced_longitude_{widget_suffix}",
        )
        elevation_m = st.number_input(
            "Elevation (m)",
            min_value=-20.0,
            value=float(get_sample_value(selected_sample_row, "elevation_m", 30.0)),
            key=f"advanced_elevation_{widget_suffix}",
        )
        slope_deg = st.number_input(
            "Slope (degrees)",
            min_value=0.0,
            max_value=90.0,
            value=float(get_sample_value(selected_sample_row, "slope_deg", 2.0)),
            key=f"advanced_slope_{widget_suffix}",
        )
        river_distance_m = st.number_input(
            "Distance to nearest river (m)",
            min_value=0.0,
            value=float(get_sample_value(selected_sample_row, "river_distance_m", 500.0)),
            key=f"advanced_river_distance_{widget_suffix}",
        )

    with col2:
        historical_flood_distance_m = st.number_input(
            "Distance to nearest historical flood area (m)",
            min_value=0.0,
            value=float(
                get_sample_value(
                    selected_sample_row,
                    "historical_flood_distance_m",
                    1200.0,
                )
            ),
            key=f"advanced_historical_flood_distance_{widget_suffix}",
        )
        rainfall_24h_mm = st.number_input(
            "Rainfall last 24 hours (mm)",
            min_value=0.0,
            value=float(get_sample_value(selected_sample_row, "rainfall_24h_mm", 80.0)),
            key=f"advanced_rainfall_24h_{widget_suffix}",
        )
        rainfall_72h_mm = st.number_input(
            "Rainfall last 72 hours (mm)",
            min_value=0.0,
            value=float(get_sample_value(selected_sample_row, "rainfall_72h_mm", 160.0)),
            key=f"advanced_rainfall_72h_{widget_suffix}",
        )
        population_density_per_km2 = st.number_input(
            "Population density (people/km²)",
            min_value=0.0,
            value=float(
                get_sample_value(
                    selected_sample_row,
                    "population_density_per_km2",
                    7000.0,
                )
            ),
            key=f"advanced_population_density_{widget_suffix}",
        )

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

    default_water_status = str(
        get_sample_value(selected_sample_row, "water_level_status", "warning")
    )
    default_weather_status = resolve_weather_status(
        selected_sample_row,
        weather_summary_status,
        selected_sample_row is None,
    )
    default_land_cover = str(get_sample_value(selected_sample_row, "land_cover_class", "urban"))

    col3, col4, col5 = st.columns(3)

    with col3:
        water_level_status = st.selectbox(
            "Water level status",
            water_level_options,
            index=option_index(water_level_options, default_water_status),
            key=f"advanced_water_level_{widget_suffix}",
        )

    with col4:
        weather_warning_status = st.selectbox(
            "Weather warning status",
            weather_warning_options,
            index=option_index(weather_warning_options, default_weather_status),
            key=f"advanced_weather_warning_{widget_suffix}",
        )

    with col5:
        land_cover_class = st.selectbox(
            "Land cover class",
            land_cover_options,
            index=option_index(land_cover_options, default_land_cover),
            key=f"advanced_land_cover_{widget_suffix}",
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
            water_level_status=cast(WaterLevelStatus, water_level_status),
            weather_warning_status=cast(
                WeatherWarningStatus,
                weather_warning_status,
            ),
            land_cover_class=land_cover_class,
            population_density_per_km2=population_density_per_km2,
        )
    except ValidationError as error:
        st.error("Invalid input. Please make sure the coordinate is inside Malaysia.")
        with st.expander("Validation details"):
            st.json(error.errors())
        return

    render_risk_summary(payload, date.today())


def render_data_sources_and_limits(
    weather_summary_status: dict[str, Any],
    geospatial_summary_status: dict[str, Any],
    experimental_model_status: dict[str, Any],
) -> None:
    st.header("Data Sources & Current Limits")
    st.caption(
        "This section explains what the app currently knows, what is experimental, "
        "and what still needs official integration."
    )

    st.subheader("Current app behavior")
    st.write(
        "- The public checker uses local sample location profiles.\n"
        "- The selected date is currently used as analysis context.\n"
        "- Live date-specific rainfall, river, and station APIs are not connected yet.\n"
        "- The experimental AI model is trained on Kaggle proxy data.\n"
        "- Official validation should continue with EM-DAT and MyWater/DID records."
    )

    status_col1, status_col2, status_col3 = st.columns(3)

    with status_col1:
        st.metric(
            "Weather sample pipeline",
            "available" if weather_summary_status.get("available") else "missing",
        )

    with status_col2:
        st.metric(
            "Geospatial readiness",
            "available" if geospatial_summary_status.get("available") else "missing",
        )

    with status_col3:
        st.metric(
            "Experimental model",
            "available" if experimental_model_status.get("available") else "missing",
        )

    with st.expander("Experimental model guardrail"):
        st.write(
            experimental_model_status.get(
                "guardrail",
                "Experimental proxy model only.",
            )
        )

    with st.expander("What a production version should add"):
        st.write(
            "- Real-time rainfall and weather warning ingestion.\n"
            "- Real-time DID/MyWater station status ingestion.\n"
            "- River and station map overlays.\n"
            "- Date-specific historical flood event lookup.\n"
            "- Official validation against EM-DAT and MyWater/DID records.\n"
            "- Model calibration before public decision support."
        )


weather_summary_status = load_weather_summary_status()
geospatial_summary_status = load_geospatial_summary_status()
experimental_model_status = load_experimental_model_status()
training_metrics_status = load_json_report(TRAINING_METRICS_PATH)
threshold_metrics_status = load_json_report(THRESHOLD_METRICS_PATH)
benchmark_metrics_status = load_json_report(BENCHMARK_METRICS_PATH)
samples_df = load_sample_locations()
admin_regions_df = load_admin_regions_df()

st.set_page_config(
    page_title="Malaysia Flood Risk AI",
    page_icon="🌊",
    layout="wide",
)

st.title("🌊 Malaysia Flood Risk AI")
st.caption(
    "Public-friendly flood risk checker with a separated research dashboard for "
    "model training, benchmarking, and API testing."
)

with st.sidebar:
    st.header("About")
    st.write(
        "Choose a location and date to view a simple flood-risk estimate. "
        "Advanced research tools are separated into their own dashboard."
    )

    st.warning(
        "Research use only. Always follow official Malaysian flood warnings "
        "and emergency instructions."
    )

    st.divider()
    st.subheader("Quick status")

    st.metric(
        "Experimental model",
        "available" if experimental_model_status.get("available") else "missing",
    )

    if experimental_model_status.get("available"):
        st.caption(
            f"Threshold: {experimental_model_status.get('threshold')} "
            f"({experimental_model_status.get('threshold_source')})"
        )

    st.metric(
        "Weather pipeline",
        "available" if weather_summary_status.get("available") else "missing",
    )

    st.metric(
        "Geospatial summary",
        "available" if geospatial_summary_status.get("available") else "missing",
    )

public_tab, research_tab, advanced_tab, data_tab = st.tabs(
    [
        "Flood Risk Checker",
        "Research Dashboard",
        "Advanced Manual Mode",
        "Data Sources & Limits",
    ]
)

with public_tab:
    render_public_checker(samples_df, admin_regions_df, weather_summary_status)

with research_tab:
    render_research_dashboard(
        training_metrics_status,
        threshold_metrics_status,
        benchmark_metrics_status,
    )

with advanced_tab:
    render_advanced_manual_mode(weather_summary_status, samples_df)

with data_tab:
    render_data_sources_and_limits(
        weather_summary_status,
        geospatial_summary_status,
        experimental_model_status,
    )
