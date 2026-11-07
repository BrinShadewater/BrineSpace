# Room floor materials: first pass

The shared floor renderer now supports five clean construction treatments while
preserving existing room colors, door geometry and furniture registration.

- Steel: recessed access panels, restrained corner fasteners and bevel highlights.
- Wet: removable side drain channels for Hydroponics, Life Support, Biodome and condenser.
- Sealed: quiet composite panel highlights for medical, science and BRINE core.
- Warm: fitted narrow strips for crew habitation and lounge.
- Technical: access panels with restrained service ticks for command, communications and data rooms.

The existing procedural material grain is slightly stronger; no generated raster
was added. Profiles are assigned explicitly by room view. Existing floor dressing
still draws afterward. All details are visual and leave collision and routes unchanged.

`output/room-floors-v3.log` passes six furnished rooms at 1280, 1600 and 2560 widths.
Final captures are in `output/room-floors-v2/`. The first run used the wrong
Hydroponics ID in the fixture and failed; the fixture now validates room IDs.
This is native rendering evidence, not a new standalone export or owner approval.

[Review furnished floors](../rooms/whole-room/floor-review.html)

## Traversable dressing

The shared floor layer now adds bordered woven rugs to warm rooms, flush circular
drain grates to wet rooms, and recessed service covers to steel/technical rooms.
Paired low-contrast outlines lead toward actual port edges and follow rotation.
The outlines join at the center into a cross for four ports or a T for three,
with no internal lines across the junction. These are floor
CanvasItem draws only: no prop registrations, collision shapes or navigation changes.
Existing room-specific floor dressing remains above this common layer.

Applied to 29 shared floor consumers. `output/room-dressing-v3.log` verifies six
furnished rooms at three window sizes; current captures are in
`output/room-dressing-v1/`. The existing production-ten walker-path test exits 0.
Earlier dressing logs failed on type inference: the route offset now has an
explicit Vector2 type; the current cryo setter comparison has an explicit bool.
No standalone export or exhaustive character animation review is claimed.

## Joined door paths

`route_outline` builds a continuous corridor boundary from actual port edges.
Missing branches close the corresponding central edge; rotation follows the ports.
`output/joined-paths-v1.log` passes Command (cross) and Hab (T) at all four rotations.
Native captures were visually inspected for the cross and both T orientations.
[Review joined paths](../rooms/whole-room/path-review.html).
