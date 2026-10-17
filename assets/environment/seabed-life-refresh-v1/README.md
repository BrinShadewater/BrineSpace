# Seabed life replacements

Three original overhead paintings replace early kelp holdfast, brittle-star and
iron-seep hydroid studies. Root contacts, five articulated arms per star and
feathered hydroid branches provide clearer species silhouettes without large
rock bases. Exact built-in imagegen briefs are preserved in prompts.json.

Selected: holdfast v1, brittle stars v1 and hydroids v1. The second hydroid study
is retained but rejected for skeletal branching. Evaluate transparency with an
actual alpha composite: raw previews can make transparent branch gaps look filled.
manifest.json registers four immutable masters and three runtime exports by SHA256.
bake.py checks source hashes, crops significant-alpha bounds (alpha >=16) with a
two-pixel margin and resamples isotropically to 512px width. It preserves remaining
alpha and source colours; no repainting, grading or stretching. PNGs use Git LFS.

sub_biome_view.gd binds three whole runtime paths. Existing .3-.65-cell sizes,
seeded distribution, habitat sediment, underwater tint, occupancy and gameplay
remain unchanged. Hydroids keep the shared ambient_fronds motion and Reduced
Motion behavior. Old art remains available.

Native review: output/seabed-life-refresh-v1/native-comparison.png shows old/new
source/new tinted/dark-seabed samples at 120 physical pixels. Station captures
use production light/fog at .25/.45 zoom and a .65 hydroid close-up. The focused
fixture checks all 21 habitat textures, alpha, bindings, deterministic placement,
actual moving hydroid pixels and their Reduced Motion freeze. The runner isolates
APPDATA/LOCALAPPDATA and fingerprints the owner's profile. Agent review is complete;
owner visual acceptance and release-export verification remain separate.
