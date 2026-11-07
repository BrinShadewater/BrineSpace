# Salvage Workshop owner asset repair

The current owner contract requires top-down, inward-facing equipment in every
room orientation. The selected matte bench still has a tall frontal tool board,
and `workshop_view.gd` pins both layout and embedded configuration to rotation 0.
Older fixed-room captures do not verify rotation. Preserve existing carried-tote
and character behavior; gameplay and character work belong to other sessions.

Brief: Engineering salvage teardown station, matte charcoal/blue-grey steel with
restrained ochre accents, localized handling wear. Preserve the dismantled pump,
rotor, cloth, sorted bearings/flanges, tool inventory and vise. Convert upright
storage to shallow overhead trays. Operator handles face the lower image edge;
the rear edge mounts toward the wall. Keep a quiet unlit lamp diffuser for runtime
power treatment. Fit within the existing room and preserve entry/crew clearance.

Reference roles: `bench-north-matte.png` supplies subject inventory and materials;
`bench-south-split.png` supplies overhead work-surface direction. Neither overrides
the owner's matte, entirely top-down camera contract. Raw generation and exact
prompt will remain in `assets/salvage-owner-v2` before any selection.

Remaining: source review/cleanup, directional integration, four distinct native
layouts, power/retained/pause evidence, card update and workflow lessons.

Source checkpoint: `assets/salvage-owner-v2/bench-raw.png` and exact prompt are
preserved. The new bench replaces the upright pegboard with shallow tool trays,
keeps the pump/rotor/sorted parts and directs the vise screw toward the operator.
`build_salvage_owner_bench.py` removes explicit magenta, including handle openings,
and writes exact clockwise quarter turns. Clean crop is 1742x625; source hash and
processing settings are in `bench-review.json`. This is an unselected candidate:
remaining pump perspective, lamp appearance and surface noise need native review.
Baseline native capture completed under
`output/salvage-owner-repair-2026-09-12/before` with empty stderr. Its pinned views
are baseline evidence only, not proof of correct rotation.

Integration checkpoint: live bench and registered-alpha tote now use exact turns
with rotated bounds. Removed obsolete bench/tote position and size overrides from
the four defaults, preserving backups and other layout fields. The 176-layout
production clearance test passes (`20260912-212307-headless`). All four native
views in `rotated-native` are distinct and show inward access with clear entry.
Native review exposed dark magenta edge contamination missed by the first absolute
color threshold. Cleanup now uses red/blue dominance over green, preserving neutral
metal while removing dark key fringes. This last alpha change still requires a
fresh native review. No new card selection yet; operating/retained/pause remain.


Verified source checkpoint: fresh `alpha-native` q0 confirms the magenta fringe
is gone; four-direction furnishing state contact reviewed for contained powered
lamp and inward access. Direct/retained RGB match, powered clock samples match,
off/on differ, and all six existing-canvas transition rows match direct references.
Actual station pause fixture passes all four orientations with operating state,
advancing running clock and frozen paused clock/pixels (`station-pause/result.json`).
Selected card refreshed from cleaned native q0. Tests: 176 layouts previously
passed; 20 side variants and 47 card identities pass `20260912-212525-headless`.
No export or owner acceptance. Older library alternatives remain historical;
this checkpoint covers the selected live bench/tote and four default layouts.
Next owner asset queue item: Galley, including large mess-hall tables.
