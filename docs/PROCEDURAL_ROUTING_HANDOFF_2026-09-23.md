# Project handoff

Updated September 23, 2026 · BrineSpace · Procedural expedition routing validation

## Objective and acceptance

Continue the procedural-site plan, diagnose the automated player's failed fresh
all-crew journey, and retain honest separation between reachability, repair and rescue.

## Accepted decisions and constraints

Normal costs, card draws, resource failures and wake/berth requirements remain.
No production balance changes, commits, pushes or packages. Prior procedural-site
implementation and art decisions remain in PROCEDURAL_SITES_2026-09-23.md.

## Current state

Changed the test player in `tests/playtest_procedural_expedition.gd` to use
`tests/procedural_route.gd`: route through empty buildable cells, exclude occupied
rooms, allow depleted deposits, consider only existing open-door frontiers, and
preserve an onward door on the nearest frontier. Actual game placement and chamber
door checks remain authoritative. Added paired UIDs and `test_procedural_route.gd`
to the procedural-sites subsystem. Final-result diagnostics now include capacity
and individual chamber status. Production gameplay is unchanged by this follow-up.

## Verification

Evidence under `output/procedural-sites-2026-09-23/`:

- `route-contract.log`: zero failures for detours, depleted/live deposits, onward
  doors, occupied approaches and bounds. `route-driver-parse.log`: clean parse.
- `route-checkpoint.log`: native load of the earlier cycle-111 seed-73 station
  found 12 door frontiers and legal onward corridor options; the nearest approach
  required a 13-cell detour. No placement or resource mutation in this probe.
- `paid-73-fresh-door-routes.log` and `expedition-73-fresh-door-routes/`: one fresh
  600-second native run at normal 4×, without strategy changes or injected resources.
  Veld rescued at 16; disk Continue at 16 preserved geography/resources; Branforth
  repaired at 39 and rescued at 78; Marsh repair started at 97. Alive conclusion
  at 111 with 32 rooms, four crew, metal 160, food/oxygen 66, power 12.
  **One failed assertion: all three rescues before cutoff.** No other reported errors.
- `marsh-berth-checkpoint.log`: saved Marsh chamber repaired, paid, powered,
  charged to 12 seconds, not yet recovered; four crew and one Hab give four berths.
  The inspected native conclusion also shows 4/4 crew capacity. This is a normal
  berth wait, not evidence of failed chamber generation or assignment.
- Inspected native `view-090.png`, `view-270.png`, and `conclusion.png`. These
  establish rendering/progression, not new purchased-art acceptance.

The earlier three first-recovery paid tests and seed-32 all-crew checkpoint chain
retain their original scope. This fresh run establishes access and repair of all
three seed-73 sites but does not supersede the missing fresh all-rescue pass.

## Next action

The berth-strategy follow-up below supersedes the previous missing strategy fix.
Owner visual and human pacing review remain open. Active checkpoints and their
later conclusion events remain separate evidence.

## Berth-strategy follow-up

The test player now budgets spare berths for all pending rescues, retains one
needed Hab while food support is established, and permits duplicate Hab rerolls.
It stops enforcing an onward chamber route once all chambers have been repaired;
the previous route guard could prevent further construction at that point.
Normal Hab cost, its additional resident, capacity and rescue rules are unchanged.

`tests/playtest_procedural_berth_strategy.gd` is a direct-run native regression
fixture, paired with its UID. It requires the recorded
`expedition-73-fresh-door-routes/final.loop` checkpoint and sets explicit test hands;
it is deliberately separate from portable subsystem tests and paid dealt-hand runs.
The driver accepts `new(false)` so this fixture can exercise its actual build and
reroll decisions without launching a second expedition loop.

`berth-strategy.log` reports zero failures: duplicate Hab reroll retains a needed
Hab; construction after completed chamber repairs spends the normal metal cost;
the Hab completes and Marsh wakes; both its new resident and Marsh count toward
the resulting six crew/six berths. The recovered state saves successfully to
`berth-strategy/recovered.loop`. Its native image was inspected: the station and
6/6 counter render, with an existing pattern-stabilization notification over the
center. This verifies the strategy correction, not fresh-run pacing or new art.
`berth-driver-parse.log` is clean.

