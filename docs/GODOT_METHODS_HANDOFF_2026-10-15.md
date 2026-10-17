# Project handoff

Updated: October 15, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: performance and visual-method research

## Objective and acceptance

Research better performance methods and possible lighting, perspective, effects
and physics improvements. Ground recommendations in current implementation and
primary sources, distinguish hypotheses from measured results, and preserve the
accepted art/gameplay contracts. This research round requires no implementation.

## Accepted decisions and constraints

- Keep current Compatibility/OpenGL and accepted overhead/cutaway presentation.
  Station props v2 keep one painted facing as room positions rotate; canonical
  visual bible §4 supersedes older four-wall-facing pipeline guidance.
- Preserve matte materials, department readability, authored contacts and owner
  layouts. Sharper imagery and restrained effects remain the owner's direction.
- Performance changes aim for exact behavior/pixels. Visual enhancements require
  comparative visual review and their own measured frame/memory cost.
- No Godot jobs during this research round. Future probes use scratch APPDATA and
  owner-folder fingerprints. Subsequent renderer timing waited for the owner's
  pause confirmation and completed as `pacing3`; see its updated handoff.
- Shared dirty checkout and unrelated character work remain untouched.

## Current state

- Added [research report](GODOT_PERFORMANCE_VISUAL_METHODS_2026-10-15.md), this
  handoff and a concise entry in [current status](CURRENT_STATUS.md).
- Strongest candidates to measure: repeated topology/hazard preparation,
  atmosphere-mask rebuilding, and whole-field rock-mesh rebuild bursts. Mask is
  only 6,400 bytes; this is primarily a preparation/call-frequency hypothesis.
- Visual pilots: one machine normal-map/task-light study; one cosmetic current
  linking nearby silt and rooted plants. Existing light maps, contact shadows,
  GPU marine snow and compartment flooding are already useful methods.
- Native kernels, MultiMesh expansion and fixed-tick interpolation remain
  conditional, higher-cost experiments. No performance benefit is established.
- MSAA 2D is unsupported in Compatibility; 3D scaling is not 2D scaling. GLES
  float target support alone does not establish full HDR/glow workflow parity.
- Source-download helper: `output/godot-research2-20261015/fetch_viewport.py`.
  Three additional pinned viewport files and SHA-256 provenance are under
  `C:/bs-render-methods-20261015/`. Earlier engine evidence remains in the prior
  research handoff; no replacement engine built.

## Verification

Read current source and canonical art rules; cross-checked primary Godot 4.7
documentation and pinned 4.7.2 source. Local report references and whitespace
checked; source archive hashes recorded. No game/test/native process, benchmark,
save-folder probe, art edit, renderer switch or runtime settings change was made.
No new FPS, image-parity, Mac or release acceptance is claimed.

## Next action

Measure the named preparation/rebuild sites on the frozen large station before
choosing an optimization. Renderer/pacing comparison subsequently completed under
its [updated handoff](GODOT_RENDERER_HANDOFF_2026-10-15.md); no switch was accepted.
For visual work, prototype a single reversible machine-lighting study with
power/blackout transitions, four room rotations and three zoom levels; review
quality and incremental cost before expansion. Current research request complete;
implementation and these experiments have not begun.
