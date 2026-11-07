# Failed drone route reuse

Updated: October 5, 2026 · BrineSpace · R4

## Objective and acceptance

Remove repeated unsuccessful path searches in the actual fleet update, preserving
movement, job timing, rewards and immediate recovery when topology changes.

## Accepted decisions and constraints

Enabled in source. Failures are keyed by origin and destination within a fleet's
current blocker topology. Compare blocker contents rather than allocation identity
or a hash; clear on any change and on restore. Limit the cache to 64 entries and
do not persist it. Successful routes retain their existing per-step validation.
Normal drones still travel beneath rooms; room-door fallback remains available to
other route callers. No cooldown, search truncation or gameplay changes.

## Current state

- `scripts/drone_fleet.gd`: owns the transient cache, invalidates after assembling
  wreck/site/queued-order/assigned-order blockers, and passes it to travel. Skips
  the topology comparison when there are no failures to invalidate.
- `scripts/drone_routes.gd`: reuses a cached empty route; avoids the second BFS
  when boolean blockers make its traversal rules identical. Dictionary blockers
  retain the existing room-port fallback. Standalone travel calls remain uncached
  unless supplied a caller-managed failure cache.
- `tests/test_drone_route_cache.gd` and paired UID; registered in the performance
  and gameplay groups. Existing runtime UIDs unchanged.

## Verification

Headless Godot 4.7.2 tests use guarded scratch APPDATA. **33 new checks pass**:
repeated failure, immediate excavation recovery at 1x/2x/4x, site depletion,
queued and assigned construction removal, changed destination/return phase,
changed origin, equal-sized topology replacement, restore, port fallback and
bounded cache. Six existing suites pass: drone fleet, jobs, lifecycle, battery,
work face and finite harvest. These include paid construction, checkpoint and
legacy restore, pause, one-time rewards and backtracking around new obstacles.

Matched instrumented comparison calls the real `Fleet.advance` using a dispatched
construction drone whose target is enclosed by four wrecks. Nine pairs (three per
simulation speed) each measure 60 blocked updates, then open a passage and compare
650 updates. **5,859 full snapshot/completion comparisons match**. This verifies
production-caller behavior in a controlled fixture, not prevalence in an owner save.

| Measure, 60 blocked fleet updates | Original | Candidate |
| --- | ---: | ---: |
| BFS searches | 120 | 1 |
| Expanded cells | 191,400 | 1,595 |
| Median elapsed across nine samples | 177.688 ms | 2.005 ms |

Both source copies have the same search/visit instrumentation. Full evidence,
frozen reference sources, final source hashes, scripts and logs:
`output/drone-route-cache-2026-10-05/`. Final focused validation reran the new
checks/comparison after avoiding unnecessary empty-cache topology comparisons.
All run groups preserve **2,936 owner non-log files**, with zero engine errors.

No art/rendering change. No native frame-time, packaged release, memory reduction,
Mac or minimum-hardware acceptance is claimed. Long stalls and texture budgets
remain unresolved; this only removes repeated work when a travelling drone cannot
reach its destination.

## Next action

R5: measure terrain-layer invalidation while excavation progress changes. Confirm
which visible output actually changes before narrowing redraws. Keep normal
station and packaged platform performance gates open; do not extrapolate this
blocked-route fixture's reduction to overall FPS.
