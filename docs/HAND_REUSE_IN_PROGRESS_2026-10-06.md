# Project handoff

Updated: October 6, 2026 · BrineSpace · Hand refresh optimization in progress

## Objective and acceptance
Reduce the measured ~5 ms card rebuild cost without stale card content, lost input bindings or visual changes. Require behavioral checks, matched CPU attribution and native retained/fresh pixel comparisons before acceptance.

## Accepted decisions and constraints
Preserve card dimensions, artwork, filters, layouts and owner settings. Recompute displayed state; reuse controls only when that presentation and the container's root identities match. Reroll and layout controls still refresh. Scene-owned metadata releases on scene exit. This does not address the unresolved GPU memory budget or certify Windows/Mac releases.

## Current state
Current hand-refresh acceptance and remaining work are recorded in
`docs/HAND_REFRESH_OPTIMIZATION_2026-10-06.md`. Three matched native station pairs
now confirm the narrow CPU savings; historical pending statements below retain
their original scope and no longer describe the next action.

Latest continuation: permanent `tests/test_hand_reuse.gd` (paired UID) is admitted
to cards-bindings in tests/index.json. Native scratch-profile run exits 0 with
74 checks/zero failures and 12 exact retained/fresh image pairs. It covers real
room thumbnails, bound duplicate-index clicks, selection, drag ghost/source fade,
cancellation, input blocking, content invalidation and row/fan hover retention.
The replacement-art fixture now uses a valid gradient and restores original
textures between layouts; reviewed fan screenshot has healthy reactor art.
100 unchanged refreshes: row 8.875 ms / fan 8.679 ms. All 2,936 owner files unchanged.
Run through the guarded output runner with --native --pristine --permanent;
the test refuses an unverified profile. These results supersede the historical
execution failures below, without claiming station performance acceptance.

Unaccepted implementation in scripts/draft_card.gd and scripts/main.gd: presentation snapshots cover room definition, category color, selection, affordability, per-resource cost colors/icons, shortfall, tooltip, prototype, artwork and optional authored-art flag. Unchanged hands skip reconstruction, preserving hover poses. Changed hands remove old roots before queuing deletion.

Baseline physical source copies, isolated fixture and runner are in output/hand-reuse-2026-10-06/. No new art or gameplay rules. Existing script UIDs retained. No commit/export/upload.

## Verification
Baseline red fixture observes 19 failures, including repeated row/fan reconstruction and hover loss; 100 refreshes cost ~380/393 ms. Baseline owner check: all 2,936 non-log files unchanged. Fixture ordering was then corrected to compare cards by bound hand_index because fan stacking may change traversal order.

Post-change headless validation has no accepted result. Session 34373 was repeatedly polled; current log remains baseline, no Godot test process was observed, and the observed launcher Python PID 2095376 subsequently disappeared. Cancellation was requested; the shell session still reports live. Bundled-Python retry session 24069 also has no result. Even print-and-exit shell controls (21491/6629) and terminal control 74264 remain reported live after producing output. This is an execution/session blocker; do not treat old logs as new validation or launch more duplicate tests without rechecking processes. Read-only sessions 99076, 52314, 8224, 88243 and 9586 likewise have not reported completion.

Bundled-Python session 24069 subsequently produced a fresh post-change result: all 50 behavioral checks pass; 100 unchanged refreshes take 8,534 us (row) / 9,457 us (fan), versus baseline 380,350 / 392,885 us. Runner exit=124: Godot did not exit within 180 seconds and was killed. All 2,936 owner files remain unchanged after the run. Behavioral/CPU evidence is available, but this is not a clean complete test pass or native station performance acceptance.

Fixture now waits for observable Control geometry/minimum-size stability, bounded to 90 frames, rather than a fixed four-frame delay. A first native comparison run is live in session 17624 using bundled Python after the headless runner reported its timeout/kill and completed owner check. Native comparisons, clean shutdown, matched station timing and adding accepted regression to tests/index.json remain pending.

Process investigation: read-only command-line query confirms PID 2117852 is our headless fixture and PID 2162184 our native fixture. The headless PID disappeared before a requested cleanup could run (Stop-Process reports no such PID). At 09:08 UTC the native log still contains only the engine header; a direct lookup no longer finds its PID, but session 17624 has not delivered its terminal result/owner check. No native pixel evidence accepted. New runner instrumentation records PID, exact command, scratch profile and terminal/timeout status; post-kill wait is bounded to ten seconds. No more test launches until existing session/process state is resolved.

## Next action
Current: measure before/after in the deterministic 40-room native workload using
the normal renderer. Diagnostic physical Main copies share current code except
the old/new _refresh_cards body and identical bounded timing instrumentation.
No private texture backend or earlier Main revision is substituted. Keep
release memory, stutters, full workload repetitions and Mac gates open.

Later diagnosis and recovery boundary: see `docs/NATIVE_TEST_ENVIRONMENT_BLOCKER_2026-10-06.md`. Windhawk-free engine AND launcher controls still reproduce the empty-engine failure; do not assume injection is the cause. Latest headless repeat is 50 checks/zero failures, 8.445/8.851 ms per 100 refreshes, still exit timeout. Native/station acceptance remains unproven.

Resume/inspect sessions 24069/34373 and current headless.log; verify authoritative process state and recover command-session execution before retrying. Repair any regression, then native comparison and matched station attribution. Only admit the change after those checks. Record the post-change owner fingerprint from the runner. Keep the full release performance, memory, original bug and PC/Mac gates open.
