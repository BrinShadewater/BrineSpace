# Industrial menu switches v1

12 Godot AtlasTexture assets: slide, rocker, lever and push, each in off/on/disabled states. Dark petrol housings, desaturated steel edges, muted sage and amber indicators match the existing menu references. No baked text.

Load e.g. `res://brineui/industrial-switches-v1/slide-off.tres`. For a TextureButton, set toggle_mode=true, texture_normal=off, texture_pressed=on and texture_disabled=disabled. Use explicit labels and keyboard focus styling in the consumer. These are fixed-size illustrated controls, not nine-slice panels; preserve aspect ratio. Start around 120-180 logical pixels wide. Separate hover/focus art is not included.

The atlas has an **opaque dark backing**, not transparent alpha. Use it against dark menu panels. State housings share registered frame sizes, but generated mechanical details vary slightly between states. Menu integration and final state-transition review remain separate from source approval.

`atlas.png` is the corrected production source, unchanged after generation. `source-v1.png` is retained only as a rejected checkerboard-backed source. `manifest.json` records all 12 pixel regions and the source hash. `prompts.txt` records both exact built-in image_gen prompts. References: terminal_button_normal.png and panel_medium_horizontal_9slice.png from the parent folder. Raster files use Git LFS.

Review: run Godot with --path . --script res://tests/review_industrial_switches.gd for the native atlas contact sheet. No live menu controls were replaced in this asset-creation pass.
