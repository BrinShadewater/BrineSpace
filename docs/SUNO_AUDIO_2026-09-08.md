# Project handoff

The subsequent [audio polish pass](AUDIO_POLISH_2026-09-08.md) updates effect
selections, measured gain, music transitions and warning cadence. This handoff
retains the original integration evidence.

Updated: 2026-09-08 · Project: BrineSpace · Task: Owner-supplied Suno audio

## Objective and acceptance
Integrate the owner's 27 exports, using the four Moonlit tracks as background
music and the other exports for matching station ambience and events.

## Accepted decisions and constraints
Use the supplied batch through prompt 12. No additional generation is required.
Preserve Downloads masters, use Git LFS for runtime binaries, keep existing master
controls, and retain paid construction/resource failures. Other working-tree edits
remain in place. No commit, publication or new standalone game package is requested.

## Current state
`assets/audio/suno-v1/` contains all 27 prepared assets (~35 MiB), provenance manifest
and usage notes. `tools/prepare_suno_audio.py` reproduces conversion and the explicit
dependency bank. New `suno_audio_bank.gd` and `station_music.gd` have paired UIDs.
`station_audio.gd` replaces matching synthesized layers and controls bounded effects.
Small hooks in main, title, crew expedition and transmission archive connect events.
Shared preferences/settings include saved music volume. WAV/Ogg are LFS patterns.
`tests/test_suno_audio.gd` exercises assets, loops, events, playback limits, pause,
mute/focus, playlist advancement, persistence and scene lifetime.

## Verification
Godot 4.6.1 import, focused audio integration, existing station-system assertions,
and the native title/settings-to-gameplay test passed (exit 0). The native settings
capture was inspected: Music volume fits correctly alongside existing audio
controls. Final verbose station-system verification exited without leaked playback
resources after fixture cleanup allowed the mixer to drain. The native title test
briefly encountered an independently edited layout script with invalid UTF-8;
that file was already corrected before retry, without changes by this audio task.

Evidence: `output/suno-import.log`, `output/suno-test.log`,
`output/suno-systems-verbose.log`, `output/suno-title-test.log`, and
`output/title-settings.png`. New script UID pairs and audio LFS attributes verified;
targeted diff whitespace checks passed. Existing raw-image loading warnings occur
in the source fixtures. These checks do not establish auditory quality or a new
packaged build. The tests now clean up the persistent playlist before shutdown.

## Next action
Listen during a normal expedition and tune relative volumes, loop seams and cue
cutoffs. All supplied variants are retained; generated clips are not claimed to
have passed a subjective listening review.
