# Draft utilities and Archived Data badge

Generated October 1, 2026 with the built-in image-generation tool, transparent
4-by-2 master at `atlases/draft-controls.png`. Reading order: hide hand, show hand,
fan, row, frame off, frame on, reroll, Archived Data. Matte gunmetal, muted petrol,
cream cards and ochre archival badge, matching the current illustrated hull UI.

Native Godot slicing trims transparent bounds, fits each glyph into 112 pixels,
then centers it on a transparent 128px canvas using Lanczos resampling directly
from the full atlas. Runtime draft controls display these masters at 30px with
linear filtering. Whole literal paths are in `scripts/ui_icons.gd`; resource
BBCode uses the same Archived Data source. PNGs retain Git LFS attributes.

Source original: exec-b6ee3aed-b980-47e8-aa5a-a78aa2cdb5f9.png.
Tooling, slicing report, native captures and original script backups:
`output/ui-refinement-2026-10-01/`. Standard Godot remaps were generated in a
minimal scratch import project for these eight new textures.
