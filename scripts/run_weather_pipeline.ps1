$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"

Write-Host "Step 1/6: Fetching weather samples..."
python scripts\fetch_weather_sample.py

Write-Host "Step 2/6: Normalizing weather samples..."
python scripts\normalize_weather_samples.py

Write-Host "Step 3/6: Building weather feature table..."
python scripts\build_weather_features.py

Write-Host "Step 4/6: Summarizing weather risk signal..."
python scripts\summarize_weather_features.py

Write-Host "Step 5/6: Profiling weather samples..."
python scripts\profile_weather_samples.py

Write-Host "Step 6/6: Validating weather pipeline outputs..."
python scripts\validate_weather_pipeline.py

Write-Host "Weather pipeline completed."
