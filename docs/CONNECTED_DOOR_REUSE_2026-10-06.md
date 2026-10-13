# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: door validation performance

## Objective and acceptance

Reduce a measured rendering preparation cost without changing door access, poses,
crew layering, lighting or simulation. Full PC/Mac release readiness remains open.

## Accepted decisions and constraints

Normal Grid reuses established connectivity only when `_door_light_state` has just
validated the same edge without yielding. Other callers keep the default live
topology check. No persistent connectivity cache, asset/quality change or gameplay
decision. No export or release certification.

## Current state

`scripts/grid_canvas.gd`: optional `known_connected` argument propagated through
the render-frame helper; only the validator supplies true. Existing adjacency,
room-presence, door-lock, hardware, crew/drone and proximity checks remain.
Existing symmetric per-frame door cache remains unchanged.

`tests/test_connected_door_render.gd`, paired unique UID and render-perf index:
frozen original frame oracle, default/live behavior and established-edge coverage.
Private evidence in `output/door-validation-2026-10-06/`.

## Verification

Scoped native attribution target checked against current normal source before
instrumentation. Three idle simulation speeds: connectivity ~379–387 us, frame
calculation ~342–347 us, parts/depth ~560–594 us, light ~185–190 us, ports
~139–152 us. Diagnostic instrumentation adds overhead; no profiled FPS acceptance.

Matched native 40-room 1080p idle/pan at 1/2/4x, 60 samples per phase:

| Phase | Door/light before ms | After ms | Saving ms |
|---|---:|---:|---:|
| Idle 1x | 1.732 | 1.590 | .142 |
| Pan 1x | 1.704 | 1.578 | .126 |
| Idle 2x | 1.736 | 1.630 | .105 |
| Pan 2x | 1.720 | 1.572 | .148 |
| Idle 4x | 1.730 | 1.615 | .115 |
| Pan 4x | 1.737 | 1.576 | .161 |

All six actual crew/drone snapshots, all 30 door entries (including frame/depth
masks), full lighting keys, powered-room counts, zoom and texture counters equal.
Reuse counter 7260→16260 proves execution. Whole-frame p95 mixed and still fails
(candidate 37.536–46.843 ms); one pair establishes no aggregate FPS gain. Fixture
uses private compressed crew, distinct from normal release gameplay. Final
3168.333 MiB unchanged and above the large-scene budget.

Actual normal source: **1686 checks pass**, covering locks/hardware, missing and
disconnected/nonadjacent rooms, crew/legacy-walker branches, drone frames, distance
thresholds, symmetric render-cache reuse and same-tick live disconnect. Original
oracle variables needed explicit types after moving the function to a helper;
failed fixture parse retained, corrected without changing runtime behavior.
All successful logs clean; all 2936 owner non-log files unchanged, including failed
isolated preparation/check attempts. UID uniqueness and test-index JSON verified.
All processes terminal.

## Next action

Attribute parts/depth preparation more closely (~0.56–0.59 ms lead); `_department_parts`
already has a bounded pose cache, so do not recreate it. Continue larger renderer
submission work for commands actually present in the station. Memory/loading,
lifecycle, original bug closure, endurance and packaged Windows/Mac gates remain
open. The accepted savings are incremental; they do not make the game release-ready.
