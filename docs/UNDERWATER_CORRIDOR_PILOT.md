# Underwater narrow-hull connection pilot

Latest implementation audit: UNDERWATER_KIT_ACCEPTANCE.md. Final native v8
refreshes the cycle review with current structural details and nursery effects.
Its four-rotation sheet, closed/sealed and offline captures were inspected; the
9,216-step route suite passes without engine errors. Use v8 review media for the
current finish; v7 remains historical production-character-scale evidence.

## Structural detail follow-up (station v6 / cards v3)

The shared surface renderer now adds shallow reinforcing bands with fasteners
and flush service grates. Neutral maintained pressure-hull construction remains
the primary identity. Detail stays at the edges; no upright props, new obstacles,
false ports, hazard states or recipe hints are introduced. Original generated
surfaces remain unchanged. These additions are native geometry, not generated
new artwork or a claim that a whole illustrated corridor can rotate.

`detail_parts()` owns the fitting rectangles used by rendering and the containment
test. 388 fitting-corner samples remain inside the hull and outside the tapered
door approaches. Rotation uses the same orthogonal transform as the hull.
The station v6 test again passes 1,616 actual walker samples through four rotations,
both travel directions, offline and incompatible-socket captures; no engine errors.
Native station and power-off views were inspected along with the 512px corner card.
Cards v3 are active in both consumers; older baked versions remain preserved.

At station overview scale the new detail is restrained; it is not a replacement
for future bespoke room focal equipment or environmental art. No new animation
has been added in this detail pass. Owner aesthetic approval remains separate.

## Station/card integration follow-up

The existing `corridor` and `corner` IDs now use the narrow kit in the real grid,
placement preview and card/inspector textures. Costs, socket metadata, draft counts
and progression rules are unchanged. Canonical straight-room north/south sockets
map to the horizontal art geometry with a one-quarter-turn offset; corners retain
west/south as their base mask. `corridor_geometry.gd` owns the shared polygons for
station, cards and pilot. The normal walker uses its existing centre/door paths.

Evidence: `output/underwater-station-v5/` and matching log. 1,616 production path
samples fall within narrow floor bounds in four rotations and both directions.
Captures include room/corridor crossings, an unpowered corridor and incompatible
neighbor infill. Both visible draft thumbnails are asserted to fit their full
silhouette. Two new cards are `rooms/underwater/*-card-v2.png`; v1 exports were
failed script-compilation evidence and are not active assets.

Full room walls must not be omitted merely because their neighbor is layered:
a narrow corridor does not supply a full-cell wall. The grid retains those room
walls and uses the shared low collar wherever either neighbor is narrow.
Corridor shading is hull-local; fixtures do not appear at full-room north anchors.
The shared ocean backdrop replaces per-cell water patches and star-shaped glints.
Legacy orbital labels/mechanics are not migrated by this visual integration.

Four gameplay suites pass (synergy/run loop, discovery, polish and balance), with
logs under `output/underwater-test_*.log`. Visual owner review remains distinct
from the automated tests; more bespoke surface variation can build on this kit.

## Latest native review (v7)

`output/underwater-corridor-v7/review/door-crossings.gif` shows the downward and
side collars at native 2x world scale, with a complete opening/crossing/closing
cycle. `four-rotation-midpoints.png` compares all four rotations without resizing.
All eight direction/rotation sequences retain individual PNG frames.

Important correction: v1–v6 used the legacy small preview actor. V7 selects the
same directional source frames but renders the production crop (26,18,40,56),
46.08 x 65.28 world size and source foot baseline y68. Earlier route checks still
tested the 7-unit foot radius, but their images were not valid character-scale
acceptance evidence. V7 supersedes those visual scale comparisons.

Checks: 9,216 route steps; jamb/water rejection; closed/sealed gates; 328 native
cycle poses (four rotations, both directions); pause freezes actor/door clocks.
The 4-second review cycle is fixture timing, not a changed gameplay timing rule.
Power-off and each sealed-end state have separate native captures. Lamps now
rotate their complete flat housings with the wall rather than only their centres.

Art remains under review. This historical isolated fixture is not the production
movement controller or a flooding simulation. Station/deck integration and a
checkout-independent package smoke have since followed; see the section above
and STATION_PACKAGE_SMOKE.md.

Owner direction: the game is now underwater. This pilot tests narrow pressure-hull
corridor/corner cards; it does not migrate the game's orbital text or systems.

## Contract under review

- Card placement remains 384 x 384 world units, even where the visible hull is narrow.
- Straight interior is 96 wide; orthogonal walls are 16 thick (128 exterior).
- The last 32 units taper from a 96-wide interior to the existing 72-wide socket.
- Connections are at cell-edge centres, one shared door per seam, same floor level.
- A west-to-south elbow connects adjacent edge centres inside one card. Rotate
  layout polygons, not completed room art; existing large props remain south-facing.
- Water outside the floor polygon is not walkable. Placement still reserves the
  entire cell; unused water space is not permission to overlap another card.

## Historical native test (v2)

Run Godot with `--path . --script res://tools/underwater_corridor_pilot.gd`.
It refuses to overwrite its evidence folder, never loads the main scene and never
accesses player saves. Current captures: `output/underwater-corridor-v2/`.

The fixture uses existing Nursery/Life Support renderers and current shared doors,
held fully open for clearance review. Corridor surfaces are code-drawn blockout
geometry, not final generated hull art. Screen water is a plain backdrop, not a
fluid system. Grid-overlay captures expose the otherwise invisible card footprints.

The same polygon-union floor check is used by the incremental movement function.
Tests traverse 9,216 one-unit steps (both ways, four rotations), including existing
room prop bounds and a 7-unit-radius character footprint. Sixteen perimeter samples
approximate the circular footprint; this is not an exact physics-body sweep.
Additional checks cover near-jamb clearance and rejection of water beside the hull.
Native screenshots verify the floor and door assembly at actual rendered seams.

Not yet integrated into the deck, station placement, production pathfinding or card
thumbnails. No new room IDs, costs, synergies, flooding, pressure or oxygen rules.
Doors are open in this study; it does not certify animated closures at the collars.

## Historical approval gate (v5; superseded by integration above)

Current follow-up: `output/underwater-corridor-v5/` uses a low collar for both
orientations and the reusable `rooms/underwater/corridor_surfaces.gd` renderer.
The generated straight and two corner candidates are preserved with exact prompts
in `rooms/underwater/generation-record.json`. Full corner paintings were rejected:
v1 drifted; v2 retained the outline better but invented tall walls. Only registered
surface samples and a flush hatch are consumed. Source art is not overwritten.

The pilot captures all ten opening poses, seals each seam separately and turns
corridor lights off in every rotation. Its movement gate blocks closed/sealed
seams. These controlled snapshots are not yet an interactive station integration
or proof of the existing gameplay controller's behaviour in narrow rooms.
Remaining: visual polish/owner review, native cycle presentation, detailed
seam inspection and the production consumer integration gate below.

Review corridor width and collar proportions before art production. Then add real
placement/socket metadata, disconnected end caps, collision and card consumers,
and test door animation on the collars. Hull windows, ribs, exterior pipes and
underwater lighting must stay outside the reserved socket and route envelopes.
