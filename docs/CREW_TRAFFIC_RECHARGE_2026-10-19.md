# Crew traffic and Marsh recharge — October 19, 2026

The retained traffic failure is fixed locally. Marsh now budgets his return to the original charging pod. Three- and four-person depletion replays pass with normal costs and failure rules. No release was rebuilt or published.

## What changed

- `rooms/underwater/corridor_geometry.gd` continuously checks the same 16-point foot outline along a corridor segment, with a rectangular fast path. The former 4px sampling could approve a shortcut through the concave elbow and then reject a real movement step on that line. Cell-mouth intersections also retain valid boundary contacts despite floating-point rounding.
- `scripts/bill_npc.gd` uses that corridor sweep when planning/checking segments. Crew clearance, movement speed, paid construction and the bounded two-candidate passage-yield search remain intact. No room art/layout was changed.
- `scripts/marsh_npc.gd` retains a minimum 35% return reserve, increasing it for the actual pod route: ordinary walking time including flood slowdown, multiplied by 1.5 for traffic, plus 20s margin, capped at 95%. The estimate refreshes every 5s in the same room and immediately after room/home/navigation/flood-speed changes. It is derived state, not a save-schema addition. Battery capacity, Power price, charge rate, finishing an active weld, pause and emergency crawl remain unchanged.
- Two paired-script regressions were added to the crew test group: `test_corridor_traffic_clearance` and `test_marsh_return_timing`.

## Reproductions and verification

The original geometry regression failed before the fix. The long-return regression also failed under the fixed 35% policy. During implementation, an additional cell-mouth boundary regression exposed a numerical rejection; it now passes. Intermediate failures and probe logs remain under `output/crew-traffic-recharge-20261019/intermediate` and the dated test-run receipts.

**11 focused checks pass** in `output/test-runs/20261019-181504-headless`: both new regressions; passage search budget; the concurrent/idle-blocker passage probe; construction, fitting routes and break checks; Marsh battery/charging/Save-Continue; corridor swim shortcuts; NPC segment clearance; Parts Passage. The constructed 6,266px long return starts at 70%, reaches the pod with a sampled minimum 24.6%, recharges fully and spends 4 Power. Its speed/clearance and bounded budget-query checks pass. This controlled navigation fixture is separate from the paid gameplay replays.

The retained paid build at **26,17**, previously still blocked after 180.1s native replay, completes in **51.4 simulated seconds** on the final native replay. The narrow-route recovery from the real three-crew checkpoint also succeeds: all four named crew are recovered by **352.1s**, followed by another 120s hold. No Tee Corridor workaround was needed. Construction blueprints were explicitly supplied as in the earlier test; resources and crew were earned through normal gameplay.

| Retained paid station replay | Surveyed mining/salvage naturally spent | Additional hold | Minimum Food / Oxygen / Water / Power |
| --- | --- | --- | --- |
| Three crew, 23 mining + 16 salvage loads | 766.2s | 360.1s; total 1,126.3s | 27 / 27 / 29 / 10 |
| Four crew, 5 mining loads; local salvage already empty | 154.1s | 360s; total 514.1s | 26 / 27 / 30 / 8 |

Both keep all crew alive, with no blackouts. The source profile already has stabilized Breathable Quarters. **120 mining and 150 salvage loads remain remotely**, so this is local surveyed depletion, not whole-map exhaustion or fresh-draft pacing acceptance. Renewable Metal behavior and the earlier same-loop stabilization wording issue were not changed.

In a separate **1,000s four-crew duty replay**, Marsh makes **four returns, four docks and four full recharges**. Minimum battery is **16.97%**, with zero time at empty battery. All four crew survive; Food/Oxygen/Water remain at least 26/27/30 and Power at least 8. A **420s native replay** reproduces the 16.97% minimum and two returns/docks. Native screenshots were inspected for context; the dock screenshot has a dialogue overlay and is not full visual acceptance.

An initial observation counter missed the first exact-full transition because it tested the prior battery against 99.9%. The counter now watches the actual returning-to-duty transition. The repeated 1,000s replay records all four completions; the earlier receipt and native counter are retained transparently. This was a harness-only correction.

Six final checkpoint/meta pairs independently validate. Final scenario processes report zero script/runtime errors. All **2,971 player files**, **29 other protected source/art inputs**, eight retained fixture inputs and the signed ZIP stat are unchanged. The three intended navigation/recharge source changes have SHA256 receipts. Earlier failed attempts are retained; the final receipts govern.

## Evidence and remaining scope

`output/crew-traffic-recharge-20261019/FINAL.json`, `preservation.json`, `checkpoint-audit.json`, `focused-tests.log`, per-case `*-results.json` / `*-process.json`, and `HANDOFF.md`.

These are local editor-source fixes and bounded scripted/native replays. They do not establish fresh offered-card pacing, arbitrary station-size endurance, process-memory headroom, performance improvement, Apple acceptance or release-package validation. Next useful validation is a manual paid run using actual offers and longer crowded/flooded routes before any release integration.
