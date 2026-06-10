# EM-DAT Export Intake Plan

This document defines how an EM-DAT export should be introduced into the project
without weakening the ML-readiness guardrails.

## Purpose

Prepare a controlled intake path for reviewing EM-DAT records as a possible
source for historical Malaysia flood occurrence labels.

## Planned Raw Export Path

    data/raw/emdat/emdat_public_export.xlsx

## Interim Review Path

    data/interim/targets/emdat_historical_flood_events_review.csv

## Review Reports

    reports/emdat_export_review.md
    reports/emdat_export_review_summary.json

## Planned Processed Target Path

    data/processed/targets/historical_flood_events.csv

## Required Filter

The initial review should focus only on:

- Country: Malaysia
- Disaster type: Flood

## Minimum Review Fields

The export must contain enough information to review:

- country
- disaster type
- event start date
- event end date, if available
- event location, if available
- event identifier or event name, if available

## Guardrail

Do not copy EM-DAT rows into the processed target file until the project confirms:

- access path is valid
- license and attribution requirements are documented
- Malaysia flood rows are present
- date fields are usable
- location granularity is understood
- target event schema mapping is valid
- target leakage risk is reviewed

## Current Decision

Use the EM-DAT export review workflow to create an interim review table only.
EM-DAT remains a candidate target-label source, not an approved training source.

## Review Command

Run:

    .\scripts\run_emdat_export_review.ps1

This reads the local workbook, filters Malaysia flood records, writes an interim
review CSV, and generates a lightweight review report.
