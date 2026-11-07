# Full-wall expansion handoff

Updated: 2026-09-08 · Project: BrineSpace · Task: additional inward-facing room installations

## Objective and acceptance
Extend the latest full-wall artwork to other rooms, retaining the owner's darker palette, substantial scale and inward-facing interfaces.

## Accepted decisions and constraints
Selected Tidal Condenser, Biodome and Thermal Power Control (`solar_array`). Life Support, Hydroponics and Battery Array have four-way access and need split installations around doors instead of a continuous bank. No gameplay or energy-balance changes.

## Current state
- Eight selected source sheets in `assets/full-wall-expansion-v2`: three horizontal, three paired east/west, and two dedicated north-facing south-wall banks. Eleven vector registrations; source pixels unchanged. Prompts, rejected candidates, source hashes and card provenance in the asset manifest.
- Added three wrappers under `rooms/full-wall-v1`, extended its manifest from 15 to 18 rooms, selected wrappers in `scripts/grid_canvas.gd`, and updated their floor-profile views/host anchors and three room-card mappings.
- Shared full-wall placement selects the new inward side views and uses the existing south-bank support. Invalid side-layout drafts fall back without rewriting saved drafts.
- Side registration now splits by actual source dimensions. Review contact-sheet height/count adapts to manifest size. Existing side regression covers the three new pairs; floor-anchor audit accepts a room filter.

## Verification
- Native full-wall review: 18 rooms × four rotations × two states, hull bounds, door lanes, relocated-prop clearance; passed. All four new-room contact sheets visually reviewed; enclosed background gaps in planter rail and thermal pipe loop excluded from vector cutouts and reviewed again.
- Side regression: 18 variants across nine rooms; source hashes, library entries, states, invalid/valid draft handling passed.
- New-room floor anchors: 24 placements across four rotations, zero missing.
- Production crew-route fixture: all three rooms, all four rotations, zero assertion failures.
- Eleven new registration source hashes verified; three native cards refreshed. PNGs use LFS attributes. No export or commit performed.
- Evidence: `output/full-wall-expansion-v2/new-rooms-q0.png` through `q3.png`, review/route logs, and `output/expansion-audit_floor_detail_anchors.log`.

## Next action
The requested three-room batch is complete. A useful next batch is door-aware split machinery for Life Support, Hydroponics and Battery Array. Preserve unrelated concurrent changes and personal room layouts.
