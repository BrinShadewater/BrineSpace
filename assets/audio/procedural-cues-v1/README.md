# Prepared procedural cues

These 45 files preserve the original 22,050 Hz mono, 16-bit PCM from
`scripts/station_audio_cues.gd`. The synthesizer remains the source of truth.
Base64 PCM and loop metadata in JSON keep runtime loading independent of editor
imports; the release manifest follows the explicit whole-path registry.

Regenerate with `tools/bake_procedural_audio.gd` under a scratch APPDATA inside
project output. The baker verifies the resolved user directory and refuses a
normal owner profile. Run `tests/test_baked_procedural_audio.gd` afterward: it
compares every sample, format, rate, channel count, duration, loop and cache identity.
Use the normal isolated Godot test workflow and fingerprint the owner profile.

No sound design, samples, pitch, duration or mix gains were changed. About 2 MiB
of PCM is prepared offline to avoid first-use synthesis during gameplay.
