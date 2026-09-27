# Department door variants handoff

Updated: September 26, 2026 · BrineSpace

## Objective and acceptance
Create room/department door variants in the preview, using the approved V2 design.
New variants are ready for owner visual review.

## Accepted decisions and constraints
Directional viewing: selector above main canvas now offers north room, right/east,
bottom/south and left/west. Side/bottom are enlarged overhead chamber fittings with
actual grating, both doors, diver facing, water and beacons sharing the full cycle;
they do not rotate the north room elevation. Bottom browser view and syntax checked.
Caution timing polish: 85-unit faded beams rotate once per 2.5 seconds, with
1.25-second prewarning and 2-second afterglow around each door movement. Cyclic
windows cover the loop boundary. Pre-opening browser view and syntax checked.
Inner-door/caution follow-up: overhead inner leaves increased from 10 to 18 units
of visible depth; matching 22-unit jambs. Four small amber beacons rotate at either
door's opening/closing phases and remain dim otherwise; tied to preview time so
pause/scrub also controls rotation. Browser opening view, syntax and cycle tests pass.
Straight-through correction supersedes the exterior detour: diver stays on x=0
for exit/return, still waiting for full hatch travel. Frame rendering now places
the sill beneath the actor and the upper frame/lintel over the actor. Inspected
crossing at cycle times 15.1 and 16; centered-route and interlock checks pass.
Outside-edge correction: eleven-unit steel depth now projects along the exterior
normal, away from the chamber face. Lintel patch now starts flush at y=140 and
uses the source wall cap's proportional height, removing its raised top lip.
Half-open browser view and JavaScript syntax checked.
Steel-width follow-up: moving north hatch now has an 11-unit textured side plane
connected to its painted top rim. Side uses existing rim steel/gasket pixels,
with a subdued shade, rather than a second front/rear plate or flat gray extrusion.
Closed face stays unobstructed. Half/full-open browser views and syntax checked.
Character scale correction: animated diver now uses the native room renderer's
65.28-unit standing height (148px source), replacing the erroneous 40-unit browser
height. Compared against the captured room character; syntax and cycle checks pass.
Inner door added: top-down two-leaf airlock artwork at (350,444), opening from
room into chamber. 45-second wrapper around outer cycle includes dry entry,
inner sealing, flood/sea trip/drain, dry exit and final closure. Both door states
interlocked; tests cover 4,501 samples and inner threshold clearance. Entry and
opening browser views checked. Uses existing airlock-low.png, no new raster.
Wall-aware swim follow-up: approach inner wait at (0,60), hold still facing hatch
through its motion; outer wait is directly in front at (0,-145), beyond the swing.
Exterior approach detours via (-70,-110), never laterally across the hull. Actor
draws before the fixed rim/frame, preserving passage between its top and bottom.
Tests cover stationary facing waits, wall clearance and leaf clearance; pass.
Closed-rim correction: top rim now draws behind the face and is concealed when
fully seated, revealing smoothly during opening. Closed dry browser view checked;
JS syntax passes. This removes the rim painted across the closed leaf's upper edge.
Gray-line follow-up: removed the old procedural gray extrusion behind the new
painted rim and stopped forcing minimum front-face width when edge-on. The rim
alone now supplies overhead thickness. Full/half-open browser views inspected;
JS syntax passes. This supersedes the earlier solid gray extrusion approach.
Painted top rim: generated ocean-hatch-rim.png with rounded steel bevel, gasket
and recessed fasteners. Registered on the moving hatch's top plane and overhead
leaves in diving-room.js, replacing the flat gray top. Source/prompt preserved;
full-open browser view and JS syntax checked. Seven-unit visible thickness.
Solid-leaf correction: filled the entire rounded extrusion and removed the rear
plate's independent outline. The five-unit edge now reads as continuous steel,
including at full opening. Half/full-open browser views and syntax checked.
Exterior finish correction: flood tint reduced to 10% when closed and fades
quadratically to zero when fully open. Upright moving leaf now uses projected
rounded front/rear silhouettes (six-unit corners) instead of rectangular strips,
retaining the five-unit edge depth. Half-open browser view and syntax checked.
Hatch depth/water polish: upright leaf now has a five-unit steel edge and top
surface visible during opening. A restrained blue overlay follows chamber water
amount on upright and overhead leaves, fading completely when drained. Browser
half-open flooded view reviewed; JavaScript syntax checked.
North lintel correction: a 78x20 cap sampled from the existing room steel now
bridges the hatch shoulders. It closes the visual gap above the opening while
leaving the swimmer visible below. Browser through-hatch view and JS syntax checked.
Full passage correction: route starts/ends at y=190 beside the inner door, crosses
the complete flooded chamber and goes outside. Exterior aperture background now
precedes actor drawing; cap is cut through over the opening. Mid-chamber and
through-aperture screenshots checked; cycle assertions pass. Browser preview only.
Latest owner correction supersedes prior hinge/size: smaller hatch, opposite
hinge. North leaf is 56x64, right hinge, outward swing; swimmer waits at (-70,-115).
Directional fitting leaf scales accordingly. Clearance test updated and passing.
North presentation correction: retain the riser and show the upright hatch face
animating outward (strip-projected rigid leaf), not just its overhead edge.
Outside swim path ends 115 units beyond the threshold, 70 units away from the
hinge side. Segment-distance assertions preserve 24-unit swimmer clearance over
3,001 cycle samples. Updated airlock-cycle.js, diving-room.js and cycle checks.
Latest motion correction: ocean hatch swings outward. Diver swims in the flooded
chamber until exterior hatch seals and water finishes draining. Updated room
cycle and all four overhead swings; separate water overlay and timeline scrub.
airlock-cycle.js and check-airlock-cycle.cjs added. 3,001 state samples pass;
browser closing, draining and dry standing states reviewed. Preview-only scope.
Exterior hatch placement correction: the hatch belongs at the pressure chamber's
north wall contact, not the opposite room entrance. The browser fitting now carries
the grated chamber throat through that riser and sends the diver north into the ocean.
Screenshot reviewed; JavaScript syntax passes. This supersedes the earlier south-exit study.
Preview only; eight new departments plus retained neutral BRINE/corridor family.
Same aperture, fixed frame and rigid sliding motion. Preserve owner saves.

