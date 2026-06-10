$ErrorActionPreference = "Stop"
$PSNativeCommandUseErrorActionPreference = $true

$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Path
$ProjectRoot = Split-Path -Parent $ScriptDirectory

Set-Location $ProjectRoot

conda activate flood-ai

Write-Host "Project root: $ProjectRoot"
Write-Host "Running ML readiness suite..."

& ".\scripts\run_target_label_source_plan.ps1"
& ".\scripts\run_target_label_source_evaluation.ps1"
& ".\scripts\run_target_source_manifest_check.ps1"
& ".\scripts\run_target_event_source_schema_check.ps1"
& ".\scripts\run_feature_table_plan.ps1"
& ".\scripts\run_feature_table_builder_dry_run.ps1"
& ".\scripts\run_training_schema_check.ps1"
& ".\scripts\run_dataset_readiness.ps1"
& ".\scripts\run_ml_training_readiness.ps1"

Write-Host "ML readiness suite completed."
