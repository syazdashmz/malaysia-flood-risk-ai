# EM-DAT Export Intake Plan Report

## Summary

- Source ID: `emdat`
- Raw export path: `data/raw/emdat/emdat_public_export.xlsx`
- Interim review path: `data/interim/targets/emdat_historical_flood_events_review.csv`
- Review report path: `reports/emdat_export_review.md`
- Review summary path: `reports/emdat_export_review_summary.json`
- Processed target path: `data/processed/targets/historical_flood_events.csv`
- Target-label candidate: True
- Direct training use allowed now: False

## Review Scope

Initial EM-DAT review should focus on Malaysia flood records only.

## Required Checks

1. Confirm the export was obtained through an approved EM-DAT access path.
2. Record license and attribution notes.
3. Confirm Malaysia flood rows exist.
4. Confirm date fields can map to target event dates.
5. Review location granularity.
6. Map records against the target event schema.
7. Keep ML training blocked until validation passes.

## Review Command

Run:

    .\scripts\run_emdat_export_review.ps1

## Current Decision

The project can create an interim EM-DAT review table, but EM-DAT is still not
approved as a direct supervised training source.
