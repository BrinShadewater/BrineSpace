# Project handoff

Updated: September 8, 2026 · BrineSpace · Directional registration evidence

## Objective and current state
Strengthen asset-placement records. The existing directional audit now compares
recorded registration paths and hashes with the indexed outline. A changed crop
or polygon can no longer pass solely because its source PNG is unchanged.

## Verification
Sixteen focused tests pass, including outline mutation, path substitution and
explicit legacy coverage. Both four-view chart-counter and mechanical-tool families
pass the stronger audit. Reports: `output/observation-chart-registration-audit.json`
and `output/mechanical-tool-registration-audit.json`. No raster changed.

## Limits and next action
Older reviews without registration fields explicitly report false verification
coverage; their existing metadata checks still run. This is provenance validation,
not pixel, placement or owner acceptance. Material workflow updated and synchronized.
Continue asset production using the guarded records.
