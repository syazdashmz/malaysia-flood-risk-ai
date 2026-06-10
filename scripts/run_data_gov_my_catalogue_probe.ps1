$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"
Write-Host "Running sample-only data.gov.my catalogue probe..."
python scripts\probe_data_gov_my_catalogue.py
Write-Host "sample-only data.gov.my catalogue probe completed."
