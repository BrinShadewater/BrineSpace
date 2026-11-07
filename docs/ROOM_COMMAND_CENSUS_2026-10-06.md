# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: renderer command attribution

## Objective and acceptance

Identify a larger measured performance remedy after rejected monitor/cache/mesh
experiments. Preserve selected art, quality, timing, layer order and owner profiles.
Full release acceptance remains open.

## Accepted decisions and constraints

Normal runtime remains unchanged. Private instrumentation records library commands
at each slot paint, then counts the retained command records of visible slots.
These are **script-submitted retained commands, not measured GPU draw calls**.
Visible-in-tree is not proof of every primitive surviving viewport/engine culling.
No performance acceptance from instrumented timings; no export or art changes.

## Current state

Native diagnostic sources/results in `output/room-command-census-2026-10-06/`.
Physical content/library preloads verified and nonempty recorded library slots
required in every measured phase. Counters reset on paint so static retained slots
are represented without pretending they redraw each frame.

## Verification

40-room native 1080p, 180-frame warm-up, 30 idle samples each at 1/2/4x. All three
snapshots agree on the following visible library census:

| Slot kind | Slots | Retained commands |
|---|---:|---|
| Split library base | 118 | 463 polygons |
| Split library live | 118 | 512 rectangles, 76 lines, 54 polylines |
| Ordinary library prop | 96 | 384 polygons |

347–348 allocated slots, 345 visible-in-tree, 332 nonempty instrumented library
slots. Registration metadata contains **89 bar screens, 52 wide trace screens,
zero radar screens and no registered specimen/field/hologram effects** among the
counted live slots. Metadata classification includes legacy screens and is not
an exact count of executed station-style branches. Do not extrapolate synthetic
radar/hologram preparation savings to this workload.

Successful run clean, all 2936 owner non-log files unchanged, process terminal.
Private compressed crew fixture, not normal packaged gameplay or FPS certification.
Counts exclude other renderer methods, doors/floors/walls, UI and exterior effects.

The matching [Godot 4.7.2 GLES3 renderer source](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp)
starts separate batches for polygon and mesh commands; rectangle commands can
share batches when texture, command type and other state remain compatible.
This explains why exchanging one polygon for one mesh is not inherently a batching
remedy. It does not measure this game's driver overhead or establish an atlas need.

Existing uninstrumented station evidence also reports door/light validation around
1.7 ms/frame, alongside room content and environment preparation. Current source
already caches crew feet per frame and symmetric connectivity within the validation
call; do not recreate those optimizations. Connected-door frame computation still
checks topology again after the validator has established connectivity.

## Next action

Profile the remaining door/light validation components and redundant render-only
connectivity work, using the current source and matched workload. Any reuse must
stay within stable rendering state; input/navigation checks must remain live.
For renderer grouping, target commands actually present (bars, traces and ordinary
prop polygons), rather than absent radar/glow effects. Broader floors/walls/UI
submission boundaries remain uncounted; obtain evidence before choosing structural
changes. Memory/loading, lifecycle, bug closure, endurance and actual Windows/Mac
release certification remain unresolved.
