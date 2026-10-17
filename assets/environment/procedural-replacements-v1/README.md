# Original environment drawing replacements

Ten original painted masters replace six previously procedural groups: glow plants,
basalt edge faces and excavation fissures, fresh/weathered foundation fascia,
cutting sediment and detached chips, pressure-leak puffs and repair sparks, and
physical exterior lamp housings. Two neutral optical masks export the existing
light geometry; consumers retain light hue, fog occlusion and animation clocks.

`prompts.json` records generation instructions. `bake.py` creates calibrated runtime
derivatives by cropping significant-alpha bounds (16/255 plus two pixels), preserving
source color and alpha, then resampling. Basalt excludes the source's blank upper
13 percent. Masters remain untouched. `manifest.json` pins all 22 raster hashes.

Integration uses explicit paths in `scripts/environment_art.gd`, validated raw PNG
loads, cached failures and the original procedural fallbacks. Drawing preserves
terrain connectivity, placement, progress, timing, quality and reduced-motion gates.
Structure shadows, progress bars and selection outlines retain geometric drawing.

Checks: `python assets/environment/procedural-replacements-v1/verify.py` runs the
runtime loader and native fixture with scratch profiles and fingerprints the real
profile before/after. The native fixture checks all 16 rock connection masks,
read-only drawing and repeat-frame determinism; it captures an actual fogged station.
Its explicitly free-built solar arrays are an art fixture, not paid-run acceptance.
Review captures live in `output/procedural-replacements-v1/`. Source audit verifies
12 identities / 22 rasters with no unregistered candidates. Owner approval and
packaged gameplay acceptance remain separate.
