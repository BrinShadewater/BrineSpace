# Cargo dolly shared-crop review

## Objective and constraints

Check existing loaded/empty art together without independent tight crops changing their scale or origin. Preserve sources and runtime behavior.

## Current state

`assets/cargo-dolly-v1/state-review-group.json` draws both existing exports with source region186,199,710,1031 and36-unit width. `states.json` now links static review and `state-silhouette-review.json`. No PNGs or gameplay code changed.

## Verification

Both export hashes and1081×1455 canvases match the index. Godot group source-region, scale and panel checks pass. `output/cargo-dolly-state-review.png` was visually inspected at native and2x scale, loaded on left and empty on right.

At alpha128, silhouette intersection-over-union is0.9906786;5251 alpha-mask pixels differ. Registered bounds differ by1×3 source pixels, approximately0.0507×0.1521 world units at the proposed scale. This is close static alignment, not exact frame identity. Hardware/texture differences and future switching motion require separate review.

## Next action

Use a common crop/origin if integrating these states, then inspect actual switching and collision in the game. `runtime_transition_verified` remains false. Ongoing asset production remains active.
