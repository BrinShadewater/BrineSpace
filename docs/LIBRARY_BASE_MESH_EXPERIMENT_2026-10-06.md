# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: prop body/shadow geometry

## Objective and acceptance

Reduce measured library renderer cost while preserving pixels, filtering, material
behavior and draw order. Full PC/Mac release gates remain open.

## Accepted decisions and constraints

**Do not admit this mesh prototype.** Corrected mesh drawing preserves tested
pixels but does not establish a useful station renderer gain. Normal runtime,
art, settings and permanent test/index unchanged. No export or release acceptance.

## Current state

Private sources, native tests, station copies and rejected logs retained under
`output/library-base-mesh-2026-10-06/`. Initial mesh combined all shadow/body
polygons with per-vertex colour. Revised version keeps ordered uniform-colour
layers separate, combining polygons within each layer. Existing DrawSlot owns
its ArrayMesh references; submit invalidation replaces them, with no global cache.
The original library base renderer remains the normal implementation.

## Verification

Initial combined-colour version: 72/96 exact raster pairs, **24 failures**; rejected.
All changed cases concern shadows. Vertex-colour storage/precision is a possible
mechanism, not separately proven. Do not claim exact equivalence or admit that
version. Revised uniform-colour layers: 96/96 exact native pairs across partial
texture alpha, overlapping concave polygons, mirroring, floor/station classification,
three fractional sizes, nearest/linear, inherited affine tint and flooding shader.

Expanded actual-art check: **160/160 exact nonblank pairs**, adding eight distinct
current source sheets (crew cinema 2–5 and fitness 1–4, selected by polygon count),
two scales/filters and dry/flooded state. Limited sample, not every current prop or
full-room/Studio/lifecycle/release acceptance. First actual-art fixture used an
unavailable Rect2i method; corrected to `has_area` and retained failed parse log.

Matched 40-room native 1080p idle/pan at 1/2/4x, 60 samples per phase. Explicit
physical content preload plus runtime guards prove candidate execution: 118 slots,
463 retained layer meshes, 173→191 builds, 183→201 base callbacks. Existing static
retention means almost no base preparation during ordinary animation; this change
principally tested retained geometry's renderer cost.

Renderer CPU baseline→candidate ms across six phases: 10.599→10.585,
10.450→10.514, 10.177→10.146, 10.384→10.386, 10.285→10.106,
10.351→10.344. No consistent material gain. Callback outliers occur on opposite
branches; whole-frame p95 mixed, candidate 37.366–50.458 ms still fails 16.7 ms.
One pair does not certify FPS improvement. Fixture uses private compressed crew,
not normal packaged gameplay.

All six actual crew/drone snapshots, powered-room counts, zoom and texture counters
match. Final texture counter 3168.333 MiB unchanged. All successful logs clean;
all 2936 owner non-log files unchanged in successful and rejected isolated runs.
Processes terminal; no pending native run.

## Next action

Stop treating per-prop geometry rebuilding as the main live renderer remedy:
static base commands are already retained, and replacing their representation
did not demonstrate improvement. Measure rendering submissions/batch boundaries
across actual visible props, walls/floors and UI, retaining the existing quality
and ordering. Use driver/renderer evidence to choose a larger remedy rather than
additional monitor/cache variants. Any broader asset-storage change needs a
measured case, exact source/filter/mipmap preservation and bounded session lifetime.
Memory/loading, lifecycle, original bugs, endurance and packaged Windows/Mac
certification remain open.
