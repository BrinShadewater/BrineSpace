# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: southeast/southwest lounge seating

## Objective and acceptance
Four groups complete: loveseat and armchair each facing southeast and southwest, each with a small side table and mug. Owner review pending.

## Accepted decisions and constraints
User explicitly requested diagonal furniture facings. Direction refers to the open front of the seat: southeast toward lower-right, southwest toward lower-left. Preserve elevated camera and visible cushion tops. Muted generic upholstery, wood and charcoal frame, restrained painted detail. No changes to existing furniture facings.

## Current state
masters/ and game-size/ contain four transparent assemblies. production.json contains exact built-in image_gen prompts and accepted sofa reference. sources.json preserves generated-source paths. build_exports.py reproduces exports and native light/dark boards. manifest.json records hashes, dimensions and proposed display widths.

## Verification
Light/dark visual review confirms requested opposing diagonal facings, visible tops and full silhouettes, smaller adjacent tables and matte painted materials. Four RGBA exports with transparent margins and alpha range 0–255. Export sizes fit proposed loveseat 365x260 and armchair 250x225 visible budgets proportionally, at 0.34 world units per pixel. Different independently generated facings have minor construction/placement differences; these are coordinated variants, not exact rotated meshes. Crew fit, seated occlusion and live placement remain untested. Combined assemblies, not separately layered animation assets. No runtime/layout changes.

## Next action
Owner review of review-light.png/review-dark.png; check crew-scale sitting and access before integration.
