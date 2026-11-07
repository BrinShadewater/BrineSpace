# Expedition reward rhythm polish

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
Make the count-up, sparkles and sounds feel more satisfying together, preserving
accepted presentation and the owner's interactive preview.

## Accepted decisions and constraints
Readable slowing beats, a single audible tick leader, earlier small landings and
a distinct Data finish. Keep rewards, exact values, artwork, reduced motion and
unblocked controls. Preview remains isolated from the owner's profile.

## Current state
- scripts/reward_count.gd: visible numbers advance on 65-120 ms slowing beats;
  every changed intermediate step emits its matching tick request. Long frames
  never produce catch-up bursts. Existing separate landing clock remains intact.
- scripts/expedition_report.gd: only Data supplies audible ticks, or the first
  positive figure if Data is zero. All counters retain distinct landing events.
  Small counters run 580 ms with 45 ms stagger; hero remains 900 ms + 120 ms delay.
  Last small landing is at 760 ms, Data at 1,020 ms: 260 ms separation, beyond
  the small tone's 180 ms playback limit. No PCM or gain change.
- tests/test_reward_count.gd: checks matched step/tick requests, readable intervals,
  slowing cadence and single-leader routing alongside previous edge regressions.
- tests/test_expedition_report_native.gd: asserts final-accent timing separation.

## Verification
Baseline beat regression failed as expected (60 assertions),
output/test-runs/20261024-215616-headless.
Numeric and routing tests PASS: output/test-runs/20261024-215804-headless;
native report PASS:
output/test-runs/20261024-215638-native.
Reviewed sparkle capture in output/expedition-reward-rhythm-20261024; native fixture
also covers compact 130%, accounting, audio volume/mute and progression return.
Native tests stay silent: listening/subjective feel acceptance remains with owner.
Scoped whitespace check passed. All Godot runs use isolated APPDATA.

## Next action
Interactive preview refreshed from process 179096 to 182584, with a fresh scratch
profile under output/expedition-ending-preview-20261024/scratch-appdata-rhythm.
Click PLAY REVEAL or press R to hear the revised sequence; startup is silent.
Review preview readiness and profile protection receipt alongside final handoff.

Preview ready and responsive; its log is clean. Protection receipts:
D:/bs-tutorial-20261021/ending-rhythm-before.json and ending-rhythm-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged. No export produced.
