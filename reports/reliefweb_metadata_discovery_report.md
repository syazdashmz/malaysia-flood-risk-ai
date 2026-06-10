# ReliefWeb Metadata Discovery Report

## Summary

- Source ID: `reliefweb_api`
- Fetched at UTC: 2026-06-10T03:03:17.185672+00:00
- Direct training use allowed: False
- Report metadata records: 0
- Successful: False

## Guardrail

This report contains metadata only. It must not be used as supervised ML training labels until source authority, licensing, location, dates, and target mapping are reviewed.

## Errors

- malaysia_flood_reports: HTTP 403 Forbidden - {"status":403,"time":33,"error":{"type":"AccessDeniedHttpException","message":"You are not using an approved appname. Kindly request an appname from ReliefWeb here: https:\/\/apidoc.reliefweb.int\/parameters#appname"}}
- malaysia_flood_maps: HTTP 403 Forbidden - {"status":403,"time":25,"error":{"type":"AccessDeniedHttpException","message":"You are not using an approved appname. Kindly request an appname from ReliefWeb here: https:\/\/apidoc.reliefweb.int\/parameters#appname"}}
- malaysia_flood_response: HTTP 403 Forbidden - {"status":403,"time":33,"error":{"type":"AccessDeniedHttpException","message":"You are not using an approved appname. Kindly request an appname from ReliefWeb here: https:\/\/apidoc.reliefweb.int\/parameters#appname"}}

## Discovered Reports

| ID | Title | Original Date | Sources | Countries | Disasters | URL |
|---|---|---|---|---|---|---|

## Decision

Use these records only for source review and follow-up dataset selection. Do not convert them directly into `flood_occurred` labels.
