# BRINE corner side review - September 12, 2026

Objective: improve inward access and the owner-disliked side camera while preserving the established corner installation.

Inspected both original full-resolution corner sources and their registrations. Northwest source combines north tank/filter/cylinder equipment with a vertical monitor/console/cylinder arm. Northeast combines north sample/analysis equipment with a vertical filter/control arm. These are existing artwork, not absent directional assets.

Generated corner-nw-side-study.png with exact prompt and review JSON under assets/brine-core-directional-v1. Rejected at source review: right-facing buttons/catches and cylinder shoulders improved, but the north arm also changed and upper west instruments became blank covers. No runtime registration/default/card changed. No tests run for an uninstalled rejected source.

Next: tighten the northwest brief with per-bay instrument inventory and verify north-arm preservation before installation; then review northeast. Current live corner sources remain authoritative. Full catalog and owner camera acceptance remain open.


## Inventory-preserving NW revision selected

Added corner-nw-inward.png and exact inventory prompt. Six west-arm screens, two bottles and lower cabinet retained, with handles/button rows on inward right edge. Full corner source repainted, including north pixels; functional north inventory retained. This is a facing correction, not completed idle-state repair: painted traces remain. Native q0 reviewed; comparison across four quarters confines RGB changes to NW bank and all prop metadata stays unchanged. 176 layouts and 20 variants pass at output/test-runs/20260912-120537-headless. Refreshed corner-cards/brine_core.png and three consumers. No export. NE arm and state/camera acceptance remain pending.


## Northeast access correction selected

Added corner-ne-inward.png, exact prompt, original registration and review JSON. Retains two four-roll cassettes, grille, angled console, lower screen and cabinet. Catches/buttons/handles now inward left. Source lower arm grew; aspect-preserving registration retains original world bounds/collision boxes. Native q0 reviewed; four-quarter comparison confines pixels to NE bank, all prop metadata unchanged. 176 layouts and 20 variants pass at output/test-runs/20260912-120927-headless. Card refreshed to corner-ne-cards and three consumers. No export. Painted display traces and final owner camera/state review remain unresolved.

## NW idle source prepared

Created corner-nw-idle.png via built-in imagegen with exact prompt. Ten screen apertures preserved (six west,three north,one corner), signals removed, buttons quiet. Four bottles/two filter cassettes retained; north bottle details repainted. Candidate vector registration keeps existing contain frame and metadata in assets, not live library. LFS verified. Runtime screen anchors/effects, direct/retained state review and card refresh remain before selection. Source review recorded in corner-nw-idle-review.json; live source unchanged.

## NW quiet state integrated

Installed idle source registration with ten operating_screens rectangles. room_asset_library draws time-based traces only while operating, using registration coordinates; brine_core_view classifies these props animated. Direct/retained six native captures:20screen cases have active and temporal changes. Native direct on-a and refreshed nw-idle-cards card reviewed.176layouts/20variants pass20260912-131937-headless; three card bindings updated and47identity parity passes. Evidence output/brine-nw-state-2026-09-12. NE and other painted BRINE signals, owner visual acceptance and pause-transition proof remain. No export.

## NE quiet state integrated

Installed corner-ne-idle.png with five source-local operating screen rectangles, preserving contain frame and collision metadata. Filter/sample/cylinder inventory retained. Direct/retained six captures:10screen cases pass active/temporal pixel checks; direct on-a and updated idle card reviewed.176layouts/20variants pass20260912-132557-headless;three card bindings updated,47identity parity pass. Evidence output/brine-ne-state-2026-09-12. Both corner screen banks now distinguish idle/working. Other BRINE painted screens, owner visual acceptance and pause-transition proof remain. No export.

## Riser idle source prepared

Created riser-idle.png and exact imagegen prompt; two painted wall displays quieted, source reviewed. Live riser unchanged. grid_canvas draws north_wall in cached Surface.WALL, so runtime signals need a dynamic pass before source selection. Power/temporal/shared-wall checks and card refresh remain. See riser-idle-review.json.

## Riser idle/dynamic split integrated

Idle texture selected in north_wall. Separate draw_brine_signals; grid cached WALL excludes signals, LIVE adds them only for visible raised fixtures. Two displays have active/temporal changes in direct and retained-content fixtures (architecture itself direct in both).176layouts/20variants pass20260912-133311-headless. Native direct on-a and refreshed riser-idle-cards reviewed;three bindings/47identity parity pass. Full station cache/power/pause/shared-wall verification still pending; do not claim fixture proves cached surfaces. Evidence output/brine-riser-state-2026-09-12.

## Actual station riser verification

Both raised-wall displays pass power, temporal and explicit paused-process pixel checks in the actual station renderer. Cached wall rebuilds remain 5 across both powered frames and paused frame; native on-a image reviewed and capture exits 0. Evidence: output/brine-station-wall-2026-09-12/{runtime,checks}.json and capture.log. Updated riser-idle-review.json. Low/shared-wall visibility and owner side-view acceptance remain open; this is technical verification, not aesthetic acceptance. No export.

## Visibility guard verification

Native visibility.gd exits 0 and asserts exposed/low/hardware-off/synthetic north occupancy/restored states. Low-wall screenshot reviewed: riser signals disappear with their architecture. Synthetic occupancy tests the guard only, not realistic neighbor geometry. Capture logs also contain environment texture errors, so exit 0 is not an error-free whole-station claim. Updated review JSON. Added actual cached-wall verification lesson to project and installed full-wall pipeline reference and visual bible. Other displays and aesthetic side-view work remain.

## South service idle source integrated

Selected service-south-idle.png with contained vector registration and one source-local operating screen; original source and previous registration preserved. Updated side-brine-memory-service-south.json and all three current card bindings to south-idle-cards. Native direct/retained powered and idle card reviewed. Six capture processes exit 0, isolated display crops change with power/time in both paths, 176 layouts and 20 variants pass 20260912-145622-headless, 47 card identities pass parity. Evidence: assets/brine-core-directional-v1/service-south-idle-review.json. Station pause for this display and owner aesthetic acceptance remain open. No export.
