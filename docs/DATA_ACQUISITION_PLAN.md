# Data Acquisition Plan

This document defines the first real-data acquisition workflow for the Malaysia
flood risk AI project.

## Current Research State

The project is ready to begin data source review, but real supervised ML training
is still blocked.

Current blockers:

- no target source candidate is ready for real training
- no verified historical flood event source is available yet
- no generated model-ready training table exists yet
- no training rows exist yet

## Immediate Goal

Find or prepare a verified historical flood occurrence source that can support:

    flood_occurred

The source must be alignable by:

- location
- date
- authority
- license or usage permission
- binary target mapping

## Preferred Source Types

1. Verified historical flood event records
2. Historical flood extent polygons
3. Official flood incident reports
4. Structured disaster/event datasets with Malaysia location/date fields

## Rejected Source Types

Do not use these as real supervised ML labels:

- rule-based project `risk_score`
- unverified social media posts
- anecdotal reports without source authority
- generated or synthetic labels pretending to be real events
- scraped content without clear usage permission

## Acquisition Workflow

1. Identify candidate source.
2. Record it in `configs/target_source_candidates.json`.
3. Check license and usage permission.
4. Confirm location fields.
5. Confirm date fields.
6. Confirm whether it can map to `flood_occurred`.
7. Convert or prepare into:

       data/processed/targets/historical_flood_events.csv

8. Run:

       .\scripts\run_target_source_manifest_check.ps1
       .\scripts\run_target_event_source_schema_check.ps1
       .\scripts\run_ml_readiness_suite.ps1

## Definition of Done

A source is ready for training preparation only when:

- candidate manifest has at least one ready source
- historical target event file exists
- schema validation passes
- row count is greater than zero
- target leakage is avoided
- license and authority are documented

## Next Step

Start external/public source research and choose the first candidate target-label
source to review.

## Source Research Shortlist

The first source-review shortlist is documented at:

    docs/SOURCE_RESEARCH_SHORTLIST.md

The machine-readable shortlist is:

    configs/source_research_shortlist.json

The recommended first implementation target is ReliefWeb discovery because it is
useful for finding Malaysia flood reports and source references before selecting
a final target-label dataset.

## ReliefWeb Discovery Plan

Before live ReliefWeb metadata discovery, validate the query plan:

    .\scripts\run_reliefweb_discovery_plan.ps1

Generated report:

    reports/reliefweb_discovery_plan.md