The concurrent fresh `expedition-73-fresh-rescue-berths/` run used the initial
multi-Hab retention strategy throughout (the later fix did not hot-reload).
It rescued Veld at 15, passed disk Continue at 16 and concluded alive at 114;
the all-three assertion was its sole reported failure. Two retained Hab cards
constrained draft choices, and the run also exhausted its available metal.
`paid-73-fresh-rescue-berths.log` retains that result. Do not present this run as
validation of the subsequent duplicate-retention correction. A fully fresh
all-rescue result remains unverified; the original three bounded first-recovery
expeditions and separate all-crew checkpoint/fixture evidence retain their scope.

## Finite extraction and blueprint ownership follow-up

`metal-route-probe.log` inspected the cycle-114 checkpoint: both mining bays
reported depleted surveyed deposits, no surveyed rock remained, and two surveyed
scrap deposits still had 12 loads each. The player had no salvage bay. The strategy
now avoids duplicate extraction bays, prioritizes a first salvage bay, and protects
its construction cost when mining is nearly depleted and no surveyed rock remains.
**The reserve is conditional on blueprint ownership.** `STARTING_UNLOCKS` does not
include the salvage bay; catalogue `unlocked` metadata alone does not put it in a
new profile's deck. Production unlocks, costs and resource yields are unchanged.

The initial ungated `expedition-73-fresh-salvage-reserve/` attempt was stopped once
that ownership mismatch was confirmed. Its events/log remain diagnostic evidence;
it is neither a conclusion pass nor validation of the ownership correction.

The native `playtest_procedural_salvage_strategy.gd` fixture (paired UID, direct run)
passes in `salvage-strategy.log`: a locked blueprint creates no reserve; an owned
blueprint protects five Metal from other construction; normal bay placement spends
it; the completed bay delivers metal from an existing surveyed scrap deposit.
This fixture supplies the hand, owned blueprint and pre-spend resource boundary;
it is not a paid dealt-hand expedition.

For the subsequent progressed-profile expedition, `progressed-profile-before.meta`
preserves a copy of the earlier completed door-routing test profile. The normal
Meta Shop purchase used its 21 earned Archived Data to buy the salvage blueprint
for 12, leaving nine (`progressed-profile-purchase.log`). No currency or room-card
injection was used for that purchase. The test operates on an isolated copy,
`progressed-profile-shop.meta`, not the owner's profile or the original evidence.

The progressed-profile attempts then exposed two more test-player assumptions.
`expedition-73-progressed-owned-salvage/` was stopped after confirming that seed 73
repeats known crew as Marsh → Branforth → Veld: the player had incorrectly used
Veld's rescue to increase its construction limits. It now recognizes any guest
recovery. `test_procedural_player_progress.gd` passes all four starters and every
other guest identity (`player-progress.log`).

`expedition-73-progressed-any-guest/` successfully bought a salvage bay with run
resources at cycle 38, but was stopped after an observed power stall. The player
had placed a solar array at (19,21), blocking the west intake of its turbine at
(20,21), rotation 3. It also froze unrelated rerolls while holding an unaffordable
reactor. The planner now reserves all existing turbine intake cells in its route
field and construction candidates, checks actual turbine intake availability for
power readiness, and retains essential support cards individually while rerolling
unneeded cards. `test_procedural_player_power.gd` passes native placement/reroll
checks (`player-power.log`); the subsystem explicitly routes it to the native lane.
Both new test scripts have paired UIDs. Stopped attempts are diagnostic evidence,
not completed expedition passes. Production gameplay remains unchanged.

Each fresh restart uses a separate copy of the same preserved earned profile and
the normal 12-Data purchase; purchase-v2/v3 logs retain the 21 → 9 balance changes.
The v3 profile is used by `expedition-73-progressed-power-safe/`.

The concise [owner review page](PROCEDURAL_SITES_OWNER_REVIEW.md) now links the
native/light-dark art comparisons, candidate inventory, map overview and Studio
capture. Provisional artwork choices remain explicitly distinct from owner approval.

## Learned-pattern placement follow-up

The v3 power-safe run concluded alive at cycle 172 with Marsh rescued, but stalled
at one Metal before completing Branforth's approach. Its all-three assertion failed.
It also logged a misleading first-recovery failure because that final check still
meant Veld specifically; the all-crew check/output now recognizes any guest rescue.
The named rescue records retain what actually happened.

