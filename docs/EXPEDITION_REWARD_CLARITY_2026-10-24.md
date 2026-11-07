# Expedition reward final-accent clarity

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
Polish the count-up, sparkle and sound sequence as a whole, particularly legibility
and avoiding crowded audio after slow frames.

## Accepted decisions and constraints
Keep existing count cadence, rising pitch, quiet final beat, settling pulse and
reduced-motion/mute rules. No reward, artwork, layout, sound asset or gain change.

## Current state
- scripts/expedition_report.gd binds the main counter to small-figure sound routes.
  Once the main counter has landed, later ui_reward_land requests are ignored.
  This protects the final chime when a long frame lands multiple figures together.
  Main zero never lands, so ordinary small-figure sounds still work for zero Data.
- scripts/reward_count.gd draws a shallow rightward sparkle fan with bounded reach;
  particles no longer cross the final digits or spread as far into adjacent captions.
- tests/test_reward_count.gd covers suppressed late and retained normal landings.
- tests/test_expedition_report_native.gd saves this revision's captures separately.

## Verification
Baseline routing regression failed as expected:
output/test-runs/20261024-232720-headless.
Final numeric/routing PASS: output/test-runs/20261024-232750-headless.
Native report PASS: output/test-runs/20261024-232752-native; clean log.
Reviewed sparkle and compact 130% captures:
output/expedition-reward-clarity-20261024/.
Existing native checks cover pitch, effects gain/mute, exact payout, progression
return and empty report. Native remains silent; subjective listening acceptance
is still for the owner. Scoped whitespace check passed.

Godot runs used scratch APPDATA. Protection receipts:
D:/bs-tutorial-20261021/ending-clarity-before.json and ending-clarity-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged. No export produced.

## Next action
Owner review of the combined reveal in a natural ending or the existing guarded
preview tool. The earlier preview process was no longer running and was not reopened
for this polish request. All illustration, source and audio changes remain local.
