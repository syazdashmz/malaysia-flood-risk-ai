# Target Source Candidate Manifest

The target source candidate manifest tracks possible future sources for the
real supervised ML target column:

    flood_occurred

## Manifest Path

    configs/target_source_candidates.json

## Generated Report

Run:

    .\scripts\run_target_source_manifest_check.ps1

This generates:

    reports/target_source_manifest_report.md

## Current Decision

The manifest can contain candidate source profiles, but a candidate is not ready
for real training until authority, license, location fields, date fields, and
target mapping are verified.

## Guardrail

The rule-based project risk score must stay rejected as a real training target
source because it would cause target leakage.
