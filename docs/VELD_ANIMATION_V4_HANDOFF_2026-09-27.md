# Veld native playback and right-idle handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Continue Veld's animations through native travel review and fill the missing
right-facing resting pose used alongside the walk and scanner action.

## Accepted decisions and constraints
V4 design lock, v3 material-ramp treatment and reversible candidate workflow remain.
No production sprite selection, commit or game export requested in this pass.

## Current state
`character/veld-animation-pilot-v4/` contains four clips / 24 frames with new
idle-east. Existing three clips are rebuilt unchanged from v3. Comparison includes
native Godot playback at 148px and 45px. New reusable tool `tools/review_veld_pilot.gd`
and paired UID support v3 and v4; per-pilot Python wrappers isolate APPDATA.

## Verification
V3 native: 85 checks pass. V4 native: 97 checks pass; sprite validator zero errors
or warnings. All 2670 real-profile file hashes unchanged after each probe. Native
captures and contact sheet inspected. Flat-foot sole-edge residuals +1.73/-1.27px
at source scale support retaining the inherited stride; uncertainty +/-1px, only
two flat-foot segments measured. Exact-boundary preliminary test failures were
6ns/sub-ns float differences, resolved by sampling inside frames; no runtime edit.

## Next action
Finish material audit and inspection orientation/transition joins, then expand
remaining directions and helmet clips. Full station/occlusion integration remains
separate from this native sprite-player check. Owner visual acceptance is pending.
