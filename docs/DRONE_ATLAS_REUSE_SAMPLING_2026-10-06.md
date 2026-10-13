# Project handoff

Updated: October 6, 2026 · BrineSpace · Drone atlas reuse and sampling investigation

## Objective and acceptance

Test whether repeated atlas uploads duplicate surviving textures; evaluate smaller
frame uploads while preserving selected animation pixels, filtering and drawing.
Do not enable an optimization without demonstrated benefit and relevant parity.

## Accepted decisions and constraints

Normal game code, assets, owner layouts and animation settings are unchanged this
interval. Keep the existing soft active-set budget and session teardown. No larger
permanent cache, atlas conversion, downscaling, renderer upgrade or quality change.
The prior emergency Metal guard remains accepted. Veld CPU storage remains experimental.

## Current state

Diagnostics live in `output/drone-weak-reuse-2026-10-06/`.
`trace-motion.gd` is a physical copy of current drone animation code. It adds a weak
reference to each uploaded texture and records a duplicate only when the previous
same-path ImageTexture is still alive at another upload. It never retains images
strongly or changes eviction/drawing. The copied 40-room epoch benchmark reloads
this adapter only inside its isolated process.

Two attempts were rejected when the native window minimized; no performance result
is accepted from them. Restoring/focusing the test window and keeping it above other
windows before warm-up allowed the next attempt to complete, with the minimization
guard still active. This setup adjustment is confined to the copied benchmark.

## Verification

Godot 4.7.2 native Compatibility / RTX 4070 Ti, isolated scratch APPDATA. All 2,936
owner non-log files unchanged. Normal `scripts/drone_animation.gd` matches its starting
SHA-256. The valid selected-Veld 40-room workload has five drones, 40 powered rooms,
180 warm-up frames and 12 short phases (idle/pan/zoom/lighting at 1×/2×/4×).

- **No live same-path duplicate uploads were observed.** The latest texture's weak
  reference was dead when its atlas reloaded. Session weak reuse therefore has no
  demonstrated benefit in this workload. Do not implement it on the assumption that
  retained canvas pins are causing these particular reloads. This does not establish
  absence of duplication in every layout/Studio/endurance workload.
- The diagnostic completes with no missing art; Veld routing remains 902 draws /
  134 poses. Texture accounting ends at 3,590.28 MiB. Window/setup and tracing differ
  from earlier runs; its frame times are not a matched optimization comparison.
- `crop-pixels.gd` tests one selected South mining body atlas, 2688×13440 pixels,
  against native 448×448 frame textures. GPU readback confirms cropped source pixels
  are byte-identical. Rerendering the same full atlas also matches exactly, ruling out
  a changing scene as the comparison's cause.
- Final crop test: 416 native raster pairs over 26 frames sampled every seventh
  index (all columns), four scales (0.125/0.3/0.73/1.0), integer/half-pixel origins,
  tint/alpha, nearest and linear filtering. **358 pairs are not exact**: 150 of 208
  nearest comparisons and all 208 linear comparisons. Across both modes, 366,124
  channel bytes differ, with maximum channel difference 202. The earlier column-zero
  linear-only probe found differences up to 2; that limited result is superseded by
  the broader test. Source pixels are preserved, rendered sampling is not.

These are offscreen native raster/lifetime diagnostics, not packaged gameplay,
minimum-hardware, Mac, FPS or total-memory certification. No frame-only runtime
backend has been installed. Crop tests establish that naive frame-texture replacement
fails the current raster parity gate; they do not yet prove the precise GPU-coordinate
operation responsible. Full logs and JSON results retain the evidence.

## Next action

Investigate the Compatibility renderer's atlas UV normalization, clipping and sampling
at scaled boundaries before constructing a runtime frame presenter. Use the same-atlas
control and exact source/raster checks; do not switch filtering or accept nearest
boundary changes silently. In parallel priority, the previously measured discovery/
interface cycle work still contributes about 31 ms and can be investigated without
changing animation storage. First-use atlas uploads, steady draw cost, full workloads,
memory budgets, packaged Windows and Mac gates remain unresolved.
