# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normal large-room retention admission

## Objective and acceptance

Install the measured large-room rendering improvement with exact selected appearance, responsive state changes, scene cleanup and accurate diagnostics. Full PC/Mac release plan remains active and uncapped frame/memory gates remain open.

## Accepted decisions and constraints

Ordered large-room canvases retain complete Moonbay base commands; other bases and all live props still redraw. Internal and inter-room ordering follows the verified prototype, shared flooded equipment stays on its existing LIVE parent. Exact deep room/bounds/layout/Reduced Motion key omits only the generic machine_clock that Moonbay base does not read. Scene/canvas owns resources; no global image cache, art changes, animation reduction or automatic quality changes. Existing immediate rendering remains for previews and non-retained surfaces. `--immediate-large-rooms` is an internal comparison switch, not a user quality setting.

## Current state

Normal changed files: `scripts/grid_canvas.gd`, new `scripts/large_room_canvas.gd` and `scripts/moonbay_base_canvas.gd` with paired unique UIDs; `tests/test_large_room_retention.gd` with paired UID; `tests/index.json` native/render-perf registration. Grid hides only rooms outside the visible set, releases demolished/replaced/non-anchor slots, and preserves visible cached commands. The slot chain inherits parent material. Child callbacks contribute to draw time, draw counts and live-room profile totals; detailed child labels remain additive.

## Verification

Actual normal-source native test: 83 checks, zero failures, 76 exact raster pairs. Covers four large types/rotations, overlap, dry/flooded, offline, nearest/linear, material/modulation and unchanged room state across filter/material changes; helmet/port/mission/layout mutation, visibility recovery, room-type replacement, removal and observed owner release. Calls actual Grid cleanup for visibility, replacement and demolition; checks child diagnostic inclusion. Grid test stub initially allowed inherited full-world draw and logged missing fixture fields; overriding stub draw corrected it, rejected log retained. No successful run engine errors. UID uniqueness and diff whitespace checks pass.

Matched native physical mixed40-room integration pair uses current normal changed Grid functions and normal helper modules, retaining earlier private crew/drone fixture substitutions elsewhere. Twelve multi-cell rooms including three Moonbays; six idle/pan 1/2/4x phases, 60 frames each. Candidate execution: 12 slots, three retained bays, seven base redraws constant, hits715→1615. Normal live-room profile already includes child callbacks: do not add detailed child times a second time.

CPU live-room stage 17.04–17.76 ms baseline →9.79–10.38 ms candidate, ~7.24–7.47 ms/frame saved. Whole-frame p95 baseline 61.03–78.65 ms →49.24–71.31 ms; all six phases lower, but all release frame gates still fail. Full crew/drone/power/zoom/door/light snapshots equal. Texture counters vary during the pair and final candidate is lower by ~62.27 MiB; not assigned to retention, no memory saving claim. One new matched pair confirms the earlier prototype direction, not three-run packaged release certification. Private asset experiments and debug=true remain fixture limitations.

All successful isolated runs preserve 2,936 owner files and terminate cleanly. Evidence: `output/moonbay-normal-admission-2026-10-06/{results.json,owner.json,station}`. Prior exact LIVE composition including dedicated active BRINE signals has its separate scope in `docs/MOONBAY_RETAINED_LIFECYCLE_2026-10-06.md`. No actual Windows/Mac release executable exported or certified here.

## Next action

Profile and reduce remaining large-room prop drawing (previously ~4.3 ms combined) using ordered static/live separation where measured. Continue renderer/system work against whole-frame timing, rather than treating this local gain as 60-FPS acceptance. Actual gameplay demolition/save, owner layout visual review, continuous zoom/focus, endurance, memory history and packaged PC/Mac certification remain broader release work. Keep exact visual and behavioral checks for each new optimization.
