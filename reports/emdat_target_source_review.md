# EM-DAT Target Source Review Report

## Summary

- Source ID: `emdat`
- Review status: review required
- Target-label candidate: True
- Candidate target column: `flood_occurred`
- Direct training use allowed now: False

## Candidate Role

EM-DAT is the next serious target-source candidate because it may contain
historical Malaysia flood disaster records with dates and impact information.

## Not Approved Yet

EM-DAT is not approved for direct supervised ML training yet.

Approval requires:

1. verified Malaysia flood record access
2. license and attribution review
3. date-field review
4. location-granularity review
5. flood classification review
6. mapping check against `historical_flood_events.csv`

## Expected Output If Approved Later

If EM-DAT is usable, it may contribute to:

    data/processed/targets/historical_flood_events.csv

## Current Decision

Proceed with EM-DAT access/sample review next. Keep `real_ml_training_ready`
blocked until a verified target source is available.
