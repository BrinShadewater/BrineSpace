# Character palette handoff

Updated: September 27, 2026. Project: BrineSpace.

## Objective and acceptance

Standardize each character across animations. Owner explicitly selected deterministic palette remapping with poses preserved. Source integration and agent visual review complete; no new owner visual acceptance or executable rebuild claimed.

## Accepted decisions and constraints

Use existing canonical idle colours and the visual bible. One fixed mapping per character; retain alpha, geometry, timing, pivots and asset selections. Preserve originals. No further generation needed for this pass.

## Current state

`character/palette-standard-v1/` contains seven palettes, frozen originals, staged results, installation mapping, processing tools and a 939-state comparison viewer. Installed 8,575 source PNG paths including equipment and unselected Veld candidates. Rebuilt robot rescue composites; 24 images changed only in robot bounds. Added `tools/review_character_palettes.gd` and paired UID. Pipeline now requires palette postprocessing for future exports.

## Verification

527 native game checks passed. Robot rescue fixture passed. Both isolated runs left the entire real profile unchanged. Preparation checked exact dimensions, alpha, transparent pixels and bounding boxes; post-install hashes and unchanged manifests were verified. Browser/native visual samples reviewed. Helmet fixture failures reproduce on preserved originals: eight distinct poses instead of ten and Branforth removal mismatch; exact idle joins pass. Details in palette README and review JSON.

## Next action

Review the palette viewer if additional colour direction is desired. Future art must use the locked palette postprocess. Broader anatomy/softness cleanup and existing helmet motion issues remain separate work; executable exports still contain their previous art until rebuilt.
