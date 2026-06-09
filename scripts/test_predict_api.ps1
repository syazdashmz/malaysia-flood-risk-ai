$ErrorActionPreference = "Stop"

$body = @{
    latitude = 3.139
    longitude = 101.6869
    elevation_m = 30
    slope_deg = 2
    river_distance_m = 500
    historical_flood_distance_m = 1200
    rainfall_24h_mm = 80
    rainfall_72h_mm = 160
    water_level_status = "warning"
    weather_warning_status = "warning"
    land_cover_class = "urban"
    population_density_per_km2 = 7000
} | ConvertTo-Json

Invoke-RestMethod `
    -Uri "http://127.0.0.1:8000/predict" `
    -Method Post `
    -Body $body `
    -ContentType "application/json"
