# Marsh short-step integration

Updated: September 13, 2026. Project: Brine Space.

## Objective and acceptance
Polish crew motion and remove the abrupt truncated-start return to idle for supported short repositioning routes. Broader animation polish remains unfinished.

## Accepted decisions and constraints
Marsh remains a blond male android with a right-temple implant and no helmet. Bill is unchanged. The authored east step is used only for horizontal dry final routes of 3.5-4.5 world units with empty goal/stage. Other tiny distances and directions are still open.

## Current state
- `scripts/marsh_ground_motion.gd` now includes the reviewed short-step logic alongside start/stop, avoiding a separate controller layer. `scripts/marsh_npc.gd` validates the optional short-step checkpoint fields.
- `character/marsh-v2/supplemental/ground-east` now contains three states and 15 frames. Short step has seven 120-ms frames, 256-square canvas, pivot 128/224, density 148, nonlooping. Explicit source root displacement is removed from the poses and reapplied through the movement curve.
- `tools/build_marsh_ground_transitions.py` preserves this selection during rebuild. `tools/crew-art-source-contracts/marsh-supplemental.json` records exact selected PNG hashes and timing. Original source contracts remain unchanged.
- `tests/playtest_marsh_walk.gd` probes now exercise production short-step behavior; legacy trial aliases remain for historical commands. `tests/test_marsh_battery.gd` checks full disk Continue during travel and settling as well as existing start/stop and battery behavior.
- Ledger contains 811 selected clips; this is inventory, not a replacement count. Bible, current status and asset workflow guidance updated.

## Verification
- All short-step/start/stop/snapshot unit suites pass: `output/crew-replacement-2026-09-12/marsh/short-step-production-*-unit.log`.
- Production 30fps native route: `short-step-production-native.log`, PASS, 104 frames. Travelling and settling actor restores and native boundary contacts reviewed in `live-idle-transition-east-step-snapshot-01-production-01-fps-30-route-4`.
- Full disk write/read and staged Continue, selected texture/clock/position/timer equality, pause/resume and battery regression pass: `output/test-runs/20260913-010317-headless`, 116 recharge-route samples. Both short-step travel and settling are included.
- Complete-pack check passes 19,346 checks, zero failures in that same run directory.
- Art validation: 143 body states, 691 references, no errors or border touches; 211 original source frames and original manifest unchanged. Clearance finalizer reports 143 states.
- Earlier native range endpoints 3.5/4.5 each passed 104 frames with reviewed foot catch-up and idle joins; see the ground-transition handoff for source/rejection/calibration history.

## Next action
Continue other tiny distances, directional starts/stops and goal-specific arrival transitions. Review 60fps and actual autonomous short-route use. Continue Marsh north/south idle and old actions/run/carry, Veld carry and Branforth older kneel/carry. No export or owner acceptance claimed. No active generation/test job from this milestone.

North idle follow-up: idle-north-video-01 submitted using dedicated start-image binding to north-standing-identity-01.png. Preserve rear facing, right-edge implant, gloves and planted boots with subtle breathing. Provider exact-prompt status confirmed in_progress; active wait session 74476, log idle-north-generation-01.log and durable sources/idle-north-video-01.job.json. Do not duplicate this request. Existing native idle/walk fixture heading map fixed to use UP/DOWN for north/south (previous conditional only supported east/west). Source remains unselected; review, extraction, native/source checks and selection are next.

North idle baseline captured and reviewed: north-idle-baseline-live.log passes 51 samples; live-idle-transition-north/state-transition-00.png shows a noticeably broader/darker old idle silhouette against the new slimmer walk. This is baseline evidence, not acceptance. Candidate native source-check fixture now supports north/south idle flags while preserving east/west. North source generation completed and was downloaded; no active session. Source overview/extraction is next.

North idle video 01 overview reviewed: 97 frames, 24fps, 1248x1664, 871,783 bytes. Maintains rear facing, planted boots and restrained breathing; no walking/turning seen in sampled overview. Proceed to fixed-registration two-pose extraction and selected-walk endpoint comparison. Unselected source; no active generation job.

North idle candidate extracted and contact reviewed: idle-north-cycle-recipe.json uses frames 8/43, original 650/650ms holds, scale 147/1481, position 67/63, 256-square canvas and pivot 128/224. Source bounds match across both poses. Candidate output review/idle-north-video-cycle-01; not yet enabled in rebuilder or runtime. Next: selected north walk comparison, then rebuild and native checks.

North idle selected and live-reviewed; current milestone in HANDOFF_MARSH_NORTH_IDLE_2026-09-13.md supersedes earlier candidate-only status.
