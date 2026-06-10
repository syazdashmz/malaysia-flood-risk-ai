# Data Source Review Checklist

Use this checklist before adding or processing any real dataset.

## Source Identity

- [ ] Source name is documented
- [ ] Source URL or reference is documented
- [ ] Source authority or publisher is documented
- [ ] License or usage permission is documented

## Target Suitability

- [ ] Source represents historical flood occurrence
- [ ] Source can map to `flood_occurred`
- [ ] Source does not depend on project `risk_score`
- [ ] Source is not synthetic unless clearly marked as non-training demo data

## Location Suitability

- [ ] Source includes latitude/longitude, geometry, state, or district
- [ ] Location fields can be mapped to Malaysia administrative areas
- [ ] Coordinates are inside Malaysia bounds where applicable

## Time Suitability

- [ ] Source includes event start date or observation date
- [ ] Source includes event end date or enough temporal context
- [ ] Date fields can be normalized to `YYYY-MM-DD`

## Processing Readiness

- [ ] Data format can be read by Python
- [ ] Raw data can be stored safely outside Git if needed
- [ ] Processed target file can match the required schema
- [ ] Data quality issues are documented
