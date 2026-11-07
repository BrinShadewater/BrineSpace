# Project handoff

Updated: October 16, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: focused crew-stall pass

## Objective and acceptance

Investigate the earlier 393 ms crew scope once, fix only proven repeated work,
preserve appearance/crew behavior, repeat 4× soak and placement performance,
then move toward release QA. This bounded pass is complete without a runtime fix.

## Accepted decisions and constraints

No speculative navigation shortcut, broad refactor or quality reduction. Keep
the previous unbatched reference plus accepted report worker; structural candidate
stays private. Scratch APPDATA/resolved user-dir guards and owner fingerprints
remain mandatory. Existing performance gates remain unmet. No new release claim.

## Current state

No production or registered-test changes. Added diagnostic helpers and unrun
conditional oracle under `output/crew-stall-20261016/`, evidence in
`C:/bs-crew-stall-20261016/`. Added this handoff,
[results](CREW_STALL_PERFORMANCE_2026-10-16.md), the focused plan and CURRENT_STATUS
milestone. Other pre-existing working-tree work preserved.

## Verification

Native instrumented 24k frames: crew max 58.247 ms, whole max 106.765 ms.
Repeated detour/reachability/passage work is concrete; the proposed fixed-endpoint
exit is unproven and unimplemented. Original 393.261 ms stall did not recur.
Two uninstrumented 480-frame runs give four exact captured-state/camera pairs:
normal idle 47.17–52.45 FPS, 4× idle 38.27–38.54 FPS, 4× placement 35.22–37.66 FPS.
Placement whole frames 67.880/59.043 ms; following 60 frames each have two >50 ms.
No phase reaches 60 FPS. Final 4× soak: 26,000 frames/582.5 s,
p95/p99 33.980/47.809 ms, max 88.411,
0 frames >100 ms, 0 reports. Full durations retained.

All 13 owner guards pass, 2,948 files unchanged;
55 installed guards and frozen runtime/source/native
identities match. Game exited; editor preserved. No WPR started. Independent
review confirms benchmark interpretation. Earlier incident caveat persists.

## Next action

Stop this optimization pass. Inventory accepted private changes and freeze a
full-current-source candidate before actual Windows package QA; this reused
diagnostic runtime cannot certify it. Mac needs native hardware/gameplay,
performance and signing/notarization/Gatekeeper validation. See release workflow
and dated evidence; keep 393 ms cause open rather than claiming a fix.
