# Wall dressing — second collection

Twelve new decorations, distinct from the first collection:

- Paired pressure gauges and a decorative station map.
- Bracketed extinguisher, emergency mask rack and guarded alarm beacon.
- Key rack, retained tools and coat hooks with a utility towel.
- Wall planter, wave pennant and framed seashell display.
- Guarded ventilation fan.

## Placement

Individual transparent PNGs are in `sprites/`. The manifest records centered
pivots, native dimensions and uniform mounting scales for 22–34-unit heights.
These fit the sample 48-unit riser. Preserve aspect ratio and render in wall space
after the hull face and before foreground occluders.

```gdscript
const Decor = preload("res://assets/wall-dressing-v2/wall_sprites.gd")
Decor.draw(painter, "wall_planter", Vector2(-149, -216))
```

`maintenance`, `safety_station` and `crew_details` are sample layouts, each with
a central hatch bay reserved. Adapt placement to actual room doors, neighboring
walls, furniture and activities. Sprites have no collision or automatic placement.
These are static illustrations: the map is not the current station layout, gauges
are not live readings, safety equipment is not usable and the fan does not animate.

## Sources and checks

Generated individually with the built-in image tool. Original RGBA sources and
exact prompts are preserved under `source/`. The first two images were recovered
from the interrupted generation; the remaining ten were generated on resumption.

The build follows the reviewed first-kit alpha cleanup: discard alpha below 128
to remove faint exterior haze, retain foreground alpha and crop with two pixels
of padding. Source/export SHA-256 hashes, dimensions and registration bounds are
recorded in `manifest.json`; original sources remain unchanged.

`build_assets.py` checks wall bounds, hatch clearance and pairwise separation.
`review.gd` checks native loading, dimensions and mounting bounds and exports
`preview.png` (1x/2x) and `wall-layouts.png` (sample strips). These validate the
standalone kit, not gameplay room integration or a packaged game export.
