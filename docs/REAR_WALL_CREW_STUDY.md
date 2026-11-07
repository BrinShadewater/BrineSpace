# Rear-wall crew presentation study

Status: **rejected by owner — keep all walls at their current low height.**

This decision supersedes every candidate recommendation and adoption checklist
below, including exterior-only raised walls. The study never changed production
room views or doors. Keep fixtures and outputs as historical evidence; do not
continue raised-wall rollout or its remaining lighting work. Any future crew-depth
repair must respect the accepted low architecture. No assets were deleted.

The cradle-circuit review showed Bill's head over the seabed while his feet were
inside the low north wall. Foot clearance is valid but does not settle this visual
relationship. Shrinking Bill, clipping his head, or changing navigation was not
used as a workaround.

`tools/capture_rear_wall_study.gd` compares the existing low wall with screen-up
32- and 56-unit rises. The fixture subclasses both drone room views; production
renderers, props, collision, doors and cards are unchanged. All columns share the
same south-facing actor and standable foot position. Wall faces use simplified
flat material; these are architectural studies, not new generated finished art.

## Results

- V1 added a backing behind the old low cap. Agent visual review rejected this:
  the remaining low cap still reads as a ledge through the actor. V1 also requested
  north sockets in rotations without north ports; metadata records that mismatch.
- V2 raises the real cap and corner/jamb tops with the wall face. It only requests
  north sockets in compatible rotations and asserts actual open state. Twelve
  comparisons cover both rooms in four sealed rotations and two exposed-socket
  rotations. Each PNG is 1600x760. Child exit 0, zero fixture failures and no engine
  errors. Import also exits 0 and generates the tool's paired UID.
- Reviewed V2 Mining q0 sealed and Salvage q2 exposed-socket images. The 56-unit
  face frames Bill's complete silhouette; 32 leaves his head near the upper cap.
  This is a preferred next trial, not owner approval or a new global wall height.

Evidence: `output/rear-wall-study-v{1,2}/`, respective logs, and
`output/rear-wall-study-import-v1.*`. Review JSON records actor hash, foot positions,
socket states and study-script revision. V2 uses inner subclasses, so its recorded
renderer hash identifies the study script, not the entire production dependency tree.

## Required before adoption

Test a north neighbour and shared doorway: raising a rear wall projects into the
neighbour's floor area. An exterior-only rule may be preferable, but must also be
reviewed when a neighbour is added or removed. Include actual door leaves/frame,
crew crossing, corners, power lighting, wall fixtures and camera bounds. Exposed
sockets in these sheets are labelled diagnostic geometry, not functioning doors.

Retain the standard 384-unit footprint, 16-unit wall ground thickness and 72-unit
aperture. A presentation rise is not additional floor space or permission to change
the accepted low side-door construction. No clipping or collision fix is claimed.

## Shared-boundary station follow-up

`tests/playtest_rear_wall_connections.gd` substitutes study views only inside a
fixture-owned real main scene. It uses the production layered compositor and
proximity-driven department door, not a separate illustrative door. Two north/south
compatible rotations compare baseline, all-raised and exterior-only at five static
crew positions. These are assigned poses, not a movement-controller crossing test.

V1 exposed a coverage defect: the southern room omits its north wall because the
northern room owns that shared edge. Raising the omitted edge cannot test shared
wall height. The V1 PASS banner only describes its weaker assertions and must not
be treated as shared-wall evidence. Files remain in `output/rear-wall-connections-v1`.

V2 raises the north room's owned south edge in the all-raised case. It verifies
that all-raised/exterior-only actually differ in pixels, and that exterior-only
differs from baseline. Every pose passes actual NPC static clearance; the real
door is fully open at the threshold and closed at the two distant poses.
Thirty comparison frames plus five base captures are 1600x900. Child exit 0,
zero assertions and no ERROR/SCRIPT ERROR entries; evidence is in
`output/rear-wall-connections-v2/` and its adjacent logs. Recorded source hashes
identify the grid and study revisions, not a complete packaged dependency closure.

Agent review of q0 threshold all-raised/exterior-only and q2 all-raised north-side
rejects the all-raised presentation: its cap crosses the neighbouring floor and
equipment silhouettes, while the original door stays at the low shared boundary.
The next candidate is therefore **exterior-only raised north backing**, with
shared walls retaining the accepted low cutaway. This is not owner approval.
Cards, neighbour addition/removal, narrow neighbours, power/fixture alignment and
continuous crossings remain open. No production room or door art was changed.

## Continuous crossing, topology and power follow-up

`--continuous-and-lifecycle` adds four scheduled production-controller crossings
(two directions at q0/q2), observed traveled segments, real proximity-door frames,
and removed/added/removed-again neighbour snapshots. The candidate height is derived
from neighbour occupancy inside this fixture, not adopted in the production grid.
Topology snapshots mutate isolated fixture placement lists; they do not test the
normal construction/demolition workflow. No navigation dimensions are changed.

`output/rear-wall-motion-v1/` passes 224 swept ticks and all arrivals. The offline
capture exposes an unshaded raised face outside the original cell mask. The study
renderer adds bounded shading to that projected wall using the actual room light
level, without changing the existing floor darkness layer.

V2 fails during concurrent main.gd editing, before fixture initialization: an
untyped count expression prevents parsing. Its task-owned Godot process is stopped
and the logs remain. No main.gd edit was made by this pass. The current declaration
is corrected by concurrent work; explicit check-only passes before V3 runs.

`output/rear-wall-motion-v3/` exits 0 with no engine errors: the 30 static
comparisons, four crossings / 224 swept ticks, three topology snapshots and an
offline study capture pass their assertions. There are 71 actual 1600x900 frames
including base captures. Simulation uses 0.1-second ticks, with every eighth tick
and arrivals captured; this is not full-speed video acceptance. Complete traces
and controller hash are in `crossings-lifecycle.json`.

Agent review: V1 crossing sample, restored exterior boundary and offline frame;
V3 offline frame. The raised wall now darkens. Read-only pixel samples at (640,340)
change from RGB (70,82,86) to (24,31,37); interior (650,440) remains (27,33,39),
and exterior (730,340) remains (14,25,31). These three samples are not whole-frame
equivalence: concurrent environment/UI changes are visibly present elsewhere.

**Still unresolved:** Bill's head above the cell boundary is brighter than the
shaded body. Per-wall tinting cannot fix actor pixels drawn afterward. The final
candidate needs a post-assembly lighting mask covering the projected interior
and actor silhouette without shading unrelated seabed/neighbours. Fixture mounting,
narrow neighbours, cards and owner approval also remain open. Do not label this
as complete lighting or production integration.
