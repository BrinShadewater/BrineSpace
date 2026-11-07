# Project handoff

Updated: September 26, 2026 - BrineSpace animation polish and latest-source audit

## Objective and acceptance
Owner requested another polish pass and asked whether all latest animations are
used. Audited the September 26 room, companion and drone revisions against live
loaders. Installed the selected BRINE chamber appearance/motion; no new drone
behavior or room balance changes. Agent verification complete; owner review pending.

## Accepted decisions and constraints
BRINE uses the v10 1254-square tube atlas, v7 45x139 figure, 184.8 source-unit body
height, eight-second drift, rigid facial region and no collar lettering. Preserve
room layouts, glass/rim occlusion, power/pause behavior and crew clearance. No
preview scene inheritance or loose overlay nodes in production.

## Current state
rooms/underwater/brine-core/brine_core_view.gd now loads the explicit final source
paths and draws the selected mesh in its existing occupant pass. A CanvasTexture
applies linear sampling only to the body; the machinery keeps its pixel treatment.
New brine_float.gd shares the final drift and cached UV/index arrays. Both retained
and direct render paths retain glass, bubbles and front rim order.

tests/test_brine_room_v2.gd now checks the selected native source density, body-only
filtering, complete loop closure and rigid face, alongside its existing traversal,
offline/pause and native pixel checks. New tools/review_brine_float.gd exports 200
native frames at 25 fps. New scripts have UID pairs. BRINE card and four architecture
captures refreshed; review is assets/animation-polish-2026-09-26/index.html.

Inventory: BRINE, Margot, aquarium, survey probe, department doors and ocean hatch
use their latest selected sets. The construction/ROV 48-clip pack, mining rover
112-clip pack, salvage 92-clip pack and v10 dock launch/recovery study are still
preview-only. The live fleet calls DroneArt.draw_drone using its fleet-v1 atlas.
Existing human crew packs were not replaced. No release executable rebuilt.

## Verification
- BRINE composition: four rotations, 640 walking samples, zero failures.
- Native BRINE room test: four rotations, 16 entrance/return routes, 3,561 movement
  samples; mesh containment, loop/face checks, motion, pause, offline and three
  viewport sizes pass. Updated room and actual retained-game captures inspected.
- Native startup sequence regression passes, including power, pause and restore.
- 200 native motion frames; browser play/pause/scrub and ten inventory rows pass,
  no page errors. This is agent review, not owner animation acceptance.
- Owner room layout and library marks verified against pre-install snapshots.

## Next action
Owner reviews the polished BRINE and inventory. Next integration priority is the
new drone fleet and its docks: native scale, eight-heading/state mapping, mining
wheel continuity, cargo/tool contact, launch/recovery and crew/obstacle clearance.
Keep each drone's controller contract; do not replace the atlas alone and call the
whole motion pack integrated. Preserve concurrent Margot and other artwork work.
