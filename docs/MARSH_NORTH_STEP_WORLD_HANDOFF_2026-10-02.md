# Project handoff

Updated: October 2, 2026 · Project: BrineSpace · Task: Marsh North short-step world study

## Objective and acceptance
Finish the full Marsh set against original masters, then full cross-family polish.
This unselected motion milestone does not complete the goal or admit the candidate.

## Accepted decisions and constraints
Whole authored source figures, common184canvas/p92,172/H148, no new scaling/grade.
Preserve exact selected idle entrance/exit. Continuous collision-aware navigation
and within-hold whole-sprite translation can keep a planted foot fixed without
warping anatomy or modifying pixel art. No changes to normal gameplay/selection.

## Current state
`character/marsh-north-step-v1/sequence-v1` assembles04anticipation/travel,
08grounded-forward landing and09transfer/closure, then selected idle. Seven120ms
holds. Explicit whole-source integer registration records all hashes;13dense
pixels/5.734world-unit nominal step. Arm envelope59px is retained for motion review;
body/master scale remains unchanged.
Staged `step_controller.gd` + UID owns a bounded5–7unit straight bare empty-goal
route and finite840ms source clock. Root advances7/13distance during.48–.60 and
6/13during.60–.72. Within-hold draw offset cancels root movement; navigation stays
continuous. It matches the real elapsed player's binary subtraction at boundaries,
respects blocked movement and normal priority/gear exclusions. Exact root cleanup
is permitted only within the base approximate-arrival tolerance; it cannot snap
through a newly blocked path. StudyMain's position override remains fixture-only.

## Verification
Current staged controller1449checks/0failures over eight dt partitions/four
lengths, binary boundaries, pause, eligibility and dynamic obstruction.
Current native781checks/32captures/0failures,engine0: real default corridor graph,
actual normal movement primitive/grid source selection, four prescribed5/5.734/6/7
unit empty-goal routes,20ms updates, peers/world paused. Normal costs/failure flags
retained. Exact target/finite arrival/pause pass. Nominal left sole depth stays
fixed between landing/transfer/closing; other lengths drift up to.682world units.
All32native holds reviewed;32lossless APNG/native presentation pairs pass.
All2931owner non-log files unchanged in failed, first-green and final intervals.
First camera-helper script error and earlier781green controller revision retained.
Review: `character/marsh-north-step-v1/world-review-v1/index.html`.
Shared renderer changed after an earlier green run; publisher refused to bind
that old run to new content. Final native plus controller interval freezes24targeted
inputs before/after and at publication; no recursive dependency freeze.

## Next action
First distinguish fresh-route arming from an ongoing gait whose last waypoint
shrinks to5–7units: idle-entry step must not restart in the middle of a walk.
The current world fixture proves idle starts only. Extend ordinary/nonempty service goals and cancellation, preserving emergency and
traffic precedence; validate actual physical interruption contexts and snapshots.
Candidate has no persisted North-step fields yet: ordinary disk/title Continue
cannot preserve it. Integrate fields/controller/contact presentation and manifest
into normal Marsh only after these gates and source/motion seams pass. Then prove
real disk/title Continue and legacy checkpoints independently. Full lateral/range
contact and transfer-arm/weight timing remain polish concerns; prescribed isolated
routes do not establish natural chooser/traffic. Continue other North routes,
Southstart/stop/step, cargo/water families and full consistency/polish.
Normal catalog stays211states/1093slots; full goal active/incomplete.
