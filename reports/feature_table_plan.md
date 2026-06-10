# Feature Table Generation Plan

## Summary

- Planned columns: 17
- Columns with usable current source/proxy: 9
- Columns still requiring future data work: 8
- Target label ready: False
- Real ML training allowed now: False

## Planned Columns

| Column | Type | Role | Source Category | Ready Now | Planned Source | Derivation Note |
|---|---|---|---|---:|---|---|
| observation_id | string | identifier | generated | False | feature table builder | Create stable unique ID from location and observation date. |
| latitude | float | feature | sample/geospatial | True | sample locations or geocoded observations | Use validated Malaysia latitude. |
| longitude | float | feature | sample/geospatial | True | sample locations or geocoded observations | Use validated Malaysia longitude. |
| observation_date | date | time | temporal | False | future observation/event table | Attach date for time-aware split and weather joins. |
| state | string | feature | geospatial | False | future administrative boundary file | Derive by point-in-polygon lookup after boundary data is verified. |
| district | string | feature | geospatial | False | future administrative boundary file | Derive by point-in-polygon lookup after district data is verified. |
| elevation_m | float | feature | terrain | True | current sample data or future DEM source | Use sample value now; replace with DEM-derived value later. |
| slope_deg | float | feature | terrain | True | current sample data or future DEM source | Use sample value now; replace with DEM-derived slope later. |
| river_distance_m | float | feature | hydrology/geospatial | True | current sample data or future river network | Use sample value now; replace with nearest-river calculation later. |
| historical_flood_distance_m | float | feature | historical/geospatial | True | current sample data or future historical flood polygons | Use sample value now; replace with historical flood proximity later. |
| rainfall_24h_mm | float | feature | weather | False | weather pipeline or future rainfall history | Aggregate rainfall over previous 24 hours. |
| rainfall_72h_mm | float | feature | weather | False | weather pipeline or future rainfall history | Aggregate rainfall over previous 72 hours. |
| water_level_status | string | feature | hydrology | False | future river/water-level source | Join hydrology status by station, basin, or nearest valid proxy. |
| weather_warning_status | string | feature | weather | True | weather warning pipeline | Map warning text or category into normalized warning status. |
| land_cover_class | string | feature | exposure/geospatial | True | current sample data or future land-cover raster/vector | Use sample value now; replace with verified land-cover lookup later. |
| population_density_per_km2 | float | feature | exposure | True | current sample data or future population raster/table | Use sample value now; replace with verified population density source. |
| flood_occurred | integer | target | target | False | future verified historical flood label source | Preferred binary target label from a verified historical flood source. Must not come from rule-based risk score. |

## Training Guardrail

Do not create a real model-training table until the target label `flood_occurred` comes from a verified historical flood source.

The rule-based risk score may be used for demos or weak-supervision experiments only if clearly labeled as proxy or synthetic.

## Next Practical Step

Create a feature-table builder skeleton that can inspect available sample columns, but refuses to mark output as training-ready when the verified target label is unavailable.
