$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"
Write-Host "Starting Malaysia Flood Risk AI API..."
Write-Host "API docs: http://127.0.0.1:8000/docs"
Write-Host "Weather summary: http://127.0.0.1:8000/weather/summary"

uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
