# Large-room revision handoff

Updated: 2026-09-29 · Project: BrineSpace · Task: owner room correction pass

## Objective and acceptance
Implement the requested doorway, enclosure, fixed-facing machinery, Moonbay locker/airlock and operational turbine corrections in Layout Studio and game. Owner visual/hands-on acceptance remains open.

## Accepted decisions and constraints
All four centerpieces face south in every room rotation. Four-cell footprints and station ports retain their existing placement rules. North-only risers, muted industrial paint and bought prop facing follow the visual bible. Normal paid building remains enabled. Existing owner layouts and concurrent character/UI edits are preserved.

## Current state
- Common shell: remove broad door backing blocks, 28-unit low doors, continuous north top cap/returns and four corner caps. Larger Moonbay ocean hatch ties into side walls.
- Farm/crane remain upright. Moonbay has south-facing sub, floored chamber, clear large pressure gates, rear grated airlock with two crew/pressure connections and dry-room diving suit/helmet shelf. Inspector helmet actions use the existing walk/equip/return/refill service.
- Tidal has pressure walls/caps, grating and an underfloor feed pipe to its ocean intake. Operational chamber fills over six seconds before the impeller spins; interruption stops/drains it, pause freezes it, and saves retain validated state.
- Authored large-room geometry now uses exact blockers. Internal four-cell seams allow clear crossings; Moonbay gate/sub changes invalidate crew navigation. Rotation tests cover all entrances, locker and rear boarding.
- Changed rooms/large-rooms/{common,hydroponics_farm,storage_depot,moonbay,tidal_power_plant,studio_view}.gd; new grating PNG and SOURCES provenance; main/grid, airlock_service, bill_npc, moonbay_missions/panel, run_save; focused tests/index and card baker. Four selected cards rebaked with a scratch copy of owner layouts.

## Verification
Isolated Godot 4.7.2: seven headless large-room checks passed; final integration/revision/Moonbay assignment three passed after exact corner fix; native Studio passed. Moonbay missions/save passed. Shared airlock test passed (1,226 travel samples, equipment/return, interlocks, interruptions, saves/UI). Earlier assignment failure is superseded by final passing run. Native 16 station rotations, 16 raised/16 low frames, eight Moonbay phases and 24 turbine-motion frames captured and visually reviewed. Test logs and contact sheets: output/large-room-revision; station: output/large-room-review/station. No owner-profile files changed: before/after fingerprint has zero changed/added/removed files. No release export performed.

An additional clean-branch check stopped on the pre-existing committed main.gd:5336 empty if block; the owner's concurrent working correction already resolves this in the main checkout tested above. That unrelated working change was not copied into the room commit.

## Next action
Restart the running game/editor to load the changes, then owner hands-on visual review. Helmet pickup uses the Moonbay inspector buttons and crew walks to the locker. No further generation or scheduled work is pending.
