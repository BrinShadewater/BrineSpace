# Project handoff

Updated: September 21, 2026 · Project: BrineSpace · Task: Galley live review

## Objective and acceptance
Natural room furnishing must also put crew interactions at the visible furniture.
Continue broader room, animation and performance work; this is one service repair.

## Accepted decisions and constraints
Preserve owner layouts and library marks. No Higgsfield or blanket upscaling.
Saved Galley furnishing differs from defaults; shipping reconciliation remains open.

## Current state
Native live captures confirm both added serving counters remain visible. Review
found crew still using retired fixed meal coordinates on empty floor.
`scripts/crew_room_activity.gd` now derives nearby clear service nodes from the
effective rectangles of `tileset-mms-58` and `tileset-mms-60`, including copies.
Bought counters keep their visual facing when the room rotates. Where their front
is inaccessible in the crew service band, an accessible rear approach is used.
Legacy layouts without these counters retain the earlier service contract.

Added `tests/test_galley_counter_stations.gd` and UID to the crew test group;
updated CURRENT_STATUS.md. Owner saved-layout bytes are unchanged.

## Verification
Focused rotation/movement/copy/collision/rear-access/legacy checks pass. Actual
saved-layout probes show nearby counter-linked stations in all four rotations.
A headless gameplay fixture has Bill choose hunger, walk from the core through
92 clear steps, reach the first serving counter and enter his meal activity facing
north. This proves that journey, not every crew/layout combination or visual motion.
Native room art was inspected separately at 52% UI zoom.

Evidence: `output/galley-live-review-2026-09-21/`, including service-before/after,
counter-test and meal-trip logs, owner snapshot and native captures.

## Next action
Review other furniture-bound interactions against bought layouts. Continue Bill's
individual joint repair and stable-build work. Do not treat a walkable old activity
coordinate as proof that crew reach the new furniture.
