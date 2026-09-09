# Project handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: Music and effects polish

## Objective and acceptance
Polish the installed Suno batch: level consistency, usable cue timing, smooth
music changes and restrained station feedback, with source and mixer validation.

## Accepted decisions and constraints
Keep all owner masters and original v1 exports. Use the existing four-track music
playlist, preserve master/music settings, paid construction and resource behavior.
No new generated sounds, publication or replacement Windows package.

## Current state
`assets/audio/suno-polish-v1/` supplies 15 explicit short edits and provenance.
`station_audio_mix.gd` gives all 27 runtime clips measured constant gains; the bank
selects polished effects while reusing original music/loops. Music has two decks
with six-second equal-power crossfades and eased priority ducking. Station audio
adds level matching, motion-loop start/stop, gradual hull-pressure intensity,
soft suppression of incidental effects and reduced warning repetition. Main only
passes the existing warning conditions to the audio state tracker.

`audit_suno_mix.py` and `polish_suno_audio.py` reproduce measurements/edits. The
expanded audio regression covers automatic crossfades, mute of both decks, ducking
and recovery, warning state changes, motion stop, and all prior audio checks.
`review_audio_mix.gd` produces a bounded native-renderer/stereo-mixer audition.

## Verification
Measured original music spread: 4.42 LUFS; airlock variants: 10.25 LUFS. Corrected
music/loop variants match their group targets. Fourteen event edits reach -23 LUFS;
one placement remains -24.5 under the bounded boost. All corrected event peaks are
at or below -3 dBTP before in-game attenuation.

Godot 4.6.1 import, focused audio regression and station-system assertions passed.
Logs and measurements are in `output/audio-polish/`. The native capture uses the
stereo Dummy driver so a surround Windows device cannot append extra speaker
pairs. This exercises the engine mixer, not physical speaker fidelity. Native
capture (`native-mix.log`, `capture-metrics.json`) contains 31.858 seconds of stereo
audio at 44.1 kHz, peaks at -18.07 dBFS, has zero clipped samples and zero dropped
capture frames. The overlap region remains non-silent. The four final logs contain
no engine/script errors; existing source raw-image warnings remain. New script UID
pairs, event-asset LFS attributes and targeted diff whitespace checks passed.

## Next action
Audition `output/audio-polish/in-engine-mix.wav`, then listen through a normal
expedition for musical phrasing and generated-sound suitability. Neither waveform
measurements nor runtime tests are claimed as subjective listening acceptance.
The previously accepted Windows package is unchanged; these are later source edits.