## Current state
assets/door-polish-v3 contains 16 generated masters, full 47-room catalog,
source provenance, exact prompts and animated review.html.
tools/preview_door_art.gd selects and registers department art;
tools/preview_riser_room.gd selects the family when drawing each room.
The V2 gallery links to the new collection.

## Verification
Full native 47-room verification passed, zero clearance failures, corridor
rotations verified, owner save fingerprint unchanged. All families reviewed
visually, including eight native room contexts. See V3 README for evidence.

## Next action
Owner review of department treatments. Production integration is not requested.

Diving-room passage follow-up: diving-room.html / diving-room.js compose the new
hatch at the north chamber/hull connection of a preserved native room capture. Separate seabed,
recessed threshold, fixed seals, moving leaf and helmeted Bill walk/swim cycle.
Four directional passage studies, 6,404 equivalent clearance samples, syntax and
browser visual checks passed. Room reference PNG and diver-preview.json preserved.
This is a browser fitting study; no native simulation or owner saves changed.

Top-down follow-up: added a true overhead hatch master and hatches-top.js with
four directional animated fitting studies, inward 90-degree travel and a 72-unit
opening. North/east/south/west use quarter turns of the overhead geometry, not
rotated front elevations. All four browser endpoint views checked; JS syntax
passes. Native room integration remains pending.

Ocean hatch follow-up: added interior/exterior closed pressure-hatch artwork and
a dedicated section of the V3 gallery. Single leaf, wheel, porthole, six locking
dogs and reversed hinges; marine exterior finish. Sources, exact prompts and
hash/alpha manifest preserved. This is an artwork study; hinged animation,
overhead mates and native room fitting are pending, not part of prior 47-room evidence.

Opening follow-up: hatches.js now renders both faces opening/closing in the gallery.
Fixed pressure ring, wheel-release interval, orthographic hinged leaf travel and
reversed hinge sides. Dedicated open/close/play/scrub controls added. Browser
endpoints visually checked and JS syntax passes. Native fitting remains pending.


## Airlock consistency pass — September 26, 2026

Objective: verify the approved thick outer hatch, swimmer clearance, seals and
warning sequence across the four preview directions. The 11-unit steel depth
stays on the outside edge; straight passage and stationary facing waits remain.

Changed: airlock-cycle.js now owns the shared depth and caution timing;
diving-room.js consumes those values. check-airlock-cycle.cjs checks the full
steel slab (not just its centerline), moving-door warnings, advance/lingering
warnings and cycle wrap. All paths above are under assets/door-polish-v3/.

Verification: syntax and cycle checks pass (3,001 outer-cycle and 4,501 full-cycle
samples). Browser inspection covered west opening, north passage layering, east
dry inner opening and south closing. No additional frame adjustment was needed.
Evidence: output/riser-room-preview/airlock-consistency-south.png.

Next: owner review of the fitting study, then native room integration and native
visual/route verification. Side/bottom views remain overhead chamber studies;
this pass does not establish full-room fitting or production readiness.
