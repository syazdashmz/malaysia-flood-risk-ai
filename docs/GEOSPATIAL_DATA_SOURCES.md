# Geospatial Data Sources

## Purpose

This registry lists planned geospatial datasets for the v0.3.0 Geospatial Foundation Pipeline milestone.

The project should not blindly download or redistribute administrative boundary data until licensing and source reliability are verified.

## Planned Sources

| Dataset ID | Name | Type | Expected Format | Status |
|---|---|---|---|---|
| malaysia_admin_boundary | Malaysia Administrative Boundary | administrative_boundary | GeoJSON or Shapefile | planned |
| malaysia_state_boundary | Malaysia State Boundary | administrative_boundary | GeoJSON or Shapefile | planned |
| malaysia_district_boundary | Malaysia District Boundary | administrative_boundary | GeoJSON or Shapefile | planned |

## Intended Uses

Administrative boundaries will support:

- point-in-boundary coordinate validation
- state-level risk grouping
- district-level risk grouping
- joining weather signals to locations
- future dashboard filtering
- future map overlays

## Data Governance Notes

Before using a boundary dataset, verify:

1. original source
2. license
3. redistribution permissions
4. coordinate reference system
5. geometry validity
6. update frequency
7. state/district naming convention
8. compatibility with Malaysia-specific administrative hierarchy

## Current Status

No administrative boundary dataset is bundled yet.

The current project still uses the broad Malaysia bounding box for MVP-level validation.
