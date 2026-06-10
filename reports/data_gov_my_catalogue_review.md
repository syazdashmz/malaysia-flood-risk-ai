# data.gov.my Catalogue Review

This report reviews the first successful data.gov.my sample-only probe.

## Summary

- Source ID: `data_gov_my`
- Reviewed datasets: 3
- Successful sample probes: 3
- Supporting feature/context candidates: 3
- Target-label candidates: 0
- Direct supervised training use allowed: False

## Review Decision

| Dataset ID | Decision | Supporting Feature | Target Label | Priority |
|---|---|---:|---:|---:|
| population_district | keep_as_supporting_geography_reference | True | False | 1 |
| water_consumption | defer_as_weak_context_feature | True | False | 2 |
| water_pollution_basin | defer_as_environment_context_feature | True | False | 3 |

## Dataset Notes

### population_district

This dataset contains state, district, date, demographic, and population fields.
It is useful as supporting geography or exposure context, especially for
validating district names and enriching district-level features.

It is not a target-label source because it does not represent flood occurrence.

### water_consumption

This dataset contains date, state, sector, and value fields. It may provide broad
water-use context, but it is not directly related to flood events.

It should be deferred as a weak supporting feature candidate.

### water_pollution_basin

This dataset contains aggregate river-basin pollution monitoring information. It
may be useful as environmental context, but it does not contain flood occurrence,
flood impact, warning, or affected-location records.

It should be deferred as environmental context only.

## Guardrail

None of these datasets should be mapped to `flood_occurred`.

The next source-search step must continue looking for a verified historical flood event source with location and date fields.

## Next Recommendation

Continue searching for an actual target-label source through:

1. additional data.gov.my catalogue IDs
2. Public InfoBanjir/JPS historical access review
3. EM-DAT event-level review
4. official Malaysia disaster/flood reports
