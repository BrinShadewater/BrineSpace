# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Moonbay wall-connected bay

Latest correction: [Moonbay pressure handoff](MOONBAY_PRESSURE_HANDOFF_2026-09-30.md) records the permanently flooded bay, cycling airlock, wider 120-unit crew doors, interlocking sea-door tips, grating and warning lights. Its accepted decisions supersede the earlier dimensions and water behavior below.

## Objective and acceptance
Owner liked the wall-connected bay and requested an ocean-facing sub, a bay-wide animated double sea door, and smaller doors at both ends of the attached airlock. Follow-up implemented; owner hands-on acceptance remains open.

## Accepted decisions and constraints
The launch bay meets the ocean hull directly. Its single sea gate spans the full 384-unit clear bay opening with two sliding leaves. One dry airlock joins the bay to the work area through two smaller 72-unit crew doors. The sub faces the ocean gate in every rotation; this owner correction supersedes Moonbay's earlier fixed-south facing. Preserve station entrances, paid building, mission rules and owner Studio layouts.

## Current state
Changed rooms/large-rooms/moonbay.gd: hull-adjacent chamber, shared hull gate, attached airlock, corresponding floors/water/blockers, rotated supporting equipment and accessible east-facing suit locker. scripts/moonbay_missions.gd now boards at the view's matching point. Updated tests/test_large_room_revisions.gd and tests/test_large_room_art.gd; rebaked only assets/large-room-cards/moonbay.png through the maintained native baker. Preserved the pre-existing sub waterline change and unrelated concurrent work.

Follow-up: Moonbay draws its full-width two-leaf gate, with common.gd skipping the old ocean hatch for this view. Both crew connections now use the small painted door and matching blockers. Facing, collision envelope and side boarding point agree. Mission progress drives opening/closing; departure waits for opening, and return reverses into the dock after opening with matching near-dock scale. Door poses derive from existing persisted phase/progress. Added halfway Save/Continue and pause checks to the existing save/revision fixtures.

## Verification
Godot 4.7.2 under scratch APPDATA: Moonbay mission, assignment, save, large-room art, Studio simulations and final rotation/revision checks pass. All four entrances reach boarding, the suit locker is reachable, and sealed bay doors block entry in every rotation. Supporting equipment clears the bay. Native four raised/four low rotations and eight station mission phases captured; all rotations plus idle/flood/launch views inspected. Moonbay card rebaked; diff whitespace check passes. Studio simulation emits shutdown-only resource leak noise after zero failures. Owner fingerprints: 2,924 readable files, zero changes.

Evidence: output/moonbay-layout-20260930/ (logs, runner and fingerprints), output/large-room-review/moonbay-r*.png, output/moonbay-review/ (phase captures).

Follow-up verification: all six focused tests pass; final pause and halfway Save/Continue checks also pass. 52 native phase/rotation captures show closed, half-open, open, closing, crew sealing and return states; contact sheet inspected alongside individual native frames. Four raised/four low rotations and eight station phases refreshed, Moonbay card rebaked. Evidence: output/moonbay-doors-20260930/{final,timing,native}/ and door-motion-contact.png. All fingerprint intervals retain the same 2,924 owner files without changes. Initial parse failure was repaired before the passing checks.

## Next action
Reload the source game or Layout Studio to review the arrangement. No export or publication performed.
