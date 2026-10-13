# Veld left-facing animation handoff

Updated: 2026-09-27. Project: Brine Space.

## Objective and acceptance
Expand missing directions without mirroring asymmetric equipment or changing the
established face, density and palette treatment.

## Accepted decisions and constraints
Locked turnaround supplies left-side scanner/right-side canister ownership.
Owner remains on mobile; continue local work without requiring preview feedback.
Candidate generation is not production selection or owner visual acceptance.

## Current state
character/veld-animation-pilot-v7 adds idle-west and walk-west: 36 frames/six clips.
The preceding 24 frames are unchanged. Colour masks handle left-facing head geometry.
Left gait has its own measured 0.15904365904365905-cell stride; east remains unchanged.
Added coverage.json against current body/equipment catalog. Native tool supports v7
and separately exercises leftward distance phase; existing paired UID preserved.

## Verification
Geometry/alpha validator passes. Native player: 148 checks pass. All 2670 real-profile
hashes unchanged under isolated APPDATA. Source sheet, final contact sheet, left mask
and native captures inspected. Two flat-foot segments improve from 5.27px residual
to zero at measured boundaries (+/-1px landmark uncertainty); rolling contacts and
held-frame sliding are not certified. Scanner visible/canisters far side reviewed.

## Next action
Rear idle and front/rear walk coverage, then corresponding helmet states and remaining
actions. Carry forward material-mask caveats and inspect native station behavior
before promotion. No runtime replacement, export or commit in this pass.
