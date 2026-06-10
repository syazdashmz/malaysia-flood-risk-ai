# ReliefWeb Discovery

This document explains the first source-discovery implementation target.

## Purpose

ReliefWeb is used as a discovery index for Malaysia flood reports, maps,
humanitarian updates, and source references.

## Current Guardrail

ReliefWeb report content must not be treated as final supervised ML labels until:

- source authority is reviewed
- license and usage permission are reviewed
- location fields are confirmed
- event dates are confirmed
- mapping to `flood_occurred` is justified

## Query Config

    configs/reliefweb_discovery_queries.json

## Generated Plan Report

Run:

    .\scripts\run_reliefweb_discovery_plan.ps1

This generates:

    reports/reliefweb_discovery_plan.md

## Next Step

Create a live metadata-only discovery script after the offline query plan is
validated.
