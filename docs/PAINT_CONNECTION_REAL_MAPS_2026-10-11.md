# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: real-station connection-cache verification

## Objective and acceptance

Improve PC/Mac performance without changing selected art or gameplay. Accept
optimizations only after matched workload and behavioral checks; full release
certification remains open.

## Accepted decisions and constraints

Keep the previously accepted door-membership, station-target sort and zoom-group
scheduling improvements. Leave the new reciprocal connection cache private:
its real-map pilot does not establish a useful overall gain. Tests are muted,
on the secondary display, in isolated profiles. Preserve owner saves and layouts.

## Current state

No production scripts changed in this trial. Private artifacts live under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/` in
`connection-query-attribution`, `paint-connection-trial` and
`paint-connection-pilot`. The pilot's `comparison.json` holds the results.

The cache holds boolean reciprocal cell-pair results only during synchronous
grid/surface paint; preview copies and outside-paint queries use the original
predicate. It clears at the end of outer paint. This relies on topology remaining
unchanged within a synchronous paint; tests establish changes between paints,
not arbitrary mutation during an active scope.

## Verification

Private native/headless oracle: 314,500 checks, zero failures. Checks cover room
definitions, rotations, footprint cells, cardinal neighbors, branches, reciprocal
results, nested scope, preview bypass, outside queries and between-paint mutation.

Six actual debug=false native gameplay runs: one reference/candidate pair for
each map, 9,720 frames total. Lighting, connected placement and successful
demolition at 1×/2×/4×; 180 measured frames per phase. All 27 full states/cameras
and 45 successful paired actions match exactly. This is a pilot, not the required
three-run candidate certification or comprehensive visual acceptance.

| Map | Mean frame ms before → trial | p95 ms before → trial | p99 ms before → trial |
|---|---|---|---|
| Large, 40 rooms | 24.473 → 24.513 | 40.356 → 40.164 | 51.818 → 51.686 |
| Owner current, 10 rooms | 11.876 → 11.776 | 17.057 → 16.730 | 26.797 → 26.505 |
| Reported, 12 rooms | 12.318 → 12.416 | 17.655 → 17.723 | 20.826 → 20.804 |

Large-map door preparation improves only 1,113.141 → 1,080.647 microseconds per
sample. Whole-frame outcomes are mixed: current about 0.85% better, reported
about 0.80% worse, large about 0.16% worse. No reason to expand or install this
cache. Frames over 50 ms: large 18→19, current 0→0, reported 1→2. No frame over
100 ms in these runs. Every map still fails the p95 gate; large/current fail p99.

Separate two-run query attribution: 3,240 frames; 9 states/cameras and 15 actions
exact. Original connection-predicate work averages 0.710 ms on lighting phases,
0.498 ms placement and 0.482 ms demolition. Reciprocal repetition exists, but
the cache's lookup/key/scope work erodes the theoretical saving. Attribution
instrumentation is not a frame-rate acceptance result.

Owner fingerprints unchanged: 2,938 files before/after both runners. Runtime
override restored; native jobs terminal. Accepted Main/Grid/Bill source hashes
unchanged. Eight completed generated trace JSON files compressed in place,
31,631,464 logical bytes, every content hash unchanged. No new screenshots or
runtime/source-tree copies. Free space checked: C: 134.82 GiB, D: 68.50 GiB before
compression; both above the 20 GiB floor.

## Next action

Measure exterior actors and foreground draw stages separately before proposing
another optimization: harvest sites, drones/probes, humans, door overlays and
effects. Existing callback evidence puts exterior actors at roughly 1.2–1.6 ms
and foreground at roughly 1.3 ms. Avoid repeating rejected shadow/style,
rotation-working-copy or connection-cache trials unchanged.

Full PC/Mac frame/loading/memory/endurance, original bug coverage, packaged
save/UI workflows, hardware testing and Mac signing/notarization remain open.
