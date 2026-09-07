# BRINE sub-biome terrain and scenery

Current provenance contract: `source-ledger.json` is the immutable expected-hash
and selection input. `manifest.json` is derived audit metadata. The migration
copied previously recorded hashes after verifying every existing source; it did
not accept changed bytes as a fresh baseline. The runtime now uses an explicit
`SOURCES` map checked against the ledger. `tools/audit_sub_biomes.py` validates
that ledger before writing its catalogue or derived manifest. A hash mismatch
stops the rebuild; unregistered candidates cannot silently enter the pack.
`output/biome-ledger-native.log` confirms all seven habitats still pass native
checks at three verified resolutions after this migration. Earlier audit wording
below describes the historical workflow.

Seven reusable habitat sets, each with a ground material and two scenery assets:

| Habitat | Ground | Props |
|---|---|---|
| Sulfur vent basin | Charcoal volcanic grit with ochre mineral staining | Anhydrite mouths, bacterial mat |
| Sponge reef | Green-grey calcareous rubble and shell grit | Vase sponges, spreading sea fans |
| Brine salt flats | Cold mud and pale fractured salt crust | Salt plates, encrusted seep stones |
| Kelp meadow | Olive-grey sand and short seagrass stubble | Ribbon kelp, exposed holdfast |
| Cold coral garden | Rose-grey sediment and crushed coral fragments | Ivory lace coral, cup coral cluster |
| Manganese nodule field | Charcoal abyssal mud with small mineral nodules | Nodule cluster, brittle stars |
| Iron seep | Rust-stained grey-brown sediment | Mineral ledges, pale hydroids |

The iron-seep expansion adds three original sources, bringing this pack to 21
selected identities and 24 preserved PNGs. Exact built-in image_gen prompts are
in `iron-seep-record.json`. Its fixed region is centered at (30,11); the original
six regions and their random placement sequence remain unchanged. Hydroids are
static scenery. Mineral ledges are decorative and do not replace rock blockers.
The audit pins source versions to runtime choices rather than promoting the
latest filename. Unselected new candidates remain unreviewed.

`output/iron-seep-native.log` records a successful native pass: all 21 textures,
stable placement, blend masks, seven habitats at three verified resolutions,
and station layering. The source sheet is `asset-sheet-3.png`; in-game evidence
is `iron-1280.png`, `iron-1600.png`, and `iron-2560.png` under the output folder.
Source and native visual review passed; owner approval and release export are
separate. Prior batch descriptions below remain historical evidence.

`index.html` is the filterable local catalogue. `generation-record.json` preserves
exact built-in image_gen prompts, including camera revisions. `manifest.json`
records measured dimensions, alpha, original source hashes and selected files.
Sources remain unchanged: no resizing, recoloring, cropping or alpha extraction.
The second batch's exact prompts are in `expansion-record.json`. It adds nine
new identities; the first batch and its selected revisions remain unchanged.
The upright v1 chimney/sponges/fans are retained as rejected sources; runtime
uses their v2 revisions. The mineral mouths retain some visible south-facing
height; sponges and fans have a stronger overhead footprint.

## Terrain use

These are ground materials plus transparent scenery sprites, consumed by a
small Godot terrain renderer. They are not a prebuilt TileSet resource or a
47-tile atlas. The renderer provides the repeated material and soft transition
geometry needed for the current station canvas.

`sub_biome_view.gd` uses quarter-cell mesh vertices, continuous world texture
coordinates and irregular feathered borders. Mirrored four-cell material spans
join matching source edge pixels. Source art is not certified seamless; mirrored
repetition can be visible in large patches. Transition alpha is generated at
runtime, so the same source can be used for different region shapes and sizes.

Props use the original canvas and aspect ratio, centered pivot, no rotations,
and full-canvas widths of 0.3–0.65 standard station cells in the live background.
They are tinted for subdued underwater placement. The catalogue shows original
source color, while the native station captures show the actual game tint.

## Live integration

The seabed background now draws six fixed habitat regions over the existing
silt and beneath wrecks, rock blockers, and all station layers. Each region uses
only its matching props. Placement has a private fixed RNG seed and is unchanged
by room building, pauses or redraws. The two-cell area around the core stays free
of these new props. Existing scenery remains available.

The newer regions sit around cells (10,26), (29,26) and (20,9), respectively.
Appending them after the first three regions preserves the original regions'
random sequence and existing prop placements. Kelp and brittle stars are static
scenery in this pass; they do not imply simulated growth or creature behavior.

This pass adds decorative terrain. It does not add hazard damage, collision,
resource yields, discovery contacts, or variable map generation. Existing rock
and wreck clearance rules remain authoritative. The regions appear visually in
existing runs too, without modifying their save data or buildable cells.

The raw PNG export bridge already includes `assets/environment`; release export
is not verified by this pass. PNGs inherit Git LFS tracking. See `NOTICE.md` for
rights.

## Reproduction

Run `python tools/audit_sub_biomes.py` to audit sources and rebuild the catalogue.
Run Godot with `--path . --script tests/playtest_sub_biomes.gd` for the native
asset sheet and station captures under `output/sub-biomes-v1/`. The fixture uses
isolated settings and save paths, checks all eighteen texture loads, deterministic
prop placement, center/outer mask values and actual capture dimensions at
1280×720, 1600×900 and 2560×1440 for each habitat. Normal rooms are included as
scale and layering references.

Visual review covers ground transitions, transparent prop exteriors, overhead
readability and station contrast. Technical checks and visual review are distinct
from owner art approval and full-run biome pacing feedback.

The first batch passed its source/native checks and synergy/run-loop, discovery
progression, gameplay polish and rock-clearance suites. Those checks exposed a missing
null guard in summary-button focus for UI-light fixtures; the guard now skips
focus when no button exists.

The expanded pack passes the source audit with eighteen selected identities
from twenty-one preserved sources. `output/sub-biomes-expanded-native.log`
records the successful six-habitat fixture at all three resolutions, and
`output/biomes-expanded-rock-clearance.log` records a passing clearance/save/
paid-build regression. The second native asset sheet is `asset-sheet-2.png`.
