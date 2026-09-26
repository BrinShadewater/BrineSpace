# Studio owner decoration fixes

Updated: September 23, 2026 · Project: BrineSpace · Task: owner room editing fixes

## Objective and acceptance
Preserve all rotations of the 19 finished rooms listed in CURRENT_STATUS and every
other room's first rotation. Clear other furnishing rotations, support stacking,
and correct the reported selection, wall, floor, bench and preview issues.

## Accepted decisions and constraints
The bench request specifically means the coiled cable underneath it. Preserve
source art, owner library marks and authored defaults. No commit, push or package.
Native agent review does not replace owner visual acceptance.

## Current state
- Backed up owner layouts/recovery and applied 84 explicit empty furnishing
  rotations across 28 unfinished rooms. Four Listening Post rotations also gain
  floor-plug deletion records; all other 100 stored entries are unchanged.
- Studio has visible Move to front/back with undo, redo and saved depth order.
  Effective floor details register after furniture placement; deleting one also
  suppresses alternative-host resurrection.
- Mining Drone Bay uses straight shared engineering wall panels. Ordinary riser
  feet overlap the floor edge. Airlock north lockers render at their saved,
  selectable location. Registered masks and a dark backing remove the bench coil
  while retaining the bag/boots and original PNG.
- Walking-preview navigation rebuilds pause during dragging/resizing and resume
  on release. Refreshed 44 room cards, retaining backups of the previous cards.
- Changed production files: scripts/room_layout_editor.gd;
  rooms/floor-profiles-v1/details.gd; rooms/whole-room/{north_wall,room_dressing}.gd;
  rooms/production-ten/mining_drone_bay_view.gd;
  rooms/underwater/airlock-v1/{airlock_view.gd,composition.json}.
  Added tests/test_studio_owner_regressions.gd and its UID/catalogue entry.

## Verification
Evidence and backups: output/studio-owner-2026-09-23. Applied receipt and card
manifest record hashes; original owner layout and recovery copies remain there.
Candidate reload validates all 84 empty rotations. Native actual-owner captures
confirm cleared Construction Bay/Reactor rotations; first-rotation data was
compared unchanged. Native before/after room captures and bench close-up reviewed;
principal Mining Bay, Heat Recovery and Airlock cards reviewed.

New targeted regressions pass (stacking/persistence, floor-detail selection and
deletion/undo, fallback hosts, drag preview deferral, locker hit bounds, bench mask).
Native room-layout-editor and layout-performance-guards pass. Airlock suite passes
1,191 travel samples plus equipment, power, pause and save/UI checks.

The submitted 22:32:06 report contained 34 identical missing floor-detail position
errors, addressed by registration. Its end window was about 165 FPS; earlier
retained hitches reached 3.6 seconds. A 60-update Construction Bay drag probe
reduced preview CPU from 6.457 ms mean (9.968 max) to 0.014 ms (0.024 max).
This is a bounded drag improvement, not proof that all long-session hitches are
resolved. No sustained full-session performance acceptance is claimed.

## Next action
Owner reviews the corrected rooms and stacking controls after reopening Studio.
Continue investigating long-session hitches if they recur, using a fresh report;
the currently measured drag path and the reproduced floor-selection error pass.
Earlier procedural scenery/pacing and animation owner-review items remain open.
