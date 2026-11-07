> Follow-up correction, October19: rerolls consume charges, not Metal. With the same2-Metal buffer, suppressing them did not shorten the observed saving/recovery time. Earlier wording implying a Metal expense or inflated saving wait from rerolls is superseded by the [fresh guided comparison](COMPANION_GUIDANCE_FRESH_RUN_2026-10-19.md). Original results and text remain below.

# Nearby companion recovery and opening pacing — October 19, 2026

Owner requested background play using normal costs. Nine fresh source-game openings compare three seeds (194043, 6113, 28417): normal expansion, an early recovery detour, then a prepared recovery policy. No desktop input, windows, supplied cards/resources, inherited unlocks, free building or disabled failures. No gameplay/balance/art edits or release changes.

## Result

**Josh is a viable early goal once Food/Oxygen are established.** All three prepared openings recovered him and survived 600 simulated seconds /30 cycles without a blackout. This is scripted mechanical/pacing evidence, not a human-fun verdict.

| Seed | Josh aboard, game time | Food / Oxygen / Water minima | Completed rooms at 10m | Control rooms at 10m |
|---|---:|---:|---:|---:|
|194043|4:09.0|8 /8 /4|10|9|
|6113|4:09.0|8 /8 /4|9|7|
|28417|3:49.2|8 /8 /4|9|8|

The already-paid Mining Drone Bay at21,20 provided a matching door to Josh's surveyed Storage Room at22,20. No extra connector was needed in these three openings. All companion targets were surveyed in the first sample; none of these times measures how long a human takes to notice one.

The prepared policy builds the actually offered Solar, Mining, Current Turbine and Hydroponics before saving for recovery, and requires a nonnegative Food/Oxygen forecast. Target selected/connected at86.2s; normal payment at185.2s deducts exactly8 Metal (11→3). Real Major Bill routing/welding completes the hull at220.4–222.6s, followed by the ordinary object-opening action and eight powered seconds of restart. Two cases wait for the next operating cycle before restart. Josh's roster membership and active actor are verified; he does not increase crew, occupy a berth or perform construction.

## Tradeoffs and reward

Saving under this policy lasts99s after target selection and includes normal paid rerolls at104.9/145.6s. It also keeps at least2 Metal after repair. **This is not the shortest achievable recovery time or a mandatory99-second gate.** After payment, sampled time to Josh aboard is44.0–63.8s, including crew approach, repair, object opening and Power/operating-cycle timing; the18s welding/8s powered restart constants were not changed.

Compared with same-seed expansion controls, Desalination completes110.0–116.7s later (284.4–286.5s rather than168.7–174.4s), and the first Corridor109.8–124.9s later. Water stays≥4 here without an opening fire, so these runs do not establish that postponement is safe under sprinkler demand. Controls all survive too; payments, work, rerolls and placements produce different later trajectories, not a single-variable replay.

Restoring Storage beside Mining naturally discovers **Ore Buffer** atcycle11–12 /220.4–240.2s, and stabilizes atcycle13–14 /260.6–280.6s. Its functioning bonus is+1 Metal/cycle; the doubled bonus applies from a later loop, while5 Archived Data and the related blueprint discount are immediate. No blueprint is automatically decrypted. One seed later finds Logistics Spine; it is not a guaranteed follow-up. Josh is met this loop and must still be bought in Meta Progression to return in future loops.

At ten minutes, Margot's still-sealed known room has a matching connected door in all three prepared cases; River remains known but unconnected. This supplies another mechanical goal, not evidence that the UI makes that next goal legible. Final prepared stocks are Oxygen8 /Food34 /Water36 and Metal69/47/48; the control has8/29/30 and Metal36/38/36. Extra room capacity, discovered patterns and changed later choices contribute; don't attribute the stock difference to the companion actor alone.

## Unsuccessful early policy retained

The first recovery policy began saving after Solar/Mining only. It rerolled the offered Hydroponics at62.2s while reserving repair funds. It recovered Josh at108.2/108.2/129.1s, then lost Major Bill: starvation330.1s in seed194043; Oxygen exhaustion255.0s in6113/28417. The ended runs appropriately cannot write a final live checkpoint (error2). This demonstrates a poor scripted opening decision; it does not isolate the8-Metal price as the cause. The later prepared cases fix the planner's ordering, with no game-rule change. A progress update initially called the first death Oxygen failure; final logs establish starvation and govern this report.

## Verification and limits

Both gameplay processes exit0 with zero script/engine/harness errors. Six surviving checkpoints validate through the production reader. Three prepared checkpoints are copied to another scratch profile and restored through production Save.restore: resources, cycle, crew, companion roster and site state match; Josh is active after restore and after five more simulated seconds; new continuation checkpoints validate. Source checkpoints, metadata and sidecars remain hash-equal. This is a short continuation check, not long-term endurance or a native UI Continue acceptance.

The first audit had six passing state checks followed by a fixture shutdown error: it cleared music streams without disabling the autoload's processing. That attempt is retained under `audit-first-attempt`. The harness now disables StationMusic before the standard audio drain, matching the existing opening harness; the full audit rerun exits0 without script/engine errors. Game audio code is unchanged.

Every Godot process uses scratch APPDATA and asserts the globalized user path before starting. All2,971 real player files,52 protected source/art/test inputs and the signed ZIP size/mtime remain unchanged. No real save restoration, reset, imports, exports, signing, upload, Git integration or cleanup.

These are600 simulated seconds in0.1s gameplay steps, not ten wall-clock minutes. Opening dialogue and feedback reading pauses are skipped. The normal light/occlusion survey is queried every simulated second by resetting only its wall-clock throttle; no survey cells are granted. Other production wall-clock throttles remain. Strategy restricts room choices/copies and uses paid rerolls. Only Josh's nearby existing-door route was pursued; River/Margot, longer/expensive routes, fire-heavy openings, larger crews, visual/sound salience, human fun, FPS/memory and Apple/release behavior remain unaccepted.

## Next useful step

Keep the current price for now. The rescue already connects exploration, a new companion and an economic pattern. Review whether the existing inspector makes “save8 Metal → repair → open → power” and the next reachable target clear to a new player; any cue/presentation change needs a separately scoped implementation. Before tuning the wait, compare a policy that avoids discretionary paid rerolls while saving. Do not infer a need for cheaper recovery or new content from this small scripted cohort.

Evidence: `output/companion-opening-pacing-20261019/analysis.json`, per-run traces, both `opening-results.json`/process logs, final audit receipts, `preservation.json`, `FINAL.json` and `HANDOFF.md`. Early failures and first audit are retained.
