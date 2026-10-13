# Project handoff

Updated: October 6, 2026 · BrineSpace · Cycle persistence attribution

## Objective and acceptance
Reduce measured cycle spikes without changing rewards, progression, immediate saving or visuals. Rendering and PC/Mac release gates remain separate.

## Accepted decisions and constraints
No delayed background saves or weakened backup protection. Preserve duplicate-award behavior, default one-argument callers and existing mutation-on-save-failure behavior. All probes use verified scratch profiles; normal art and GPU backends unchanged.

## Current state
Changed scripts/meta_state.gd, scripts/main.gd and tests/test_meta_fields.gd (existing UID retained). Stabilization accepts an optional nonnegative reward and writes pattern plus reward together; Main computes the same authored reward before that call. Four simultaneous awards now make four protected writes instead of eight. No broad batching across unrelated events.

Diagnostic copies/logs/results: output/cycle-detail-2026-10-06/. Bounded method timers attribute baseline card rebuilding to about 4.9–5.3 ms per refresh and resource refresh to about 2.5–2.7 ms. Discovery with no new event takes only ~20 us; avoid optimizing its inexpensive state transition.

## Verification
One matched deterministic 40-room HEADLESS CPU pair: cycle-three discovery/stabilization 12.671→7.311 ms (~5.36 ms less). Same-epoch writes 9→5 include one separate unchanged save; reward writes 8→4. Final four discovered/four stabilized patterns and 20 Data match; all 12 phase crew/drone/power/zoom/action/speed states match. Interface refresh remains ~12 ms. Headless phase times and dummy GPU counters are not native frame or memory acceptance.

Regression fails red on old one-argument API, then meta field/reward and isolation tests pass. Checks cover disk reload, one-write reward, duplicate idempotence, legacy caller, negative reward, injected write failure preserving prior disk, and explicit retry. Discovery progression executes all checks with exactly one failure: its expected foundation omits hydroponics_farm/storage_depot/moonbay/tidal_power_plant. All four already exist in HEAD's starting list; no roster/test expectation changed. Other progression checks pass; suite is not reported green.

Native probe did not create a window and was stopped; no native result accepted. Initial diagnostic variable-name parse conflict corrected; failed logs retained separately where available. Both CPU runs and tests preserve all 2,936 owner non-log files. No packaged gameplay/Mac/visual acceptance performed this interval.

## Next action
Verify this narrow save change in a visible native matched workload once display startup works. Address repeated hand-card rebuilding with explicit presentation invalidation and hover/input/state regression coverage; resource forecast reuse needs separate measured invalidation checks. Resolve the foundation test mismatch against accepted large-room availability. Atlas sampling, memory budgets, long native soak, original bug closure and packaged Windows/Mac certification remain open.
