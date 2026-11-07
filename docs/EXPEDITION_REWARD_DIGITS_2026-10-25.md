# Expedition numeric steadiness polish

Updated: 2026-10-25 / Project: BrineSpace

## Objective and acceptance
Polish the existing combined count-up/sparkle/sound reveal, smoothing a visual
rough edge without adding more effects or changing accepted reward timing.

## Accepted decisions and constraints
Keep the existing Barlow interface face, artwork, count cadence, pitch, landing
pulse, chime and reward math. Preserve zero, mute, reduced-motion and interruption
behaviour. Apply typography only to numeric labels owned by reward counters.

## Current state
scripts/reward_count.gd wraps the label's existing Font in a cached FontVariation
with tnum enabled, then reserves the final text width using that same font. Numeric
font remains at completion, preventing a final switch back to proportional digits.
No font binaries or global theme changed.

tests/test_reward_count.gd now uses the real bundled interface font and verifies
that 1111 and 8888 have the same advance, in addition to previous timing/routing
and interruption checks. tests/test_expedition_report_native.gd verifies retained
numeric alignment after landing and captures this revision to a new directory.

## Verification
Source font inspection showed proportional digit advances (1=303, 8=472 units)
and an existing tnum feature. Baseline equal-width regression failed three checks:
output/test-runs/20261025-114310-headless.
Final numeric/routing PASS: output/test-runs/20261025-114336-headless.
Native report PASS: output/test-runs/20261025-114339-native; clean log.
Sparkle and compact 130% captures reviewed:
output/expedition-reward-digits-20261025/.
Native includes existing pitch, effects gain/mute, final-beat, accounting and shop
return checks. Native runs remain silent; subjective listening acceptance remains
with the owner. Scoped whitespace check passed; no broad asset batch or export.

All Godot runs used scratch APPDATA. Protection receipts:
D:/bs-tutorial-20261021/ending-digits-before.json and ending-digits-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged.

## Next action
Owner review during a natural expedition ending or via the guarded preview tool.
The previous interactive preview was already closed and was not restarted.
