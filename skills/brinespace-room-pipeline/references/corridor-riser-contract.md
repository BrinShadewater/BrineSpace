# Corridor, riser and floor production contract

Owner direction consolidated September 8, 2026. Current project status and later
owner corrections govern; dated native captures are evidence, not blanket approval.

## Art direction

- Raised walls default on; preserve subsequent explicit visibility preferences.
- Department risers need different construction and materials, not just recolors.
- Corridor shapes have three finishes: transit, utility and observation. Straight
  and turning-bay wall sources differ; corners and T-junctions share turning sources.
- Industrial floors use small grating, metal and recessed service modules. Plain
  large slabs were rejected. Keep solid perimeter strips and aligned center runs;
  vary panels deliberately rather than shuffling the atlas indiscriminately.
- Built-in protected pipes are wanted; loose drains, cables, hatches and legacy
  wall overlays were removed from the corridor set. Do not restore that clutter.
- Windows sit centrally in upright risers, never on low top faces. Exposed north
  entries use doors without windows; all corridor entries default to gray doors.
- Corners default alternately west/south and east/south. Count completed and queued
  corners, preserve manual rotation, and never rotate existing saved rooms retroactively.

## Geometry and integration workflow

1. Inspect authoritative hull/port geometry and current renderers before drafting.
2. Preserve originals and prompts. Register upright, low-top, cap and return samples
   independently; do not stretch an entire source sheet to fit a wall band.
3. Keep concave wall returns at the inside vertex. Applying the exposed-end rise
   there projects walls into the crossing. Test all four rotations.
4. Keep the floor editing grid distinct from visual module scale: current 48-unit
   cells hold four 24-unit modules. Clip to the footprint; retain explicit overrides.
5. Carry art_variant through the live floor renderer and cache key, not only cards.
   Match entrance lanes across shapes, variants and opposite rotations.
6. Distinguish default closed doors from shared connected live doors. Do not draw
   a closed overlay over an animated opening or omit a cap when neighbors mismatch.
7. Refresh both card consumers and every alternate card. New shader/finish IDs
   must reach both default and live connected renderers.
8. Capture native dry and flooded views. Check shape clipping, actual closing state,
   paused pixels, and physics separately. A shader mask assertion is not a visual review.

## Evidence and resumption

Start at `docs/CORRIDOR_ART_SESSION_CLOSEOUT_2026-09-08.md` and CURRENT_STATUS.
Reusable checks: `test_corridor_wall_variants.gd`, `test_hallway_floor_tiles.gd`,
`test_corridor_water_variations.gd`, `test_room_flooding.gd`,
`test_room_catalog_cards.gd`, and `test_corner_defaults.gd`.
Use isolated saves/layouts. Old Studio tests can reference retired controls; select
current controller tests and record failures instead of claiming broad acceptance.

Current corridor review is `output/corridor-polish-v3/index.html`; corner directions
are in `output/corner-defaults-v1/index.html`. Preserve earlier rejected or superseded
studies as evidence. Local files are not a committed backup or tested export.
