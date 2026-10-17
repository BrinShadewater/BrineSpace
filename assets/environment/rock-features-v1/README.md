# Decorative seabed rock features

Three original built-in imagegen paintings add a fissured slate slab, low layered
shale ridge and porous basalt pockets. Matte grey/umber surfaces, restrained
mineral threads and overhead silhouettes match the current ocean floor.
Exact generation prompts are in prompts.json; the ridge camera correction is
preserved in layered-ridge-v2-prompt.txt. Ridge v1 is retained but rejected for
oblique projection and tall visible side walls. Ridge v2 uses shallow top faces.

Four immutable masters and three 512px runtime exports are hashed in manifest.json
with dimensions and centred pivots. bake.py verifies source hashes, crops
significant-alpha bounds with two-pixel padding and resamples isotropically once.
It preserves retained alpha and colours without painting or grading. PNGs use LFS.

rock_feature_view.gd caches three whole-path textures. site_scenery.gd selects
original/split/layered/porous artwork through a fixed coordinate/family calculation
at existing rock placements. Original rocks remain selected for one of the four
outcomes. Widths .20-.38 cells, tint, small companion stones and positions stay
consumer-owned; timber families retain their selections. No RNG, save format,
navigation, collision, resource or mining behavior changes. Variants are decorative.

Native review: output/rock-features-v1/native-rocks.png compares 120px sources
with 95px source/tinted/pale/dark samples. Station captures at .25/.45 zoom and
.65 close-up use production Scenery rendering and underwater light/fog. The
fixture chooses coordinates that exercise all three variants through the actual
selection helper; it checks deterministic selection, unmodified placement data,
all four outcomes, unchanged timber families, alpha/512px loading and occupancy.
verify_rock_features.py uses scratch APPDATA/LOCALAPPDATA and owner fingerprints.
Agent review is complete; owner visual acceptance and release verification remain
separate. This fixture does not prove visibility in every seeded expedition.
