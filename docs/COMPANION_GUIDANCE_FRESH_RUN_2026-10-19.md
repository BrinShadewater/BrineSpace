# Fresh companion guidance test, no rerolls while saving — October 19, 2026

Owner requested a fresh background run using normal costs and skipping rerolls while saving8 Metal. Six fresh source-game openings use the same three earlier seeds: the main policy pays once8 Metal is available; a matched control retains the earlier2-Metal reserve. Both skip rerolls from target selection until repair payment. All six survive600 simulated seconds /30 cycles without blackouts or Food/Oxygen/Water exhaustion.

## Main result

**Josh joins at208.3s /3:28.3 in all three main runs.** The policy first completes Solar, Mining, Current Turbine and Hydroponics using actual offered cards and paid construction, then follows the Journal's next connected recovery. It selects Josh at86.2s, pays at161.0s and saves for74.8s. The first eligible sampled delivery leaves9 Metal; the normal8-Metal repair spends it to1. The policy does not wait for an extra2 Metal buffer. There is no instant grant, restored opening, blueprint injection, free build, failure override or clock-based repair.

| Seed | Policy | Repair paid, s | Josh aboard, s | Desalination complete, s | Food /Oxygen /Water minima |
|---|---|---:|---:|---:|---:|
|194043|buffer2|185.2|249.0|286.5|8 /8 /4|
|194043|exact8|161.0|208.3|261.3|8 /8 /4|
|6113|buffer2|185.2|249.0|285.4|8 /8 /4|
|6113|exact8|161.0|208.3|262.1|8 /8 /4|
|28417|buffer2|185.2|229.2|284.4|8 /8 /4|
|28417|exact8|161.0|208.3|251.3|8 /8 /4|

All three main runs retain normal physical crew repair: Major Bill must travel and weld; hull progress is not set by the harness. The8-second powered restart and operating-cycle rules stay in force. Ore Buffer is naturally discovered atcycle10 /200.6s and stabilized atcycle12 /240.2s, with the existing immediate Data/discount and later-loop doubling rules. Current-loop Josh is not automatically bought for future loops. Other later patterns vary and are not guaranteed rewards.

## What the guidance did in actual fresh play

The script chooses the target shown by the current UI helper, opens the real Journal Crew tab and presses its actual Inspect Recovery button. The inspector's real repair/open action performs the payment and object opening. Live checklist state, exact Metal shortfall, worker status, restart progress and action visibility are recorded during the normal opening; no sites are inserted into survey memory. Mining supplies the already-paid matching door to Josh in these seeds.

The one-second decision trace records Step2, Step4 and Recovery Complete. Step1 was already satisfied when the target was selected; the object-opening action refreshes and consumes Step3 within the same decision, so a separate retained Step3 sample is not claimed. All guidance headings/actions derive from the live site state, not supplied UI fixture values. Normal source costs/failures and physical crew work are asserted for each run.

After Josh joins, the inspector offers **Margot, sector20,22** as the next surveyed companion with a connected door. Both its live link and the actual Journal target button successfully focus that unbuilt site in all six runs, showing its next repair step and current shortfall. No second rescue is paid or forced. This verifies fresh-run navigation/state; it does not establish that a new human player notices the clue. The previous normal/compact native presentation review remains separate evidence; these headless runs add no new pixels or visual-salience acceptance.

## Reroll correction and comparison

**Ordinary rerolls consume a reroll charge, not Metal.** `_discard_card` decrements `rerolls_remaining`, swaps the card and refreshes the UI; `_refill_hand` changes the draft, not the resource stock. My earlier suggestion that paying for rerolls inflated the Metal-saving wait was misleading. References to “paid rerolls” in older reports mean charge use; they must not be read as Metal payments.

With the same2-Metal buffer, skipping rerolls leaves payment at185.2s and recovery at249.0/249.0/229.2s, exactly matching the earlier buffered observations. Keeping the extra reserve is what postponed the payment in this cohort. Paying once8 is available advances payment24.2s and Josh's arrival20.9–40.7s; differences after payment also include crew travel and the operating-cycle boundary. The main policy's74.8s saving interval is still not a global optimum.

No rerolls occur during the saving window in either policy; normal charge-based rerolls may resume after repair payment. Suppressed-decision counts are repeated eligible script checks, not the number of charges that a player could have spent. Holding cards also changes later draft/build choices, so later stock or room-count differences must not be attributed solely to the companion or a timing improvement.

Desalination finishes251.3–262.1s in the main policy,23.3–33.1s earlier than the new buffered controls. Stored Water never falls below4 here; no severe fire was injected. This is not a guarantee that every fire-heavy opening can postpone Water production safely. Skipping rerolls preserves charges/cards, but does not manufacture Metal or prove faster mining.

## Verification and limits

The background gameplay process exits0 with zero script/engine/harness errors. Six checkpoints validate; copies of the three main checkpoints restore through production Save.restore in another scratch profile. Resources, cycle, crew, roster and site state match; Josh is active, the checklist says Recovery Complete, and after five more simulated seconds he remains active and rewritten checkpoints validate. Original checkpoints, metadata and sidecars remain hash-equal. The audit exits0 without script/engine errors; its teardown logs retain3 CanvasItem RID and6 ObjectDB warnings, so no leak-clearance claim is made.

All processes use scratch APPDATA and verify globalized user:// before gameplay. All2,971 real player files,59 current source/art/test/UID inputs, five retained probe/evidence inputs and signed ZIP size/mtime remain unchanged. Only new test artifacts and documentation changed. No desktop input/window, game-code/asset/tuning edits, imports, builds, signing, upload, merge, commit, push, release or cleanup.

These are scripted600-game-second openings using deterministic0.1s steps, not ten wall-clock minutes or blind human play. Dialogue/feedback reading pauses are bypassed. Production light/occlusion survey runs at a simulated one-second sampling cadence, with no granted cells; other wall-clock throttles remain. Prior-source comparison is a separate cohort with unchanged recovery method bodies, not a same-process performance benchmark. Only Josh's nearby existing-door route is recovered; larger/longer routes, second rescue, severe-fire pressure, human fun, rendering/FPS/memory, endurance and Apple/release acceptance remain open.

## Direction

Keep the8-Metal cost and current guidance. The ordinary fresh-run recovery and next-target flow work in this cohort. The next useful observation is whether a first-time player notices and follows that flow, or whether another nearby companion route offers a similarly satisfying decision. Do not repeat the no-reroll saving experiment as if it were still pending, and do not propose rerolls as a Metal sink.

Evidence: `output/companion-guidance-fresh-20261019/` contains the independent probe/loop, six results and traces, UI-state changes/action history, comparisons, process/audit logs, preservation receipt, `FINAL.json` and handoff. Earlier evidence files remain intact.
