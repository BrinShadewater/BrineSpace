# Finite harvest artwork refresh

Three original purpose-built paintings replace reused early study sprites in
the extraction renderer: low manganese nodules, a collapsed grey/ochre service
frame and a torn graphite cable harness. Other habitat/wreckage selections are
outside this batch. Exact built-in imagegen briefs are in prompts.json.

Selected: mining-v1, frame-v2, cable-v1. Four immutable masters and three runtime
exports are registered by SHA256 in manifest.json. Frame v1 was rejected for
its oblique side faces; v2 corrects the camera to the overhead station perspective.
No synthetic painting, colour grading, mirroring or stretching. bake.py checks
master hashes, crops fully transparent margins and resamples isotropically once
to 512px width. Repository PNG assets use Git LFS.

scripts/harvest_site_art.gd names the three whole runtime paths. Existing physical
widths (.48/.30/.34/.23 cells), cluster positions, tint, shadow, survey corners,
load labels and whole-piece depletion remain unchanged. Site capacity, rewards,
collision/buildability, power use, discovery, pause and save behavior remain
owned by the existing finite-harvest logic.

Native review: output/harvest-refresh-v1/native-depletion.png shows both kinds
at 24/18/12/6/0 remaining loads, using 190px cells (largest piece 91.2px wide),
plus individual sources at 95 physical pixels. Station captures use production
underwater light/fog at .25/.45 zoom and centred .65 close-ups. Native checks
verify actual source textures/alpha, explicit bindings and exhausted buildability.
tools/verify_harvest_refresh.py runs scratch APPDATA/LOCALAPPDATA and the existing
stock conservation/survey/depletion/pause/save/detour test. Agent visual review
is separate from owner approval and actual release packaging.
