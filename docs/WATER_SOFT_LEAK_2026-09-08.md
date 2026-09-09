# Softer water and hull leak

Updated: September 8, 2026 · Project: BrineSpace

## Objective and acceptance

Owner requested less net-like water and a better leaking crack. Native before/after
preview: `output/water-soft-leak-comparison.png`. Owner visual acceptance pending.

## Accepted decisions and constraints

Visual refinement only; existing flooding and survival rates retained.

## Current state

`scripts/flood_surface.gdshader` replaces intersecting caustic ridges with two
soft noise layers producing broad, slowly drifting illumination. Existing puddle
coverage and depth tint remain. `scripts/flood_visuals.gd` replaces the three
straight leak lines with a stable fractured-metal outline, bevel, curved stream,
animated droplets and expanding impact ripples. Severity controls stream size and
spray; deeper water shortens the stream. Uses the paused simulation clock.

## Verification

Native four-height and Save/Continue fixture passes; room preview visually
reviewed. Log: `output/water-soft-leak-native.log`. Scoped whitespace check passes.
No physics changes, new art assets, or full-station performance claim.

## Next action

Owner review of water softness and leak appearance.
