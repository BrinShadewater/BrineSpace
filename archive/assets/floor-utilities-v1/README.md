# Floor utility decorations

13 separate top-down RGBA sprites for BrineSpace floor decoration. These complement
the upright/general utility kit rather than reusing wall props as floor decals.

| Family | Included pieces |
| --- | --- |
| Thin signal wires | clipped straight bundle, bend, T junction |
| Power cables | paired straight run, bend, sealed T splitter |
| Cable-cover mats | straight rubber ramp, corner mat, T mat |
| Floor pipes | paired straight pipes, paired elbow, recessed service channel |
| Service cover | separate slatted cover beside the channel |

Steel/charcoal finishes, small amber marks and subdued wire colors match the
underwater utility style. Mats have a low non-slip surface with narrow edge
markings. Pipes lie parallel to the deck in shallow saddles. The service cover
is a separate decorative piece, not a dimension-matched animated channel lid.

## Use

`sprites/` contains individual source-resolution PNGs. `manifest.json` records
actual sizes, hashes, source regions, center pivots, suggested family scales and
connector anchors. `floor_sprites.gd` loads PNGs directly and draws without stretching.
All entries explicitly use `floor_under_actors`, `top_down`, and no collision.

Draw these from a room's floor pass, before furniture and crew:

```gdscript
const FloorUtilities=preload("res://assets/floor-utilities-v1/floor_sprites.gd")

func draw_floor_details() -> void:
    var center:=Vector2(-40,20)
    FloorUtilities.draw(self,"mat_straight",center)
    var join:=FloorUtilities.port("mat_straight","east",center)
    var next:=FloorUtilities.center_for_port("mat_t","west",join)
    FloorUtilities.draw(self,"mat_t",next)
```

For embedded room rendering pass the room's `painter` instead of `self`. Use nearest
texture filtering. Suggested units per source pixel are wire 0.12, cable 0.15,
mat 0.20 and pipe 0.16 in the game's 384-unit room coordinates. Preserve uniform
scale and inspect placement against actual furniture and door routes. Connector
anchors aid decorative assembly; they do not promise seamless autotiling.

These assets do not implement electricity, fluids, collision or walkability.
Covered crossings can visually explain a cable route, while uncovered pipe runs
belong alongside machinery or perimeter service lanes. Do not use a floor pass
to make a visibly obstructed doorway appear clear to the navigation system.

## Source and validation

The exact original and background-repair prompts are in `source/`. Both generated
images are retained, at their actual 1254-square RGB size. The original returned
opaque black despite a transparency request and was rejected for cutout extraction.
Imagegen prepared a white-background revision; dark insulation and mats were not
removed with a black color key. The revision is not claimed pixel-identical to the
original. `build_assets.py` uses the existing connected light-neutral cleanup on
reviewed source regions. No enclosed-gap seeds were required.

The sheet contains twelve requested groups; the channel and its loose cover were
split into two usable sprites, giving thirteen exports. Every PNG has real alpha
with a transparent exterior and opaque subject. Native Godot loaded all thirteen,
checked floor-layer metadata and connector transformations, and generated:

- `preview.png`: 1x placement scale beside a 2x detail view.
- `floor-layouts.png`: joined decorative runs on a simple deck at 3x.

Both native previews were visually reviewed. Log: `output/floor-utilities-v1.log`.
`review.gd` uses an isolated canvas and does not load or change player saves.
No gameplay rooms were modified and no packaged-game export is claimed.
