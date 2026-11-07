# Solar facing handoff

## Objective and constraints
Continue full directional catalog. Preserve thermal bank inventory, inward controls, independent operating monitor/pumps and accepted south source.

## Changes
assets/solar-directional-v1 contains selected side pair, rejected first edit, prompts and archived registrations. Restored four finned panels, two converter cores and two pumps per strip. Two side registrations preserve proportional frames and add wall_contact. Pipeline, bible and coverage updated.

## Verification
output/solar-directional-2026-09-12/final proves source replacement changes only side pixels, with unchanged inventory and bounds. seated captures add wall seating; comparison shows only side bank changes, north/south RGB identical and independent props unchanged. Native side views reviewed. 176 routes pass after seating; existing side variant suite passed before mounting update. No q0 card change or export.

## Next
Review retained north source in native room and verify independent monitor off/on and temporal behavior. South remains owner-accepted. Then continue Tidal Condenser and full catalog. Goal active.


## North and state follow-up
North source retained after native review. off/on-a/on-b native captures and state-checks.json prove independent monitor operating and temporal changes in every rotation; bank/pumps stay static. This supersedes the pending Solar checks above. South owner acceptance preserved in ledger. Continue Tidal Condenser and remaining catalog; no export.

## Owner orange-brightness correction

The later owner playtest supersedes the earlier palette acceptance: wall-length orange was too bright. `assets/solar-directional-v2` now supplies the selected north, paired side and south sources. A deterministic HSV pass reduces orange value to 72% and saturation to 82% while preserving hue, shading, geometry, alpha and every non-orange pixel. The q0 catalog card was refreshed from the selected live room.

Native q0-q3 captures in `output/solar-orange-repair-2026-09-12/native` show the same bank inventory and wall seating with restrained burnt-orange structure. `test_preferred_room_layouts` passes 176 orientations, `test_side_wall_variants` passes 20 variants, and `test_room_catalog_cards` passes 47 identities in `output/test-runs/20260912-170420-headless`. No gameplay, operating-state logic or independent floor machinery changed; no export was built.
