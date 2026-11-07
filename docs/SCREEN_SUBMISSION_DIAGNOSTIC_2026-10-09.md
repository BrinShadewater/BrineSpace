# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: screen command submission attribution

## Objective and acceptance
Locate costs inside the screen/effect path after exact numerical reuse saves only
~0.055ms/frame. Preserve normal rendering, original calls, animation sampling and
saved playback. Instrumentation is diagnostic, not production optimization.

## Accepted decisions and constraints
Actual debug=false frozen crew-cache package; private two-file Grid/RoomContent
overlay, isolated profiles, unchanged owner guard. Typed proxy forwards the same
five CanvasItem calls and arguments, timing after caller argument construction.
These windows include timer and dispatch overhead, exclude downstream GPU drawing,
and are not exact timings of an uninstrumented production path. No quality changes.

## Current state
D:/bs-release-crew-cache-20261009/screen-submit-diagnostic/ holds overlay, hashes,
source and workloads/. Original PreparedScreens formulas remain unchanged. Library
effects and ordinary-library calls have separate timing categories. Verified physical
QA package reused; normal source and delivery untouched.

## Verification
Session79179 exits0:54040-room idle samples at1/2/4x, zero engine/missing-art errors,
owner2,938 unchanged. Six exact state comparisons against both all-visible baseline
orders match, including playback. Station screens paint107 slots/frame; ordinary
library paints cost~0.138-0.141ms. No station-effect timing occurs in this selected
fixture, so no claim about all effect types.

Submission windows:36 antialiased polylines cost388.03/398.04/400.83us per frame;
480 rectangles41.01/41.91/42.58us;72 lines7.50/7.64/7.91us. No radar arcs/circles
appear in the selected scene. Instrumented screen-body totals901.01/913.20/917.91us
include proxy overhead and nested submission windows. Counts and intervals are
separate units; do not add nested values or call this a matched FPS improvement.
workloads/analysis.json preserves timings and exact state checks.

## Research and next action
Inspected Godot's renderer at the executable's reported commit
ed1daf0bf001b61586d9930840f2f1394092c079. The positive-width antialiased polyline
path compensates width, calculates segment joins and allocates three polygon strips
for its center and feather edges. Source:
[renderer_canvas_cull.cpp](https://github.com/godotengine/godot/blob/ed1daf0bf001b61586d9930840f2f1394092c079/servers/rendering/renderer_canvas_cull.cpp).

Next investigate reuse of equivalent stroke geometry/submission resources while
retaining the engine's feathering, joins, float precision, color and command order.
Any prototype needs actual pixel comparisons at varied scales/clock values and
matched performance; no replacement mesh equivalence proven yet. Keep antialiasing
and animation quality. Whole-frame budget, original bugs, endurance and Mac gates
remain open; this~0.4ms window alone does not explain all remaining frame cost.
