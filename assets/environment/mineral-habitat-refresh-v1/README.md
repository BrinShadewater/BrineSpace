# Sulfur and brine habitat replacements

Three original built-in imagegen paintings replace the early anhydrite vent,
bacterial mat and salt plate studies. Matte grey mineral collars, ochre/cream
growth and thin fractured salt plates use the overhead seabed camera. Exact
prompts are preserved in prompts.json, and unchanged generated masters remain
alongside exports. No generated source was recoloured or repainted locally.

bake.py verifies immutable master hashes, crops significant-alpha bounds (>=16)
with a two-pixel margin and resamples isotropically once to 512px width. Remaining
alpha and colour are preserved. manifest.json registers three masters and three
runtime sprites with SHA256, dimensions and centred pivots. PNGs use Git LFS.

sub_biome_view.gd binds three whole runtime paths. Existing .3-.65-cell widths,
seeded placement, sediment textures, underwater tint and static rendering remain
unchanged. Art creates no occupancy or collision and changes no gameplay rules.

Native comparison: output/mineral-habitat-refresh-v1/native-comparison.png shows
old/new source/new tinted/dark-seabed samples at 120 physical pixels. Production
station captures cover .25/.45 zoom and .65 salt close-up. Bacterial growth is
intentionally quieter against sediment than the pale vent and salt crusts.
tests/review_mineral_habitat_refresh.gd checks 21 loaded habitat textures, alpha,
512px widths, explicit bindings, deterministic placement and static salt pixels.
tools/verify_mineral_habitat_refresh.py uses scratch APPDATA/LOCALAPPDATA and
fingerprints the owner profile. Agent native review is complete; owner visual
acceptance and playable export verification remain separate.
