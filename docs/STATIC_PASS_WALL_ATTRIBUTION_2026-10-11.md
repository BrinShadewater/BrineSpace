# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: remaining zoom redraw costs

## Objective and acceptance

Measure static-pass character preparation before removing it, then identify the
substantial remaining wall redraw work. Attribution is not performance acceptance.
Preserve exact gameplay/camera/UI state and existing playback calls.

## Accepted decisions and constraints

Muted secondary display, isolated profiles, owner fingerprints, reused debug=false
runtime with small script overlays. No screenshots/art copies, gameplay changes,
quality reduction or production edits. Wrappers call original methods exactly once;
timing records retain at most eight process frames.

## Current state

Private probes/evidence in
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`static-actor-sampling-attribution`, `static-room-pass-attribution`.
Corresponding runners in `output/renderdoc-tools-2026-10-08/`.
Initial private actor probe mixed spaces/tabs and failed parsing. Corrected before
accepted run; `parse.log` preserves diagnostic. Failed launch proves no acceptance.

## Verification

Two native 1080-frame large-station replays, idle/pan/selection/zoom-selection at
1x/2x/4x. Each matches the installed control's 12 complete phase states/cameras
and 54 UI snapshots: 24 matched phases/108 paired UI snapshots overall.
Accepted logs clean; owner guards both 2938 unchanged.

Tracked getters: Branforth 1080 live calls, nine floor and nine shell calls.
Static total 1.568 ms across all frames, mean 0.00145 ms/frame, max 0.198 ms.
All tracked getter mean 0.0836 ms/frame. Bill/Veld/Marsh getters not exercised;
companions' own texture functions not instrumented. Do not generalize this to all
actor work. Removing these static getter calls does not address this workload's
large stalls, and may affect playback state. Keep production calls unchanged.

Nine wall redraw frames have detailed per-pass attribution. Representative slow
2x zoom frame 76:

| Shell pass category | ms |
|---|---:|
| Render submission | 4.756 |
| Room configure | 2.038 |
| Door setup | 1.198 |
| Crown callback | 1.015 |
| Actor preparation block | 0.474 |
| Companion preparation block | 0.168 |

Getter timing is nested inside actor preparation. Existing global profiler stages
also overlap these measurements. Instrumentation overhead is present; do not claim
additive whole-frame savings. Solar arrays contribute most among room types in
this sample (~1.390 ms across measured shell substages).

Checked [Godot's supported triangle-array API](https://docs.godotengine.org/en/stable/classes/class_renderingserver.html#class-renderingserver-method-canvas-item-add-triangle-array).
Current modular floors already draw meshes; October 6's
`LARGE_BASE_QUADS_TRIAL_2026-10-06.md` rejects the equivalent rectangle-to-triangle
approach on station timings. No repeated batching experiment or renderer upgrade.

Jobs terminal and runtime override restored. Evidence 12.19 MiB plus 5.67 MiB
scratch; C 122.95 / D 69.53 GiB free. No deletion-policy bypass attempted.

## Next action

Private size-only wall-slot settling experiment: retain each slot's complete old
commands at the correct scale, rebuild a bounded number during landed zoom, and
keep any structural/layout/door dependency change immediate. Ensure the settling
backlog cannot finish early and newly revealed/interactive rooms are complete.
Check native pixels, zoom/Fit behavior and matched station performance before
admission. This is a hypothesis, not an installed fix. Full release gates and
large mining-rover upload stalls remain open; indexed provider remains private.
