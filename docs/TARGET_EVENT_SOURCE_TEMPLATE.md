# Historical Flood Events Target Template

This template defines the required CSV structure for a future verified historical
flood event source.

## Template Path

    templates/targets/historical_flood_events_template.csv

## Future Working Data Path

    data/processed/targets/historical_flood_events.csv

The working data path is intentionally ignored by Git because it may contain
large, changing, or externally licensed data.

## Required Columns

- `event_id`: unique event identifier
- `source_name`: source organization or dataset name
- `source_url`: source URL or reference
- `license_name`: source license or usage permission
- `event_start_date`: flood event start date in `YYYY-MM-DD`
- `event_end_date`: flood event end date in `YYYY-MM-DD`, or blank if unknown
- `latitude`: event latitude
- `longitude`: event longitude
- `state`: Malaysian state or federal territory
- `district`: district or best available administrative area
- `flood_occurred`: binary target value, `0` or `1`
- `verification_status`: `verified` or `reviewed`
- `notes`: short notes about assumptions, mapping, or quality

## Guardrails

- Do not derive `flood_occurred` from the rule-based `risk_score`.
- Do not use unverified social media or anecdotal reports as real labels.
- Do not train a supervised ML model until this source passes schema validation.
- Keep raw/processed source data out of Git unless licensing and size are safe.

## Validation Command

    .\scripts\run_target_event_source_schema_check.ps1
