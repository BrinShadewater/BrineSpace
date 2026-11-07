# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: large-room paid-run pacing

## Objective and acceptance

Measure when the one rare large-room card enters a normal paid run and whether the starting economy can build it. Use the result to guide later balance tuning without treating an automated player as human acceptance.

## Accepted decisions and constraints

One of the four large rooms is offered per run, in Farm → Depot → Moonbay → Plant order for the first four runs, then randomly. Large rooms cost more than standard rooms. Normal construction and failure rules apply. Moonbay needs an assigned crew member for its mini-sub missions. No owner save or Studio layout may be used for probes.

## Current state

`tests/playtest_balance.gd` now accepts `--large-room-intro=0..3`, seeds the site and deck before starting a run, records first sighting, first affordability, first legal site and construction, and keeps a seen rare card when cycling other cards. `--save-for-large-room` stops ordinary purchases while the rare card is unaffordable. `--reserve-large-room` plans a legal 2×2 anchor at the start and keeps small rooms off those four cells. When Moonbay needs more Rare Minerals, this policy can build an affordable Salvage Workshop from the actual hand. `--launch-moonbay` tries one Survey order and advances its mission during the same paid-run simulation. The harness no longer confirms the draft a second time after `_start_reboot_cycle()`; that had skipped an introduction slot. The diagnostic player still makes its own build choices, and its results are only evidence for that policy.

With fresh starting unlocks, seed 4404 and no resource grants (the harness's `industry+biosphere` pair is a report label; current runs do not select doctrines):

| Intro | Card | First seen | Resource state on sighting | End | Result |
|---|---|---:|---|---:|---|
| 0 | Hydroponics Farm | Cycle 23, after 11 paid orders | 3 Metal, 11 Biomass; cost 16 Metal, 3 Biomass | Cycle 60: 2 Metal | Held in hand; never affordable or built |
| 2 | Moonbay | Cycle 23, after 11 paid orders | 3 Metal, 1 Rare Mineral; cost 20 Metal, 2 Rare Minerals | Cycle 35: 2 Metal, 1 Rare Mineral | Held in hand; never affordable or built |

The deliberate-saving policy adds two useful bounds for the Farm:

| Seed | First seen | First affordable | Connected 2×2 site | Outcome |
|---|---:|---:|---|---|
| 4404 | Cycle 23 | Never by cycle 60 | Not evaluated after affordability | Metal reached 13 by cycle 30 and stayed there through cycle 60; cost is 16 |
| 9021 | Cycle 29, after 13 paid orders | Cycle 39 | None found from cycle 39 through 50 | Metal reached 32 by cycle 50, but no legal footprint remained beside the station |

The original Farm run placed 14 paid orders by cycle 60 and had 46 cycles with no new order under that player policy. Food, oxygen, water, power and integrity remained healthy at cycle 60. The saving runs show two different pressures: finite Metal in one site seed, and finding room for a late 2×2 placement in another. A human can plan open space and pursue different mining or salvage routes, so these results do not establish that the costs or timing are wrong. Moonbay could not be purchased in those initial runs; the reserved-space run below exercises one mission.

## Reserved-space paid run

With the same fresh unlocks and seed 9021, the diagnostic player reserved a legal large-room anchor before its first purchase. No resources or cards were granted. Ordinary rooms still paid their full costs and were completed by crew and drones.

| Introduction | Reserved anchor | Card appeared | Support and purchase | Completed |
|---|---|---:|---|---:|
| Hydroponics Farm | (18, 20) | Cycle 19 | Affordable at cycle 19; paid order at cycle 19 | Cycle 21 |
| Moonbay | (18, 19), with open ocean face | Cycle 19 | Salvage Workshop paid at cycle 47; its first Rare Mineral made Moonbay affordable and the paid order followed at cycle 48 | Cycle 51 |

The Moonbay then dispatched Bill on Survey at cycle 55 to a distant, nonhazardous deep site. The mini-sub returned at cycle 64 with “Survey complete. Site identified.” Boarding, chamber phases, travel and survey took 189.2 simulated seconds. This is one completed normal-economy mission, not a duration or hazard-rate verdict. Recover, Deep Access, hazardous return and repair remain covered by the separate paid Moonbay walkthrough, which starts with test resources.

## Verification

The Farm and Moonbay headless runs, both saving-policy runs, and both reserved-space runs exited 0 with zero harness errors under scratch `APPDATA`. Reports include `output/large-room-review/paid-farm-reserved-9021.json` and `paid-moonbay-mission-9021.json`; earlier runs and logs are alongside them. `test_large_room_draft.gd` passed. Existing missing legacy UI atlases produced resource errors in this isolated checkout, as already recorded in the large-room handoff. No game balance values or runtime logic were changed. The real `BrineSpace` user folder matched before and after all runs across 2,652 readable non-log files.

## Next action

Have the owner play a normal run to judge whether reserving a 2×2 area and buying a Salvage Workshop feel discoverable and satisfying. Tune timing, costs and mission length from that feedback. Hazard frequency needs more than one mission. Owner visual acceptance and release/merge remain separate.
