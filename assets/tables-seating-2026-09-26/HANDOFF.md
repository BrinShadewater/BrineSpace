# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: small surfaces and dining seating

## Objective and acceptance
Four candidates complete: small wooden side table, small utility table with lower shelf, kitchen table with four chairs, and opposing-bench dining booth. Owner review pending.

## Accepted decisions and constraints
Use accepted painted furniture materials and overhead/cutaway view. Neutral matte upholstery, wood and charcoal metal. Preserve clear seat surfaces and avoid the undersized chairs seen in the earlier compact dining assembly.

## Current state
Four transparent masters and four calibrated game-size exports saved here, alongside production.json with exact built-in image_gen prompts, sources.json, manifest.json, repeatable build_exports.py and light/dark review sheets. Original existing assets unchanged.

## Verification
Four RGBA exports have alpha range 0–255 and transparent margins. Native light/dark review complete: full silhouettes, visible seat tops, separate chair/table gaps and coherent matte furniture materials. Dining sets receive substantially larger export footprints than small surfaces; sizes remain proposals at 0.34 world units per pixel. Side-facing seats look plausible but character fit, seated occlusion and navigation remain untested. These are combined assemblies, not separate animated seating layers. No runtime or layout changes.

## Next action
Owner visual review, then character sitting and access checks before integration. Preserve masters for any later component separation.
