# Crew Hab matte berth handoff

Updated: 2026-09-12. Project: Brine Space.

## Objective and acceptance
Continue room art improvements. The east berth already has the overhead camera; this pass addresses material glare and painted-on illumination while preserving inward access.

## Accepted decisions and constraints
Warm habitation materials and personal inventory remain. Preserve other authored directions, geometry, original raster and LFS. A reading lamp should remain steady rather than flicker with machine time.

## Current state
Selected assets/crew-hab-directional-v1/east-matte-idle.png in side-crew-hab-berth-wall-east.json with source-local reading_lamp polygon. Prior registration and exact prompt preserved. Full-wall/library decoders carry optional lamp metadata; crew_hab_view draws the powered diffuser in direct and retained animation paths.

## Verification
Native idle and powered east reviewed. Baseline/installed catalogs exit 0; q0/q2/q3 RGB and all prop metadata identical. 176 preferred layouts and existing 20 variant regressions pass 20260912-152023-headless. Existing q0 card retained. Direct/retained lamp checks tracked in output/hab-east-matte-2026-09-12/checks.json.

## Next action
Six native state captures exit 0. Both direct/retained lamp crops change with power and remain steady across operating times; retained powered east reviewed. Continue other authored berth finishes and remaining rooms. Owner aesthetic acceptance remains open. No export or commit.

## West authored mate selected

Selected west-matte-idle.png through side-crew-hab-berth-wall-west.json, preserving its own personal-item arrangement and right-side access. Own reading_lamp polygon uses existing steady runtime overlay; no further code changes. Original and previous registration retained. Native idle/powered west reviewed; six state captures exit 0, direct/retained lamp crops active and steady, 176 layouts and 20 variant regressions pass 20260912-152547-headless. q0/q1/q2 RGB and all placement metadata unchanged, so existing card retained. Evidence: assets/crew-hab-directional-v1/west-matte-idle-review.json. Actual station pause, remaining horizontal finishes and owner aesthetic acceptance remain open.
