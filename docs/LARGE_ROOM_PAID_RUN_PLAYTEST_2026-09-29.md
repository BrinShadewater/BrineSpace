# Project handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: large-room paid-run pacing

## Objective and acceptance

Measure when the one rare large-room card enters a normal paid run and whether the starting economy can build it. Use the result to guide later balance tuning without treating an automated player as human acceptance.

## Accepted decisions and constraints

One of the four large rooms is offered per run, in Farm → Depot → Moonbay → Plant order for the first four runs, then randomly. Large rooms cost more than standard rooms. Normal construction and failure rules apply. Moonbay needs an assigned crew member for its mini-sub missions. No owner save or Studio layout may be used for probes.

## Current state

`tests/playtest_balance.gd` now accepts `--large-room-intro=0..3`, seeds the site and deck before starting a run, records first sighting, first affordability and construction, and keeps a seen rare card when cycling other cards. It also no longer confirms the draft a second time after `_start_reboot_cycle()`; that had skipped an introduction slot in this harness. The diagnostic player still makes its own build choices, and its results are only evidence for that policy.

With fresh starting unlocks, seed 4404 and no resource grants (the harness's `industry+biosphere` pair is a report label; current runs do not select doctrines):

| Intro | Card | First seen | Resource state on sighting | End | Result |
|---|---|---:|---|---:|---|
| 0 | Hydroponics Farm | Cycle 23, after 11 paid orders | 3 Metal, 11 Biomass; cost 16 Metal, 3 Biomass | Cycle 60: 2 Metal | Held in hand; never affordable or built |
| 2 | Moonbay | Cycle 23, after 11 paid orders | 3 Metal, 1 Rare Mineral; cost 20 Metal, 2 Rare Minerals | Cycle 35: 2 Metal, 1 Rare Mineral | Held in hand; never affordable or built |

The Farm run placed 14 paid orders by cycle 60 and had 46 cycles with no new order under this player policy. Food, oxygen, water, power and integrity remained healthy at cycle 60. This points to Metal acquisition or spending as the limiting factor for these two large rooms in this scenario. It does not establish that the costs are wrong for a human player or other seeds. Moonbay mission duration and hazard frequency were not exercised in these runs because no Moonbay could be purchased. The separate paid Moonbay walkthrough remains the functional mission check.

## Verification

Both headless runs exited 0 with zero harness errors under scratch `APPDATA`. Reports are `output/large-room-review/paid-farm-kept.json` and `output/large-room-review/paid-moonbay.json`; logs are alongside them. Existing missing legacy UI atlases produced resource errors in this isolated checkout, as already recorded in the large-room handoff. No game balance values or runtime logic were changed. The real `BrineSpace` user folder matched before and after the run across 2,652 readable non-log files.

## Next action

Play a human normal run with deliberate Metal collection and saving after the rare card appears. Decide whether to adjust rare-card timing, prices or Metal income from that result. Then judge Moonbay mission duration and hazard frequency in a run that actually builds it. Owner visual acceptance and release/merge remain separate.
