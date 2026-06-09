$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

Set-Location "C:\Users\Danish\Coding\Project\AI\malaysia-flood-risk-ai"

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Step 1/4: Fetching weather samples..."
python scripts\fetch_weather_sample.py

Write-Host "Step 2/4: Normalizing weather samples..."
python scripts\normalize_weather_samples.py

Write-Host "Step 3/4: Building weather feature table..."
python scripts\build_weather_features.py

Write-Host "Step 4/4: Profiling weather samples..."
python scripts\profile_weather_samples.py

Write-Host "Weather pipeline completed."
