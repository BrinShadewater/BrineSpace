# utility-kit-style-v2 — refreshed collection

20 reusable decorations restyled against the established BrineSpace room art.
This revision supersedes `utility-kit-v1` for future asset use; the earlier pack remains
untouched for provenance and comparison.

## Finish and use

Maintained matte surfaces, readable pixel clusters, sparse edge highlights and
restrained functional accents replace noisy wear and glossy highlights. Keep
source aspect ratios. The local Godot helper reads `manifest.json` and raw PNGs
from `sprites/`; metadata retains intended layers and suggested scales.

Native `review.gd` exports the included previews. Utility connectors have newly
reviewed coordinates where generation moved the source artwork; inspect joined
runs for each actual placement. These are decorative parts, not guaranteed
seamless autotiles or functioning systems.

Wall strips are diagnostic mounting studies only. The current game requires low
walls: use each host's actual wall band, doors and occlusion, and do not raise a
wall to fit a sprite. Floor details stay beneath actors and furniture. No game
room or gameplay renderer was changed by this standalone asset refresh.

## Provenance and checks

`source/refresh-prompts.json` records this pass's exact built-in image-tool prompts
and references. Older prompt files are historical. The manifest records current
source/export hashes, actual sizes, crop regions and registration. New RGB sources
use the project neutral-background cleanup; reviewed gap seeds remove enclosed
background without erasing dark mechanical recesses or painted glass.

The coverage ledger and all-pack overview are under `output/art-style-refresh` in
the project. Native rendering, applicable layer/connector/bounds checks and pixel
alpha/hash checks pass. These are asset checks, not packaged-game acceptance.
