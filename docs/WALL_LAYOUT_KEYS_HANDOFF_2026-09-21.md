# Project handoff

Updated: 2026-09-21 · Project: BrineSpace · Task: Complete wall-layout key audit

## Objective and acceptance
Ensure Studio layouts actually drive current wall rooms, including saved deletions
and rotation-specific restoration. Overall art, Bill gait and release scope remains open.

## Accepted decisions and constraints
Player layout bytes and named owner reference layouts unchanged. No new art or
Higgsfield. Art asset IDs remain stable; the existing Studio catalog owns layout keys.

## Current state
full_wall_prop.gd resolves layout_key(room) through RoomLayoutStore.asset_for with
asset_id fallback for uncatalogued fixtures. Initial, repeated and deleted-bank
paths use that key. Anomaly/Radio q2 restoration calls corrected likewise.
Medical Office and Medical Center q3 restoration now reads the canonical key and
honors null deletions instead of adding old stations back over bought furnishings.
Expanded test_split_layout_keys.gd covers all 34 wall-based catalog rooms, ten
setups each, including both medical-room deletion paths. Existing UID/index retained.
Twelve affected room cards refreshed (later Medical Center change affects q3 only,
not the q0 card). Maintained/installed room workflow updated.

## Verification
output/layout-key-audit-2026-09-21/ contains initial 47-view setup audit. Empty
metadata for non-wall rooms is not classified as a bug: they apply on render.
340-setup final guard passes. Native twelve-room batch produced 48 views/7,680
walking samples, with two failures in Medical Office q3. These exposed restored
legacy furniture, not bad owner positioning. After correction, Medical Office
four views/640 samples pass; Medical Center four views/640 pass after its related
fix. Other batch views passed unchanged. Medical Office before/after inspected.
Card log reports twelve baked. Player layout exact-byte comparison and whitespace
check pass. Geometry evidence is not owner art acceptance or actual release testing.

## Next action
Continue Bill gait and room detail review. Do not rearrange owner references to
compensate for an ignored key or reinstated deletion. Earlier release builds and
station performance captures predate these restored furnishing paths.

## Production navigation follow-through
The actual grid.bill_room_geometry entry point was exercised for all four rotations
of the 19 rooms affected by the split/single-wall key corrections. All 76 snapshots
contain expected visible saved tileset additions and exclude deleted tileset props.
Evidence: output/navigation-layout-audit-2026-09-21/audit.gd, audit.log, report.json.
This checks selected prop presence in crew geometry, not every route, legacy prop
or interaction. No player data or production code changed during this follow-through.
