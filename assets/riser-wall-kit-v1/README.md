# Riser wall kit v1

Twelve reusable front-facing attachments in the station's dark steel and teal palette:

- Five ocean windows: small porthole, medium, panoramic, tall and twin portholes.
- Four hull pieces: infill panel, reinforced access panel, small access cover and structural rib.
- Three screens: single monitor, dual monitor and wide status display.

The individual PNGs have transparent exteriors. Window glass retains the painted ocean view. Ocean scenery and screen readouts are static artwork; this kit does not implement animation or powered states.

## Placement

`manifest.json` records actual dimensions, centered pivots and uniform suggested scales. Mounting heights range from 24 to 40 units inside a 48-unit riser. Preserve source aspect ratio rather than stretching a window to fill a wall.

```gdscript
const Walls = preload("res://assets/riser-wall-kit-v1/wall_sprites.gd")
Walls.draw(painter, "ocean_window_panoramic", Vector2(-115, -216))
# Or draw one of the isolated sample layouts:
Walls.draw_layout(painter, "observation")
```

Draw in wall space after the hull face and before foreground occluders. These decorative sprites have no collision. The observation, engineering and science samples reserve a central hatch bay; actual room placement must also respect its real doors, neighboring rooms and wall visibility. The kit does not enable global raised walls or furnish gameplay rooms automatically.

## Source and verification

`source/atlas.png` preserves the 1254 x 1254 RGB generation and `source/prompt.txt` preserves its prompt. `build_assets.py` uses the project's neutral exterior cleanup and reviewed crop regions to create twelve RGBA cutouts. The manifest records source/output SHA-256 hashes.

`review.gd` loads every PNG natively, verifies mounting bounds and hatch clearance, and exports `preview.png` (1x/2x sprite review) and `wall-layouts.png` (three sample hull strips). These validate the standalone kit, not complete gameplay placement or a packaged game export.
