# Hydroponics south-facing art candidate

The existing `hydroponics_bay` identity uses a cross layout. No gameplay data,
costs, unlocks or production changed in this art pass.

`rooms/whole-room/hydroponics_view.gd` registers four assemblies from the retained
generated candidate and uses the shared deterministic shell/embedded interface.
Ground centers rotate; art and footprint dimensions remain south-facing. Floor
depths follow the depicted top planes rather than full sprite height. Irrigation
marks, nutrient bubbles and a console trace use the operating clock and stop
offline. These are visual activity cues, not new simulation systems.

`tests/playtest_south_facing.gd --hydro` passes all four layouts, 16 front/behind
comparisons and continuous routes, ground anchors, bounds, cross ports and
room-level active/offline/pause checks. Logs: `hydro-depth.log`, `hydro-floor.log`
under `output/whole-room-pilot-01`. The second pass replaces a floor sample that
included a baked panel joint; native q0 before and q1 after were inspected.

Generated source, prompt, guide, hash and review record are in that output folder.
The runtime candidate PNG has the Git LFS filter. Some nutrient-skid perimeter
plumbing remains outside its silhouette. This is isolated registration, not
station/card acceptance or owner approval. Next: matching card, actual-game
consumer integration, mixed-room seams and viewport/overview verification.

## Station integration follow-up

Hydroponics now uses the layered renderer in the actual grid, including previews,
shared-wall ownership and crew rendering. Main uses the new Godot-baked
`hydroponics-card-v1.png` with aspect-preserving card display; legacy art remains
on disk. The card PNG has the LFS filter. Costs and production are unchanged.

`playtest_whole_room_station.gd --hydro` selects Hydroponics as the distinct
neighbor. `hydro-station-1280.log` passes four orientations, 404 actual walker
samples, shared-wall pixel checks, operating/offline comparisons and 40-room
fit bounds at 1280x720. The q0 pair/card capture was inspected. Screenshot names
retain the historical `life` prefix, but the log identifies the selected room.
Wider viewports, post-integration regressions and owner approval remain pending.

## Wider verification

`hydro-station-1600.log` and `hydro-station-2560.log` pass the same actual-consumer
rotation, wall-pixel, route, operating/offline and mature-fit checks. Together
with the 1280 run, the three target 16:9 viewport sizes have technical coverage.
Reviewed the 1600 q3 vertical pair and 2560 mature capture: planted beds retain
a distinct green identity, while legacy Bio Lab art remains visibly inconsistent
with the new clean pack. These are visual findings, not owner approval.

All five post-integration suites pass with no `ERROR:` or `SCRIPT ERROR:` entries:
`test_synergy_manager-hydro.log`, `test_discovery_progression-hydro.log`,
`test_polish_gameplay-hydro.log`, `test_run_balance-hydro.log` and
`test_nursery_gameplay-hydro.log`. The integration is verified for the documented
scope. Remaining room identities and other asset groups in the expansion ledger
are not completed by this Hydroponics checkpoint.
