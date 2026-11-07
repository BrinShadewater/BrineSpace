# Expedition reward rising finish

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
Refine count-up, sparkles and chime with a slightly more rewarding build and landing,
within the accepted quick terminal-style reveal.

## Accepted decisions and constraints
A subtle rising pitch on lead ticks and a small settling pulse on Archived Data.
Keep existing gain/PCM, quiet final beat, exact reward math, artwork, layout and
reduced-motion behaviour. Controls stay usable. No animation on zero rewards.

## Current state
- scripts/station_audio.gd: play_reward_tick routes through existing UI audio
  cooldown/voice/volume handling, then sets pitch from 0.94 to 1.12 based on progress.
- scripts/expedition_report.gd: sound routing binds each counter as progress source;
  only the existing lead counter uses ticking audio. Landing sounds remain fixed.
- scripts/reward_count.gd: hero label settles from 104% to its original scale over
  180 ms, using a left/middle pivot. Original scale and pivot restore at finish and
  every interruption path. The same landing clock controls chime, pulse and sparkle.
- tests/test_reward_count.gd adds transform restoration and interruption coverage.
- tests/test_expedition_report_native.gd validates actual per-voice pitch and rising
  successive ticks, waiting on voice/cooldown state rather than a fixed delay.

## Verification
Baseline settling-pulse regression failed as expected:
output/test-runs/20261024-224224-headless.
Final numeric/routing/interrupt tests PASS:
output/test-runs/20261024-224327-headless.
Final native PASS: output/test-runs/20261024-224408-native; clean final log.
Existing native checks include actual effects gain/mute, exact rewards, compact
130% bounds, no-discovery ending, and progression return. Sparkle capture reviewed:
output/expedition-reward-lift-20261024/. Native tests remain silent, so owner listening
acceptance is still pending. No new PCM or broad asset batch needed.
Scoped whitespace check passed. All Godot work used scratch APPDATA.

## Next action
Interactive preview refreshed from process 196596 to 196220, using fresh
scratch-appdata-lift beneath output/expedition-ending-preview-20261024.
Click PLAY REVEAL or press R to try the rising ticks and settling pulse together.
Startup stays silent. No export produced.

Preview readiness confirmed; clean startup and responsive window. Protection
receipts D:/bs-tutorial-20261021/ending-lift-before.json and ending-lift-after.json:
2,971 owner profile files unchanged; signed ZIP unchanged.
