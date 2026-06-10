# ReliefWeb Metadata Discovery Report

## Summary

- Source ID: `reliefweb_api`
- Fetched at UTC: 2026-06-10T03:01:45.509048+00:00
- Direct training use allowed: False
- Report metadata records: 0
- Successful: False

## Guardrail

This report contains metadata only. It must not be used as supervised ML training labels until source authority, licensing, location, dates, and target mapping are reviewed.

## Errors

- malaysia_flood_reports: HTTP 400 Bad Request - {"status":400,"time":2,"error":{"type":"UnexpectedValueException","message":"Unrecognized field 'name' in parameter 'fields'."}}
- malaysia_flood_maps: HTTP 400 Bad Request - {"status":400,"time":2,"error":{"type":"UnexpectedValueException","message":"Unrecognized field 'name' in parameter 'fields'."}}
- malaysia_flood_response: HTTP 400 Bad Request - {"status":400,"time":3,"error":{"type":"UnexpectedValueException","message":"Unrecognized field 'name' in parameter 'fields'."}}

## Discovered Reports

| ID | Title | Original Date | Sources | Countries | Disasters | URL |
|---|---|---|---|---|---|---|

## Decision

Use these records only for source review and follow-up dataset selection. Do not convert them directly into `flood_occurred` labels.