The copied profile already knows and has stabilized Industrial Heat Capture, but
the greedy player's reactor placement did not use it. The player now reserves a
legal, matching-door reactor neighbor of a mining bay only when the profile knows
that recipe and has the required Rare Mineral. Other buildings and turbine intakes
respect the planned cell, and a reactor card prioritizes it. No hidden recipe is
revealed and no simulation bonus, unlock, cost or yield was changed.

`test_procedural_player_recipe.gd` (paired UID, native subsystem lane) verifies
unknown-recipe exclusion, turbine/intake preservation, actual paid reactor placement
and normal functioning-cycle activation. `player-recipe.log` passes with the
recipe active. The retained `player-recipe-before-door-check.log` exposed that
physical adjacency alone was insufficient; the corrected plan checks matching doors.
Its explicit room/card setup remains fixture evidence, separate from paid runs.

The next fresh attempt uses isolated `progressed-profile-shop-v4.meta`, again
purchased normally from the preserved 21-Data profile; see purchase-v4 log.

## Fixed-strategy checkpoint continuation

`expedition-73-progressed-known-recipe/` began a fresh map with the v4 progressed
profile and the corrected player. It passed disk Continue at cycle 16, rescued
Marsh at 51 and Branforth at 134, and reached its 900-second limit alive at 163.
The all-three assertion failed at that cutoff. An active pre-conclusion checkpoint
was retained as `final.loop`; the subsequent test conclusion remains a separate
event and is not counted as full-recovery acceptance.

Before that conclusion, the active isolated profile was copied to
`progressed-profile-v4-active.meta` (SHA256
`940766c02507e5b77ddaa43f6df5cc7e98e919e64244ebf48e1c5db19f323605`). Comparison
with the post-conclusion profile found exactly one changed field: lifetime
research points 36 → 43. `continuation-profile-diff.json` records this. The
continuation uses a copy of the active profile, excluding those seven conclusion
points; all other profile fields match. Resources, cards and geography come from
the active checkpoint without injection.

`expedition-73-progressed-known-recipe-continued/` continues that checkpoint with
the unchanged player strategy. `fixed-strategy-hash.json` records the driver hash.
This is a checkpoint chain with a documented boundary, not one uninterrupted
900-second run. Human pacing acceptance remains separate.

The second leg ended alive at cycle 221 with Marsh and Branforth recovered,
44 rooms and normal resource reserves. Its all-three assertion still failed.
The event stream has a 239.427-second gap between cycles 185 and 186; Windows
briefly reported the CPU-active native process as unresponsive, but it recovered
and continued. This establishes a severe temporary slowdown, not a permanent
hang or a proven construction/pathfinding cause. No speculative production fix
was made from the last recorded construction order.

The next continuation starts from that leg's active `final.loop`, with the saved
pre-conclusion profile (`progressed-profile-v4-leg2-active.meta`). Comparison
against the concluded profile again found only the seven-point conclusion award
(36 → 43); that award is excluded. Player strategy remains unchanged. The driver
now samples existing main-controller subsystem timings and retains the ten worst
frames in `frame-profile.json`, plus the active profile before concluding. These
timings exclude render/GPU work and do not imply an FPS measurement.

The final leg passed at cycle 290: Marsh at 51, Branforth at 134 and Veld at 290,
six crew/six berths, 47 rooms, and all three paid wards fully recovered. Its log
has zero test failures or engine/script errors. Native Veld rescue and conclusion
captures are retained in `expedition-73-progressed-known-recipe-final/`; the Veld
capture was inspected. Normal costs, failures and 4× play remained active, with no
resource/card injection. This establishes the repeated-character order in a paid
checkpoint chain; the earlier cutoff assertions remain failures in their own legs.
The player's 12-corridor cap caused additional card waiting near the final ward;
it eventually used a dealt T-corridor and corner without another strategy change.

The final leg sampled 6,045 active controller frames: mean 20.519 ms total and
19.456 ms crew, worst 3,111.893 ms total (3,111.545 ms crew) at cycle 279.
The four-minute gap did not recur, but the crew spikes are a real performance
finding. A focused saved-station probe is investigating them. This is not a
performance acceptance pass; render/GPU costs are outside these samples.

That probe subsequently isolated unnecessary construction break searches and
per-frame replanning of Marsh's return trip. Focused fixes, regression results
and sequential before/after measurements are recorded in the
[performance handoff](PROCEDURAL_PERFORMANCE_HANDOFF_2026-09-23.md).
