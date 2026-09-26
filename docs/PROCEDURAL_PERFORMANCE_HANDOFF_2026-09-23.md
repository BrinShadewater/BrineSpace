# Procedural expedition performance follow-up

Updated: September 23, 2026 · Project: BrineSpace · Task: procedural sites

## Objective and acceptance

Finish the repeated-character paid recovery check and investigate crew stalls
found while profiling the resulting large station. Keep normal costs, yields,
charging rates, collision checks and progression. No commit, push or packaging.

## Accepted decisions and constraints

The seed-73 progressed-profile chain recovers Marsh at 51, Branforth at 134 and
Veld at 290, concluding with six crew, 47 rooms and zero final-leg failures.
Earlier cutoffs at 163 and 221 remain failed assertions in their own logs. The
chain excludes intermediate conclusion rewards and uses actual checkpoint state.
It is not uninterrupted fresh play or a human pacing target. See the
[routing evidence](PROCEDURAL_ROUTING_HANDOFF_2026-09-23.md).

## Current state

- `scripts/bill_npc.gd`, `scripts/crew_construction.gd`: check reachable meals/rest
  only when eligible crew would claim new work. Empty queues, swimmers and work
  claimed by another builder no longer trigger those searches every frame.
  Existing work finishes before a break; cancelling orders still releases crew.
- `scripts/marsh_npc.gd`: a return to the charging pod follows its existing path
  instead of rebuilding and smoothing the same route every movement frame.
  Movement still checks collision; an empty/invalidated route is searched again.
  Topology rebuilds clear paths as before. No new save fields or persistent cache.
- `tests/test_construction_break_checks.gd` plus UID and crew index entry cover
  idle/eligible/ineligible/claimed/cancelled construction. Battery tests now cover
  route reuse, locked access and replanning. `test_marsh_unlock.gd` explicitly
  requests authored identified wards for its charging/save fixture.
- The paid player records controller timings, worst-frame context and the active
  profile before conclusion. `--watch-recharge` observes an existing paid station
  without building/rerolling and requires a completed normal recharge.

## Verification

Evidence root: `output/procedural-sites-2026-09-23/`.

| Same saved station, 8 cycles / 160 frames, dt 0.05 | Mean frame ms | Worst ms | Route searches |
|---|---:|---:|---:|
| Before both fixes | 279.716 | 486.980 | 235,516 |
| Construction eligibility fix only | 237.536 | 485.559 | 3,836 |
| Both fixes | 10.661 | 162.610 | 3,676 |

These sequential headless probes restore the same 47-room paid checkpoint with
normal simulation rules; they are CPU measurements, not native FPS or paid play.
All complete eight cycles without logged errors. Mean cost falls 96.19%; remaining
spikes are not presented as a smooth-frame acceptance pass. The phase probe
attributed 11,156.567 of 11,671.9 crew milliseconds to Marsh before route reuse.
Logs/JSON: `crew-soak-before`, `crew-soak-after`, `crew-soak-final` and
`crew-phase-profile`. The phase probe subclasses the controller only in the
generated evidence directory; the production controller was not refactored.

Focused checks pass: construction-break regression, paid construction matrix,
autonomous primary-work meal/rest, Marsh battery (93 route samples, transitions
and save/Continue), and Marsh recovery/charging. The pre-fix regression and old
unidentified-ward fixture failure remain in separate logs.

The native observation passes in `expedition-73-postfix-recharge/`: Continue
restores the paid map/resources, Marsh walks from the northern branch, docks at
cycle 300 and finishes charging at 301, then the station concludes alive at 309.
Normal costs/failures, charging Power and player-facing 4× time remain enabled.
No construction, hand changes or resource injection occur in this observation.
The log has zero failures or engine/script errors; `view-090.png` was inspected.
Across 1,743 active controller samples, mean total time is 8.827 ms (crew 7.769),
worst 326.527 ms (crew 326.209). This is a different workload from the earlier
construction leg, excludes drawing/GPU time, and is not a comparative FPS claim.

## Next action

Owner artwork and human pacing acceptance remain open; the
[review page](PROCEDURAL_SITES_OWNER_REVIEW.md) collects comparison captures.
Remaining occasional crew spikes need a separate bounded investigation using the
retained actor/timing context. The earlier 239.427-second event gap at cycle 185
recovered without intervention; these probes establish two expensive code paths,
but do not prove the exact cause of that historical gap. No smooth-frame or
historical-stall resolution is claimed.
