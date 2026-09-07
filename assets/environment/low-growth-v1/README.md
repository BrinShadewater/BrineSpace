# Low seabed life

Three small scenery identities expand the space between larger habitat props:
narrow seagrass rosettes, dusty rose encrusting algae, and dark mussel beds.
They are static decorative life, with no growth simulation, food yield or
collision. Mussels are marine animals; the pack combines vegetation and attached
life rather than treating every organism as a plant.

Four original PNGs are preserved. Seagrass v1 was rejected because its broad
blades resembled the existing kelp. The selected v2 has narrow blades and more
open gaps. Both algae and mussels use v1. Exact built-in image_gen prompts live
in `generation-record.json` and `revision-record.json`. No local raster cleanup,
resizing or recoloring changed the sources.

`low_growth_view.gd` adds three fixed groups within the kelp, cold-coral and sponge
habitats. The eight placements use canvas widths of 0.18–0.38 station cells and
retain aspect ratio, center pivot and camera orientation. Runtime tint subdues
source color; the smaller grass blades are deliberately subtle at distant zoom.
Existing habitat meshes, scatter positions, resources and occupancy are unchanged.
Room geometry and larger wreckage draw above these details.

`manifest.json` records explicit selected paths and original hashes. Run
`python tools/audit_environment_pack.py assets/environment/low-growth-v1/manifest.json output/low-growth-v1/source-audit-new.json`
with a new output path to verify provenance. Run
`python tools/build_environment_catalogue.py assets/environment/low-growth-v1/manifest.json`
to rebuild the catalogue after verification. Native dimensions and alpha counts
are in `output/low-growth-v1/source-audit.json`.

`tests/playtest_low_growth.gd` passes: three selected alpha sprites, all three
groups at 1280×720, 1600×900 and 2560×1440, actual capture dimensions, unchanged
occupancy and resources. `output/low-growth-native.log` contains the result.
The source sheet and representative station captures were visually reviewed:
transparent exteriors, complete silhouettes, fine grass distinct from broad kelp,
low algae relief and subdued shell clusters. Owner approval remains pending.

The seven-biome fixture also passes after the source-ledger migration; see
`output/biome-ledger-native.log`. Native checkout verification is not packaged
release verification. PNGs inherit Git LFS and the existing environment raw-PNG
export bridge. Rights remain governed by NOTICE.md.
