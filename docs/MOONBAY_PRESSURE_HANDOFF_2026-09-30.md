# Project handoff

Updated: 2026-09-30 · Project: BrineSpace · Task: Moonbay pressure cycle and doors

Latest visual correction: [full sub hull and wall-top corners](MOONBAY_HULL_CORNERS_HANDOFF_2026-09-30.md). The submerged sub now stays opaque, with a mild blue tint; pressure-cycle behavior below remains current.

## Objective and acceptance
Implement the owner's wider crew doors, interlocking retracting sea doors, full airlock grating, permanently flooded sub bay, crew-triggered airlock filling/draining and rotating warning lights. Implemented and visually reviewed in native captures; owner hands-on acceptance remains open.

## Accepted decisions and constraints
The hull-connected bay and ocean-facing sub remain. The 384-unit sea gate has two retracting leaves with complementary interlocking tips; both crew doorways are now 120 units wide. The sub bay always contains water. Only the attached airlock fills and drains, with its two crew doors interlocked. Yellow rotates during airlock use; red rotates while the exterior gate moves. This supersedes the earlier dry-bay and 72-unit crew-door descriptions. Normal paid construction, survival, mission and repair rules remain.

## Current state
Room geometry, grating, water, doors and beacons: rooms/large-rooms/moonbay.gd. Actual crew pressure cycle and safe blocked-route recovery: scripts/moonbay_missions.gd. Persisted chamber_water now describes airlock water; cycle_clock preserves warning motion through Continue. Crew enter the lock, flood, board, and return through the lock before draining and opening the dry door. A lost wet route retains the pilot reservation and returns through the pressure cycle.

Local crew immersion and sealed-sub breathing use scripts/room_flooding.gd; scripts/bill_npc.gd geometry signatures include wet-door state. Studio preview and panel/room descriptions match the cycle. Updated focused assignment, save, revision and Studio tests plus tools/review_moonbay.gd; rebaked only assets/large-room-cards/moonbay.png. Preserve unrelated concurrent changes, especially the other Bill movement edits.

## Verification
Godot 4.7.2: focused missions, save, assignment, large-room revisions/art, room flooding and Studio simulations pass. Actual crew complete the pressure journey in all four rotations; permanent bay water and crew-door interlocks checked. Final assignment also forces a lost wet boarding route and verifies valid snapshots and safe dry return. Paid native walkthrough passes Survey, Recover, Deep Access, Save/Continue, hazard return and four-Metal repair. Pause and halfway door/warning restoration checked.

Native evidence includes 60 phase/rotation captures, four low-wall rotations, fourteen station phase views and the updated card. Reviewed idle, flooding, gate motion and dry-door crew views. Logs and fingerprints: output/moonbay-pressure-20260930/{acceptance,recovery,native}/; contact sheet: output/moonbay-pressure-20260930/door-motion-contact.png. All tests/probes used scratch APPDATA; each owner-profile comparison found zero changes across 2,924 files. Scoped diff whitespace check passes. Some revision/Studio fixtures emit shutdown-only resource leak noise after passing assertions.

## Next action
Reload the source game or Layout Studio for owner review. No export or publication performed; no implementation blocker remains.
