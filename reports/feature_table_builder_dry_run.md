# Feature Table Builder Dry-Run Report

## Summary

- Source exists: True
- Source rows: 6
- Source columns: 17
- Mapped training columns: 13
- Missing training columns: 4
- Target available: False
- Output allowed: False
- Can create real training table: False

## Source

- Source path: `C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai\data\samples\sample_malaysia_locations.csv`
- Planned output path: `C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai\data\processed\model_training\training_features.csv`

## Mapped Training Columns

- elevation_m
- historical_flood_distance_m
- land_cover_class
- latitude
- longitude
- population_density_per_km2
- rainfall_24h_mm
- rainfall_72h_mm
- river_distance_m
- slope_deg
- state
- water_level_status
- weather_warning_status

## Missing Training Columns

- observation_id
- observation_date
- district
- flood_occurred

## Guardrail

This dry run must not create `training_features.csv` until the verified `flood_occurred` target label is available.

Current decision:

    Do not create the real training table yet.
