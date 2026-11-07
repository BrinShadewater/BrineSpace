# Everyday wall dressing v1

Twelve separately generated reusable wall decorations: analog clock, digital clock,
handset intercom, communications panel, paper calendar, noticeboard, ocean picture,
botanical picture, diver poster, jellyfish poster, bulkhead lamp and first-aid box.

## Use

Transparent PNGs live in `sprites/`. Suggested heights are 18–32 world units on a
48-unit riser. `manifest.json` records dimensions, centered pivots, uniform scales,
categories, source bounds and SHA-256 hashes. Preserve aspect ratios.

```gdscript
const Decor = preload("res://assets/wall-dressing-v1/wall_sprites.gd")
Decor.draw(painter, "analog_clock", Vector2(-155, -216))
```

Draw after the hull face and before foreground occluders. Actual room placement
must respect its doors, shared walls and furniture. Choose a few objects around
activities rather than repeating every accessory in every room. Paper decorations
belong in dry interiors. The three sample layouts illustrate mounting and reserve
a central hatch bay; they do not automatically furnish existing gameplay rooms.

These are static decorations: clocks do not track game time, comms are not
interactive, and the lamp does not supply dynamic lighting. The generated digital
clock depicts 08:30 despite the prompt requesting 06:30; its decorative readout is
not a verified time display. Calendar marks and poster details are illustrative.

## Production and review

Generated with the built-in image tool, one request per asset. Exact prompts are
preserved in `source/prompts.json`; original RGBA images retain their native sizes
and alpha. Faint generated exterior haze would distort automatic trim bounds.
`build_assets.py` discards alpha below 128 and crops with two pixels of padding,
preserving foreground alpha rather than replacing it with an opaque mask. This
cleanup choice is recorded per sprite; original sources remain unchanged.

Native Godot `review.gd` loads all twelve sprites and produces `preview.png` at
1x/2x and `wall-layouts.png`. The build validates wall bounds, hatch clearance and
pairwise layout separation. Native checks verify texture dimensions, wall bounds
and hatch clearance. This is standalone asset evidence, not packaged-game or
full room integration validation.
