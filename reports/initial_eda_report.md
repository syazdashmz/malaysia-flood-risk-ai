# Initial EDA Report

## Summary

- Sample locations available: True
- Sample location rows: 6
- Weather summary available: True
- Ready for initial EDA: True
- Ready for real ML training: False

## Sample Location Columns

- location_name
- state
- latitude
- longitude
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
- risk_score
- risk_class
- confidence

## Numeric Profiles

| Column | Count | Min | Max | Mean |
|---|---:|---:|---:|---:|
| latitude | 6 | 2.9225 | 6.1254 | 3.9266 |
| longitude | 6 | 101.3801 | 103.3260 | 101.9716 |
| elevation_m | 6 | 8.0000 | 1450.0000 | 263.0000 |
| slope_deg | 6 | 0.8000 | 18.0000 | 4.4167 |
| river_distance_m | 6 | 350.0000 | 2500.0000 | 1066.6667 |
| historical_flood_distance_m | 6 | 500.0000 | 9000.0000 | 2650.0000 |
| rainfall_24h_mm | 6 | 25.0000 | 120.0000 | 79.1667 |
| rainfall_72h_mm | 6 | 70.0000 | 260.0000 | 168.3333 |
| population_density_per_km2 | 6 | 120.0000 | 7500.0000 | 2653.3333 |
| risk_score | 6 | 16.5000 | 89.5600 | 65.1733 |

## Weather Summary Keys

- forecast_count
- max_weather_signal
- record_count
- risk_engine_weather_warning
- signal_counts
- warning_count

## Weather Signal Counts

- advisory: 0
- none: 4
- severe: 0
- warning: 2

## Interpretation

The current assets are suitable for initial notebook-based EDA. They are not sufficient for real ML training yet because the model-ready training table is still missing.

## Next EDA Direction

1. Inspect sample location distribution.
2. Review weather signal counts.
3. Compare readiness reports.
4. Define the first model-ready feature table generation plan.
5. Keep real training blocked until validated target labels exist.
