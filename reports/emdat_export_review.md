# EM-DAT Export Review

## Summary

- Raw export path: `data/raw/emdat/emdat_public_export.xlsx`
- Raw export exists: True
- Source rows: 69
- Malaysia flood rows: 69
- Rows with location text: 69
- Rows with latitude/longitude: 19
- Rows with admin units: 59
- Rows with usable start date: 68
- Review ready: True
- Ready for training: False
- Direct training use allowed: False
- Target-label candidate: True

## Output

- Interim review table: `data/interim/targets/emdat_historical_flood_events_review.csv`
- Final processed target table: `data/processed/targets/historical_flood_events.csv`

## Review Status Counts

- admin_unit_review_required: 40
- coordinate_review_required: 19
- location_text_review_required: 10

## Guardrail

This review table is not the final supervised ML target table. Do not train the official model from EM-DAT rows until license, location granularity, date mapping, schema mapping, and leakage checks pass.

## Next Actions

1. Review EM-DAT license and attribution requirements.
2. Confirm state/district mapping from admin-unit fields.
3. Decide which rows can map to verified `historical_flood_events.csv` records.
4. Keep real official ML training blocked until target-source validation passes.
