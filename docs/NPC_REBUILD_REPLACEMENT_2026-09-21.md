# Superseded NPC navigation rebuild

Updated: September 21, 2026. Project: BrineSpace.

## Objective and acceptance
Fix the navigation error exposed by the paid station animation review without
changing room geometry, owner furnishing, actor needs or normal resource rules.
The broader animation/room/performance objective remains unfinished.

## Accepted decisions and constraints
Preserve existing changes and owner data. No Higgsfield, publication or new export.
Accelerated setup reproduction does not prove a normal player trigger.

## Current state
scripts/bill_npc.gd assigns each rebuild a revision. All four staged yield points
check that the station still exists, the actor is alive and the build still owns
the graph. Superseded work returns before touching replacement dictionaries or
clearing the newer in-progress flag. Existing navigation geometry is unchanged.
Added tests/test_npc_rebuild_replacement.gd and its UID; registered under crew in
tests/index.json. Updated maintained and installed character godot-integration
reference with the interleaving lesson. No visual-bible change was needed.

## Verification
Focused regression failed before the fix with the same missing-room-key engine
error, then passed: a staged build yielded, a synchronous replacement added a room,
and resumed old work left the replacement graph/signature intact without errors.
The final regression uses populated walkable graphs and compares point IDs and
connections as well as geometry/signature.
Logs: output/npc-rebuild-replacement-{before,after}.log.
Existing segment-clearance regression passed. Native staged Save/Continue test
passed with zero failures, including graph/state parity and loading guards;
timing from this concurrent run is not a performance claim.
Original paid-station probe reran without the engine error but did not capture a
maintenance sequence within its observation window (complete=false, no captures).
A follow-up trace shows Bill active, recovered and walking toward hunger service,
initially running and unpaused, then paused by frame 150 with frozen needs/foot.
The observation window was therefore not 180 seconds of advancing simulation.
The fixture now minimizes queued crew dialogue through its existing UI method;
the corrected run completed an autonomous east kneel/repair/stand/departure
sequence with 71 captures and no logged engine error. However, inspection showed
the work room below the viewport, so this is behavior evidence only. The camera-follow
recapture in output/bill-paid-station-visible-2026-09-21 completed successfully: 71
captures of an autonomous north-facing Life Support tank maintenance sequence,
including kneel, repair, stand and departure. Full viewport and eight native-scale
pose samples were inspected; the fixed foot coordinate and tank contact remain
consistent. A 100 ms-per-frame room crop GIF is available as bill-life-support.gif.
This is a controlled paid fixture with manual 30 Hz simulation and dialogue
minimization, not human expedition acceptance or startup-camera validation.
Evidence: output/bill-paid-station-review-2026-09-21 and
output/staged-restore-after-rebuild-fix.log.

## Inactive/dead restore follow-up
A restore that deliberately clears navigation must also invalidate pending warm-up
work. The extended regression reproduced 529 points returning after an inactive
restore and a stuck building flag after a dead restore. Both yielded interleavings
now pass after the inactive/dead branch advances the build revision and clears the
flag. A new NPC shares the static room cache, so each cold-build test case clears
that cache and explicitly requires a yield; otherwise it tests synchronous work.
Logs: output/npc-dormant-rebuild-{before,after}.log. Native staged Save/Continue
rerun passed with zero failures: output/staged-restore-after-dormant-fix.log.
No navigation geometry, resource rules, saved-file schema or artwork changed.

## Next action
Continue broader station motion/composition and ordinary expedition review.
The captured north service sequence does not certify every direction/equipment state. Both brinespace-7d3072b5bf3f53a0 packages predate
this source fix. Native Apple Silicon and owner motion/composition acceptance
remain open; batch the next export after a meaningful polish checkpoint.
