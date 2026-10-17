# Project handoff

Updated: October 3, 2026 · Task: James water lifecycle/clearance

## Objective and acceptance
Full James animations matching original masters, then consistency/polish. Incomplete.

## Accepted decisions and constraints
Preserve selected pixels/rulers/grade/tools; keep physical heading/movement independent. Staged source remains unselected.

## Current state
### James staged heading-safe rise and full-bridge clearance — October 3, 2026

V342 staged same exact selected artwork. Initial1153check diagnostic found816
direction changes canceled a still-active stop and jumped upright. Staged player
now completes its finite rise before adopting a new resting heading; actor direction
and physical movement remain independent. Nonmutating preview predicts the exact
clip for clearance, including active rise and helmet bank; no playback time consumed.
Fixture-only Grid subclass passes the predicted whole envelope to actual James
swim_segment_clear on synthetic flooded geometry. Normal renderer remains unchanged.

Final scratch runs:3697clearance/lifecycle checks0,816changed-heading pose matches
and correct terminal facing,272gear changes,32open/intersecting-blocker cases;
290all-phase entry checks0/48cases and2289restart/pause/fresh-restore checks0/272samples
rerun after player changes. Owner profile unchanged. Tested source snapshots and
post-run hashes retained; prelaunch freeze false. Existing V341 pixel chronology
is unchanged, but its older behavioral revision is superseded by these checks.

Not game acceptance: main-scene rendering/ordinary actor routes, exterior geometry,
resuming swimming toward a different heading during the rise, blocked-space
fallback and whole-run Continue remain. Complete temporal review and responsiveness
before normal installation. Full animation coverage/master fidelity and whole-family
polish still incomplete. No generated art, production selection or global crew change.
Handoff: character/james-west-carry-walk-keys-v1/water-clearance-review-v342/HANDOFF.md.

## Verification
3697clearance +290entry +2289interruption checks0;816heading/272gear samples;32synthetic collision cases;owner unchanged. Logs/reports/tested text source snapshots retained here; executable pairedUID sources remain in V340.

## Next action
Check changed-heading swimming restart and blocked-space fallback, then complete full motion/native main-scene/exterior/Continue evidence before normal integration. Continue remaining families and master fidelity/polish.
