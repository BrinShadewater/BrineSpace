# Corridor junction and floor polish

Updated: September 8, 2026 · BrineSpace · T-wall correction and nine floor patterns

## Objective and acceptance

Stop T-corridor walls protruding into the crossing and give every corridor shape/variant a distinct polished floor. [Review nine combinations](../output/corridor-polish-v2/index.html). Owner acceptance pending.

## Accepted decisions and constraints

Reuse the industrial atlas; keep small modules, solid outer strips, aligned service lanes, north-entry doors and clean walking space. Preserve explicitly edited floor cells and saved finishes. No owner layout file was written.

## Current state

`rooms/underwater/corridor_dressing.gd` now detects concave wall vertices. Inner side returns start at the vertex instead of extending 35 units into the crossing; exposed convex ends keep their structural lift. This also fixes the matching inner elbow return. Authoritative hull, collision, entrances and neighbor culling remain unchanged.

`rooms/whole-room/modular_floor.gd` selects nine shape/variant arrangements: transit alternates tread and grating, utility keeps the covered pipe lanes, and observation uses finer grating. Each shape and variant selects different perimeter plates. Endpoint service modules remain shared and symmetric. `corridor_surfaces.gd` passes the active variant into the floor renderer, and mesh cache keys include it. Existing source pixels are unchanged.

Nine refreshed cards and provenance references are in `assets/corridor-polish-v2`; both card consumers point there. The gallery includes all rotations and notes. The underlying atlas remains `assets/hallway-floor-tiles-v2/source.png`.

## Verification

- 72 native raised/low shape/variant/rotation captures pass. All nine default views and a rotated T-junction visually inspected.
- Focused floor checks pass nine distinct UV arrangements, concave T-return positions, full footprint coverage, bounded UVs, preserved saved finishes and current finish selector behavior.
- Native routing fixture passes all corridor shapes, four rotations, T connection masks, branch samples and tapered-face coverage.
- All 47 card identities agree and decode. No new raster source was generated; this pass composes existing registered artwork.

Evidence: `output/corridor-polish-v2/{native,floors,routing,cards}.log`. Prior unrelated editor-fixture limitations remain recorded in the hallway floor handoff; this pass does not claim full Studio or exported-build acceptance.

## Next action

Owner reviews the shortened wall returns and differentiated floor patterns, then supplies specific visual notes.
