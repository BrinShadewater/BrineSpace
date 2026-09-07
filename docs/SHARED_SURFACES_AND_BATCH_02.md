# Shared floor, door and card pass; room art batch 02

## Implemented in the four layered room types

- `room_floor.gd`: one 48-unit seam grid over low-contrast procedural material
  grain. No resampled source-room patches, baked seams or half-tile patch edges.
  Original PNGs are untouched. Floor material is still the existing neutral
  station palette; departmental migration of the four older rooms is not complete.
- `room_door.gd` and station adapter: one shared two-leaf assembly per valid
  connection, retracting through the existing ten-frame crew-crossing timing.
  Fully open leaves disappear from the complete 72-unit aperture. No second
  legacy bitmap frame. Leaves render before cell lighting so mixed-power rooms
  shade their respective halves. No new locks, power dependency or pressure rules.
- Cards: all sockets sealed, two north fixtures retained. Nursery v6 and Life
  Support/Hydroponics/Reactor v4 load in the current station/card consumers.
  Previous card versions remain available.

## Evidence

`tests/test_shared_room_surfaces.gd` checks seam spacing, matching constants and
ten monotonic aperture states. `playtest_four_room_station.gd` now also asserts
fully open doors when the real crew foot reaches a threshold.

`shared-surfaces-final.log`, `surfaces-1280.log`, and `surfaces-2560.log` under
`output/whole-room-pilot-01` pass the native inherited room/state tests, 1,616
four-room route samples, mixed-light neighbors, and paused fades. Associated
capture directories retain closed doors, crew crossing, dark/idle states and
40-room overview evidence. Synergy, discovery, gameplay-polish and run-balance
regression suites also pass (`*-surfaces.log`). Save paths remain fixture-only.

## Generated art, not yet integrated rooms

Built-in image generation produced three distinct 1254-square candidates, each
with its own prompt. See `NEXT_ROOM_BATCH_BRIEFS.json` for exact v1 prompts,
canonical layout notes and the camera/style reference. All selected outputs are
in `output/room-batch-02`; generation originals remain in Codex's image directory.

| Candidate | Department | Selected file | Review |
|---|---|---|---|
| Mining Drone Bay | Robotics | mining-drone-bay-v2.png | Physical docking cradles and repair equipment distinguish it; wall socket trim is not canonical and must not be imported as geometry. |
| Med Bay | Medical | med-bay-v2.png | Teal beds, white ceramic, blank diagnostic screens; IV stands and stool require explicit footprints/occlusion registration. |
| Crew Hab | Habitation | crew-hab-v2.png | Warm textiles and personal objects; angled lounge chair needs a south-facing revision or explicit owner exception before acceptance. Extra north cabinet must not obstruct a rotated route. |

V1 lamp lenses remained visibly lit. V2 removes those light sources without a
global blackout. Visual inspection supports unlit lamp bases, not a guarantee of
pixel-identical preservation or absence of every painted highlight. Generated
walls, floors and sconces are reference material only: the authoritative floor,
wall/door assembly and north fixtures must replace them on integration. Do not
quarter-turn these complete bitmaps or count them as newly verified room types.

V2 exact edit prompt, shared by the three individually edited candidates:

> Use case: precise-object-edit. Edit target: attached room candidate. Preserve the existing image canvas, room framing, floor, wall geometry, furniture positions, pixel-art rendering, departmental colours and every equipment silhouette. Change ONLY all wall/ceiling light lenses and fixture emission: make the lenses dark neutral glass with NO self-lit white/cyan centers and remove their cast light spill. Keep soft neutral ambient visibility; do not darken the entire room. All screens remain blank. This is the non-emissive base; game code will add two standardized north sconces and emission. No text, new objects, grid seams or other changes.

SHA256 selected outputs:

- Mining: A8096F042B0AF2C757B758A83571251AC0D24FA9ABA64D0A5A79C9338422E8B9
- Medical: 50F2BFEF97600CCD77CFDEBAC8C8A003B2A3E5A410012798C1EA4D26EA7D6A6F
- Crew: 1EA8B97262BBD697B69671EDA03D6870BD4E64470BE796F59A3C931F2C9F42E0

Next production step: register separate props, operator clearances, pivots,
motion envelopes and light/screen regions, then validate all four layouts in
Godot before switching normal room/card consumers. The older four room sources
still need their own departmental finish/non-emissive-base migration. This pass
does not mark the full historical asset-expansion scope complete.
