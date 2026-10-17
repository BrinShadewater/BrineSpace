# Common-prop visual audit — September 26, 2026

Reviewed all **57 current prop exports** against the visual aesthetic bible and locked accepted reference artwork. Overall, the set shares the painted industrial style and overhead/cutaway perspective. One relative-size concern and three material-polish candidates remain. No artwork or runtime configuration was changed during this audit.

## Scope

The 37 calibrated common props and seating include ten current matte plant replacements. Also reviewed: six storage props, six counters/desks/surfaces, and eight submarine utilities. Rejected v1 artwork, literal-topdown seating, superseded shiny plants and superseded metal-seat masters are historical iterations, not additional current deliverables.

## Pixel density and relative size

All 57 exports declare 0.34 world units per source pixel, or approximately **2.94 pixels per world unit**, consistent with the locked reference family's approximate ratio. This holds only when their manifest's suggested display width is used. Export dimensions alone cannot establish physical scale or visual detail density.

**Needs crew-scale comparison: `common-table-and-chairs-v2`.** Its bundled chairs look substantially smaller than the standalone seats at proposed widths. Side-facing orientation accounts for some apparent narrowing, so a precise scale correction should wait for a same-scene character comparison. Consider adjusting the assembly or separating its components after that check. Do not simply upscale every export.

The remaining props have plausible relative sizes in the comparison sheets, with no other clear size outlier found. Their world sizes remain proposals; these are not live placement tests.

## Art style and materials

The set generally matches the accepted muted, painted industrial family: readable construction, subdued local colors, matte materials and limited accents. The current matte plants and revised painted-metal seats are coherent with that direction. Small utility safety colors are intentional.

| Asset | Finding | Priority |
|---|---|---|
| `common-workstation-v2` | Pale corner trim and high-contrast frame highlights are stronger than most of the set. A localized reduction would improve consistency while preserving its endorsed futuristic form. | Moderate polish |
| `seat-utility-chair-blue` | Bright continuous cushion piping and stronger upholstery texture stand out beside neutral seating. | Optional polish |
| `seat-task-chair-olive` | Similar cushion-edge contrast and texture difference. Color itself is suitable. | Optional polish |

No wholesale redraw is indicated. These are visual recommendations, not new owner rejections of previously reviewed designs.

## Perspective

The current props broadly share the approved overhead/cutaway family, with visible tops and readable front faces. No clear conflicting isometric yaw was found. Tall objects naturally expose more upright face; that alone is not evidence of a camera mismatch. The accepted references themselves vary, so this audit does not claim an exact common camera angle from raster images.

Keep the approved seat perspective. Character sitting alignment, seat height, floor-contact anchors, and the wall-counter/desk/workbench rear-edge contact still need a live room check before integration. Straight rear edges express wall-flush design intent, not verified placement.

## Technical checks and evidence

- 57 RGBA exports inspected; all outer borders transparent.
- All 57 export hashes and corresponding master hashes match their manifests.
- Three comparison reference hashes match the locked catalog.
- Native-size comparison sheets reviewed, plus the dark aggregate preview and closer comparisons of flagged props. The corrected first-page layout avoids clipping the wide table assembly in the review sheet.
- No runtime registry, owner layout or gameplay changes; no runtime-fit claim.

`checks.json` records every current asset, its actual dimensions, source paths, density and integrity results. `page-1-light.png` through `page-5-light.png` and their dark versions compare native exports with accepted references. `findings-comparison.png` isolates the review candidates. `world-unit-light.png` and `world-unit-dark.png` show all 57 at the proposed 0.34 scale using nearest filtering; these are comparison boards, not screenshots of the game.

First useful follow-up: stage the table assembly and standalone seats beside the same character at their proposed sizes. Material polish can then be limited to the workstation trim and, if desired, the two colored cushions.
