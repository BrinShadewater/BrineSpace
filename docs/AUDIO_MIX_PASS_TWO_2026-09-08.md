# Audio mix pass two

Updated: September 8, 2026 · Project: BrineSpace · Task: another audio polish pass

## Objective and acceptance

Improve cue clarity and mix recovery using the existing supplied sound library.
Keep station character and verify playback with focused tests and a native capture.

## Accepted decisions and constraints

Keep Moonlit music and existing Suno assets. No new generation or gameplay changes.
Previous Windows packages stay frozen; these changes are in the working source.

## Current state

`scripts/station_audio.gd` now fades only the final quarter of very short cues
(up to 0.2 seconds for longer effects). Previously the fixed 0.2-second fade
attenuated a 0.1-second UI click for its entire life. Priority warning, discovery
and terminal sounds lower ambience by 3 dB with a 0.2-second attack and 1.5-second
recovery. Effects mute and gameplay pause release that attenuation; user volume
and layer envelopes remain independent.

`scripts/station_music.gd` shuffles with its own random generator, preserving
cosmetic randomness without consuming the gameplay random sequence.

`tests/test_suno_audio.gd` adds attack, cue expiry, ambience duck and gradual
mute-release assertions. `tests/review_audio_mix.gd` accepts an optional
`--output=` destination to retain previous audition recordings.

## Verification

Focused Suno audio fixture passes, with zero engine errors. The native stereo
mix capture passes: 1,413,120 frames, peak -17.52 dBFS, zero dropped frames and
successful WAV save. Evidence is in `output/audio-pass-two/`; the recording is
`in-engine-mix.wav`. Targeted whitespace checks pass. Existing raw-image warnings
remain separate. This capture is a bounded playback check, not a worst-case peak
guarantee or subjective headphone/speaker acceptance.

## Next action

Listen to the new mix and ordinary gameplay for cue balance. Include this pass in
the next requested Windows rebuild; the prior audio playtest predates these edits.
