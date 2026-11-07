# Construction warning in fresh adaptive openings — October 20, 2026

Six fresh normal-cost source openings survive 600 simulated seconds /30 cycles: three seeds, each calm and under two severe artificial compartment fires. Emergency Water placement reads the actual construction-preview warning before choosing a site; it does not call the earlier private route chooser. Warning queries do not spend resources, queue work, move Bill, assign his goal or advance station RNG. No paid Water order is placed while its preview warns.

| Seed | Pressure | Margot aboard (s) | Desalination complete (s) | Survived |
| --- | --- | ---: | ---: | --- |
| 194043 | Calm | 288.6 | 320.8 | Yes |
| 6113 | Calm | 288.6 | 324.3 | Yes |
| 28417 | Calm | 308.6 | 356.0 | Yes |
| 194043 | Double fire | 288.6 | 312.4 | Yes |
| 6113 | Double fire | 288.6 | 313.4 | Yes |
| 28417 | Double fire | 428.6 | 303.3 | Yes |

All main runs recover Josh at208.3s, finish with both companions and no blackouts. Desalination pays exactly5 Metal once; each companion recovery pays8 once. Normal physical construction/ward work and failure rules stay enabled. No supplied cards, resources, progress or repair-clock override. No saving-window rerolls; rerolls cost charges, not Metal. Optional expansion waits for the two goals except urgent offered survival support.

## What the warning changed

All three fire cases encounter an amber **NO SAFE CREW ROUTE** preview before Water payment. In two, safe access to the preferred site returns and it can be used. Seed28417 at285.6s still cannot safely serve19,18 from Bill's refuge at19,21; a legal clear preview at18,21/rotation0 is selected instead. Metal is6 before the normal5-Metal plant purchase. The unit completes303.3s. Margot's paid repair pauses at10.6/18s, preserving exact resources/progress, resumes320.6s without another charge, and she joins428.6s. This is a new observation; the earlier direct-route cohort's14.7s pause remains separate.

Reactive water still has limited margin: each severe-fire run has64.8s from ignition to extinction,8 Water used for suppression and89.6 summed dry-sprinkler room-seconds; hulls later seal in all three. Water reserve reaches zero. Earlier retained water-first cases had12.9s fires and no dry spray. The warning prevents a stranded paid build under this policy; it does not make emergency reaction as safe as preparation. Keep the current prices and warning.

Pressure is fixed fire1.0 at280s in the actually paid Mining and Hydroponics rooms, which do not naturally self-heat. Calm runs receive no injected hazard. This is severe burst capacity, not natural fire frequency. Sampling is deterministic0.1s game steps/one-second decisions with reading pauses bypassed and normal survey queries on a game-time cadence; the250ms preview cache remains active. Other wall-clock behavior can vary, so timing differences from retained cohorts are not a controlled speedup or exact reproduction.

## Emergency Save/Continue bug found and fixed

Two extra inspection checkpoint writes in seed194043/double-fire were refused with `Checkpoint not written: companions. Previous checkpoint kept.` All six end-of-run checkpoints were valid. A separate fresh reproduction retained the refused snapshots and traced the mismatch: Josh's NPC, playback and personality records each validate, but the companion wrapper only accepted idle/curiosity goals. Runtime fire safety legitimately set `fire-retreat`.

`scripts/companions.gd` now accepts that existing evacuation state for active dry companions with no staged/personality action, while retaining all other validation. It does not normalize the actor to idle, remove his route or change gameplay. Invalid companion construction/repair/unknown goals, inactive evacuation and flooded evacuation remain rejected; legacy absent personality stays supported. No new save field or format version.

TDD: the new `test_companion_fire_save.gd` first failed three checks on a real fire-safety retreat. After the fix, its final15 checks pass, including disk Save/Continue, exact resources/position and physical exit from the burning room. It has a paired UID and belongs to the existing `companions` test group.

One additional post-fix fresh194043/double-fire run survives600s, with Margot288.6s and Desalination313.4s. Both previously failing inspection saves now succeed at280.6/283.6s. Those two actual emergency checkpoints plus its final checkpoint all restore, advance five game seconds and re-save successfully. The diagnostic reproduction and post-fix confirmation are retained separately from the six-case main cohort; do not combine them into a larger balanced cohort.

## Verification and preservation

- Seven relevant tests pass: companion fire save, companions, personality, repair, topology, run save, construction preview. The final fire-save fixture adds legacy-personality/flood guards and passes15 checks. Logs: `output/test-runs/20261020-003752-headless/` and `20261020-003950-headless/`.
- All six main end checkpoints validate; all three main fire checkpoints restore through five seconds/re-save on final source. Three additional post-fix checkpoints (two emergency/one final) restore and continue. Original scratch checkpoints/meta/sidecars hash-equal after these copied audits.
- 18 native checks pass using actual seed28417 warning/reachable checkpoints, copied to separate scratch APPDATA. All four1600×900/1280×720 captures visually reviewed; warning and alternatives fit within the station. Fire-map synchronization for the restored UI only, no extra gameplay stepping or desktop input. [Emergency warning](../output/construction-warning-opening-20261020/fresh-warning-1280x720.png), [reachable alternative](../output/construction-warning-opening-20261020/fresh-reachable-1600x900.png).
- Main/confirmation/audit/native processes exit0 with no script/engine errors. Fixture shutdown warnings remain: main12 CanvasItem RIDs/24 ObjectDB, native2/4, each three-restoration audit3/6, single-run diagnostic/confirmation2/4, personality test4/8. They are retained in logs; this is not leak or lifetime-memory acceptance. The final focused15-check regression has no warnings.
- All2,971 real player files hash-equal, protected source/art/retained inputs unchanged except the intended companion-validator/test-index edits and direction notes. Signed Windows ZIP size/mtime unchanged. Existing dirty work preserved. No build, integration, signing, upload or publication.

This is scripted source-game evidence and visual review, not blind human playtesting, general balance, performance/endurance, Apple or release-package acceptance. A new Windows candidate still needs the maintained release workflow and actual package validation.

Receipts, traces, preserved failed inspection snapshots and corrected confirmation: `output/construction-warning-opening-20261020/`. Primary interpretation is `analysis.json`; final preservation and file hashes are in `FINAL.json` and `preservation.json`.
