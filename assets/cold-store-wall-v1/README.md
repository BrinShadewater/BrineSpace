# Project handoff — Cold Store wall-length assets

Updated: 2026-09-08

## Objective and accepted direction
Owner requested wall-length art assets following the smaller matte Cold Store correction. Two standalone south-facing assemblies: continuous refrigeration bank and ingredient shelving/preparation wall. Matte charcoal, muted ochre, modest height and deliberate pixel detail; no polished silver treatment.

## Current state
refrigeration.png and pantry.png are true-alpha native exports, both 1983×793. Original RGB sources and exact source hashes remain in matching JSON registrations. Both source images had baked checkerboards. Read-only neutral registration at 160 removes exterior background; pantry opening seeds are (440,260) and (700,465). render_assets.gd rebuilds the exports. Originals preserved. These are separate reusable assets; no room placement, door-mask or gameplay changes were made.

## Verification and next action
Native Godot export passes (output/cold-store-wall-assets.log). Both cutouts visually reviewed; pantry upper/lower opening alpha reads zero. PNG LFS attributes checked. Assets are ready for layout selection; live Cold Store keeps its current through-aisle and smaller V2 props. Wall-length assembly placement must preserve actual room ports. No package rebuilt.

## Refrigeration prompt
Create ONE WALL-LENGTH REFRIGERATION BANK standalone game art asset for BrineSpace, matching supplied matte pixel-art fridge reference. A long horizontal continuous bank of FOUR compact insulated cold-storage compartments, shallow depth, common low compressor plinth and straight upper beam, meant to occupy one room wall at realistic crew height. Overall silhouette roughly 3.5 times wider than tall. Alternate two smoky inspection-window doors and two solid panel doors, with a small shared temperature panel near one end. Distinct connected industrial assembly, not four duplicated images. Matte dark charcoal painted steel, desaturated ochre SMALL corner/handling accents, dim blue-grey windows, subdued food silhouettes. Chunky deliberate pixel clusters, stepped shading, restrained edge scuffs. NO chrome, polished silver, bright frost, specular shine, neon or photorealism. Straight-on elevated orthographic camera from SOUTH with level horizontal edges, no diagonal yaw. Square outer corners with small construction bevels, all details contained inside silhouette, no protruding pipes. Transparent alpha exterior; no floor, room, wall background, people, text or painted checkerboard. Wide landscape canvas with margins, full ends visible. Reference supplies rendering/material and modest height; widen the functional assembly without making it taller.

Reference: rooms/underwater/cold-store-v1/fridge-source-v2.png (materials and style).

## Pantry prompt
Create ONE WALL-LENGTH INGREDIENT STORAGE AND PREPARATION installation sprite for BrineSpace, matching supplied matte rack reference. Very wide low horizontal assembly about 3.5 times wider than tall: LEFT third two low open shelves holding assorted sealed subdued ingredient tubs; CENTER weighing/prep counter with compact scale, two stacked insulated delivery boxes underneath; RIGHT enclosed supply cupboards with two shallow ingredient shelves above. Shared continuous charcoal frame and plinth, square corners with modest bevels. Asymmetric practical supported furniture rather than repeated mirrored bays. Do not stretch a single rack. Modest crew-scale height even though wall-length. Matte dark charcoal-grey painted steel, sparse muted ochre guards, simplified food/container shapes and blocky deliberate pixel clusters, stepped values, restrained wear. No shiny silver, chrome, vivid food photography, white sparkling rims or neon. Same elevated orthographic SOUTH camera, level horizontal front, no diagonal yaw. Entire isolated asset with generous outer margin. True transparent alpha exterior and open-shelf gaps; NO checkerboard, room, floor, wall backdrop, people or readable text. Keep all objects supported and inside silhouette. Reference supplies material and pixel rendering only.

Reference: rooms/underwater/cold-store-v1/rack-source-v2.png (materials and style).
