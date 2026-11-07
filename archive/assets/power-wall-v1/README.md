# Power-room wall assets

Updated: 2026-09-08. Project: BrineSpace.

## Objective and direction

Continue standalone wall-asset production with distinct Current Turbine and Heat
Recovery banks. Use connected functional bays, modest scale and matte Engineering
finishes. These are new reusable sprites, not replacements for the live machines.

## Deliverables

- `turbine.png`: intake strainer/valves, analogue generator controls and cable
  cabinets. 1881x836 RGBA; diagnostic display width 320, visible height 84.93 units.
- `heat.png`: plate-fin exchanger, insulated pipes, manifold, pump and service
  storage. 1882x836 RGBA; width 320, visible height 76.91 units.

Sources, exact built-in imagegen prompts, source polygons and hashes are retained.
Both are horizontal south-facing fronts. Room placement, side views, floor
footprints and crew clearance are not registered. Heat Recovery's north/south
through-route especially requires a side-wall or split placement design.

## Review and workflow refinement

Turbine V1 has readable functional bays and restrained material highlights. Heat
V1 was rejected for reflective ribbed coils and granular insulation; V2 simplified
insulation but retained repetitive rib shine. V3 changes only the requested core
design to broad matte plate fins, improving small-scale readability. Earlier
sources remain rejected references, not alternative runtime selections.

`tools/review_registered_wall_asset.gd` exported neutral160 source UV registrations
without modifying raw rasters. Both native 1040x900 boards were inspected at room
scale and enlarged, on light/dark grounds. Logs: `output/power-wall-turbine.log`
and `output/power-wall-heat.log`, both PASS without ERROR/SCRIPT ERROR. RGBA and
transparent corner samples pass; backed recesses correctly remain opaque.
`manifest.json` binds current sources, exports and boards to their hashes.

The material-review skill now records the repeated-rib failure and plate-fin
correction. This is a bounded source-design lesson, not a reason to flatten all
metal or change existing machinery. Candidate visual review remains separate
from owner acceptance. No game behavior or production room/card binding changed.

## Next action

Use owner feedback for any material revisions. For installation, author the actual
sealed-wall directions or split banks and verify route, wall-contact and card
consumers. Continue future art passes with distinct functional bay sequences.
