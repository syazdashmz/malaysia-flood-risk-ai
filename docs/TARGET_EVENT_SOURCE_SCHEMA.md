# Target Event Source Schema

This document defines the expected schema for a future verified historical flood
event source that can generate the supervised ML target column:

    flood_occurred

## Expected Local Path

    data/processed/targets/historical_flood_events.csv

This file is intentionally missing for now.

## Required Columns

- event_id
- source_name
- source_url
- license_name
- event_start_date
- event_end_date
- latitude
- longitude
- state
- district
- flood_occurred
- verification_status
- notes

## Validation Rules

- `flood_occurred` must be binary: `0` or `1`.
- `verification_status` must be `verified` or `reviewed`.
- date fields must use ISO date format: `YYYY-MM-DD`.
- coordinates must be numeric and within broad Malaysia bounds.
- source and license fields must be documented before real training use.

## Generated Report

Run:

    .\scripts\run_target_event_source_schema_check.ps1

This generates:

    reports/target_event_source_schema_report.md
