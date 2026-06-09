# Data Sources

This project uses a staged data strategy.

## Stage 1: Transparent MVP

The first working version uses manually entered features:

- Latitude
- Longitude
- Elevation
- Slope
- Distance to nearest river
- Distance to nearest historical flood area
- 24-hour rainfall
- 72-hour rainfall
- Water-level status
- Weather-warning status
- Land-cover class
- Population density

This allows the API and app to work before full automated data integration.

## Stage 2: Public Data Integration

Planned sources:

| Dataset | Purpose |
|---|---|
| MET Malaysia forecast API | Forecast rainfall and weather condition |
| MET Malaysia warning API | Weather warning severity |
| Public InfoBanjir | Water level and rainfall station status |
| NASA SRTM DEM | Elevation and slope |
| Copernicus Land Cover | Land-cover and surface-type features |
| OpenStreetMap | River distance, road access, buildings, exposure |
| Historical flood inventory | Labels and historical flood proximity |
| Malaysia boundary | Coordinate validation and state/district mapping |

## Stage 3: Research Dataset

The cleaned research dataset should contain one row per location or grid cell.

Recommended columns:

- location_id
- latitude
- longitude
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
- flood_label
- flood_probability_target
- event_date
- source_quality

## Data Quality Rules

1. Coordinates must be inside Malaysia.
2. Latitude must be between roughly -1.5 and 7.5.
3. Longitude must be between roughly 99 and 120.
4. Duplicate flood points must be removed or grouped.
5. Historical flood events must preserve date and location.
6. Model labels must not be created using the same feature being tested without leakage control.
7. Train/test split must include spatial or temporal validation.

## Important Research Note

The original reference repository used distance to historical flood points as a major feature. For this project, we will keep it as a useful signal, but we will avoid using it as the only label-generation rule because that can create target leakage and inflated accuracy.
