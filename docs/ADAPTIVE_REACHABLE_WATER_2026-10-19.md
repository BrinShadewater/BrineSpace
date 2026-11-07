# Adaptive Water preparation: reachable construction follow-up

October 19, 2026. The refined adaptive policy survives all three fresh double-fire cases and recovers both Josh and Margot, retaining normal costs and the 8-Metal recovery price. This follows nine initial adaptive runs, of which seven survived. These are separate cohorts: **12 fresh runs total, not one 9/9 result.** No game feature or balance change was implemented.

## What changed in the test policy

The initial nine-run policy prioritizes Margot, switching to Desalination when a fire is active, stored Water is at or below 2, or the visible Water forecast is negative. The switch stays in force until the plant functions. An unfinished paid repair is paused through its normal inspector button and resumed without refund, recharge or progress loss. Already-opened thawing may continue alongside water construction. Optional expansion is deferred until both goals finish, except urgent actually-offered survival support. All room/repair/failure rules and physical crew work remain normal.

All calm and single-fire cases survived. Two initial double-fire cases did not: a 5-Metal Desalination order was paid but remained unbuilt. The actor traces put Bill in corridor sector 19,21, rotation 1, with east/west doors. Its west neighbor was unbuilt; its east exit was burning Hydroponics. Normal fire safety forbids re-entry into a burning compartment, leaving no safe route to the preferred plant site at 19,18. The live ward guidance also reported a blocked approach. This evidence explains a refuge/access problem; it does not prove a general pathfinding defect or that every player response must fail.

The focused follow-up changes only construction choice during the emergency. Wait until Bill is out of a burning room. Check the preferred placement through production `CrewConstruction.approach`; if unreachable, inspect currently legal placements/rotations with the normal placement, ocean-intake/hazard and crew approach checks, choosing a reachable worksite. The actual offered card is still required and its full 5 Metal is paid through the ordinary build action. No actor movement, path, equipment, health, resources or progress is forced. No fire-navigation override is enabled.

In seed 28417, the selected room moves from inaccessible sector 19,18 to sector 18,21 beside Bill's shelter at 19,21. It is a normal legal three-door Desalination placement with an exposed intake. The earlier paid weld is paused at its actual progress, and later resumes through the normal inspector action without requiring another 8 Metal in stock. Production code already supports that paid pause/resume; only the test policy uses it.

## Focused fresh double-fire results

All three use a new empty scratch profile, the same normal paid opening, and the retained pressure event: maximum fire 1.0 at 280 simulated seconds in the actual Mining and Hydroponics compartments, with sprinklers armed. These rooms do not naturally self-heat. This is a severe capacity test, not natural fire incidence. Same source hashes, initial hand/resources/paid foundations and common paid hull-repair policy; retained earlier cohorts remain separate comparison evidence.

| Seed | Margot aboard, s | Desalination complete, s | Both fires out after burst, s | Dry sprinkler room-seconds | Paid pause / resume | Minimum Oxygen |
|---|---:|---:|---:|---:|---:|---:|
|194043|288.6|313.5|64.8|89.6|0 / 0|5|
|6113|288.6|312.4|64.8|89.6|0 / 0|5|
|28417|428.6|303.3|64.8|89.6|1 / 1|5|

All three reach 600 simulated seconds /30 cycles with Bill alive, both companion actors active, no blackouts, both fires out and all target hulls sealed. Each pays 8 Metal once for Josh and once for Margot, plus normal 5-Metal water construction and paid hull repairs. The pause/resume in the third seed preserves its paid flag, resources and exact stored progress; no second charge is recorded.

Reactive construction remains less protective than preparation. Each focused run spends 8 Water on the burst, incurs 89.6 summed dry sprinkler room-seconds, and extinguishes both fires 64.8 seconds after ignition. Retained water-first cases spend 6 Water, have no dry spray and extinguish in 12.9 seconds. Thus reachable adaptive construction avoids the observed deadlock in these three tests, but does not erase the delay before new Water arrives.

Without a fire, the initial adaptive cohort preserves Margot-first timing: 288.6/288.6/308.6 seconds, compared with 328.6/328.6/348.6 for retained water-first openings. The conservative any-fire trigger pauses a nearly finished third-seed rescue even for a single-room fire, delaying Margot to 388.6 seconds in that initial case. An emergency threshold based on reserve sufficiency could be a later experiment; these results do not justify making every fire an automatic stop or changing prices.

## Verification and preservation

The focused gameplay and audit processes exit 0 with no script/engine/harness errors. All three Water ledgers balance. All three copied final checkpoints restore production state in another scratch profile: resources, cycle, crew, companion roster/site state and fire/hull fields match; both companions remain active through five simulated seconds and valid checkpoint rewrites. Original checkpoint/meta/comms inputs remain hash-equal. The initial cohort separately has seven valid checkpoint reads and four pressure continuations. Teardown warnings remain in logs; no memory/leak acceptance is claimed.

All 2971 real player files stay hash-equal across the entire task. All 61 protected source/art/test/UID inputs, 23 retained evidence inputs and signed ZIP size/mtime remain unchanged at follow-up closeout. Only new test artifacts and documentation were written. No source/art/balance changes, desktop input, imports/exports, signing, upload, Git integration or cleanup.

These are scripted source-game runs with 0.1-second stepping and one-second decisions. Reading/dialogue pauses are bypassed; normal survey queries use a game-time cadence and other wall-clock throttles remain. Seven pure policy-decision checks cover the calm/fire/low-Water/negative-forecast branches; no independent naturally reached low-Water-only full-game cohort is claimed. No blind-human fun/legibility, new visual, actual-release, real-time performance, memory/endurance, arbitrary timing, larger-crew/depleted-deposit or Apple acceptance.

## Direction

Keep the 8-Metal recovery price and current production rules. Adaptive Water preparation is viable in this tested cohort when construction is chosen for the crew's actual safe access; waiting for an inaccessible paid order recreates the emergency trap. Earlier preparation still buys the stronger buffer. The next useful product discussion is how construction/recovery guidance communicates that access and emergency choice to a player; no additional UI, AI or pricing change is authorized or started by this experiment.

Evidence: `output/adaptive-reachable-water-20261019/` holds the focused probe, three fresh traces/results, route-choice and paid pause/resume events, retained-baseline comparisons, process/audit logs, preservation, `FINAL.json` and handoff. Initial nine-run results remain in `output/adaptive-margot-water-20261019/` and [their report](ADAPTIVE_MARGOT_WATER_2026-10-19.md).
