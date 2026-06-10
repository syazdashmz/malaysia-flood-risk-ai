$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

$env:PYTHONPATH = "src;."

Write-Host "Project root: $ProjectRoot"
Write-Host "Validating target source candidate manifest..."
python scripts\generate_target_source_manifest_report.py
Write-Host "Target source candidate manifest check completed."
