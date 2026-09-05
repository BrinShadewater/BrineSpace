# Full-run Discovery Balance Pass — 2026-09-04

## Outcome

The discovery/polish work is merged into local `main`. Remote documentation, rights files and CI were preserved; the only merge conflict was the README's Verification/Development Notes boundary. Merged-result tests passed before the completed discovery worktree was removed. Nothing was pushed.

The clearest pacing problem was exhausted draft access: all 18 losses in the corrected baseline sweep ended with zero rerolls. A focused regression reproduced a sustainable station with no affordable card and no way to reach its next foundations through waiting. Draft recovery now rebuilds one charge every four simulation cycles while below three charges. It does not disclose recipes, alter draws, spend Research, or revoke directive reward overflow. Paused time earns nothing; reboot clears partial progress.

Matched full-run results improved from **12/30 to 21/30 completions**. Every doctrine pair completed at least one run after the change. This is a comparison of one automated policy, not a target player win rate or a claim that the game is balanced.

## Matched results

Each row uses the same three seeds: `4404`, `9021`, `1729`.

| Doctrine pair | Baseline wins | With draft recovery |
|---|---:|---:|
| Industry + Biosphere | 2/3 | 2/3 |
| Industry + Science | 2/3 | 3/3 |
| Industry + Recovery | 3/3 | 3/3 |
| Industry + Anomaly | 2/3 | 2/3 |
| Biosphere + Science | 0/3 | 1/3 |
| Biosphere + Recovery | 0/3 | 3/3 |
| Biosphere + Anomaly | 1/3 | 2/3 |
| Science + Recovery | 0/3 | 2/3 |
| Science + Anomaly | 1/3 | 2/3 |
| Recovery + Anomaly | 1/3 | 1/3 |

| Observation across 30 runs | Baseline | With recovery |
|---|---:|---:|
| Simulated cycles | 852 | 833 |
| Cycles with no build | 424 (49.8%) | 359 (43.1%) |
| Newly learned patterns | 115 | 116 |
| Decrypted blueprints | 106 | 102 |
| Newly decrypted room types built during their run | 70 | 78 |
| Median first discovery | Cycle 2 | Cycle 2 |

Discovery volume is essentially unchanged. The improvement is chiefly access to further decisions and reuse of rewards, not more recipes or guaranteed discovery. Raw unlock totals also depend on when a run ends.

### Held-out check

Seed `42` was run across all ten pairs after choosing the recovery cadence, without further tuning: **4/10 completed**. That seed rolled Harmonic Station as the final directive for every pair. The other six runs ended on three second-stage deadlines, two final deadlines and one crew collapse. This weaker result is a useful warning against treating the matched 70% completion rate as general balance. The held-out report is `%TEMP%\brinespace-balance-heldout.json`.

## Method and reproduction

`tests/playtest_balance.gd` runs the actual main scene with normal costs and failures, clean starting knowledge, zero mastery, three-card hands, seeded random deck shuffles, all three directives and seeded orbital events. It advances real cycle/input handlers quickly instead of waiting 20 wall-clock seconds per cycle. It does not force card order, grants, room unlocks or victory.

The fixed comparison policy, `curious-builder-v3`, evaluates visible resources, power reserve, room production/costs, matching doors, the current directive and recipes already learned during the run. It tries new neighbor combinations and can repeat learned links for an explicit link/Resonance objective. It never inspects the draw pile to select actions or consults undiscovered recipe definitions. At most three builds happen between cycles; an idle player may spend a reroll on alternating cycles.

Early diagnostic policies were corrected before the matched comparison: the first ignored reserve buffers and learned yields, and the second incorrectly refused zero-power rooms during a shortage. Those exploratory results are **not** the baseline in the tables.

Run from the project root with Godot 4.6.1:

```text
Godot --headless --path . --script res://tests/playtest_balance.gd -- --output=<absolute-report.json>
```

Optional filters: `--seed=4404`, `--pair=biosphere+science`. For native screenshots, omit `--headless` and add `--capture-dir=<absolute-directory>`. Images cover cycles 3/10/20, the real end screen and the final station. Captures assert that Fit Station contains every room. Invalid pair filters fail rather than reporting an empty successful sweep.

`e882ec6` contains the diagnostic harness with pre-recovery gameplay for reproducing the headless baseline. Use the subsequent fix commit for the matched after-run. Both reports were produced with policy v3. Saves use `user://brine_balance_playtest.json`; loaded player meta is cleared before the run and test writes never overwrite `brine_save.json`.

Local evidence (generated, not committed): `%TEMP%\brinespace-balance-before-v3.json`, `%TEMP%\brinespace-balance-recovery.json`, `%TEMP%\brinespace-balance-captures`, and the corresponding Godot logs. JSON reports include every build, resource/hand snapshot, discovery/unlock cycle, prototype use and failure reason.

## Visual finding

The native Biosphere + Science run at seed 4404 completed all three directives at cycle 34 and learned five patterns. Its mature station exposed a camera bug: Fit Station was clamped at 22% zoom and cut off rooms. The overview range now reaches 2%, with a matching finer-grained slider. A tall connected-station regression failed before the fix and passes afterward. UI checks retain the compact draft countdown instead of adding another overlay.

## Verification

- All five regression/integration scripts passed: `test_synergy_manager`, `test_discovery_progression`, `test_polish_gameplay`, `test_run_balance`, and `playtest_polish` (52 focused regression cases plus scene assertions).
- All 23 GDScript files parsed, including the separate core animation scripts. Asset import and the main-scene smoke test completed without engine errors; smoke exit was `0`.
- Native full-run capture matched the headless Biosphere + Science result and passed all room-in-viewport assertions. The final station, recovery countdown, summary and 1280/1600/1920/2560 UI layouts were inspected. The retained discovery/FX scene playtest also passed in the native renderer.
- Both draft recovery and expanded-station fit were observed failing in focused regressions before their fixes, then passing afterward. Final logs were checked for `SCRIPT ERROR:` and `ERROR:` as well as process exit codes. `git diff --check` passed.
- The 30-run before/after comparison and ten held-out runs all completed without harness errors. These accelerated automated runs do not replace normal-speed human playtesting.

## Remaining work

- Some first discoveries are still very late: Industry + Recovery seed 9021 first learns at cycle 17, and Biosphere + Science seed 9021 at cycle 21. Slow reroll recovery alone does not solve those openings.
- The remaining nine losses are six second-stage doctrine deadlines and three final Resonance deadlines. Some healthy, large stations reach 150–170 of the required 180 Resonance; other runs lose time recovering power and mining access.
- One Biosphere + Recovery run wins by repeating a single learned pattern. That is a valid build path but weaker evidence for the desired continual-learning experience.
- The bot never suspends rooms, plans several placements ahead, or spends knowledge from previous reboots. Do not weaken survival systems merely to make this policy win every seed.
- Three matched seeds and one held-out seed per pair are a small sample. Run human sessions at normal speed and a broader seed set before retuning final targets or changing the starting deck.
- A new blueprint can still be stranded behind an expensive hand temporarily; recharge provides recovery, not instant access. Measure the frustration against the value of the drafting decision before removing that tradeoff.
