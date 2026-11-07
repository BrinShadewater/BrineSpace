# Project handoff

Updated: September26,2026 · BrineSpace · Josh and River polish

## Objective and acceptance
Owner: “Lets also do josh and river,” following Margot's full artwork/animation
integration. Match painted detail, sizing, perspective and motion; preserve identities.

## Accepted decisions and constraints
Josh lavender upper body/neutral twin tracks; River ivory-sage wheeled chassis.
Keep established world sizes, behavior and all existing keys. Independent directional
art, preserved legacy assets, scratch APPDATA for every Godot check. No release build.

## Current state
Owner colour/consistency follow-up selects `josh-weld-v3` and `josh-power-v2`;
previous exports frozen under review/pre-consistency. New audit_consistency.py
records density, source resize factors, ground contact and head-paint diagnostics.
Both robots now register final opaque ground contact after resampling (y172).
No palette reduction or source upscaling. Native action/pause/restore rerun passed;
the entire real profile fingerprint was unchanged.
Final native water rerun also passes with the entire real profile unchanged.
Browser torch/standby chains sampled at32 action/facing/time selections, no errors.

`character/robot-polish-v1` holds sources/prompts, deterministic build/extraction,
validation, old baselines, runtime packs, contact sheets and comparison preview at
http://127.0.0.1:8774/ . Josh76 states/228 refs; River68/211 including water.
184px frames/pivot92,172/standingHeight148, stride0.1. `companion_npc.gd` selects
whole literal manifest paths and River waterline140/derived clearance. Registry,
pipeline notes and current status updated. New `test_robot_polish.gd` plus UID and
crew-group entry. No commit. Concurrent room/door work preserved.

## Verification
Export validation PASS; 80 browser combinations without console errors. Native robot
test PASS after correcting fixture reset; native companion-water PASS; headless
animation-expansion PASS. Native scale/action/water captures visually sampled.
Binding audit validates five robot partitions;12 pre-existing portrait-registry
mismatches remain outside this animation pass (recorded in pack README).
All tests isolated. Final two runs verified entire real profile unchanged; earlier
water wrapper flagged an unrelated new-room test sidecar/log change and left it
untouched. Exact evidence and source omissions/reuse are in the pack README.

## Next action
Owner review in preview/native source game. Especially inspect track readability,
diagonal transitions and Josh's far arm while welding. Pack is installed in source;
release packaging and owner visual acceptance remain pending.
