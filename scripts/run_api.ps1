$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ProjectRoot = Split-Path -Parent $PSScriptRoot
Set-Location $ProjectRoot

$env:PYTHONPATH = "src"

Write-Host "Project root: $ProjectRoot"
Write-Host "Starting FastAPI server on http://127.0.0.1:8000"
Write-Host "Press Ctrl+C to stop."

uvicorn api.main:app --reload --port 8000
