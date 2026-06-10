# Source Research Shortlist

This shortlist defines the first real-data discovery targets for the Malaysia
flood risk AI project.

## Research Priority

| Priority | Source | Role | Initial Decision |
|---:|---|---|---|
| 1 | ReliefWeb API | Discovery source | Review first |
| 2 | EM-DAT International Disaster Database | Candidate target source | Review second |
| 3 | data.gov.my | Malaysia open data discovery | Review third |
| 4 | Public InfoBanjir / JPS flood information | Malaysia flood context source | Review fourth |

## Source 1: ReliefWeb API

- Homepage: https://reliefweb.int/
- Documentation: https://apidoc.reliefweb.int/
- Role: discovery source
- Initial decision: review first
- Direct training use now: no

ReliefWeb should be used first as a report discovery index. It can help discover
Malaysia flood reports, disaster updates, maps, source names, dates, and
humanitarian references.

Guardrail:

Do not treat ReliefWeb report content as final training labels until source
authority, license, location fields, and date fields are reviewed.

## Source 2: EM-DAT

- Homepage: https://www.emdat.be/
- Documentation: https://doc.emdat.be/
- Role: candidate target source
- Initial decision: review second
- Direct training use now: no

EM-DAT is a strong candidate for verified disaster occurrence and impact review.
It may support event-level flood occurrence research, but its location
granularity must be checked before it can support district-level or coordinate-
level training.

## Source 3: data.gov.my

- Homepage: https://data.gov.my/
- Documentation: https://developer.data.gov.my/
- Role: Malaysia open data discovery
- Initial decision: review third
- Direct training use now: no

data.gov.my should be searched for official Malaysia datasets that can support
flood labels, rainfall, hydrology, administrative areas, or other model features.

## Source 4: Public InfoBanjir / JPS flood information

- Homepage: https://publicinfobanjir.water.gov.my/
- Role: Malaysia flood context source
- Initial decision: review fourth
- Direct training use now: no

Public InfoBanjir may be useful for flood monitoring context, but historical
access and machine-readable availability must be reviewed before using it.

## Decision

The first implementation target should be a small ReliefWeb discovery script
because it is public, JSON-based, and useful for discovering Malaysia flood
reports without committing to a target-label dataset too early.

## Next Implementation Step

Create a source discovery module that can query ReliefWeb for Malaysia flood
reports and save reviewed metadata into a local, non-training discovery report.
