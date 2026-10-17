# Project handoff

Updated: October 15, 2026 · Project: Brine Space · Task: Krusher angled-chair removal and turn-face polish

## Objective and acceptance
Remove sitting in angled corner chairs and improve rough faces during turns, preserving the accepted body and neck registration.

## Accepted decisions and constraints
The angled corner armchair library/sp-crew_lounge-4 is decorative for all crew, including copied variants. Ordinary straight seating remains. V12 supersedes V11 as the current art candidate; normal roster integration and owner visual acceptance remain separate. No game repository commit or playable export.

## Current state
scripts/crew_room_activity.gd excludes the corner seat. tests/test_marsh_rest_polish.gd reflects all-crew exclusion; targeted test_chairs.gd plus UID/runner lives here. character/krusher-animation-package-v12 holds the complete portable candidate. Face generation provenance, extraction, masks, comparison sheets and deterministic rebuild scripts live here. Old activity review now links to this current index.html; earlier recordings remain historical evidence. Existing private Site updated with Previous/Revised playback; remote-preview.json records publication.

## Verification
20 chair checks pass; normal seating retained for all four profiles. V12 has 586 states / 8,058 holds / 3,486 indexed PNGs. 35 drawings affect 54 states / 144 holds. Independent validator checks exact timing, pivots, dimensions, alpha, outside-face pixels and hashes. All 3,486 lossless WebP exports decode identically. Native production movement/renderer trials: 72 carrying/swimming turns, all 552 turn holds, 11,103 checks / zero failures and 2,268 captures. All 12 native detail sheets and 35 source before/after drawings inspected. The owner's 2,947 fingerprinted non-log files remain unchanged in both runners. Browser checked both revision modes, continuous turn context and both gear modes. No new head/neck separation observed in reviewed frames. Underwater faces remain dark under actual water lighting.

## Next action
Owner visual review of revised turn faces in the updated private gallery. Further animation work should use V12, retaining current collar/helmet geometry. Previous V11 no-defect review is superseded by the owner's rough-face correction. No fresh complete roster/gameplay acceptance is claimed.

Final private preview published successfully: source 0e38bdc9a16d1633740bcdaf87ce31df0f018afb. Browser confirmed final revision options and continuous turns. Initial comparison binding collision was corrected before final publication; gallery validation passes 659 checks.
