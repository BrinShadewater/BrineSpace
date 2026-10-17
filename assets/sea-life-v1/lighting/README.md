# BrineSpace lighting batch 2

September 29 style pass: painted-v2 caustics replace the dense photographic web
with broad, diffuse islands and quieter gaps. Shaft centres/widths and bubble
rims have subtle irregularity; the beacon has fine 24-band Bayer modulation.
Six textures changed. Warm/cool lamps and wide pool remain identical. Runtime
color, size, pivots and timing are preserved. Previous rasters, bake and native
captures remain in review/before-style-20260929. Both generated sources remain.
See review/style-pass.jpg and review/style-audit.json for comparison and measured
world-scale density. The audit also reviews retained sea-life treatment.

Nine PNGs: warm/cool lamp halos, wide floor-pool study, three surface shaft
studies, seamless caustics, four-cell hull bubble atlas and directional beacon.

Installed: warm/cool lamps, caustics, hull bubbles and beacon. Wide floor-pool
and all three shaft variants remain review-only; the existing surface shafts
stay procedural until the owner chooses them. Existing lamp tint, brightness,
0.30 alpha, bubble placement/radius/clock/fade and quality rules remain intact.
The beacon retains its four-second turn, orbit and two-second pulse. Caustics
scroll from clock times motion, so Reduced Motion holds them still.

The halo extends the existing code-native Bayer light rather than introducing
a different finish. The caustic source uses built-in imagegen; all other shapes
are deterministic extensions of existing procedural art. Exact provenance and
algorithms live in prompts.json, with dimensions, pivots and hashes in manifest.
No baked lighting color on halos or beacon. Bubble rims retain their original
pale blue and white highlight. Runtime caustic color and strength are unchanged.

Rebuild: `python assets/sea-life-v1/lighting/bake.py` (Pillow, NumPy).
Raster checks: `python assets/sea-life-v1/lighting/validate.py`.
Godot checks and native screen-2 captures: `python tools/check_lighting_art.py`.
The runner isolates APPDATA/LOCALAPPDATA and fingerprints the owner profile.

Runtime loads whole literal paths through SafeImage.raw_texture, validates
dimensions and warns once per failed texture. Each drawing retains its original
procedural fallback. Sources and review sheets are authoring-only; the release
manifest ships the five installed PNG files, excluding review-only variants.

Review: review/contact-sheet.jpg and review/native/ for native-rendered comparisons.
