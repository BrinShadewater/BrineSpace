# Preferred room layouts

Updated: September 9, 2026 · Project: BrineSpace · Task: extend owner Studio preferences

## Objective and acceptance
Match the owner's saved larger equipment and selective removal of benches/lights across the remaining rooms and rotations. Preserve personal saves and existing artwork.

## Accepted decisions and constraints
The 49 saved orientations across 17 identities are the reference, copied verbatim into authored defaults. Larger props supersede the earlier blanket modest-scale preference for this layout pass; department materials and architecture stay unchanged. Each room keeps its functional identity. Three empty corridor identities retain their architecture. No new artwork, balance changes or export.

## Current state
- `rooms/full-wall-v1/default-layouts.json`: all 188 Studio entries (47 identities × four quarters). 49 owner entries preserved exactly; 127 other furnished orientations adapted; 12 corridor entries retain existing empty interiors. Fixed-facing blueprints remain fixed-facing. BRINE's other Studio quarters use its preferred core composition.
- `scripts/room_layout_store.gd`: gameplay honors Studio's default free placement, including older saves without the flag. Detached stale art and explicitly constrained layouts retain fallback. Flip and placement-mode changes invalidate crew geometry.
- `scripts/room_asset_library.gd`, `tools/modular_room_geometry.gd`, `scripts/bill_npc.gd` and the two BRINE corner registrations: normalized two-piece collision follows the L-shaped furniture, its scale and flips; the empty notch is no longer an invisible blocker. Owner positions are untouched.
- `assets/preferred-layouts-v1/cards`, `scripts/room_card_art.gd`, `scripts/grid_canvas.gd`: 44 native furnished-room cards refreshed; three corridor cards retained.
- Added paired tests `test_preferred_room_layouts.gd` and `test_layout_free_placement.gd`. Existing side-wall source test now isolates defaults from room composition overrides.

## Verification
- 188 native editor/runtime prop comparisons: no position or size differences. All eight rotation sheets reviewed; final 13 refinements recaptured. Evidence: `output/layout-preferences/render-report.json`, `sheet-1.jpg` through `sheet-8.jpg`.
- 176 furnished orientations: every actual door connects through the production crew clearance and segment checks. Dedicated fixture excludes player saves.
- Live station graph crosses BRINE and all four connected corridors with its recovery pod present; `station.png` reviewed at 1600×900. This verifies graph reachability, not an exhaustive animated crew tour.
- Free-placement/legacy/constrained/stale guards, collision notch/mirroring, 20 directional variants, live refresh/cache invalidation, full Studio editing/recovery workflow and 47-card consistency checks PASS without script errors. Exact logs are in `output/layout-preferences/`.
- The original personal file is byte-identical to the captured SHA-256. Snapshot and provenance: `owner-layouts.json`, `source.json` in the evidence directory.

## Next action
Owner visual review in Layout Editor/game. Local source and cards are integrated; no Windows executable was rebuilt. Other sessions' changes remain intact.
