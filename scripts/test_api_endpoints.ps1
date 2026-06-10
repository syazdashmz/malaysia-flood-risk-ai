$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$BaseUrl = "http://127.0.0.1:8000"

Write-Host "`n--- HEALTH ---"
Invoke-RestMethod "$BaseUrl/health" |
  ConvertTo-Json -Depth 10

Write-Host "`n--- EXPERIMENTAL MODEL STATUS ---"
Invoke-RestMethod "$BaseUrl/experimental/flood/model/status" |
  ConvertTo-Json -Depth 10

Write-Host "`n--- EXPERIMENTAL FLOOD PREDICTION ---"
$Payload = @{
  city = "Kuala Lumpur"
  temperature_c = 27.5
  humidity_pct = 88
  wind_speed_ms = 3.2
  rainfall_3day_mm = 95
  rainfall_7day_mm = 180
  rainfall_14day_mm = 260
  rainfall_cumsum7_mm = 180
  month = 12
  is_monsoon = 1
} | ConvertTo-Json

Invoke-RestMethod `
  -Uri "$BaseUrl/experimental/flood/predict" `
  -Method Post `
  -ContentType "application/json" `
  -Body $Payload |
  ConvertTo-Json -Depth 10
