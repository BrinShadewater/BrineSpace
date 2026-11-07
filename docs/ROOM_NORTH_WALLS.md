# Raised north walls

## Owner decision — supersedes the study below

Keep all walls at the current low height, including exposed north boundaries.
The raised-wall study below is historical evidence, not the accepted station
direction. Do not promote its raised geometry into additional rooms or cards.
Settings now default to low walls, ignore the retired saved raised-wall preference,
and retain low walls on Accessibility reset. The raised-wall toggle is removed;
the renderer study code is preserved, inactive in normal play.
Preserve existing door, floor, and prop registration while doing so.

Settings regression: `tests/test_low_wall_settings.gd` passes with child exit 0,
`LOW WALL SETTINGS: 0 failures`, and empty stderr in
`output/low-wall-settings-v1.log` / `.err`. It covers a fresh session, an isolated
legacy saved `true` value, absence of the retired toggle, and Accessibility reset
including persistence. It does not claim a new visual or packaged station review.
The older `playtest_north_walls.gd` below tests the superseded study UI and is not
a current acceptance gate; its original evidence remains historical.

Native follow-up: `tests/playtest_low_wall_station.gd` captured Command, Hab,
Med Bay, Hydroponics, straight corridor and corner at all four rotations into
`output/low-wall-station-v1`. Child exit 0, 24 dimension-checked 1600x900 frames,
zero fixture failures and no ERROR/SCRIPT ERROR lines. Raw-PNG loading warnings
remain; this is checkout rendering, not export verification. Hab q0 was visually
inspected with the low north edge visible. This fixture uses paused isolated
placements and does not yet cover connected seams, crew crossings or power loss.

Visual failure: `corner-q1.png` shows hydroponics machinery outside the narrow
corner hull after the fixture switches room identities. Do not count the 24
successful captures as visual acceptance. Investigate stale content/cache or
room-view dispatch using a fresh corridor-only comparison before altering art.

Resolved retained-content defect: the LIVE pass kept a prior furnished room's
cell-keyed canvas visible when a procedural corridor replaced it. Content
eligibility now excludes narrow corridors and non-layered replacements; no art,
door or collision geometry changed. The new assertion failed on all eight
straight/corner rotations before the fix (`low-wall-station-negative-v2`, exit 1),
then passed with all 24 native captures (`low-wall-station-fixed-v3`, exit 0,
zero ERROR/SCRIPT ERROR lines). PNG loading warnings remain. Fresh corner-q1
was visually inspected: the stray hydroponics assemblies are gone; connected
seams, real crew crossings and packaged verification remain separate work.

Connected follow-up `output/low-wall-connected-v4` passes 28 native 1600x900
captures: the previous 24 plus four cardinal Command/Command pairs. Reciprocal
door topology passes, child exit 0, no ERROR/SCRIPT ERROR lines. East and north
pair frames were visually inspected: low perimeter bands and shared closed-door
jambs align at this overview scale. This is not open-door animation or crossing
acceptance, and does not cover every department pairing.

Airlock follow-up: the forced raised-wall branch is removed from current station
source. A low cutaway hatch and exterior-reaching chamber now render in all four
rotations (`output/airlock-low-cutaway-v2`, AIRLOCK PASS, 1,039 movement samples,
no ERROR/SCRIPT ERROR lines). The exterior aperture subsequently passed native
review and `card-low-cutaway-v1.png` is now selected; the old raised card remains
historical. Dedicated Airlock package v2, mixed-station controlled-tour package
v3 and the corrected autonomous mixed-station export v4 pass their scoped
checks. V4 visits all 17 rooms with 180 door transitions. See
`rooms/underwater/airlock-v4/README.md` for revision-specific limitations.

The layered station renderer adds a 48-unit screen-facing wall above the north
edge, with a ledge, panel joints and department fittings. North neighbors suppress
the extension, including incompatible neighbors, to avoid covering another room.
Floor dimensions, door logic, collision and furniture registration are unchanged.
Warm rooms use framed keepsakes and a noticeboard; clinical rooms use a cabinet
and chart; wet and technical rooms use ventilation, a service line and gauge.
This is a procedural first pass in the station renderer; existing baked card art
and standalone room study scenes do not include this extension.

Native fixture tests/playtest_north_walls.gd passes four departments at all four
rotations and asserts a working north/south connection. Captures were inspected
for Hab, Medical and the connected pair. Log: output/north-walls-v2.log.
Review: rooms/whole-room/wall-review.html. No standalone export is claimed.


## Optional wall layer and ocean windows
Menu > Settings > Accessibility now includes Raised walls and ocean windows.
It applies immediately, persists in display.raised_walls, and defaults to on.
Turning it off restores the original low shell; resetting Accessibility restores it.
A stable cell-coordinate selection gives two-thirds of exposed walls ocean windows.
Frames have glass reflections, distant seabed silhouettes and small fish; department
fittings now have mounting shadows, bevels, fasteners and functional small details.
Native output/north-walls-v3.log verifies four departments at four rotations, a
connected pair, actual settings button signals, saving, reload and restoration.
The Hab window and classic connected view were visually inspected.


## Material polish v4
Inset panel bevels and vertical shading break up the flat wall face. Hab gains timber lower trim, more legible miniature landscapes and warm shielded lamps; other departments use cooler lamp lenses. Window frames now have a mounting shadow and lit upper/left edges. Native output/north-walls-v4.log passes the existing rotations, connected pair and persisted layer toggle; Hab capture visually inspected.
