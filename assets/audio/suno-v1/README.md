# Owner-supplied Suno audio

The later [mix polish](../suno-polish-v1/README.md) supersedes the effect selections
and runtime mix behavior described below. This directory retains the original
prepared exports as reproducible sources; its music and loop files remain active.

September 8, 2026. All 27 WAVs supplied by the owner are represented here. Original
masters remain in `C:/Users/Alex/Downloads`; `manifest.json` records filenames,
SHA-256 hashes, durations, runtime paths and processing. The owner authorized use
in BrineSpace; this record does not make a separate licensing determination.

Rebuild with `python tools/prepare_suno_audio.py` (numpy + imageio_ffmpeg).
Music and ambience use 48 kHz stereo Ogg Vorbis quality 5; effects use PCM16 WAV.
Processing attenuates peaks only, trims silence at effect edges, fades music/effect
boundaries, and overlaps 250 ms at ambience loop seams. No source files are changed.
Audio formats are tracked by Git LFS. Explicit script preloads retain these assets
as dependencies in Godot's selected-resource exports.

## Runtime use

- Both Moonlit Canyon and both Moonlit Test Run exports form a shuffled four-track
  playlist, repeated in that order, surviving title/loading/gameplay transitions.
  A separate saved Music volume slider can silence music while retaining effects.
- Interior and ocean variants replace synthesized machinery and pressure beds.
  Each station instance selects one variant of each loop. Ocean level rises with
  low hull integrity. The low synthesized receiver texture remains.
- Flooding and moving-drone loops follow their actual active state; paused motion
  is silent. Flooding holds silent when its airlock lacks power or is suspended.
- Construction completion, newly powered rooms, cargo delivery, stabilized
  patterns, warnings and recovered/replayed transmissions trigger matching cues.
- Door cues follow visible completed door closures and airlock sealing completion.
  Visible door feedback uses the normal retained-door renderer; the explicit
  `--redraw-doors-lights` diagnostic path does not provide those ordinary-door cues.
- Effects rotate variants, limit concurrency to one per kind, and apply cooldowns.
  Frequent clips have 2–5 second playback budgets with a 200 ms fade; full prepared
  clips remain available because several generated sounds exceed requested lengths.
- Existing master volume, mute and focus-loss mute cover all sources. Pausing holds
  active gameplay effects; station ambience and music continue during planning.

The mix starts conservatively. Automated tests establish integration, not a
listening judgment. Review generated content, effect starts/cutoffs, loop seams
and relative levels through headphones and speakers during normal play.
