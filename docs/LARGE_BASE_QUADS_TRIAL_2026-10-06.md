# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: repeated large-base quad trial

## Objective and acceptance

Reduce measured large-base renderer cost with exact selected output. Accept only a matched station improvement plus relevant visual checks. Original PNGs, settings, owner layouts and normal renderer unchanged.

## Accepted decisions and constraints

Private prototype under `output/large-base-quads-2026-10-06/`; no normal integration. Reject floor triangle batching: it does not reduce actual draw calls and increases preparation. Wall triangles remain unaccepted due a nearest enclosure seam. Preserve original rectangle sampling where it is required.

## Current state

Quad helper packs original float positions/colors/UVs into one triangle array. Private Common/Wall/room/retained-canvas copies and generators retained. Candidate floors share original Common art dictionary; private walls share original wall textures. Short wall tails and linear-filtered partial floors retain original commands. Current matched station candidate uses floor batches only; every Common/Tidal/Moon wall consumer is original. Source variants, captures, failed matrices and successful controls preserved.

## Verification

- Initial504-case native piece matrix:30 flags, of which24 are legitimately blank subpixel strips, four linear partial-floor differences and two nearest partial-wall differences. Corrected blank accounting and preserved tail/linear commands:504 exact pairs (480 visible/24 blank), zero failures/errors/warnings, shared image dictionaries. Owner2,936 unchanged.
- Full overlapping-room candidate initially fails18/135 checks, nearest q1/q3. First mismatch213 pixels in one vertical column. All-original control135 checks/80 pairs clean. Removing floor batches and Common/Tidal wall batches did not clear it because Moonbay's independent WallMaterial consumer remained private; earlier 'all batching disabled' interpretation was incomplete. Disabling that consumer gives clean135/80 control. Floor-only batching then independently passes135 checks/80 exact room pairs, including rotation/filter/flood/material/offline/clock/layout/filter/hide/remove transitions and ownership cleanup. No normal bug claim.
- Native matched current40-room floor-only pair: all six full crew/drone/door/light/power/zoom states equal; texture endpoints identical, no missing art/engine errors or selected ordinary duplicates. Owner2,936 unchanged, processes terminal.
- Actual draw calls essentially unchanged (idle1 6513.10/6514.03, idle2 6291.43/6291.43). Large-base callbacks increase about0.33–0.36ms per frame; renderer CPU/GPU and p95 mixed, no gain. p95 control/candidate: idle1 41.588/41.352; pan1 44.585/44.448; idle2 41.120/41.613; pan2 42.801/45.816; idle4 45.907/45.862; pan4 49.258/49.376ms. Gates fail; floor prototype rejected. Readiness13.286/12.227s is one observation, not attributable to this renderer change.
- Upstream primary-source review: Compatibility renderer records consecutive same-texture rectangle commands into batches, while polygon commands create separate batches. This is consistent with unchanged floor call counts; upstream master is not proof of this executable's exact source revision. Sources: [Godot GLES3 canvas renderer](https://github.com/godotengine/godot/blob/master/drivers/gles3/rasterizer_canvas_gles3.cpp), [Godot rendering architecture](https://docs.godotengine.org/en/4.5/engine_details/architecture/internal_rendering_architecture.html).

## Next action

Stop converting already-batched rectangle runs. Separate large-base cost by room type and actual command categories. Moonbay's water renderer emits many antialiased polyline ribbons/arcs; vertical painted door leaves use polygon commands. These are concrete candidate batch breakers, not yet attributed causes. Use matched renderer masks/counters, then optimize the measured category while preserving antialiasing, ordering, clocks, source sampling and default effects. Full provider/lifecycle/loading/memory/frame, packaged bugs, endurance and Windows/Mac gates remain open.
