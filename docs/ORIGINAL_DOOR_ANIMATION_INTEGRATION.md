# Original door animation restored to layered connections

The original `dooranimated.png` is unchanged. `animated_door_atlas.gd` registers
the existing ten playback frames on its 4x3 sheet (744x534 pixels per cell).
The fully open frame's transparent span at x216..527 is 312 pixels and maps to
the canonical 72-world-unit clear opening. The whole sprite width is not used
as the aperture. Existing legacy-room door rendering remains unchanged.

The shared layered connection adapter draws one assembly per east/south-owned
edge. It reuses the source's threshold, moving leaves, header and illuminated
jambs. The threshold draws after floors and before crew. Upright pieces render
before or after crew based on ground depth and the existing rendered foot offset.
The original source's broad shoulders are compressed into the existing jamb
envelope; this is registered component adaptation, not a uniform bitmap scale.

For east/west crossings, threshold and leaf travel follow the wall while jamb
height remains screen-up. This is an edge-on reassembly of the existing art,
not newly authored side-facing artwork. Its appearance still needs owner review.
The fallback procedural leaves remain only for a missing atlas. No door locking,
pressure simulation or power-dependent access mechanics were introduced.

The embedded station crew path now draws the same foot-anchored contact shadow
as the standalone room path; previously its early return skipped that shadow.
Source y68 is registered as the foot baseline rather than the padded crop's y74.
That aligns the artwork and shadow with the existing ground-depth/collision point
without changing movement. Individual walk frames can still lift a foot naturally.

Verification:

- `tests/playtest_animated_door.gd`: source dimensions, clear alpha span, bounds
  for every registered component, 88 close-up crossing poses over four directions
  including reverse traversal, fully open crossing interval, mixed-power and pause.
- Native output: `output/whole-room-pilot-01/animated-door-final/` and matching log.
- `atlas-door-station-final.log`: inherited station/lighting tests pass, including
  1,616 four-room route samples, threshold-clearance checks and mature-station view.
- Four gameplay regression suites pass (`*-atlas-door.log`).

Remaining limitations: no new directional source, no dynamic frame shadows,
and the source's cyan emission is still painted into the atlas (room shading
affects it, but it is not an independent emissive channel). Geometry assertions
and screenshot review are not a claim of perfect occlusion for every future prop
layout. The current bounded room layouts and test crew are the verified scope.
# Wall overlap and station finish correction — September 5

Layered rooms now render their shells before door assembly, followed by props/crew
and the depth-selected foreground door pieces. Previously, the shell could paint
over door jambs that had been sorted behind the walker. Preview rendering retains
its complete room queue. Physical openings remain 72 world units; no wall/collision
cutout was widened to hide the overlap.

The original atlas is unchanged. A one-time transparent SubViewport applies a
reversible ivory/charcoal station material with neutral-white task lamps (owner
refinement after the initial muted-green trial). Its cached
texture is used only for layered-room connections; legacy doors keep their source
finish. Alpha and frame registration are preserved. This retains the original
surface wear and is not a newly authored directional door asset: the east/west
edge-on reassembly is still visually narrow and deserves owner review.

Native evidence: `output/whole-room-pilot-01/door-finish-v2/` (88 crossing poses),
and `door-finish-station/` (four-room routes, mixed legacy station and lighting).
