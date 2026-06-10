# EM-DAT Export Intake Plan Report

## Summary

- Source ID: `emdat`
- Raw export path: `data/raw/emdat/emdat_public_export.csv`
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

## Current Decision

The project is ready to receive an EM-DAT export for review, but EM-DAT is still
not approved as a direct supervised training source.
