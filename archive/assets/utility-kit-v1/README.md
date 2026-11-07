# BrineSpace utility decoration kit

20 independent transparent PNG sprites for underwater station rooms, with source
atlases, exact prompts, repeatable extraction and a Godot drawing helper.

| Family | Pieces | Suggested units per source pixel |
| --- | --- | --- |
| Rigid pipes | straight, elbow, T, shutoff valve | 0.18 |
| Ventilation ducts | straight, elbow, T, grille terminal | 0.20 |
| Flexible tubes | straight, elbow, Y, spare coil | 0.16 |
| Armored power cables | straight, elbow, T junction, fused box | 0.15 |
| Signal wires | straight bundle, elbow, terminal junction, spare coil | 0.10 |

The existing airlock fitting atlas supplied pixel rendering and material guidance.
Steel, charcoal jackets, restrained amber coding and muted teal tubing keep the
families distinct without introducing futuristic neon or generic loose clutter.
Use wall saddles, equipment endpoints or supported storage to explain placement.
Keep floor routes clear: these sprites do not create automatic collision, power,
fluid, ventilation or interaction behavior.

## Files and usage

- `sprites/`: twenty individual, trimmed RGBA PNGs at source resolution.
- `manifest.json`: source/output hashes, actual sizes, family scales, center pivots,
  source-coordinate extraction history and named connector anchors.
- `utility_sprites.gd`: cached raw-PNG loader and aspect-preserving drawing helper.
- `preview.png`: native Godot gallery at recommended 1x placement scale and 2x.
- `assemblies.png`: native 3x connector review, retaining visible paired collars.
- `source/`: unmodified atlases and exact generation prompts.
- `build_assets.py`: repeatable extraction using the existing room cleanup helper.
- `review.gd`: isolated Godot texture/anchor checks and native review capture.

In a Node2D or existing CanvasItem drawing method:

```gdscript
const Utilities=preload("res://assets/utility-kit-v1/utility_sprites.gd")

func _draw() -> void:
    var start:=Vector2(80,80)
    Utilities.draw(self,"pipe_straight",start)
    var joint:=Utilities.port("pipe_straight","east",start)
    var tee_center:=Utilities.center_for_port("pipe_t","west",joint)
    Utilities.draw(self,"pipe_t",tee_center)
```

Use nearest texture filtering, uniform scaling and the real equipment/structural
anchors. The suggested scale is in the game's 384-unit room coordinate system.
The helper does not rotate artwork or invent directional views. The pipe and tube
elbows have east/south exits, while duct/power/wire elbows have west/south exits;
the manifest records what was generated rather than assuming prompt compliance.
`south_west` on the hose coil and numbered box tails identify individual ends.

## Generation and validation

Both requested 1536-square sheets returned **1254 × 1254**. Mechanical returned
RGB with a white background; electrical returned genuine RGBA and its alpha was
preserved. Mechanical extraction removes only edge-connected light-neutral pixels.
Explicit reviewed gap seeds remove the hose coil's enclosed white center and the
two small openings in the valve wheel. Generated bright metal highlights remain.

All 20 PNGs have transparent exterior and opaque subject pixels. Bounds, declared
anchors and dimensions are validated during extraction. Source regions were
reviewed individually because the requested equal cells were not exact. Native
Godot loaded all 20 textures and passed connector-transform checks; the gallery
and five straight/junction assemblies were visually reviewed. Log:
`output/utility-kit-v1.log`.

These are reusable **decorative modules**, not a seamless autotile or simulated
utility network. Generated diameters and lengths vary slightly; paired flanges
remain visible and every room assembly still needs a seam and clearance review.
No gameplay rooms were changed and no packaged-game export is claimed.
