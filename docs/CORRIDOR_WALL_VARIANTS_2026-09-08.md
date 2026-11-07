# Corridor and corner wall variants

Updated: September 8, 2026 · BrineSpace · Dedicated routing architecture

## Objective and acceptance

Give corridors and corners unique walls and variants. Six new original designs supply three straight-corridor treatments and three turning-bay treatments. Corner and T-junction shapes share the turning-bay sources, giving nine native shape/variant combinations. [Review all variants and rotations](../output/corridor-wall-variants-v1/index.html). Owner visual acceptance is pending.

## Accepted decisions and constraints

Transit uses navigation panels and recessed rails; utility uses ducts, manifolds and maintenance controls; observation uses gasketed underwater windows and environmental instruments. Straight and turning designs have different equipment arrangements. Preserve the authoritative hull, narrow side returns, chamfers, openings and neighbor culling. Risers remain on by default. No owner layout file was written.

## Current state

- `assets/corridor-wall-variants-v1`: six unmodified generated PNGs, exact prompts, SHA-256 provenance, registrations and nine native cards.
- `rooms/underwater/corridor_wall_art.gd`: shared registered skins. Long upright faces repeat/crop proportionally; low hull plates sample quiet solid panels, and structural return samples follow angled faces.
- `corridor_surfaces.gd` and `corridor_dressing.gd`: new low hull, raised face, cap and return materials. Removed the old generated-overlaid procedural riser windows/vents to avoid covering the new equipment. The subsequent owner cleanup removes all legacy deck props, drains, service pipes, cable runs, inspection hatch and mounted overlays.
- `scripts/room_card_art.gd` and `scripts/grid_canvas.gd`: three primary cards plus six alternates refreshed. Existing `art_variant` values 0/1/2 select transit/utility/observation; existing placement and save behavior are retained. The Layout Studio's standard corridor preview shows variant zero; the review gallery exposes all variants.
- `tools/register_corridor_walls.py`, `tools/finalize_corridor_walls.py` and `tests/test_corridor_wall_variants.gd` reproduce registration, native captures, card installation and the gallery. New Godot scripts have paired UIDs.

## Verification

Native fixture passes six source registrations, nine distinct rendered variants, 72 raised/low rotation captures, dark response capture and neighbor culling. Visual review caught observation glazing leaking into a low top-face source sample; registration now selects lower solid panels. Corrected raised and low captures reviewed.

`test_corridor_detail_bounds.gd`: 248 fitting corners remain within hulls and clear of socket approaches. `playtest_corridor_routing.gd`: all three shapes at four rotations, T connection masks, branch foot samples, and five corner/six T tapered faces per rotation pass. The final low-panel sampling correction changes texture coordinates only. `test_room_catalog_cards.gd`: all 47 primary/grid/variant identities agree and decode. Six source hashes, PNG LFS attributes, gallery links and JavaScript syntax checked. Existing raw-image export warnings remain; exported-build acceptance was not tested.

Evidence and logs: `output/corridor-wall-variants-v1`. Native routing captures are under `output/corridor-joins-v1`. The gallery includes rotation selection, raised/low switching, source inspection and browser-local notes/export.

## Next action

Owner reviews the nine combinations and supplies specific art notes. Preserve source provenance and the opening geometry when applying corrections.

## Owner cleanup follow-up

The corridor set now uses a clear deck with its structural floor material retained. Existing owner floor-tile settings are preserved. Legacy `draw_props`, `draw_details` and `detail_parts` interfaces remain empty for caller compatibility. Observation skins render their window band centered over a solid panel backing. For each rotated north-facing boundary port, the riser uses solid panels and a closed registered door with a 72-unit leaf opening; no window is drawn on that face. Connected neighbor culling still takes precedence and live connected doors remain owned by the shared door system.

`test_corridor_wall_variants.gd` additionally checks port-to-riser matching across all three shapes and four rotations, and absence of legacy fitting records. All 72 native raised/low views and nine cards refreshed. Cleanup-specific logs are `cleanup.log`, `cleanup-routing.log` and `cleanup-cards.log`. Visually inspected clean corner observation and north-entry straight corridor. No new raster source or owner layout write was needed. Owner acceptance remains pending.
