# Codex brief: station props on magenta

Goal: re-export the station props from the room designs as clean individual
images, so they drop into the game without re-cutting and without moving any
saved room layout. Context: [station props v2](STATION_PROPS_V2_2026-09-25.md).

## What to produce

One PNG per prop, redrawn from the existing room design. Work one room (or one
Extras sheet) at a time.

1. **Background:** flat pure magenta `#FF00FF`, every non-prop pixel. No floor, no
   grid, no wall, no vignette, no noise.
2. **No drop shadow** outside the prop's outline. Shading *inside* the outline
   (recesses, under desks, cushions) stays exactly as painted.
3. **Same view, facing and style** as the room design: top-down, props facing into
   the room from the north wall, same ink outline weight, same palette.
4. **Same scale and proportions** as the prop in the design sheet. Do not crop,
   stretch or re-pose. The prop must fit the same footprint so layouts stay put.
5. **Hard edges:** no anti-aliased blend into the magenta. A 1-pixel dark ink
   outline against pure magenta is ideal. Avoid magenta-tinted edge pixels.
6. **One prop per image**, centred with at least 16 px of magenta on every side.
   Multi-part props (a desk with its chair, the lounge sofa + table + bench) stay
   together only if they are one prop in the list below.
7. **Glass and transparent parts** (tanks, domes, screens) are painted opaque, as
   they look in the design. No real transparency.
8. **Resolution:** at least the size the prop occupies in the 1254 px design sheet;
   2x is welcome (it is downscaled on install).

## Naming

`<prop id>.png`, using the existing ids so the catalog and layouts bind unchanged,
for example `galley-1.png`, `crew_lounge-3.png`, `science-extra13-2.png`. Numbers count
props on each design sheet from top to bottom, then left to right; the current
cut `assets/station-props-v2/sp-<id>.png` shows which prop each id is. The lounge rug is `crew_lounge-3-rug.png`
(the rug alone; the sofa, table and bench stay in `crew_lounge-3.png`).

Floor pieces (hatches and pads) should be painted flat, as seen from above, with
no shadow at all: `airlock-3`, `engineering-extra2-3`, `engineering-extra4-3`,
`mining_drone_bay-3`, `salvage_drone_bay-3`, `construction_drone_bay-3`.

## Priority

1. The 22 props whose cuts needed the most hand cleaning: `clone_lab-2`, `crew_hab-1`, `crew_hab-2`, `crew_hab-3`, `data_archive-1`, `med_bay-3`, `med_center-3`, `mycelium_nursery-2`, `ore_refinery-1`, `ore_refinery-4`, `pressure_control-1`, `quarantine_cell-1`, `salvage_drone_bay-2`, `xeno_lab-4`, `science-extra10-1`, `science-extra13-1`, `science-extra13-2`, `science-extra3-1`, `science-extra5-4`, `science-extra8-1`, `recreation-extra2-1`, `recreation-extra3-1`.
2. Props with glass or with colours close to their floor (`xeno_lab-1`,
   `recreation-extra3-1` bookcase, `recreation-extra3-4` table, the lounge set).
3. Everything else, a room at a time.

## Out of scope

Drones and drone docks, the airlock pressure chamber and cryo pods (live
machinery with their own art pass), floors, riser walls, doors and crew.

## Install (Claude side)

Chroma-key each image on `#FF00FF` with despill, fit it to the prop's existing
canvas (same anchor as the current cut) and install over
`assets/station-props-v2/sp-<id>.png`; then rebake the room cards. Saved layouts,
roles and categories are unaffected.
