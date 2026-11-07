# Expedition reveal synchronization polish

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
Polish how ticking numbers, sparkles and sounds work together on the ending screen.

## Accepted decisions and constraints
Preserve the accepted fast count-up, short sounds, existing art/layout and reward
math. Keep reduced-motion, zero rewards, bounded tick requests, exact values and
uninterrupted controls. Give Archived Data more emphasis than smaller figures.

## Current state
scripts/reward_count.gd now starts a separate landing clock when the final number
is first shown, setting landed state before emitting the chime. Brightness and
sparkles use that same clock. A slow frame can no longer consume the whole sparkle
window while still emitting a fresh chime. Small-figure brightness is reduced from
28% to 16%; hero remains 28%. Sparkles have a small visible core at their first frame.

Added slow-frame regression to tests/test_reward_count.gd. Native report fixture
asserts landing age zero when the chime is emitted, then advances into the sparkle
for capture. Changes: those three files plus current status and this handoff.

## Verification
- Baseline expected regression: 3 failures,
  output/test-runs/20261024-202552-headless.
- Numeric test PASS: output/test-runs/20261024-202626-headless.
- Native report PASS: output/test-runs/20261024-202628-native, clean log.
  Includes paused audio routing, volume/mute, exact payout, progression return,
  compact 130% text bounds and empty/reduced-motion paths.
- Reviewed sparkle and compact captures in output/expedition-reward-sync-20261024.
  Native runs remain silent; these are visual/timing and routing checks, not a
  claim of listening acceptance. Existing audio PCM and configured gain unchanged.
- Scoped whitespace check passed. Scratch APPDATA used throughout.
  D:/bs-tutorial-20261021/ending-sync-before.json and ending-sync-after.json:
  2,971 owner profile files unchanged; signed ZIP unchanged.

## Next action
Owner feel/listening review during a naturally completed expedition. No export.
