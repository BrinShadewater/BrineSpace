# Painted wall cap handoff

Updated: September 26, 2026 Â· Project: BrineSpace Â· Task: wall top edges/caps

## Objective and acceptance
Match the caps to the existing painted industrial risers. Owner clarified caps,
not the first four rooms. Ready for visual review in the existing gallery.

## Accepted decisions and constraints
Preserve wall height, room footprint and door gaps. Reuse authored cap artwork
and registrations; no raster masters changed. Preview-only.

## Current state
Changed tools/preview_riser_room.gd, tools/preview_riser_variations.gd and
assets/room-risers-v4/review-gallery.html. All four full-room edges now use painted
16-unit caps, with corner blocks and existing door cutouts. Horizontal strips
crop the source proportionally; vertical strips rotate the same material.
Render after the room's props pass to cover the former caps. Corridors retain
canonical shape-specific authored-cap rendering. Gallery shows cap above face.
Evidence: gallery.png and brine-core.png alongside this file.

## Verification
Native all-47 verification passed: zero clearance failures, including 12 corridor
rotation captures. Session: output/riser-room-preview/session-80fb8f3d85bd4ca9a6787159c66c6178.
Stderr empty; owner save fingerprint unchanged. Visually checked full room caps
for BRINE, observation, reactor and medical rooms plus the browser gallery.
Scoped git diff whitespace check passed.

## Next action
Owner visual review; production integration remains outside this preview change.

## Four-wall polish follow-up — September 26, 2026

Reviewed all 44 furnished rooms on six native-scale four-edge sheets and all
12 rotations of the three corridor shapes. Corrected inward trim orientation on
east/south caps and flipped south corner UVs. Aligned horizontal tops to the
native -3-unit offset, removing the old top-edge sliver. Materials and source
masters retained: the painted steel and room accents match the current risers.
Full-room cap density is 3.6875–4.25 source pixels/world unit; source aspect is
preserved. Narrow corridor tops now opt into proportional cropped/repeated UVs,
rather than squeezing entire source strips. Their canonical depths are retained.
The opt-in is only set by the preview; production registrations are unchanged.

Changed: tools/preview_riser_variations.gd, rooms/underwater/corridor_wall_art.gd,
review-gallery.html, and cap-review evidence/index/density-audit.json.
Native full-47 pass: session-3b4f6f7eb35a41209c18b025b518dba0, zero clearance failures.
After corridor sampling change, all four rotations retested per family:
session-8436816fdcf24735bbd2e67a051a9119 (straight),
session-ac5a690b16754160b35cd41dca68e266 (corner),
session-e9cc7af6695f4c858264b005ab340594 (tee).
All session paths are under output/riser-room-preview. Save fingerprints unchanged.
Visual evidence: edges-1.png through edges-6.png, corridor-caps.png; audit-before
sheets preserve the preceding context review. Preview-only; next step owner review.

## Cap overlap correction - September 26, 2026

Owner identified caps overlapping other elements. Confirmed the preview drew caps
last, over props and crew. Replaced that with the existing shell/content passes:
legacy shell, replacement riser/caps, north door, then props/crew. Shell pass is
restored afterward. Old/new comparison and corridor path remain intact.
Changed tools/preview_riser_room.gd; refreshed cap review captures and page.
BRINE pilot passed and visually confirms the south cabinet base is no longer cut
off. Medical room checked too. Pale legacy doorway-end blocks remain a material
mismatch for a later door/jamb finish pass; this change does not repaint them.
Full 47-room native validation passed, zero clearance failures; owner save fingerprint unchanged. Session: output/riser-room-preview/session-36d8ed66910e43f8aef6811417729c9a. Six four-edge review sheets refreshed.

## Matched doorway-end blocks - September 26, 2026

Completed the remaining reported cap/jamb finish mismatch in the preview. Side
and south jambs use the room's existing cap artwork, sampled without stretching,
at canonical Geometry.jamb_rects positions and the native -3-unit top offset.
North raised-door frames remain owned by the door renderer. Door aperture,
footprints and furniture/crew-over-wall layering are preserved. No source repaint.
Changed tools/preview_riser_variations.gd and gallery/review pages; refreshed six
four-edge sheets and BRINE evidence. BRINE, medical and observation native previews
visually checked. Full 47-design native verification passed, zero clearance
failures and empty stderr; owner save fingerprint unchanged. Session:
output/riser-room-preview/session-01a4ebeccb614272a95a9d5f4ed9b256.
Preview-only. Next action: owner visual review of cap-review/index.html.

## Duplicate corner shell removed - September 26, 2026

Owner still saw wall fragments at the outer corners. The revised preview was
painting the legacy shell underneath the replacement cap pass; its old corner
bevels and shadows extended beyond the new silhouette. Removed that legacy shell
pass and the legacy draw_wall/draw_cap calls inside draw_riser. Revised preview
now draws only its own caps/returns/jambs, followed by props and crew. Old-wall
comparison and dedicated corridor rendering remain available.
Changed tools/preview_riser_room.gd and tools/preview_riser_variations.gd; refreshed
gallery cache tags and cap-review evidence. Observation pilot passed; observation,
BRINE and medical native corners visually checked. Production is unchanged.
Corner correction verification: all 47 designs passed, zero clearance failures, empty stderr, owner saves unchanged. Session: output/riser-room-preview/session-f9cf63a213494ffd8c1baa5d89147d03. Six review sheets regenerated. Next: owner visual review.

## Fitted cap corner pieces - September 26, 2026

Owner requested more seamless corner pieces. Replaced rounded beam-end crops with
16-unit textured mitres: two triangles continue the horizontal and vertical
bevels into one inner corner. Mirrored placement covers all four full-room corners.
Samples come from each room's existing cap at the straight strip's pixel density;
no new raster masters or changes to footprints, door gaps or layering. Dedicated
corridor geometry remains unchanged. Changed tools/preview_riser_variations.gd;
gallery and cap-review cache tags refreshed. Observation and BRINE previews
visually checked. Preview-only; next step owner visual review.
Mitre verification: all 47 designs passed; zero clearance failures, empty stderr and unchanged owner save fingerprint. Session: output/riser-room-preview/session-5d2d6a48b41a42bab2fcac3e1ab14b92. Six native-scale four-edge sheets refreshed.
