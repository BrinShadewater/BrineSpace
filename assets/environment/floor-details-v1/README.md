# Small ocean-floor remains

Three original built-in imagegen paintings add sparse shell fragments, empty
urchin tests and abandoned calcareous worm tubes. Matte bone/umber materials,
overhead silhouettes and fine restrained detail match the current seabed.
Exact initial briefs are in prompts.json; the second tube brief is preserved
in worm-tubes-v2-prompt.txt. Tube v1 is retained but rejected for upright,
barnacle-like shapes. Selected tube v2 uses low curved tubes; its visible tube
count differs from the prompt and is not a gameplay requirement.

Four immutable masters and three 512px runtime exports are recorded in the
SHA256 manifest, with dimensions and centred pivots. bake.py verifies source
hashes, crops significant-alpha bounds with two-pixel padding and resamples
isotropically. No local painting, grading or retained-alpha thresholding.
Repository PNGs use Git LFS.

floor_details_view.gd names whole PNG paths and caches three textures. It anchors
one cluster beside the first existing prop in each applicable biome: shells in
brine, tests in nodules and tubes in sulfur. Widths .24/.20/.22 cells respectively,
offset .32/.23 cells. These smaller details inherit the existing underwater tint
and draw beneath station geometry. Existing habitat positions, random sequences
and saves are untouched. No occupancy, resource, collision or discovery behavior.
sub_biome_view.gd invokes the renderer after its existing habitat props.

Native review: output/floor-details-v1/native-details.png compares 120px source
with 60px source/tinted/pale/dark samples. Station captures at .25/.45 zoom and
.65 close-up exercise production fog/light; controlled lighting exposes all
three details. Tests verify texture/alpha, deterministic three-cluster placement,
empty/duplicate input behavior, unchanged original placements and room occupancy.
verify_floor_details.py isolates APPDATA/LOCALAPPDATA and fingerprints the real
owner folder. Agent visual review is separate from owner and release acceptance.
