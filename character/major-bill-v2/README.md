# Major Bill — integrated animation pack

102 transparent 92×92 frame PNGs across 17 animations. The current game's entire four-direction idle/walk/run matrix is present and used by the station renderer. This pack includes the subsequent animation cleanup pass.

| Animation | Directions | Frames each | Cycle duration | Playback |
|---|---|---:|---:|---|
| idle | north, east, south, west | 6 | 1.44 s | loop |
| walk | north, east, south, west | 6 | 0.90 s | loop |
| run | north, east, south, west | 6 | 0.60 s | loop |
| interact | east | 6 | 1.02 s | one-shot |
| kneel | east | 6 | 1.00 s | one-shot |
| repair | east | 6 | 0.96 s | loop |
| stand | east | 6 | 1.00 s | one-shot |
| walk bonus | southeast | 6 | 0.90 s | loop |

Movement directions match `main.gd` and the grid renderer. The current walker does not request diagonals or work actions. The east-facing action chain is prepared for future work behavior; this pass does not introduce a job/repair gameplay system. North/south/west work actions and additional diagonal locomotion are not part of the current requirement matrix.

Cycle durations above are the authored reference/preview timings. In-game walking and running advance with actual travel distance: 0.12 and 0.168 station cells per cycle respectively. Idle and actions use the visual clock.

## Outputs

- `frames/`: individual transparent PNGs.
- `rotations/`: four neutral fallback sprites, taken from idle frame zero.
- `final/spritesheet.png`: 6 columns × 17 rows in manifest order.
- `final/*-strip.png`: each animation as a transparent strip.
- `final/manifest.json`: exact per-frame milliseconds, source hashes, pivots, provenance and loop flags.
- `final/major-bill.tres`: tested native Godot SpriteFrames resource with matching per-frame durations.
- `qa/contact-sheet.png`: all exported frames, visually inspected.
- `qa/previews/`: individual GIFs at their authored timings. One-shots repeat for review.
- `qa/animation-preview.gif`: all animations advancing at their individual timings; preview restarts at three seconds.
- `qa/repair-sequence.gif`: idle → kneel → repair twice → stand → idle.
- `qa/before-after.gif`: saved prior pack beside the cleanup at authored timings.
- `qa/before-after-metrics.json`: per-animation head-box diagnostics and colour counts; these are diagnostics, not an aesthetic score.
- `qa/native/`: real-game storage, corridor and nursery screenshots, plus paired close-up frames for all twelve movement animations.
- `references/approved-concept.png`, `generated/`, `prompts.json`, `generation-pass-2.json`, `generation-pass-3.json`, `cleanup-sources.json`: retained art, exact built-in imagegen prompts, accepted sources and rejected-candidate reasons.

## Playback and integration

The renderer reads the manifest's explicit frame paths, so it also works without editor imports. Loaded textures carry a geometry tag used by layered and modular rooms. All consumers draw the full canvas with foot pivot (46, 86), preserving a 74-pixel standing height at the existing station character scale. The old tight crop and extra procedural bob are removed for the new character. Historical fixtures using old textures retain their original geometry.

Playback restarts on state changes, direction changes, a visual-clock reset, or a teleport exceeding half a cell. It remains frozen with the paused visual clock. Walking/running phase advances from the actual actor position measured in cells, so repeated draw calls, stationary poses and camera zoom cannot advance the gait. Equal distances produce equal phase advances at different travel speeds. One-shot animations clamp at the final frame. The manifest supplies timing and stride lengths.

For independent AnimatedSprite2D use, assign `final/major-bill.tres`, enable nearest filtering, and use offset `(0, -40)` with a centered sprite to anchor its feet to the node origin.

## Pose and timing refinements

- Shared row baselines retain airborne feet and the kneel's lowering motion; frames are not individually stretched or grounded.
- Nine reference-generated cleanup rows replace the four cardinal walks, north/east/west runs, interaction and repair. The original south run and southeast walk were retained because their cleanup candidates lost useful gait variation. Four idle rows and the kneel/stand transition retain their source poses with the common export cleanup.
- Head-size registration applies only a bounded ±3% uniform scale correction; it never independently warps limbs. Side-run row height is 68 pixels rather than 74, reducing the apparent growth when switching from upright walking to leaning running.
- Area downsampling removes high-frequency source texture before export. Final alpha is binary, edges are hard, and all 102 frames share a 64-colour non-dithered palette. This reduces speckle and colour shimmer; the fine detail is deliberately softer than the prior nearest-neighbour shrink.
- Rear gait pose ordering was adjusted after contact/passing review. Repair uses a smaller wrist turn and a return sequence instead of the earlier large tool swing. Source order is recorded in `build_pack.py` and the manifest.
- Walk contacts last 170 ms; passing frames last 130–150 ms. Run frames use 85–110 ms; idle has a slower breathing rhythm.
- Idle/kneel/repair/stand endpoints are pixel-identical, preventing a pose pop at the transitions.
- Standing reuses the kneel frames in reverse. No directions are mirrored, preserving asymmetric chest equipment.
- Source poses remain AI-generated sprite art; small silhouette/detail differences remain. This pass reduces drift rather than claiming pixel-identical heads across all poses. The camera is still modestly elevated, as in the approved study.

## Rebuild and validation

Run `python character/major-bill-v2/build_pack.py` from the repository root; `package.py` is a compatibility wrapper. Requires Pillow and NumPy. Rebuild uses only the saved repository-local sources and does not call an image service or depend on `.codex` paths.

`python character/major-bill-v2/review_cleanup.py` regenerates the comparison using the retained `qa/before-cleanup/` snapshot. The cleanup's front-walk source returned an opaque light checker backdrop; its connected exterior is removed during extraction, preserving enclosed highlights.

Validation completed with Godot 4.6.1:

- Sprite manifest validation: zero errors or warnings at 15% center-drift tolerance.
- `tests/test_major_bill_animations.gd`: complete movement coverage, frame counts, geometry tags, timing selection, loop/clamp behavior, native SpriteFrames timing, matching action endpoints, distance/speed invariance, stationary gait hold, pause and teleport reset; zero failures.
- `tests/playtest_major_bill.gd`: real renderer, state/facing resets, clock reset and pause behavior, storage/corridor/nursery consumers, action poses, and changed rendered pixels in every movement animation; zero failures.
- Godot editor import succeeded. Existing raw room-source loading warnings appear in the native fixture; no script errors were reported. Release export is outside this pass.
- Cleanup export check: 102 frames, binary alpha, 64 opaque colours. Side-run head-width ranges dropped from 3/4 pixels to 1 pixel; repair dropped from 2 to 1. Other pose measurements vary and remain documented rather than being treated as blanket improvement.

Tests use unique fixture save paths, and normal game costs/failure conditions are unchanged. PNGs inherit repository Git LFS rules; GIF previews have a local LFS rule. No assets were committed by this pass.
