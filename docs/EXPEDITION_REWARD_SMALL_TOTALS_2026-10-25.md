# Small expedition reward build-up polish

Updated: 2026-10-25 / Project: BrineSpace

## Objective and acceptance
Review the established reveal for rough edges, keeping count-up, sparkle and sound
coherent without adding effects or disturbing accepted timing.

## Accepted decisions and constraints
Preserve exact rewards, final accent priority, sparkle, pitch rise, volume, reduced
motion and quiet zero values. An animated value of 1 has no intermediate step and
therefore should not prevent another counting figure from supplying the ticks.

## Current state
scripts/expedition_report.gd selects a tick leader only when its target exceeds 1.
Data remains the preferred leader. With Data 0/1, station figures of 0/1 are skipped
until a value with actual intermediate steps is found. A Data reward of 1 retains
its hero chime and pulse; zero remains silent. All timing and visual code unchanged.

tests/test_reward_count.gd now builds representative report controls and real
counters against an audio spy, exercising Data 0/1 with station values 1 and 24.
This checks actual selection/routing, not only the sound-filter helper.
The native fixture saves this revision's captures to its own directory.

## Verification
Baseline: two expected failures, output/test-runs/20261025-160850-headless.
Numeric/routing test PASS: output/test-runs/20261025-160907-headless.
Native report PASS: output/test-runs/20261025-160910-native.
Native covers existing standard-reward pitch, gain/mute, cadence, sparkle, exact
payout, compact 130% bounds and progression return. No changed pixels require a
new visual redesign review; prior design acceptance remains scoped to its reports.
Captures: output/expedition-reward-small-20261025/. Native remains silent; owner
listening acceptance is still pending. Scoped whitespace check passed.

All Godot runs used scratch APPDATA. Protection receipts:
D:/bs-tutorial-20261021/ending-small-before.json and ending-small-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged. No export produced.

## Next action
Owner listening review with a one-Data expedition or guarded preview. No preview
was launched as part of this pass. Focus-pause settings were inspected and retain
their documented running-station-only scope; no new focus behaviour added.
