# Sound variation pass

Updated: September 8, 2026 · Project: BrineSpace · Task: another sound polish pass

## Objective and acceptance

Reduce mechanical repetition in the new sound set while preserving quiet station
character and avoiding cut-off tails or clustered crew feedback.

## Accepted decisions and constraints

Use existing sounds. No credits, external generation or gameplay changes. Keep
priority signals stable and cosmetic randomness separate from the game simulation.

## Current state

`scripts/station_audio.gd` varies footsteps, tools, repairs, launch and hull cues
between 0.96–1.04 playback pitch and -1 to +0.5 dB relative level. Changes use the
existing audio-only random generator. Crew Foley shares a 0.6-second cooldown
across kinds, in addition to each cue's individual cooldown and voice limit.
Cue cleanup and tail envelopes now account for pitch-adjusted duration, so slower
playback retains its tail. UI confirmations and priority tones retain fixed pitch.

`tests/test_suno_audio.gd` checks pitch bounds, cross-kind crew cooldown, and a
forced lower-pitch case that must outlive its original duration and then release.
`tests/review_audio_mix.gd` has an optional `--variation` audition schedule with
repeated footsteps, tools, repairs and launch sounds.

## Verification

Focused audio integration passes with zero engine errors, including the prior
construction, comms, outcome, mute, spatial-gating and music checks. Initial logs
retain a corrected GDScript type-inference error; final evidence is under
`output/audio-variation/`. Native stereo capture passes: 1,404,928 frames,
peak -27.91 dBFS, zero dropped frames, successful WAV save and no engine errors.
Targeted whitespace checks pass. The bounded capture establishes signal integrity,
not subjective listening acceptance or worst-case station headroom.

## Next action

Listen to the new in-engine audition and normal gameplay for preferred balance.
This pass changes source playback behavior; previously exported Windows packages
and the individual base WAVs are unchanged.
