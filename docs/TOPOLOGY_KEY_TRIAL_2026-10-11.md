# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: complete-input topology signature reuse

## Objective and acceptance

Reduce measured crew topology overhead while preserving exact signature strings,
locked-cell side effects, rebuild scheduling and gameplay. Private until repeated
matched native comparisons and relevant navigation/save/mutation checks pass.
Full PC/Mac release readiness remains open.

## Accepted decisions and constraints

No frame-number-only invalidation or gameplay changes. Each query reads all
original cell/id/rotation/door/branch/lock/Moonbay inputs. Hardware/layout revision
read after room queries, preserving first-load query side effects. Key includes
scalar type markers where numeric equality could hide formatting differences.
Locked-room dictionary still clears/rebuilds on hits; cached inputs deep-copied.
Actor-owned cache stores primitive inputs and owned door arrays, no world/room/art
owners. Original mutable public door ownership and raw sorted signature preserved.
Original art and production source unchanged. Muted secondary display, isolated
saves/user directory, bounded outputs, reused runtime, 20 GiB free-space floor.

## Current state

`prepare-topology-key-trial.py` writes private full Bill and a function-identical
standalone reference/candidate oracle. `run-topology-key-pilot.py` adds the same
bounded timers/counters to both full actors and source-guards loaded scripts.
No rendering changes or effects-storage trial included in either lane.

Native mutation oracle14,567 checks pass, 1,122 hits/6,162 misses. Covers empty
station, five rotation values/types, four lock values/types, thirteen Moon phases,
hardware locks, multi-cell references, changed/reordered borrowed door arrays,
branch/room locks, station-open, boarding, position type, layout revision,
caller-mutated locked dictionary, placement/demolition and weak world release.
Includes layout/hardware changes during a door query. Initial review moved final
revision/hardware reads after queries, matching original evaluation order; corrected
oracle is clean. This validates the exact function body, not the entire navigation
system or actual owner Studio mutation/input flows.

## Verification

One native debug=false RTX4070Ti/1080p mixed40-room/52-cell pair, 2,160 frames.
All12 complete gameplay states/camera paths/action-speed labels exactly match.
Source guards pass; no missing art/engine errors; owner2,938 files unchanged.
Job terminal, override restored. Texture peak2928.086MiB/end1939.219MiB equal.

| Metric | Original | Key reuse |
| --- | ---: | ---: |
| Topology us/frame | 1388.787 | 879.950 |
| Mean frame ms | 29.475 | 28.883 |
| p95 ms | 43.791 | 42.924 |
| p99 ms | 51.913 | 50.495 |
| >50ms frames | 16 | 12 |
| Maximum ms | 86.818 | 87.519 |

Topology cost -36.64%, mean frame time -2.01%. One pair is preliminary; maximum
does not improve and all frame-time release gates still fail. No general FPS or
release certification claim. Instrumentation overhead is shared, not independently
removed from frame times.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/topology-key-oracle/`
and `topology-key-pilot/` including native logs, owner/source identities and comparison.
Private scripts under `output/renderdoc-tools-2026-10-08/` named
`prepare-topology-key-trial.py`, `run-topology-key-pilot.py`,
`run-topology-key-mixed-repeats.py`.

## Next action

Three alternating mixed pairs now complete in `topology-key-mixed-repeats/`:
6,480frames/36full states/cameras exact, owner2,938 unchanged, sources unchanged,
job terminal/override restored. Topology1384.785→897.668us/frame (-35.17%).
Candidate19,449 calls =19,440hits+9misses, proving actual reuse. Peak/end texture
unchanged every run. Pooled mean29.878→29.660ms (-0.73%), but pair changes+0.594%,
-4.213%,+1.490%; two of three slower. p9544.506→44.545,p9953.030→53.234,
>50ms53→55,max90.474→94.614. Do not admit as a sustained frame-speed improvement.

Current Main.get_room_doors returns owned String arrays (rotation explicitly str
converts each door, cache returns duplicates), so the prototype's second deep copy
is redundant. A lean revision removes it and the separate payload list, folds
each key entry into one tuple, and replaces the type-marker append loop with a
literal. Same complete inputs/evaluation order/owned cached key retained. Native
14,567 mutation checks pass again, same1,122hits/6,162misses, no errors, owner same.
Standalone proof tests the exact new function body; full navigation tests pending.

Lean private pair now complete in `topology-key-lean-pilot/`:2,160frames/12full
states/cameras exact, owner2,938 unchanged, jobs terminal/override restored. CPU
topology1388.088→767.856us (-44.68%); mean30.567→29.506ms (-3.47%), p9544.943→
44.268,p9954.716→51.913,max100.013→89.621,>50ms23→16,>100ms1→0. Peak/end texture
same. Initial pair was preliminary. Three alternating lean mixed pairs
in `topology-key-lean-mixed-repeats/` subsequently completed:6,480frames/36states
and cameras exact, sources/owner2,938 unchanged, job terminal/override restored.
Topology1394.160→777.169us (-44.25%),19,440hits/9misses. Whole mean30.513→29.963ms
(-1.80%); all three pair means improve2.296%/1.488%/1.619%. p9545.541→45.215,
p9953.659→53.871,max93.077→97.408,>50ms70→64, no>100ms either lane; peak/end
texture unchanged every run. Sustained mean gain repeats; tail/max still mixed,
and release frame gates fail. Still private pending relevant regression/real maps.

Eighteen plain-actor native comparisons now running (session37251) in
`topology-key-lean-original-maps/`: reported/current/original large, three alternating
pairs each. No attribution wrappers/timers, no diagnostic counter collection.
First reported six runs complete; current underway. Finish same job, then summarize
with `summarize-topology-key-lean-original-maps.py`; relevant crew/navigation/save
checks still precede integration. Reuse runtime; no new screenshots/runtime copies.
Prepared original-map v1 runner was NOT executed; do not run it unchanged unless
new evidence justifies it. Keep v1 and lean artifacts separate. No production
change. Original real-map and crew/navigation/save checks still precede integration.
Selected-source-guard effects revision timing/integration,
actual gameplay endurance, package/GTX1650/M1/Mac and remaining release gates stay open.
