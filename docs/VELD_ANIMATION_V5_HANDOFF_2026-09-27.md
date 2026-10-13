# Veld scanner continuity handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Owner is on mobile and asked to continue animation work without preview access.
Match the scanner action to the new right-facing idle and remove transition drift.

## Accepted decisions and constraints
Locked character design and palettes still apply. User-authorized reversible
candidate work continues; no extra approval requested. Mobile localhost preview
access is not a blocker and no external hosting was created.

## Current state
`character/veld-animation-pilot-v5/`: revised side-facing scanner source, exact shared
idle endpoints, 480ms reading hold (1340ms action), single handheld scanner and empty
holster during inspection. Four clips / 24 frames. Eighteen unaffected frames are
byte-identical to v4. Reproducible builders, prompts/rejection, comparisons and native
capture saved. tools/review_veld_pilot.gd supports v5 with its existing paired UID.

## Verification
Geometry/alpha validator: no errors or warnings. Native sprite-player check: 100
passes including exact entry/exit and post-action neutral hold. All 2670 real-profile
hashes unchanged under scratch APPDATA. Native render and frame sheet inspected.
Foot-band bounds move at most 1px; ground row 171 throughout inspection. The longer
native capture exposed a test-reference mistake after walk wrap; frame_at_elapsed
clamps, so looping expectations now explicitly use modulo. No runtime fix was needed.

## Next action
Complete remaining material audit and expand other directions/helmet states. Check
native station occlusion and integration only after representative quality is ready.
No runtime pack selection, game export, commit or owner visual acceptance this pass.
