# Expedition reward sound handoff

Updated: 2026-10-24 / Project: BrineSpace

## Objective and acceptance
Add satisfying count-up ticks and a little chime on landing to the existing reveal.

## Accepted decisions and constraints
Quiet mechanical ticks, softer small-figure landings, brighter Archived Data finish.
Use existing effects volume/mute and station UI audio routing. No changes to reward
math, layout, artwork or reveal timing. Avoid tick floods and offscreen/repeat chimes.

## Current state
- scripts/reward_count.gd emits sound requests only on changed displayed values,
  at most once per 70 ms per counter; emits one landing event per animated value.
- scripts/expedition_report.gd connects counters to the station audio helper.
- scripts/station_audio.gd registers pause-safe UI events with shared tick cooldown,
  one voice per kind, short limits, and existing effects/master gain handling.
- scripts/station_audio_cues.gd defines deterministic tick, land and chime synthesis
  and full literal paths to three baked JSON PCM assets under
  assets/audio/procedural-cues-v1/. Runtime reads/caches baked data.
- tools/bake_procedural_audio.gd supports --only for narrow baking. Only the three
  new cues were baked, using scratch APPDATA under output/reward-audio-20261024.
- tests/test_reward_count.gd adds tick/landing bounds, once-only and silent-edge
  checks. tests/test_baked_procedural_audio.gd now covers 48 cues.
- tests/test_expedition_report_native.gd verifies actual paused-report audio routing,
  effects gain and effects mute. Native runs stay master-muted on secondary display.

## Verification
Headless: test_reward_count and test_baked_procedural_audio PASS,
output/test-runs/20261024-195926-headless (433 baked parity checks).
Native: PASS, output/test-runs/20261024-200040-native; clean final log.
Earlier native assertions incorrectly equated master mute with per-voice gain and
expected a tick during the sparkle tail. Corrected assertions now test actual
half-volume tick gain and explicit effects mute at landing.

Preview: output/reward-audio-20261024/reward-preview.wav (1.6 seconds, illustrative
mixed sequence at configured gains, eight ticks plus small/hero landings; peak .085).
No claim of human listening acceptance; owner can review the preview or natural run.

Protection receipts D:/bs-tutorial-20261021/ending-sound-before.json and
ending-sound-after.json: 2,971 owner profile files unchanged; signed ZIP unchanged.
Scoped whitespace check passed. No export produced.

## Next action
Owner listening/feel review in a naturally completed expedition.
