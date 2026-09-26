# Owner bug reports — September 23, 2026

## Objective and acceptance

Resolve the five submitted reports about Bill stuck in doors, flooded-room repair,
stored Power and lag. Reproduce from report snapshots, retain normal costs and
failure conditions, and leave the player's save/profile unchanged.

## Accepted decisions and constraints

Use isolated copies under `output/owner-bugs-2026-09-23/`. No commit, push or package.
Keep collision, oxygen limits, repair costs and death meaningful. Continue restores
existing state; it does not resurrect an already dead actor.

## Current state

- `scripts/flood_safety.gd`: free cramped swim starts before low air; select nearby
  joins that actually fit the swimming pose; preserve a work route across the
  dry/flooded threshold; accept breathable wading refuges. If no refuge is reachable,
  a collision-checked local adjustment can still free a caught doorway pose.
- `scripts/hull_repair.gd`: use clear alternate work positions when furnishing
  blocks the old fixed anchor, check flooded work positions for swim clearance,
  face the work wall, and budget hazardous travel separately from dry travel.
  Smooth a route only after the air check; retry unavailable air at a bounded
  interval, bypassing the delay immediately when the air budget improves.
- `scripts/bill_npc.gd`: cache the nearby room owners used by swim collision checks.
  Overhanging props remain included; geometry rebuilds invalidate the cache.
  Reject unjoinable smoothed routes before assigning a meal/work destination,
  and bound those failed attempts too; an empty route must not grant a remote meal.
- `scripts/main.gd`: the Power chip explicitly says FULL when storage is capped.
  Report 045553 had 16/16 stored and report 180349 had 12/12; surplus generation
  is intentionally vented. Existing intake and stored-charge rules remain intact.
- New `tests/test_owner_report_regressions.gd` (+UID/index) covers the reported
  causes. `tests/test_npc_segment_clearance.gd` adds cache/overhanging-prop checks.

## Report findings

| Capture | Finding |
| --- | --- |
| 18:53:03 | Bill caught at a flooded threshold; Reactor's fixed repair anchor behind furniture; dry transit overcounted as tank use. Paid repair now completes in replay. |
| 18:03:49 | Report sampled roughly 156 ms/frame. Bill repeatedly planned and smoothed an unsafe repair route despite having no usable locker. Profile-matched replay reproduced 100.70 ms mean simulation update; delayed retry/deferred smoothing reduced it to 13.25 ms. Worst frame remains 240.89 ms. |
| 05:00:49 | Bill's standing position could not start a swimming route. Local clearance now resumes movement. Station also has zero Metal, no airlock and widespread flooding; the available wading room has no full-body swim route from Bill's compartment. A long unattended replay can still drown him. |
| 05:02:41 | Bill is already dead in the submitted snapshot. Preserve that state; investigate lag without treating resurrection as a bug fix. |
| 04:55:53 | Power storage full at 16/16, plus one blocked turbine intake. Clarify capacity rather than inflate generation or storage. |

## Verification

Focused regressions cover repair positions, oxygen estimates, doorway transitions,
refuges, absent refuges and the FULL label. Existing hull repair, Power and native
flood retreat suites pass. Navigation segment parity passes 26,624 comparisons.
Native report replay shows the paid Reactor repair, then restores a sealed Reactor
and living Bill through disk Continue. Before/welding/after captures are retained.
The four isolated profile-matched snapshots each ran 160 controller updates at
0.05 seconds (simulation work, excluding GPU/drawing):

- 18:53 repair snapshot: 1.83 ms mean / 25.83 ms maximum in the short warm-up replay.
- 18:03 lag snapshot: 100.70 → 13.25 ms mean after the blocked-air retry correction;
  258.91 → 240.89 ms maximum. Both use the report's profile and saved station.
- 05:00 doorway snapshot: 6.14 ms mean / 368.77 ms maximum, with the actor moving
  clear of the doorway. The cold unsuccessful escape search still spikes.
- 05:02 already-dead snapshot: 1.10 ms mean / 3.43 ms maximum; no resurrection.

Logs are under `output/owner-bugs-2026-09-23/<timestamp>/`. Native visual evidence
shows `16/16 FULL`, physical welding, and the repaired/dry Reactor after Continue.
Early diagnostic probes without the copied report profile are retained as diagnosis,
not used for the profile-matched timing comparison. Intermediate failed fixtures
are retained; final passing test logs use the `-complete` or `-accepted` suffix.

## Next action

Implementation and final log/visual review are complete locally. Seven focused
suites/replays finish with no engine errors or warnings; native captures were
inspected at gameplay scale. No processes from these fixtures remain running.
Owner playthrough after
restarting the source game remains the acceptance check for feel and sustained
rendering performance; short simulation timings do not establish sustained FPS.

