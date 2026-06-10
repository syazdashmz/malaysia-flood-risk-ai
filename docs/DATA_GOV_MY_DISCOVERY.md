# data.gov.my Discovery Plan

This document defines the next source-discovery path after ReliefWeb access was
blocked pending an approved appname.

## Purpose

Use Malaysia's official open data portal to discover datasets that may support:

- flood target labels
- rainfall features
- hydrology features
- administrative district references
- weather or environmental context

## Official API Entry Point

The Data Catalogue API endpoint is:

    GET https://api.data.gov.my/data-catalogue

The API requires an `id` parameter for a specific dataset. Dataset IDs are found
from the public Data Catalogue pages.

## Initial Search Themes

The first manual/API review should focus on:

1. flood
2. banjir
3. rainfall
4. rain
5. river
6. water level
7. district
8. weather

## Guardrail

data.gov.my datasets should not be treated as target labels until each dataset is
reviewed for:

- source authority
- license or usage permission
- location fields
- date fields
- whether it can map to `flood_occurred`
- whether it is target data or supporting feature data

## Current Decision

Use data.gov.my as the next official Malaysia-first source discovery path.

## Catalogue Candidate Plan

The first reviewed catalogue candidate list is stored at:

    configs/data_gov_my_catalogue_candidates.json

Generate the candidate plan report with:

    .\scripts\run_data_gov_my_catalogue_plan.ps1

This writes:

    reports/data_gov_my_catalogue_plan.md

The current candidates are supporting-data candidates only. They are not direct
`flood_occurred` labels.

## Sample-Only Catalogue Probe

Run:

    .\scripts\run_data_gov_my_catalogue_probe.ps1

This writes:

    data/interim/source_discovery/data_gov_my_catalogue_probe.json
    reports/data_gov_my_catalogue_probe_report.md

These outputs are for source review only. They are not supervised ML labels.

## Catalogue Review

After the first sample-only probe, review decisions are stored at:

    configs/data_gov_my_catalogue_review.json
    reports/data_gov_my_catalogue_review.md
    docs/DATA_GOV_MY_CATALOGUE_REVIEW.md

Current decision: the reviewed datasets are supporting/context candidates only.
None are approved as `flood_occurred` target labels.
