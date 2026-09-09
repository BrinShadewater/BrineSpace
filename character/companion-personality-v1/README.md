# Companion personality animation pack

September 9, 2026. Extends the selected companion designs without replacing their
portraits, locomotion packs or rescue art. Raw imagegen sources and exact prompts
are under `sources/`. Rebuild: `python tools/build_companion_personality.py`.
Requires Pillow and NumPy. Each manifest retains its source SHA-256.

28 clips / 96 exported frames on 92x92 canvases with pivot (46,86):

- Margot: sit, groom, nap and pet reactions, with entry/exit clips. These stationary
  poses face south; she turns toward the viewer before them. Shared entry poses
  and reversed exit poses are derived from the authored sheet. One scale preserves
  the lower seated/sleeping silhouette. No mirrored views.
- River: four-direction sensor sweep and downward equipment inspection, 4 phases
  each, 300 ms/phase, nominal 44-pixel standing height.
- Josh: four-direction attentive head/arm gestures and in-place tread pivots,
  4 phases each, 300 ms/phase, nominal 70-pixel height. Pivot clips are ordered
  neutral/turn/turn/neutral. The north-watch source's excessive face reversal is
  omitted by holding its earlier rear-facing tilt for one extra frame.

Separate pose playback uses saved simulation elapsed time, not wall-clock time.
Main action loops and contact sheets are available under each character directory;
`review.html` includes native captures and the original procedural River cue.
Manifest validation and native action/recovery tests pass. Native snapshots establish
scale and poses; they do not establish owner approval of full-speed transitions.

Runtime behavior and validation: `docs/COMPANION_PERSONALITY_2026-09-09.md`.
