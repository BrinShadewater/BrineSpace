# Clone Lab registered pass

Medical host, localized Bio/Science equipment. Source remains the original
1254-square image and hash in source-review.json; exact built-in prompt remains
in production-briefs.json. No regeneration or destructive cleanup was needed.

clone_lab_view.gd registers the complete vessel, incubator, nutrient cartridge
cabinet and console separately. Ground footprints are 64x65, 98x75, 78x59 and
94x56 world units. The vessel's visible height is about 134 units, distinct from
its ground depth. Full silhouettes stay within the four-unit safety margin.
Ground centres rotate while south-facing art and effect orientation stay fixed.

The generated shell/floor is not the gameplay room: shared pale Medical floor,
quiet two-module seams, service inlays and walls replace it. Canonical west/east/
south sockets control shared doors and flush infill. Both station and card maps
use clone-lab-card-v1.png; the full silhouette fits the draft card. White fixtures
remain independent from equipment operation. Other session's Battery integration
was preserved when updating the shared consumer lists.

Effects: vessel fluid marks, incubator scan needle, cartridge flow and console
traces. No clone body is baked in. Static glass and source indicator colors remain
part of the illustration; this is not a complete emissive/contents-layer export.
Existing creation, costs, unlocks and capacity rules were not changed.

Native evidence:

- clone-state-v1 (1600x900), clone-state-1280-v1 and clone-state-2560-v1:
  all four rotations, four-host motion/stillness/pause, source effect containment,
  full-assembly non-overlap and service bounds, database topology, 1,212 static
  socket-route samples. Six real economy cases: functioning, missing biomass,
  missing data, full habitats, missing power and suspended. Non-power shortages
  stay lit while machinery stops. Fixture resets resources/population only in
  its own isolated scene, not player data.
- clone-station-v1: 404 production walker neighbor samples, four rotated Nursery
  connections, shared-wall visibility, motion comparisons and mixed 40-room fit.
- clone-depth-v1: 32 native front/behind poses using production actor crop/scale
  through the actual registered renderer. All poses are standable. Vessel front/
  behind was visually inspected; the remaining captures are available for review,
  not an automated pixel-occlusion certificate.
- Existing synergy, discovery, polish and run-balance suites passed in clone-*
  logs. All these logs were scanned: no ERROR or SCRIPT ERROR entries.
- Card and native viewport/state/neighbor images inspected; four-rotation
  comparison at output/clone-four-rotations-v1.png preserves native crop pixels.

Remaining gates: owner aesthetic approval, normal playable release acceptance, dynamic
clone contents/emergence and other neighbor
families. Inherited raw-PNG export warnings remain. No flooding or new controller.

Workflow additions: visual fixture saves now include process ID to prevent
simultaneous sessions overwriting/removing each other's saves. Reusable
tools/capture_registered_room_poses.gd takes --view and --output and does not
access saves. tools/review_cryo_rotations.py now accepts --source / --output for
other registered rooms and refuses to overwrite review evidence.

Contrast-edge follow-up:

- The full forty-prop review is in PROP_EDGE_REVIEW.md. Incubator v1 retained
  dark floor around its top arch, left support and lower cabinet corners.
- Tightened only its source outline; footprint, scale, pivot and operating
  anchors remain unchanged. Light-background v2 native diagnostic and card v2
  visually reviewed against source. Station/card/export consumers select v2.
- Fixture assertions exclude three background points and preserve three nearby
  equipment points. `output/clone-state-v3.log` passes four rotations, six actual
  economy cases, all host-state comparisons and 1,212 canonical route samples.
- Native edge/card/state logs contain no ERROR/SCRIPT ERROR entries. PNG remains
  LFS-managed; old source and card remain untouched. Export scope is recorded
  separately in EXPORT_VERIFICATION.md.
- `output/clone-depth-v2` captures 32 standable production-actor poses after the
  contour correction. All four q0–q3 depth sheets visually inspected: actor is
  behind upright props at the rear and drawn in front at the front. The vessel
  fully occludes the rear pose; the incubator leaves only the head visible.
  This closes static pose review, not continuous corner movement or transparency
  simulation. The successful depth log contains no engine errors.
