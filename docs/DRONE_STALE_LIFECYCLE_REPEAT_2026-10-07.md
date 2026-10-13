# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: stale drone cleanup lifecycle and repeatability

## Objective and acceptance
Reduce stale lookup texture memory with immutable image ownership preserved, no
duplicate uploads and bounded runtime overhead. Full PC/Mac release scope remains.

## Accepted decisions and constraints
Private candidate only. Classify as a transient memory improvement, not a verified
FPS gain or compliance with large-scene memory budget. No changed art or filtering.

## Current state
New driver `output/compressed-crew-2026-10-06/test-drone-stale-lifecycle.py`;
private native lifecycle probe/results in `output/drone-stale-lease-2026-10-07/lifecycle/`.
Gameplay runner/comparator now accept `--reverse`; second pair and instrumentation
in `output/drone-stale-lease-2026-10-07/gameplay-reversed/`.
All physical normal Motion/SessionArtCache/flood inputs restored byte-exact.

## Verification
Native lifecycle probe:14 checks/zero failures/errors/warnings/leaked instances.
Stale second entry removes despite recent first entry; exact byte accounting;
expired weak metadata pruned; reports read-only. First owner exit retains cache
lifecycle; final owner drains workers, clears all image lookup bookkeeping and
disconnects trim; two subsequent frames execute no callback. New scene reconnects,
loads the actual invisible PNG correctly, and final exit cleans again.

Reversed native40-room1080p idle/pan/zoom1/2/4x pair,60 frames per phase:
all9 full crew/drone/door/light/zoom/power states, pinned image metadata and
viewport dimensions match. Both98 uploads, phase upload counts equal.
Again exact64,225,188bytes less at zoom2x, other8 texture endpoints equal.
Thus both matched comparisons reproduce the61.24991MiB transient savings.
Both clean exits/logs; no>100ms frame in this pair (historical104ms stall open).
Median phase means37.3501->37.55043ms; p95mixed, no overall FPS gain.
Candidate720 trim calls,total23,982us,mean33.31us,max791us,17 removed lookups,
20 weak entries at endpoint. Includes release work in trim timing; these are
CPU wall times in this run, not driver/GPU-time guarantees.
Each owner fingerprint2,936 files unchanged; all processes terminal.

## Next action
Third matched comparison to meet three-run candidate target, then normal-budget
runtime drone/session tests before deciding source admission. Preserve the
native pixel/lease probe and lifecycle test as regression coverage if admitted.
Do not overinvest in this61MiB saving: larger crew memory and zoom redraw stall
still dominate the outstanding release performance work.
