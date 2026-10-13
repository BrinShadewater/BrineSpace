# Lossless moving-station and PNG payload checks

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Validate the latest private lossless loaders with installed UI/grid changes at
successive animated station states, and cover corruption beyond PNG header checks.
This advances visual/reliability admission evidence; uncaptured performance and
the full PC/Mac release gates remain required.

## Accepted decisions and constraints

Provider stays private. No new production edits, art conversion, reduced quality,
animation timing or gameplay changes. Tests use scratch profiles, muted secondary
display, disabled input, owner fingerprints and the existing physical release
runtime/art packs. Script overlays only; avoid a screenshot batch.

## Current state

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`indexed-payload-corruption-validation/`, `indexed-moving-station-verification/`.
Runners/comparator in `output/renderdoc-tools-2026-10-08/`:
`check-indexed-payload-corruption.py`, `run-indexed-moving-station-verification.py`,
`compare-indexed-moving-station-verification.py`.

Moving lanes reuse the previously validated art packs, overlay current script
inputs/hardened loaders and the installed inspector pooling. Current surface-key
function is applied to indexed dispatch. Both lanes use the same fixture-only
survey/notification/light clocks and the established hidden-capture-HUD guards.
Hashes retain each capture; six ordinary final witness screenshots remain.

## Verification

PNG fixture: 77-byte file with valid signature, IHDR, chunk structure/CRCs and IEND,
but intentionally invalid compressed IDAT data. Eighteen actual debug=false native
checks pass: index/palette recovery, exact original pixels and accounting, synchronous
and actual worker loading, consumed jobs and session cleanup.

Godot emits four expected codec diagnostic groups (one warning and three errors
per attempted decode). The copied wrapper initially rejected any engine error,
despite native exit zero and all checks passing. Corrected wrapper validates exactly
those four groups and rejects all others. Existing native result/log revalidated;
no unnecessary native rerun. Original failed wrapper outcome/log retained. These
deliberate corruption errors do not relax packaged-art or unexplained-error gates.

Six actual debug=false native Windows RTX 4070 Ti 1080p lanes: reported 12-room,
frozen current 10-room and deterministic 40-room saves, reference/indexed each.
Idle/pan/zoom/lighting at 1x/2x/4x. Samples at logical frames 0/30/60/89, plus
actor-free workshop case transitions where available. Simulation pauses briefly
for each render to settle; screenshot readback makes FPS figures unsuitable.

| Map | Exact rendered samples | Exact paired phase states/cameras | Peak texture MiB reference → indexed |
|---|---:|---:|---:|
| Reported 12 | 52/52 | 12/12 | 1558.786 → 1528.257 |
| Current 10 | 48/48 | 12/12 | 1940.676 → 1942.066 |
| Large 40 | 52/52 | 12/12 | 3028.007 → 2629.410 |

All **152** sample pixel hashes, crop rectangles, clocks, complete gameplay state,
camera, light levels and terrain context match. Only save timestamp excluded.
Current lacks an actor-free workshop, hence no four case-transition samples there.
Large witness visually inspected: station/props and inspector are unobscured;
preserved source art/UI appearance within this witness's scope.

Actual drone movement sampled: current active drone has 18 distinct positions;
four large-station drones have 27/38/37/35. Observed states include outbound,
working, returning, docking and docked, with launching also on current. Reported
station drones remain docked; do not claim moving-drone coverage on that map.
These successive settled-clock samples are not every frame of every animation
join, continuous native frame pacing, all flood states or cross-platform acceptance.

Large captured texture peak saves 398.598 MiB (~13.16%). Current peak increases
1.390 MiB in this captured replay; savings are not universal. This is resource
observation during readback/capture, not latest uncaptured memory/FPS certification.

Both owner guards: 2938 files unchanged. Jobs terminal; runtime override restored
to guarded empty fixture. New evidence ~55.52 MiB; C 123.01 / D 69.96 GiB free.
Existing art/runtime reused, no screenshot batch or source-art copies.

## Next action

Run matched uncaptured latest-provider comparisons with installed grid/UI changes,
bounded upload/cache diagnostics and full state checks. Use actual cache/fallback
execution counters to investigate the current-map peak before admission. Preserve
movement/pixels/timing and scene release; keep redraw/4x simulation stalls in scope.
Frame gates, target GPU/M1, broader gameplay/visual/endurance, packaging and signing
remain open. No release certification or itch.io action.
