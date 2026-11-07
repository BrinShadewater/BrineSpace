# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: complete riser wall decorations

## Objective and acceptance
Complete the remaining 42 integrated wall designs in the existing riser preview, following the accepted five-room direction. Generation and preview validation complete; new artwork awaits owner visual acceptance.

## Accepted decisions and constraints
Keep host-wall materials, perspective and panel fit. Built-in bookshelves remain in observation/archive rooms. Connected north centres stay clear for doors; ocean exposure replaces decorations with windows. Preview-only; production decorations remain paused. Original masters and owner layouts preserved.

## Current state
`assets/room-risers-v4/integrated-v1/`: 47 masters, exact prompts, registrations, reference/source hashes, 42-room subject list, alpha/bounds audit, previous native comparisons and six review sheets. `review-gallery.html` now displays all 47 and matches corridor dimensions. `tools/preview_riser_variations.gd` applies integrated slices to corridor studies too, reports actual face height and captures without guides. `tools/register_integrated_risers.py` reproduces registration. No commit or export made.

## Verification
Scratch-APPDATA native session `8fcd9dca4870441287d0226a92dda121` passed: 47 designs / 185 captures / 44 walking checks / 0 clearance failures; owner-save fingerprints unchanged. Visually reviewed all 44 furnished closed/ocean pairs, three corridor segments and connected medical doorway. Browser 47/47, search, artwork comparison, ocean controls and native modal checked. All 47 registrations pass completeness, bounds, unique source and alpha checks; LFS attribute confirmed. Gallery screenshot in `integrated-v1/review/gallery-proof.png`.

## Next action
Owner reviews http://127.0.0.1:8796/assets/room-risers-v4/review-gallery.html. Revise named art if requested; production renderer adoption has not been performed. Preserve concurrent drone/core-art work.

## Polish continuation — September 26
Owner requested BRINE screen banks/permanent north door and smaller handheld objects. Three revised sources and four exact generation prompts are preserved in integrated-v1/polish-v2; selected listening source ends in -final. Override registrations keep previous art intact. Gallery/native renderer enforce BRINE north-door exception. Full47-room session d487e6041f734a768eb86083027f9fac and final listening session2d423b16d5554f869eaef8c2603cf8d7 passed with unchanged saves. All44 furnished pairs reviewed for style, scale and perspective; native revised sources reviewed and browser checked. Next: owner visual review; production integration remains separate.

## Shape and helmet continuation — September 26
Accepted constraint: corridor/corner/tee risers follow the canonical narrow straight/L/T footprint, never a square-room template. Changed preview_riser_room.gd segment draw dispatch, preview_riser_variations.gd actual hull/module rendering and four rotation captures, gallery shape cards/rotation controls, registration builder shape-helmet-v3 override. Generated airlock helmet edit references Bill's selected helmet, with original and prompt retained. Full session4da8b2828fce4a7ba541f0c651be505d passed; 12 rotations and airlock visually reviewed; saves unchanged. See shape-helmet-v3/README.md. Next action: owner reviews shaped risers and helmets; production remains untouched.
## Painted wall caps — September 26, 2026

Owner clarified the requested redesign concerns wall top edges/caps. The preview
now uses each riser's registered painted cap artwork around all four room edges,
with 16-unit strips, corner joins and existing doorway gaps. Caps render after
room props so the older wall tops cannot cover them. Gallery strips show the cap.
All 47 native designs passed with zero clearance failures; owner save fingerprint
unchanged. BRINE, observation, reactor and medical room captures visually checked.
Preview-only; production integration remains pending. Evidence and handoff:
`assets/room-risers-v4/integrated-v1/cap-review/README.md`.


## Four-wall polish follow-up � September 26, 2026

Reviewed all 44 furnished rooms on six native-scale four-edge sheets and all
12 rotations of the three corridor shapes. Corrected inward trim orientation on
east/south caps and flipped south corner UVs. Aligned horizontal tops to the
native -3-unit offset, removing the old top-edge sliver. Materials and source
masters retained: the painted steel and room accents match the current risers.
Full-room cap density is 3.6875�4.25 source pixels/world unit; source aspect is
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

## Fitted cap corner pieces - September 26, 2026

Owner requested more seamless corner pieces. Replaced rounded beam-end crops with
16-unit textured mitres: two triangles continue the horizontal and vertical
bevels into one inner corner. Mirrored placement covers all four full-room corners.
Samples come from each room's existing cap at the straight strip's pixel density;
no new raster masters or changes to footprints, door gaps or layering. Dedicated
corridor geometry remains unchanged. Changed tools/preview_riser_variations.gd;
gallery and cap-review cache tags refreshed. Observation and BRINE previews
visually checked. Preview-only; next step owner visual review.
