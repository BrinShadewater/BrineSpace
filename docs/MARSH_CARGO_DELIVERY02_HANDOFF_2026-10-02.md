# Project handoff

Updated: October 2, 2026 · BrineSpace · Marsh complete cargo routes and arrival

## Objective and acceptance
Complete the full master-matched Marsh animation set and all-family consistency/
polish. Active/incomplete. Cargo sequencing milestone, not full art acceptance.

## Accepted decisions and constraints
Preferred staged family SouthNorth01/EastWest02; normal catalogue unchanged.
Whole figures, own-facing identity, exact endpoints and one neutral scale.
Preserve normal routes, North arrival facing and two-second timer. Scratch APPDATA
and owner fingerprints required. Preserve unrelated/concurrent large script edits.

## Current state
scripts/marsh_npc.gd adds incoming cargo arrival presentation and validated snapshot
field; scripts/grid_canvas.gd renders its turn/unload clock. No raster changes.
Delivery01/02 and arrival-branches01 fixture .gd/.uid pairs and prepare/fingerprint
helpers added, both delivery publishers and delivery02 recorder added.
character/marsh-cargo-held-material-v1/delivery-02-actor-review contains 117 pairs,
16 reviewed boards and scoped assessment. Pipeline/bible/status/skill mirrors updated.

## Verification
Baseline 3298 checks/97 captures identified abrupt West->North arrival. After fix:
3722 checks, 4 completed normal controller routes, 1244 samples, 117 restores+pause,
117 exact source/native pairs visually inspected. All five arrival-turn poses then
four unload poses. Additional seeded East/South/North actual-arrive branches:
1058 checks, 300 samples, 26 restores, compatibility/context validation. All audits
615 bounded inputs stable per interval, 2931 owner files unchanged, 0 errors/failures,
exit 0. No live job. Baseline boards not all reviewed; seeded branches no visual claim.

Independent current normal-catalogue arrival save gate now passes 81 checks:
four full checkpoints/four fresh actual visible Title Continues, exact actor/
player/source/root/derived-clock parity, pause and resumed timer. All eight paired
renders inspected. 615 bounded inputs/2931 owner files stable, 0 failures/errors,
exit 0. No staged art injection. Added arrival_save01 prepare, fixture+.uid,
fingerprint, publish and record tools; arrival-save-01-actor-review holds evidence.

## Next action
Preferred staged family's normal selection/persistence remains pending. Review grounded
arrival pivot (current stationary turn uses walking legs), remaining proportions/
grade/case/contact and helmet context before normal coherent-family admission.
Continue remaining Marsh families and full cross-family consistency/polish.
