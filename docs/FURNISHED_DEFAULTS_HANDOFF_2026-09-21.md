# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Furnished defaults and nearby service

## Objective and acceptance
Ship the reviewed furnishing consistently for fresh profiles and ensure crew use it.
The broader art, Bill animation, polish and release goal remains unfinished.

## Accepted decisions and constraints
Preserve named owner reference layouts and Studio marks. No Higgsfield.
Native geometry and agent review do not imply owner visual acceptance.

## Current state
Promoted 12 effective Galley/Isolation Vault/Cold Store rotation entries in
rooms/full-wall-v1/default-layouts.json; other entries and player layouts preserved.
tools/review_room_composition.gd supports candidate --defaults selection.
scripts/bill_npc.gd now applies the 32-unit pacing minimum only to non-station
choices. The previous rule rejected the nearby Cold Store freezer service point
and selected curiosity in the core instead. Collision, occupancy and route guards remain.
Room pipeline gameplay-preview-contract reference updated in maintained/installed copies.

## Verification
Evidence: output/furnished-defaults-2026-09-21/.
Local and empty-user candidate defaults: 12 identical native PNGs, each run 1,920
walking samples, zero failures. Original Cold Store test failed at destination
selection; diagnostic confirmed Bill chose core curiosity beside two freezer stations.
After fix, native test_cold_store exits zero: three crew, completion, save/restore,
frozen time, suspension, paid construction and 612 continuous route samples.
Native test_galley also exits zero after the shared selector change; see
 test-galley-service-fix.log. No release archive was rebuilt.

## Next action
Continue Bill gait repair and targeted room polish with native previews. Retain
owner reference layouts. Refresh release packages only at a stable milestone and
then establish actual Apple Silicon launch/gameplay acceptance.
