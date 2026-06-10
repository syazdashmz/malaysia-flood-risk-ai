# Training Table Schema Report

## Summary

- Exists: False
- Valid CSV: False
- Row count: 0
- Required columns: 17
- Missing required columns: 17
- Target column present: False
- Schema valid: False
- Training ready: False

## Expected Columns

| Column | Type | Role | Required | Description |
|---|---|---|---:|---|
| observation_id | string | identifier | True | Unique row identifier. |
| latitude | float | feature | True | Observation latitude. |
| longitude | float | feature | True | Observation longitude. |
| observation_date | date | time | True | Observation date. |
| state | string | feature | True | Administrative state. |
| district | string | feature | True | Administrative district. |
| elevation_m | float | feature | True | Terrain elevation in meters. |
| slope_deg | float | feature | True | Terrain slope in degrees. |
| river_distance_m | float | feature | True | Distance to nearest river in meters. |
| historical_flood_distance_m | float | feature | True | Distance to nearest known historical flood area in meters. |
| rainfall_24h_mm | float | feature | True | Rainfall over previous 24 hours. |
| rainfall_72h_mm | float | feature | True | Rainfall over previous 72 hours. |
| water_level_status | string | feature | True | Hydrology warning/status category. |
| weather_warning_status | string | feature | True | Weather warning category. |
| land_cover_class | string | feature | True | Land cover category. |
| population_density_per_km2 | float | feature | True | Population density per square kilometer. |
| flood_occurred | integer | target | True | Preferred binary target label. |

## Observed Columns

No columns were found.

## Missing Required Columns

- observation_id
- latitude
- longitude
- observation_date
- state
- district
- elevation_m
- slope_deg
- river_distance_m
- historical_flood_distance_m
- rainfall_24h_mm
- rainfall_72h_mm
- water_level_status
- weather_warning_status
- land_cover_class
- population_density_per_km2
- flood_occurred

## Interpretation

The training table is not ready for baseline ML training yet. This is expected until a real model-ready feature table is created.
