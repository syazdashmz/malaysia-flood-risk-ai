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
