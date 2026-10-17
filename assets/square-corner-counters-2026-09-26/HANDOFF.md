# Project handoff

Updated: 2026-09-26 · Project: Brine Space · Task: square-room corner counters

## Objective and acceptance
Owner corrected diagonal corner concept: counters must fit square rooms. Three replacement L-counter candidates generated: utility, reading/storage and refreshments. Owner review pending.

## Accepted decisions and constraints
Square room axes govern footprint; diagonal lounge facing does not apply. Horizontal back run and approximately vertical left return, open lower-right inner corner, elevated visible worktops and shallow front faces. Original props untouched.

## Current state
Transparent masters and calibrated game-size exports here with production.json, sources.json, manifest.json, reproducible build_exports.py and light/dark sheets. Built-in image_gen used. Earlier assets/corner-counters-2026-09-26/production.json describes superseded diagonal attempts; those are not current deliverables.

## Verification
Native light/dark review confirms recognisable square-aligned L silhouettes rather than diagonal diamonds, intact inner cutout and readable accessories. Generated left outer edges retain slight perspective taper; exact flush pixel contact with room walls is not verified. Reading variant rendered gray rather than the requested wood, with two plants; record actual result rather than asserting prompt compliance. All three RGBA exports have transparent margins and full alpha range. Density convention is 0.34 world units per source pixel. No live placement, collision or wall-contact test performed. No runtime/layout changes.

## Next action
Follow-up audit found low character-relative proportions and unresolved inner-return depth as well as the known taper. AUDIT.md and crew-doorway-study.png record the static crew/entry comparison. All proposed bounds clear conservative doorway lanes, but north clearance is only 8.8–10.1 world units; do not enlarge uniformly to fix proportions. No runtime clearance claim.

Owner review of revised square-room direction. Before integration, compare against actual room wall geometry and correct taper/anchors where necessary for exact flush contact.
