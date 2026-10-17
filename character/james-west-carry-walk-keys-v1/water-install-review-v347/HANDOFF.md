# Project handoff

Updated: October 3, 2026 · Task: James swimming installation

## Objective and acceptance
Finish James for the next playable release soon; full animation goal incomplete.

## Accepted decisions and constraints
Preserve accepted source art/tools/grade and owner saves. Release focus, no new speculative material trials.

## Current state
### James swimming handoff installed for release closeout — October 3, 2026

V347 installs scripts/james_water_player.gd and james_water_phase_player.gd,
both inheriting the accepted cargo player. Grid uses this player and builds exact
selected-pose finite rows only after all normal bare/helmet overrides load; fresh
scenes therefore have the same banks before checkpoint restoration. No source art,
grade, scale, pivot or selected original clip clocks changed. Concurrent Grid work
preserved. The former staged water repair is now selected in normal gameplay.

New james_water_clearance.gd checks the entire finite clip along the distance the
actor can travel before completion. Flooded checks use actual segment geometry;
exterior checks use conservative swept alpha bounds against existing wreck/hull/
registered prop blockers, without moving the actor to predict clearance. Obstructed
clips use existing immediate locomotion fallback; smooth blocked cancellation is
not claimed. New heading/stop requests at reorientation completion start from the
completed neutral pose and finish the requested heading before rising.

11521candidate checks0 across288rows/2304completion commands, flooded blocking,
open-sea current/future obstruction and read-only prediction. Installed normal
player/Grid native51checks0, two24-unit move() routes and two fresh-scene whole-run
disk restores; no fixture player/Grid replacement. Actor/playback/clock/pause and
resume pixels exact. Ten native crops actually viewed, all LFS; deep flood lighting
limits material review and stills do not certify full continuous motion. Existing
test_branforth_crew PASS, minimum separation32.01; dry actions, checkpoint admission,
crew clocks and legacy saves covered by that existing regression. All runs use
scratch APPDATA and owner files unchanged. ScriptUIDs paired; post-run bindings
saved, no prelaunch freeze. Initial parse-name collision repaired before testing.

Next: final selected animation motion/master consistency, furniture/hazard lifecycle
and ordinary autonomous water/exterior visual review, then fresh playable export
and packaged gameplay/Continue. Stop adding stationary water studies. Full animation
goal remains incomplete. No executable build or publication yet.
Handoff: character/james-west-carry-walk-keys-v1/water-install-review-v347/HANDOFF.md.

## Verification
11521 candidate checks, 51 installed native checks, two fresh-scene disk resumes, existing crew regression PASS; all owner files unchanged. Ten native crops viewed; dim flood lighting and static review limitations retained.

## Next action
Return to selected family motion/master and furniture/hazard lifecycle review. Then build and validate the next playable version. No further stationary water studies.
