# Door connection reuse handoff

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Reduce measured door/light validation overhead without changing connectivity,
visual state, gameplay or owner room layouts. Scope is a render validation call;
this does not establish whole-render or ordinary-play FPS gains.

## Accepted decisions and constraints
Connectivity is symmetric under main._placed_rooms_connected: matching branch
owner plus opposing room ports. Inputs do not mutate during the synchronous
validation call. Reuse an edge result only inside that call; never retain it
across calls/frames. Preserve current room changes, rotation, power and fades.
No asset generation, owner-room edits, publication or commits.

## Current state
scripts/grid_canvas.gd::_door_light_state creates a local connections dictionary.
Vector3i(min endpoint x,min endpoint y,axis) identifies each undirected grid edge,
including negative coordinates without relying on a packed grid-width integer.
Both room visits share the result; the dictionary dies on return. Actual renderer,
geometry, door frame rules, actor depth, light levels and key formats are unchanged.
No refactor of main.gd. Its connectivity policy remains authoritative.

## Verification
Attribution evidence: output/door-light-attribution-2026-09-21/.
Native100-room snapshot, complete keys equal between original and instrumented
subclass. Connectivity was the largest measured helper,400calls and about1.15ms
inclusive per validation call. Wrapper overhead affects attribution; helper times
are not an exclusive breakdown or FPS measurement.
Candidate and installed evidence: output/door-edge-reuse-2026-09-21/.
Both native runs exit0 without logged errors. Seven complete-key comparisons pass:
normal, blackout, interior-off, partial fade, branch split, rotation and restored.
All reduce connectivity calls400->220. The final probe calls installed production
code against a preserved pre-change method, not two copies of candidate code.
Paired before/after/after/before blocks,10warmups and100calls per block:
before3214.13/3208.06us; installed2880.76/2864.88us. Means3.211->2.873ms,
0.338ms (10.5%) reduction for this paused100-room call. Counting-wrapper overhead
is present. No scene-wide rendering/FPS claim, human expedition or visual acceptance
claim follows. No artwork changed and complete door/light state remained identical
in the seven scenarios. Current runtime references and source hashes are recorded.

## Next action
Keep this alongside the recent Bill work repairs for the next meaningful release
checkpoint. Current f2ec1eb651c14137 packages predate these changes. Continue room
and ordinary-expedition review, measured live-room rendering work and Apple Silicon
hardware testing. Owner reference-room findings remain staged, not authorized
layout edits. Broad goal remains unfinished.
