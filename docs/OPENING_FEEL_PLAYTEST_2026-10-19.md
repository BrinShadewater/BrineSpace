# Opening discovery and exploration playtest — October 19, 2026

Owner requested a ten-minute opening assessment, then asked to run gameplay in the background rather than take over desktop input. This report keeps the interrupted native observation separate from automated gameplay.

## What happened

The native UI playthrough used fresh seed194043, normal costs/failures and1× speed. Buying Solar, Mining, Hydroponics and a Current Turbine produced **Cultivated Current at cycle7** (first sampled around2m23 active /3m25 wall). It stabilized atcycle9 (around3m01 active /4m30 wall), with visible paired-room artwork, later-loop bonus wording and5 Archived Data. Choosing the turbine beside Hydroponics while solving Power caused the discovery without consulting hidden recipes.

Computer Use was stopped through physical Escape. The run ended atcycle10 /3m39 active /5m13 wall with the explicit log **“Expedition archived.”** It was not a full ten-minute run or a spontaneous resource failure. The observer attempted a live checkpoint after archival, received error2 and retained no resumable live checkpoint. Preserve the partial run and its archive; do not reseed or restore it. Earlier startup-wrapper parse failure was corrected before gameplay and is retained under `startup-failure`.

Three separate **headless background runs** then each simulated600 seconds /30 cycles using the existing cautious offered-card strategy. They took69 seconds of total wall time, opened no window and injected no desktop input.

| Seed | Completed rooms, including Core | Blackouts | Survived | New synergies |
|---|---:|---:|---|---:|
|194043|9|0|Yes|0|
|6113|7|0|Yes|0|
|28417|8|0|Yes|0|

All retained normal prices/failures, used actually offered cards and paid construction/rerolls, and finished with8 Oxygen /29 Food /30 Water. Final Metal36/38/36; there was no resource-collapse ending. The planner did not inspect the draw pile or unknown recipes. Three written checkpoints validate through the production Save reader.

## Findings and next experiments

1. **The first connection can emerge from a sensible placement decision.** The native reveal made the participating rooms and lasting reward clear. The immediate Biomass bonus was less urgent than the opening survival needs. That is an observer impression from one partial session, not a player-study result.
2. **Discovery depends on placement, even when the same room identities appear.** The cautious script separated the turbine and Hydroponics and found no synergy in any run. This suggests testing subtle spatial clues or earlier opportunities with a first-time player; it does not prove the system is too obscure or justify forcing a recipe.
3. **Existing nearby discoveries deserve attention before adding more content.** Survey samples encountered River/Josh/Margot recovery rooms in all three runs; the script never attempts recoveries. The next focused exploration test should pursue a visible recovery target through normal paid routes, then assess how legible its value is in the native presentation.

## Limits

Background simulation bypasses opening dialogue/read pauses and advances gameplay in0.1s steps. It is not ten wall-clock minutes or a blind human playtest. The strategy restricts allowed room identities/copies and may decline affordable cards, so idle time is not evidence of a broken draft. Its no-affordable-card/no-pending-build samples total46/30/27 seconds; do not treat that as all waiting time. Survey uses a real-time throttle: headless survey counts are sampled opportunities, not exact reveal timing or visual salience. No background rendering, sound, FPS, memory, balance or general fun acceptance is claimed.

No gameplay/art/rate changes, imports, exports, signing, upload, Git integration or cleanup. All2,971 real player files,48 source/art/test inputs and signed ZIP size/mtime match the before receipt. Native partial and automated cohorts remain separate.

Evidence: `output/opening-feel-20261019/` contains native timeline/captures/finish record, `background/analysis.json`, three decision traces, production checkpoint audit, process log, preservation receipt, `FINAL.json` and handoff. Future automated pacing checks should use background execution; desktop controls are needed only for a specifically chosen interactive/visual review.
