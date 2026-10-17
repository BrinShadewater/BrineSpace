# Project handoff

Updated: October 3, 2026 · Task: James staged water continuity

## Objective and acceptance
Full James animation set matching original masters, followed by consistency/polish. Incomplete.

## Accepted decisions and constraints
Preserve original selected pixels, registration, grade, tools and independent actor physics. Staged only until motion and collision evidence passes.

## Current state
### James staged all-phase swimming stop and restart — October 3, 2026

V340 staged James-only player reuses exact selected swim/stop textures and metadata.
Finite phase-specific stop prefixes, reverse restart rows and re-stop rows preserve
current poses. No generated art, grading, scale changes or normal loader edits.
Initial interruption trial2017checks/56failures identified floating point slot
boundary selection. Restart phase now enters just inside the intended slot;
transition movement is consumed once rather than replayed as gait distance.
Final isolated runs:290entry checks0 across48all-phase/cardinal/both-gear cases;
2289interruption checks0 across272bridge samples including pause, independent fresh
player restore, restart, re-stop, completion and moving restart entry. Owner profile
unchanged. Two bare/helmet entry boards actually viewed; all48entry pairs exact.
98LFS images, three paired scriptUIDs. Post-run hashes retained, no prelaunch freeze.

Technical/still evidence does not establish temporal smoothness or game acceptance.
Full derived motion at gameplay scales, direction/equipment changes, actual whole
bridge actor clearance, ordinary NPC interruptions and whole-run Continue remain.
Do not install until those checks pass; existing master material/proportion/cargo
and remaining hazard/death/rest/core consistency work remains. Full goal incomplete.
Handoff: character/james-west-carry-walk-keys-v1/water-stop-bridge-v340/HANDOFF.md.

## Verification
290entry/2289interruption checks0;48entry/272interruption scenarios; two entry boards viewed;98LFS PNGs; scratch profiles unchanged. Prior56failures corrected.

## Next action
Review complete derived playback at148/82/54/27, test facing/gear changes, then integrate full-bridge clearance through actual renderer/NPC route and verify whole-run Continue. Continue remaining families and master polish.
