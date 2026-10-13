# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: moving-water cost attribution

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness plan. Release gates,
selected animation pixels/timing, normal simulation and owner data remain required.
These diagnostic probes do not certify gameplay FPS or either platform.

## Accepted decisions and constraints

No downscaling, frame removal, renderer upgrade or automatic quality reduction.
Keep this work private until matched actual-runtime gains and visual/lifecycle
checks justify integration. No new normal-source rendering change is accepted.

## Current state

Actual 3,000-frame Moon component census identifies the water group (including
interleaved threshold grating) at 4.65 ms/frame at 2x and 3.81 ms at 4x, summed
across three bays. First phase 5.11 ms includes startup/warmup in cumulative totals;
do not treat it as clean per-phase timing. Walls/windows cost 1.09/0.92 ms at 2x/4x.

The previous full-water ribbon-grid prototype passed 481 native checks but its
apparent ~60 microsecond gain was redraw-order bias. Balanced-order measurements
show full-water medians 215 -> 213 microseconds across cases, with only 4/12 better;
reference-first deltas ~-55 and candidate-first ~+65 microseconds. No robust gain.

New private probes compare the original water module against:

- Dynamic native-equivalent triangle batching: 25 checks, 24 exact raster pairs,
  zero failures. Large-bay direct water medians 1.12–1.17 ms versus 4.46–4.82 ms
  batched. Captured command count drops to 10, but fresh GDScript triangle building
  costs roughly 4.4–5.0 ms in last-sample stage counters; submission ~0.14–0.21 ms.
  Reject this implementation as a CPU remedy. Command counts are recorded API
  commands, not a GPU draw-call census. GPU benefit remains unmeasured here.
- Unbatched command capture/replay control: 25 checks, 24 exact raster pairs,
  zero failures. Large-bay total medians 1.15–1.21 ms direct versus 1.51–1.63 ms
  captured. Last-sample recording ~0.45–0.49 ms and native replay ~1.05–1.12 ms
  for 163–167 commands. Capture overhead is real; these counters are not the
  decomposition of the original direct implementation. They indicate native
  submission remains substantial after coordinate construction.

Godot's CanvasItem polyline wrapper delegates to RenderingServer, and native
polyline submission constructs stroke geometry. Merely switching to the server
API retains that geometry work; it is not an evidence-backed batching remedy.
Primary references: [CanvasItem source](https://github.com/godotengine/godot/blob/master/scene/main/canvas_item.cpp),
[renderer canvas source](https://github.com/godotengine/godot/blob/master/servers/rendering/renderer_canvas_cull.cpp).
These sources describe current upstream implementation, not a byte-identical
source audit of the locally installed 4.7.2 binary.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/
moon-component-attribution/, water-ribbon-grid/, water-dynamic-cost/,
water-native-cost/ and water-cost-summary.json. Failed/first-order-biased evidence
is retained separately. Changed checkout files: this note and CURRENT_STATUS.md.

## Verification

Both new native probes use the QA engine (debug=true), 24 advancing-clock cases:
large bay/airlock/door, partial/full water, two starting clocks, pump off/on,
asymmetric transform and modulation. Queue order alternates; first sample excluded.
Final raster bytes match, cache-owning canvas releases, logs have no errors/warnings.
Both isolated runs preserve all 2,936 non-log owner files; all processes terminal.
This is narrow water evidence, not full-room motion/layer/rotation acceptance.

## Next action

The dynamic batch needs cheaper geometry construction, not just fewer commands.
Investigate reusable stroke topology/buffers or native bulk preparation, measuring
both CPU and GPU before selecting an implementation. Preserve the existing engine;
any native helper would require Windows and Mac dependency/packaging validation.
Do not revive the rejected fresh-GDScript triangle path without a measured remedy.
Full FPS/stutter/loading/endurance/original-report/Mac certification gates remain open.
