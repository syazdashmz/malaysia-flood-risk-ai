# EM-DAT Export Intake Plan

This document defines how an EM-DAT export should be introduced into the project
without weakening the ML-readiness guardrails.

## Purpose

Prepare a controlled intake path for reviewing EM-DAT records as a possible
source for historical Malaysia flood occurrence labels.

## Planned Raw Export Path

    data/raw/emdat/emdat_public_export.csv

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

Prepare the EM-DAT intake workflow before importing any raw CSV export.
EM-DAT remains a candidate target-label source, not an approved training source.
