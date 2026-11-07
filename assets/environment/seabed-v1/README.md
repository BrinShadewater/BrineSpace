# BRINE seabed environment kit

17 distinct asset identities cover the silt plain, vent basin, wreck field,
overgrown shelf and trench-edge visual themes. This is a reusable visual kit,
not an implementation of five procedural biomes or their gameplay systems.

Open `index.html` for the filterable local catalogue. `manifest.json` records
selected versions, original dimensions, SHA-256 hashes, alpha counts and bounds.
`generation-record.json` preserves the exact generation prompts. Original PNGs
are retained without resizing, recolouring, cropping or background extraction.
The requested dimensions were not guaranteed by generation; use measured sizes
in the manifest. Raster assets use the repository's existing Git LFS rule.

## Contents and placement

| Family | Assets | Suggested full-canvas width in station cells |
|---|---|---|
| Ground | Silt plain | 3, repeated with alternating mirrored UV orientation |
| Terrain | Basalt shelf, trench edge, mineral outcrop | 1.5–3, 3–5, 0.5–1 respectively |
| Hazard features | Vent chimney, brine pool | 0.8–1.5, 1.5–3 |
| Ecology | Coral garden, tube worms | 0.3–0.8 |
| Wreckage | Corridor, engineering wreck, cargo, foundation frame | 1–2, 1.5–2.5, 0.3–0.8, 1–2 |
| Loose salvage | Hull fragment, pipe fragment | 0.2–0.5 |
| Water overlays | Silt plume, bubble stream, current wisp | 0.5–1.5; composite at restrained opacity |

Use the actual runtime cell size, not the bible's historical scale. Keep image
aspect ratio and the original canvas. Default placement pivot is canvas centre.
Water emitter anchors in the manifest are provisional authoring guides, not
verified particle origins. Water images are static source layers, not animation
strips. Do not rotate upright features as if their lighting and height rotated
with the ground; move their positions and preserve the overhead camera.

## Live integration

The follow-up [sub-biome pack](../sub-biomes-v1/README.md) adds six feathered
terrain regions and twelve matching scenery props through this background renderer.
The original library and sources below remain intact.

`seabed_background.gd` draws the silt and five small scenery identities before
station connectors, floors, hulls, characters and feedback. Scenery uses its own
fixed seed, never consumes the gameplay RNG, and never moves when rooms are built.
The starting anchor stays quiet, with a few small authored surroundings.
Textures load once as raw PNGs; the canvas clips the fixed tile/scenery set.
The source texture is **not certified seamless**: alternating mirrored repeats
join matching edge pixels, with some visible symmetry in the sediment pattern.

The raw-image export plugin now includes `assets/environment`. A packaged build
has not been tested in this pass. No saves, costs, occupancy, resource deposits,
damage, discoveries or clearance jobs are implemented by this scenery module.
Large hazard features and wreck structures are library assets only. Adding them
as gameplay obstacles requires authoritative placement and state rules.

## Review and verification

Generation, technical validation, native rendering and owner approval are
separate stages. Every selected image must pass the alpha/hash audit; all sprites
must have actual transparent pixels. The first trench and vent candidates used
too much front-facing height; revised sources correct their camera. The first
current candidate incorrectly included a station, and the first silt plume
included solid rocks. These original versions are retained as rejected candidates
and must not be consumed. Use `selected_source`, not a glob selecting the first PNG.

Vent v2 retains a soft exterior sediment halo and a landscape canvas; preserve
its aspect ratio and composite over dark ground. The v3 attempt to remove that
halo returned an opaque painted checkerboard and is rejected. The silt plume has
a dense granular centre: use restrained opacity when layering it as disturbance.

Run from the project root:

```powershell
python tools/audit_seabed_assets.py
# Substitute the configured Godot executable for godot below.
godot --path . --script res://tools/preview_seabed_assets.gd
godot --path . --script res://tests/playtest_seabed.gd
```

Native evidence is written under `output/seabed-v1/`. The station fixture uses
separate temporary save paths and checks stable scenery plus raw texture loading.
Window sizes are 1280×720, 1600×900 and 2560×1440. The synergy/run-loop,
discovery-progression and gameplay-polish regression suites pass. Owner visual
approval remains open; hashes and load checks do not grant that approval.

Copyright © 2026 Alex Yesilcimen. All rights reserved. See `NOTICE.md`.
