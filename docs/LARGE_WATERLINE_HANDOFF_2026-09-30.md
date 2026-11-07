# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Large equipment waterlines

## Objective and acceptance
Close the condition pass's large-equipment gap: exposed artwork keeps its original
materials, submerged portions darken/fade with rising water, and draining restores
the dry appearance. Cover all four large-room types and rotations at gameplay zoom.

## Accepted decisions and constraints
Owner authorized continuing this work. Reuse selected painted sources, source
density, placements and overhead perspective. No source resampling or recoloring.
Preserve separate Moonbay/tidal chamber water, mission rules and owner Studio data.

## Current state
scripts/large_wet_equipment.gd gives each movable prop its own existing submersion
shader, using its floor baseline and the ordinary 76-world-unit waterline rise.
rooms/large-rooms/studio_view.gd routes wet props through these child commands;
drained props return to the original immediate drawing. Hidden/offscreen equipment
is suppressed and removed/replaced rooms release their wet canvases. grid_canvas.gd
adds the hide/cleanup call and carries the existing unpowered dimming state.

rooms/large-rooms/common.gd clips fixed painted machinery into exposed/submerged
regions while retaining source UV registration. Horizontal waterlines are computed
in floor axes, including sideways source art. Hydroponics beds/cargo gantry use room
water; the mini-sub/turbine use their independent chamber water; peripheral intake
and control equipment use room water. The tidal rotor is shaded at flooded depth
and holds its visual angle under Reduced Motion; simulated angle remains unchanged.
Four room draw scripts pass these depths. No gameplay, costs, crew bindings, source
PNGs or saved layouts changed. Fixed machinery uses static clipped shading; movable
props use the existing subtle shader meniscus. Both freeze at the applicable state.

New paired scripts/tests: large_wet_equipment.gd, test_large_waterline.gd and
review_large_waterline.gd. tools/verify_large_waterline.py runs isolated gates and
owner fingerprints; tools/preview_large_waterline.py packages five stepped native
depths without pixel resizing. Preview:
output/large-waterline-v1/large-room-water-depths-v1.gif. All native stages and
normal-zoom/four-rotation captures accompany it.

## Verification
Current-checkout closeout: output/large-waterline-20260930-090025. UID, clipping
geometry and native review all PASS, zero failures; all 2,924 owner-profile files
are unchanged, with no deltas. Scratch profile contains the supplied layouts and
large-waterline.meta. The four-room rendering sample passes: p95 grid 6.031 ms,
forced-render wall p95 33.886 ms, worst 42.121 ms. Repackaged and reviewed native
preview from this run. This verifies the implementation after concurrent checkout
work; the earlier profile deltas below remain historical evidence.

Earlier evidence: output/large-waterline-20260930-044734. UID, clipping geometry and
native review PASS, zero native failures. All four room types/four rotations cover
dry, .25, .65, full and drained states. Geometry gates prove no missing/duplicated
area and a horizontal split for quarter-turned square, sub and intake source sizes.
Native dry/drained equipment crops are byte-identical; actual paused simulation
and advancing clocks under Reduced Motion hold rendered equipment pixels. Wet
unpowered props keep inactive screens/dimming; removed-room canvases disappear;
no missing artwork loads. Agent reviewed the four-room native board and rotated
normal-zoom equipment. Source diff whitespace checks pass.

Four wet large rooms, simulation held: p95 grid draw 7.863 ms, forced-render wall
p95 44.260 ms, worst 50.838 ms; fixture budgets PASS. This is a bounded rendering
sample with forced flushing and host load, not full gameplay/60 FPS acceptance.

Fixture corrections: exclude the legacy walker as well as NPCs; settle normal
lighting/hazard overlays and supply healthy oxygen before pixel comparisons. A
test-only RefCounted set_process call was corrected. Normal game behavior was not
changed to make these tests pass.

Scratch APPDATA/LOCALAPPDATA used. Final owner comparison FAIL: 2,861 files compared,
13 changed test-meta/log/startup-image paths (summary.json lists each). Attribution
unresolved with concurrent activity; main progress/checkpoint/room_layouts.json
unchanged. No owner restoration. Earlier compile/geometry diagnostic intervals
preserved the owner profile; subsequent failed/native intervals retain their logs.

## Next action
Owner visual review; previous large-equipment waterline limitation is closed in
source. Playable release acceptance remains separate. No commit, push or export.
