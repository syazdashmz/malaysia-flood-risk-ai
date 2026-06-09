$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"
Write-Host "Generating geospatial artifact plan..."
python scripts\generate_geospatial_artifact_plan.py

Write-Host "Validating geospatial artifacts..."
python scripts\validate_geospatial_artifacts.py

Write-Host "Geospatial checks completed."
