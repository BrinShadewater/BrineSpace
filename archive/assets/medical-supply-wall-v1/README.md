# Medical supply wall and cart

Updated 2026-09-08. BrineSpace ongoing wall/prop production.

## Objective and current state

Add clinical supply/preparation furniture that complements treatment equipment,
with modest scale and matte cream/teal materials. `wall.png` is 2172x724 RGBA,
shown at 320 units wide (68.17 high). `cart.png` is 1254x1254 RGBA, shown at
36 units wide (43.49 high). Both are south-facing standalone candidates.

The wall groups closed supplies, preparation surface, gloves and a closed return
area. The compact cart carries a closed cassette, bandage roll and sealed packets.
No new medical action or supply gameplay is implemented.

## Sources and refinements

Wall V1 and cart V2 are selected. Cart V1 retained as rejected for reflective rim,
cassette and packet highlights; V2 preserves pale colors while reducing gloss.
It also replaces true alpha with RGB checkerboard, so it required new registration.
Exact built-in imagegen prompts, source revisions and reference roles are retained
in `prompts.json` and `manifest.json`.

Read-only neutral185 registration excludes the source-specific checkerboards.
Wall neutral extraction left small exterior spikes above its rear rail: final
geometry excludes pixels above source y147, preserving the older registration in
`wall-neutral-v1.json`. This is a local silhouette repair, not permission to crop
real protruding fittings. Neither original source raster was edited by cleanup.

## Verification

Native logs `output/medical-supply-wall-final.log` and
`output/medical-supply-cart.log` PASS with no ERROR/SCRIPT ERROR. Both 1040x900
light/dark scale boards were visually inspected; wall board was rerendered after
the rear-edge repair. Export corners, cart undercarriage and wall exterior strip
have alpha zero, while sampled cart/wall contents remain opaque. Hashes and native
dimensions are recorded. PNGs use Git LFS.

## Next action

Owner review and room placement remain pending. Select actual wall/bedside
positions and validate paths, floor footprints and card consumers before binding
the assets. No production layout, medical behavior or package changed. Continue
the active wall/prop production goal with the documented material and alpha checks.
