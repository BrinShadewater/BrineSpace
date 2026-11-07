# Sealed maintenance case

## Objective and state

Small portable companion for the pressure-seal wall: closed slate case, rubber caps, ochre latches and south-facing handle. Intended width26 world units. `seal-maintenance-case.png` is the transparent1536×1024 export.

Built-in generation produced V1; a targeted V2 repair removed surrounding glow and excessive chipped-edge wear. Both raw sources and exact prompts are preserved. V2 checkerboard was removed through neutral185 vector registration with handle seed760,752.

## Verification

Godot source/hash/export check passed. Native light/dark review: `../../output/seal-maintenance-case-review.png`. Handle opening alpha0 and lid alpha255 were checked. Fine molded ribs simplify at actual scale; object was not enlarged to compensate. Review findings and hashes are in `material-scale-review.json`.

## Remaining work

Owner review and supported placement with handling clearance. Static closed art only; no inventory, carrying or opening behavior added.

## Proposed bench arrangement

`bench-group.json` records a measured clear mat rectangle and case placement at26-unit width against the328-unit wall. The complete case including handle fits within that rectangle. Godot group hash/bounds check passed; `../../output/seal-case-bench-group.png` was visually inspected at native and2x scale. Tools stay uncovered and open working area remains. This is a static support proposal, not runtime host attachment, collision or crew interaction validation.
