# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: unchanged crew update attribution

## Objective and acceptance

Find measured simulation overhead before changing navigation. Preserve topology
signatures, locked-cell side effects, rebuild scheduling, movement and save state.
Full performance/release goal remains open.

## Accepted decisions and constraints

Private diagnostic only; production unchanged. Do not optimize fire refresh from
its small measured cost. A topology reuse trial must compare every source input,
including same-tick mutations; a frame number alone is insufficient invalidation.
No new gameplay behavior, monolith refactor or permanent resource cache.

## Current state

Prepared and executed private `bill-update-attribution/runner.py`, one native
debug=false RTX4070Ti/1080p mixed40-room/52-cell run, 1,080 measured frames.
Original topology body is unchanged; wrapper measures elapsed time and stores
bounded per-actor cumulative calls/total/max counters. Fire timing wraps only the
existing refresh call inside Bill.update, not separate Main calls. Reset/report
at phase boundaries; no per-call event list. Actual loaded source guard passes.

| Scope | Measured cost |
| --- | ---: |
| Topology construction, all measured actors | 1,375.7–1,409.8 us/frame |
| Topology calls | 6/frame, last phase6.033 with rebuild calls |
| Fire refresh inside actor updates | 4.6–4.8 us/frame |

All12 gameplay states/camera paths/action-speed labels exactly match the existing
mixed reference. Instrumentation is attribution, not performance improvement.
No engine errors/missing art. Owner2,938 files unchanged; job terminal, override
restored. Artifacts:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/bill-update-attribution/`
(`hotspot-summary.json`, report, identity, owner and source-guarded log).
Preparation tool: `output/renderdoc-tools-2026-10-08/prepare-bill-update-attribution.py`.

Source explains redundant queries: Main computes actor.topology before update to
schedule at most one rebuild; Bill.update queries it again. Additional calls
occur during rebuilding. Topology enumerates every occupied cell, formats six
inputs plus Moonbay state, sorts strings, joins and appends layout/hardware state.
It also clears/rebuilds actor.locked_room_cells. Derived actors may execute work
before base update, so merely passing the earlier signature without validation
would risk stale same-tick state.

## Next action

Private complete-input key prototype: read the same cell/id/rotation/door list/
branch/room-lock/Moonbay inputs, layout geometry revision and hardware lock state;
reuse only the expensive sorted/formatted result when inputs equal. Preserve
locked-cell updates and owned mutable values on hits. Test source equivalence,
same-tick mutations, return ownership, current save/crew/mission/navigation and
matched native real maps before integration. First measure key overhead; abandon
if it does not reduce actual topology cost and matched frame timing.

Separately the selected-source hash guard revision passes576 exact rendering
pairs and21 fallback/lifetime checks; revised storage timing still precedes its
normal integration. All release/package/target-hardware/Mac/endurance gates remain.
