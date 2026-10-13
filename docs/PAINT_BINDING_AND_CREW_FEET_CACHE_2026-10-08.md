# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: paint binding attribution and cache invalidation fix.

## Objective and acceptance
Continue full PC/Mac readiness. Optimize executed work and fix invalidation bugs while preserving selected pixels/clocks/layering. No release/FPS certification from diagnostic samples.

## Accepted decisions and constraints
Do not pursue blanket renderer-state binding rewrite: simple fast path already dominates. Door crew-foot cache may reuse stable same-frame positions only for same station and cell scale. Store numeric owner identity, not a retained scene reference. Preserve existing dirty source and paired UIDs.

## Current state
Normal scripts/grid_canvas.gd: crew_feet cache key adds cell scale and station instanceID alongside frame counter; reuse size for lift/companion conversion. Existing grid UID unchanged. Added tests/test_render_crew_feet_cache.gd and unique paired uid://dco4nete82bql; registered performance-diagnostics in tests/index.json. Prior hundreds of dirty grid changes preserved; this turn only small cache-key edit, no monolith refactor.

Private paint-census-contents/large/grid and paint-stage variants, runners, immutable packs, results under output/renderdoc-tools-2026-10-08/{paint-binding-census,paint-stage-census}. Actualdebug=false40room/fourcrew three60frame idle phases, explicit unique contents source bound to ordinary/large canvases. Diagnostic timings include hooks, not FPS acceptance; shorter chronology differs from9x180 so lower1734.531MiB peak is NOT memory saving.

## Verification
Binding census: large23817simple paints/~299800us, only107librarybase/149ordinaryprop paints; ordinary28938simple/~411535us, others actor362/crew1086/librarybase149/prop_pass1110/prop1624. No flip/custom/dock/aquarium exclusion category appears for executed library_live. Large state6fields, ordinary11-13; costly full binding not dominant large path. Stage census: preparedscreens23817large/~187160us +27852ordinary/~212591us; nonstation1086/~55005us; registered effects0. Do not attribute graphics cost to unexecuted effects. Actual1x nested profile live_rooms5501us, content_draw2263/prepare287, roomsetup610, door/lightvalidation1328, env_lines982, seabed890, actors_effects1299, station3439; overlapping scopes cannot be summed. No missing art/errors/leaks/unfocused samples, adapters restored, owners2936same, bothjobs terminal.

Cache correctness fixture: old9checks/6failures; fixed initial9/1 due fixture process_frame signal before framecounter increment. Corrected observable frame-change wait; original method via retained candidate source9/6fails, normal source native9/0 and headless9/0. Checks current crew/companion pixel coordinates/lift, sameframe zoom invalidation, nearest door-depth query, station replacement, reuse counts and nextframe refresh. Normal source fixes these independently of historical2/13counter issue; no claim that this explains it. Test substitutes scale/actor providers, not full room pixel certification. Owners2936same all runs. Scoped whitespace/indexJSON/uniqueUID checks pass. No packaged build contains fix yet; release gameplay/visual checks pending. No aggregate FPS benefit measured.

## Next action
Prioritize door/light validation and remaining executed preparation/submission cost; nearest crew gather already cached, avoid duplicate caches. Candidate cache key adds a cheap scale/ID check to hits; include in next actual normal-source profile and camera/door motion regression. Prepared monitor waveforms measurable, but registered effects absent and earlier typed preparation already installed; avoid repeating old work. Keep full original bug/load/memory/endurance/transitions/targetPC/M1/signing/notarization/frozen-package gates open. Current control EXE restored; obsolete candidate/ordinaryQA recovery contracts still apply. Disk remains constrained.
