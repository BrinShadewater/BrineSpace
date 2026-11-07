# Expedition reveal final-beat polish

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
One more polish pass on the count-up, sparkle and sound sequence. Retain the fast,
restrained reveal and improve smoothness rather than adding more effects.

## Accepted decisions and constraints
Exact values, single chimes, slow-frame landing synchronization, reduced motion,
zero reward silence and responsive controls remain. No audio PCM, volume, artwork,
reward calculation or screen layout changes.

## Current state
scripts/reward_count.gd reserves the final 100 ms from intermediate count ticks,
leaving a short anticipation beat before the chime. Landing time remains 380 ms,
now named centrally. Particle radius uses cubic ease-out for a quick burst that
slows; brightness uses smoothstep for a softer settle. Existing peak sizes and
brightness remain unchanged.

tests/test_reward_count.gd adds timing checks at 30, 60 and 144 FPS for a minimum
90 ms final tick/chime gap and exact once-only landing, alongside prior edge cases.

## Verification
- Baseline failed the final-beat regression at one tested frame rate:
  output/test-runs/20261024-223206-headless.
- Final numeric/routing PASS: output/test-runs/20261024-223224-headless.
- Native report PASS: output/test-runs/20261024-223227-native; clean final log.
- Reviewed current sparkle capture in output/expedition-reward-rhythm-20261024.
  This fixture manually advances the hero for capture while small figures run
  naturally; the preview supplies the actual full sequence. Native tests remain
  silent, so listening/subjective feel acceptance remains with the owner.
- Scoped whitespace check passed. All Godot runs use scratch APPDATA.

## Next action
Updated interactive preview process 196596 replaces process 182584, using fresh
scratch-appdata-finish beneath output/expedition-ending-preview-20261024.
PLAY REVEAL / R repeats the current production reveal with sound. Startup is silent.
No export produced. Preview readiness/protection receipt verified before final reply.

Preview is ready and responsive; startup log is clean. Protection receipts:
D:/bs-tutorial-20261021/ending-finish-before.json and ending-finish-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged.
