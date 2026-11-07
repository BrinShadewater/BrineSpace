# Veld face highlight correction

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner reports persistent white face splotches in B/D/E/F/G. Correct specifically,
preserving approved geometry, equipment and the separate silver hair streak.

## Accepted decisions and constraints
Deterministic colour correction, no pose or timing changes. A/C unchanged.
Visual acceptance remains pending; runtime selection untouched.

## Current state
character/veld-animation-pilot-v12 corrects two causes in materials.py: pale
highlights missed the warm skin threshold, and skin's final ramp anchor was white.
Larger pale islands adjacent to the face are now included below the hairline;
small islands are excluded to protect eye glints. Side-profile skin ramp ends at
locked warm skin-light, not white. Existing east hair and silver corrections kept.
tools/review_veld_pilot.gd supports v12 with paired UID unchanged.

## Verification
42 alpha masks unchanged; 12 A/C frames byte-identical. Manifest validator clean;
160 native checks pass and 2670 real-profile hashes unchanged under scratch APPDATA.
Inspected enlarged before/after faces in all five affected clips. Cheek/forehead
white patches visibly reduced; source facial geometry unchanged. Eye preservation
uses bounded heuristics and is not a hand-labelled segmentation guarantee.
review-all/all-animations.gif retains A-G labels; face-before-after.png shows crops.

## Next action
Owner review of corrected faces across all frames. Held front/rear walks remain
outside candidate pending phase/equipment correction.
