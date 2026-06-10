# EM-DAT Target Source Review

This document reviews EM-DAT as a candidate source for historical Malaysia flood
occurrence labels.

## Summary

- Source ID: `emdat`
- Candidate target column: `flood_occurred`
- Target-label candidate: True
- Direct training use allowed now: False
- Review status: review required

## Why EM-DAT Matters

EM-DAT is a strong candidate because it contains historical disaster occurrence
and impact records. It may help identify verified Malaysia flood events that can
support target-label creation.

## Current Guardrail

EM-DAT must not be used directly for supervised ML training until the project
confirms:

- Malaysia flood records are accessible
- event date fields are usable
- location granularity is usable
- flood classification fields are available
- license and attribution rules are documented
- records can map to `data/processed/targets/historical_flood_events.csv`

## Known Limitations

EM-DAT focuses on major disasters. It may not contain smaller district-level or
local flash-flood events. It may work better as one of these:

1. target-label source for major flood events
2. validation source for manually prepared labels
3. seed source for finding official reports
4. country-level disaster reference source

## Review Checklist

- [ ] Can Malaysia records be filtered?
- [ ] Can flood records be filtered?
- [ ] Does the source include event start date?
- [ ] Does the source include event end date?
- [ ] Does the source include country, region, state, or district?
- [ ] Does the source include flood subtype or disaster classification?
- [ ] Are non-commercial use and attribution rules acceptable?
- [ ] Can records map into the target event schema?
- [ ] Is the dataset granular enough for model training?

## Decision

Review EM-DAT next. Do not approve it for training until a sample/export is
examined and mapped against the target event schema.

## EM-DAT Export Intake Plan

Before importing any raw EM-DAT export, follow:

    docs/EMDAT_EXPORT_INTAKE.md
    configs/emdat_export_intake_plan.json
    reports/emdat_export_intake_plan.md

The planned raw export path is:

    data/raw/emdat/emdat_public_export.csv
