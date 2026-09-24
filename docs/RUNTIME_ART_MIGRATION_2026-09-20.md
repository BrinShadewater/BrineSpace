# Runtime art migration handoff

Updated: September 20, 2026 · Project: BrineSpace

## Objective and acceptance
Restore runtime image bindings broken by the bought-art migration; keep scene
behavior and authored layouts intact. Establish scoped evidence before Mac work.

## Accepted decisions and constraints
No Higgsfield. Preserve owner layouts and library marks. `legacy/retired` is a
storage location, not proof that all its art is unused: hidden original furniture
can still load for initialization, collision bounds or directional views.

## Current state
Updated eight scripts: power_room_view, tidal_condenser_view, cold_store_view,
galley_view, workshop_view, observation_room_view, construction_drone_bay_view and
command_center_view. Paths now reference existing migrated originals. Observation
shelves-down lives in legacy/default; the other directions live in legacy/retired.
Power machines use three explicit paths to avoid exporting an entire archive root.
No source pixels, cards, layouts or owner data changed in this repair.

Added tests/test_runtime_room_art.gd with paired UID, registered in room-art.
It initializes Grid and forces hidden loaders in all four directions. Added a
release-manifest regression for formatted legacy paths and explicit bindings.

## Verification
Evidence: output/runtime-art-paths-2026-09-20/.
- Before: 88 directional checks, 100 missing-image failures, exit 1.
- After: same check, zero failures, exit 0.
- Native catalog: ten live room identities, 40 captures, no warnings/errors.
  Visually inspected q0 overview; no claim of full rotation aesthetic acceptance.
- Read-only release closure: 15,382 paths; eight sampled migrated bindings included.
- Five release manifest/assert-safety tests pass; diff whitespace check passes.

Native editor execution and dependency closure do not establish a working exported
release. No export, signing, notarization or Mac execution was performed.

## Environment and foundation follow-up
scripts/grid_canvas.gd now uses five explicit FOUNDATION_PATHS. The room regression
passes 93 checks including all five, and release closure excludes rejected weathered
candidates. Source pixels and placement rules are unchanged.

The station fixture exposed 51 logged missing environment paths; a new exhaustive
runtime check also found silently skipped seabed and wreck textures. Repaired 21
ROOT constants under assets/environment, and changed those loaders plus rock_view
(22 scripts total) from Image.load to SafeImage.load_png for raw export loading.
New tests/test_runtime_environment_art.gd (paired UID, underwater group) exercises
19 prop/terrain packs, six base seabed images, eight wreck stages and basalt.

Evidence in output/runtime-art-paths-2026-09-20/environment/:
- before.log: 66 checks, 65 failures; after.log: 66 checks, zero failures.
- release-closure.json: all 66 required paths selected.
- native-lit.log: powered five-room station, no warnings/errors.
- station-default.png: normal gameplay fog; lit core reveals terrain and supports.
- station-fog-hidden-diagnostic.png: diagnostic only, fog hidden for art inspection.
- Five release manifest/assert-safety checks pass.

The reused riser fixture omitted a powered core and could capture before camera
settlement. Its corrected review copy recenters, waits for retained-layer state,
and includes a powered core. Fog is unchanged in production. Do not infer missing
terrain from a fully dark, unpowered fixture. This does not prove every biome or
wreck is aesthetically accepted, nor that an exported executable works.

## Next action
Diagnostic capture visually reviewed: supports align beneath the south room edges;
restored seabed and scenery are visible with fog hidden. Return to Bill's walking
body motion next. Before
Mac release work, run the maintained exporter and actual release gameplay checks;
editor execution and dependency closure are insufficient. Retain the composition
pilot for owner review before wider decoration rollout. Audit-tool metadata that
still assumes pre-migration raster roots needs migration-aware handling when used.
