# Polish and balance follow-up — October 19, 2026

Local implementation and isolated validation complete. This pass corrects stabilization timing and makes emergency Water demand easier to read. Room prices, production/consumption rates, sprinkler costs and battery tuning are retained. No export or publication occurred.

## Changes

- **Later-loop stabilization bonus.** A pattern earned in this loop retains its base per-cycle output until the next loop, matching the owner's rule. Archived Data and the related blueprint discount still apply immediately. Normal forecasts and Parts Passage placement previews use the same eligibility. Inactive links still produce nothing.
- **Checkpoint-safe inheritance.** The set of doubled patterns is frozen at loop start. An optional `inherited_stabilized_synergies` checkpoint field preserves it, including when loading a checkpoint from before a pattern was earned. The checkpoint version stays unchanged. Malformed values are rejected; older checkpoints remain loadable and infer eligibility from the profile minus their recorded current-loop stabilizations. Older files cannot reconstruct a loop-start set that was never recorded. Profile unlocks and currency are not reset.
- **Clear reward copy.** The reveal card separates **FROM NEXT LOOP** output from **AWARDED NOW** Archived Data. Inspector, archive, log and toast wording agree. The empty discovery journal now points to blueprint purchases in Meta Progression instead of promising an automatic prototype.
- **Actual sprinkler status.** The switch distinguishes OFF, ARMED, READY, SPRAYING, LOW WATER, NO WATER and NO POWER. Prepaid spray remains visible with an empty reserve; partial coverage gets LOW WATER. Water tooltips and contribution details state the number of burning/spraying rooms and that 1 Water buys 5s of spray per burning room, separate from the per-cycle estimate. Status polling is capped at four scans per second; explicit refreshes remain immediate, with no stable-state relayout writes.

Changed production files: `scripts/main.gd`, `run_save.gd`, `room_fire.gd`, `hardware_panel.gd`, `synergy_reveal.gd` and `title_archive.gd`. Added three paired-script regressions, registered them in the test index, and updated the existing Parts Passage preview fixture to cover current-loop and inherited bonuses separately. Art and the prior navigation/recharge fixes are unchanged.

## Verification

**10 focused tests pass:** discovery progression, Meta Shop, Parts Passage, gameplay polish, RunSave, sprinkler feedback, stabilization loop timing, stabilization checkpoint rollback, synergy comment/reveal holds, and synergy evaluation parity. The last covers 8,043 checks / 1,188 cases / 112 authored recipes. The first final batch had nine passes and one old immediate-double preview expectation; the fixture now explicitly tests both timings and passes separately. Latest per-test receipts are in `FINAL.json`.

**20 native checks pass**, including live three-cycle stabilization, staged Save/Continue, a real next-loop reset, partial sprinkler coverage, Water details and normal/compact layout bounds. Final captures at 1600×900 and 960×540 were inspected. Initial fixture mistakes—physical versus scaled viewport coordinates, an incorrect audio cleanup call and a wall-clock animation deadline during a cold render—were corrected. The final fixture waits for observable card opacity/scale, with a bounded frame limit. Initial attempts are retained or described in the task evidence.

### Paid balance replays on the final source

| Case | Result |
| --- | --- |
| Fresh seeds 6113 / 28417 / 90571 | All reach cycle 70; Water minimum 4, final 30; no blackouts |
| Actual Desalination offers in those runs | First offered at 64.3s; completed at 168.7 / 174.4 / 167.2s |
| Three-crew retained station | Surveyed mining/salvage empty at 766.2s; survives another 360.1s; Food/Oxygen/Water/Power minima 27/27/29/10 |
| Four-crew retained station | Surveyed stocks empty at 154.1s; survives another 360s; minima 26/27/30/8; Marsh battery minimum 16.97%, zero empty time |

Fresh runs use only visible offered cards, normal paid construction/rerolls, fresh profiles without perks, and sprinklers armed from the start. The inherited cautious policy restricts the rooms it chooses and may decline a Galley; one seed has none by cycle 70. This is bounded policy coverage, not general draft/human pacing or severe multi-fire acceptance. The larger-crew fixtures retain their paid station/profile, including existing progression; 120 mining and 150 salvage loads remain remotely. They do not establish whole-map exhaustion or arbitrary station-size endurance. No broader numerical retune was justified by these results.

Six final checkpoint/meta pairs independently validate and carry the frozen bonus set. Final gameplay/native processes have no script/runtime errors. All **2,971 player files**, **32 other protected source/art inputs**, four retained fixture inputs and signed ZIP size/mtime are unchanged.

Evidence: `output/polish-balance-followup-20261019/FINAL.json`, `preservation.json`, `checkpoint-audit.json`, `final-tests.log`, `parts-final.log`, `ui-results.json`, per-case results/process receipts and final PNG captures. Earlier failures and the pre-snapshot cohort are retained transparently.

Next useful work is manual paid play with actual offers, crowded/flooded routes and varied Water consumers. Source/native checks do not establish release-package, performance/memory, Mac or iPad acceptance. The published build is unchanged.
