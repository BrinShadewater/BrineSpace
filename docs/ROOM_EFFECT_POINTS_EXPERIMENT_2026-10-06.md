# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: animated room drawing

## Objective and acceptance

Reduce measured room-content overhead without changing pixels, clocks or layering.
Full PC/Mac release performance and certification remain open.

## Accepted decisions and constraints

**Do not admit this prototype yet.** Fixed hologram circle samples and preallocated
monitor/hologram point arrays show a small focused saving. The copied station
fixture was later found to load the earlier external content renderer in both
branches, so its station comparison is invalid as optimization evidence.
Normal runtime remains unchanged.
No quality changes, exports or owner profile writes.

## Current state

Private original/candidate libraries, preparation scripts, native comparisons and
unadmitted oracle/test drafts retained in `output/room-effect-points-2026-10-06/`.
No new permanent test/index or runtime changes. Floors already use texture-grouped
ArrayMesh geometry caches; do not propose initial floor batching as missing work.

## Verification

Private native comparison: 510 checks / 406 exact raster pairs pass, including
179 current station registrations, synthetic screen/effect clocks, Reduced Motion,
nearest/linear filtering, affine tint and current flooding shader. These are
metadata-driven effects tests, not complete prop artwork or release certification.

Three alternating native preparation pairs draw all 179 registrations per callback:
2527.8→2413.1, 2606.5→2461.9, 2739.97→2593.7 microseconds (~5% focused saving).

Invalid optimization comparison (fixture wiring discovered in the next turn):
native 40-room, 1080p, idle/pan at 1/2/4x, 60 samples per phase:
content callback candidate-minus-reference deltas +60.4, +3.2, +46.3, +1294.5,
-1010.6, +27.6 microseconds. Opposite outliers and mostly unchanged/slower phases
do not measure the candidate library at all. Recorded p95 37.9–48.0 ms still fails the
16.7 ms target. No aggregate FPS benefit claimed. Both fixtures use private
compressed crew and the accepted room context; they are not packaged release runs.

All six actual crew/drone snapshots, powered-room counts, zoom and texture counters
match. Final texture memory 3168.333 MiB, unchanged and above the 3072 MiB budget.
Successful logs clean; all 2936 owner non-log files unchanged. All processes terminal.

## Next action

Correct the explicit content preload and assert the candidate path actually executes
before repeating this experiment's station comparison. Investigate retaining static
monitor commands or cached screen geometry, especially
radar rings/grid lines, with native exact comparison and ordered overlapping screens.
Avoid extrapolating focused array-allocation gains to the station. Rendering masks
remain diagnostic only. Larger frame, memory, loading, lifecycle, original bug,
endurance and actual packaged Windows/Mac acceptance gates remain unresolved.
