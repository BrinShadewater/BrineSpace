# Veld owner colour feedback

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner accepted A/front idle and C/rear idle as pretty good. B/D/E/F/G faces too
white; B/E/G equipment needs more silver and fabric should match A. F too bright.

## Accepted decisions and constraints
A is the matching reference. Preserve A/C and all poses, timing and geometry.
Reversible deterministic colour work authorized; no production promotion.

## Current state
character/veld-animation-pilot-v10 adds face luminance percentile matching to A
inside existing face masks. Side cloth uses thigh exposure matching; west now
receives the same measurement. East bright neutral equipment is isolated by a
soft source highlight mask so its silver survives fabric darkening. Locked hue
ramps remain. Masks are conservative colour/region heuristics, not hand-labelled
semantic maps. tools/review_veld_pilot.gd supports v10, paired UID retained.
review-all/all-animations.gif keeps the same A-G labels and frame numbers.

## Verification
A/C twelve frames byte-identical. All 42 alpha masks unchanged. Exact idle/action
joins and frame timings retained. Manifest validator no errors/warnings; 160
native checks pass, 2670 real-profile files unchanged under scratch APPDATA.
Native 148/45px capture reviewed. Owner visual acceptance remains pending.

## Next action
Review v10 A-G overview with owner. Refine any remaining face/material mismatch;
then resume held front/rear walk phase/equipment corrections and edge cleanup.
