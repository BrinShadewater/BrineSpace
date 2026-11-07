# Reusable room floor dressing

16 separate transparent PNGs for Engineering, Medical, Science, Cargo, Operations,
Command, Habitation and Cultivation. All use a top-down floor projection and are
intended to render beneath furniture and crew.

| Department | Pieces |
| --- | --- |
| Engineering / wet service | bolted access plate, linear drain, round inspection hatch, tread service mat |
| Medical / Science | bedside mat, lab access panel, boot-scrub tray, hollow specimen alignment ring |
| Cargo / Operations / Command | cargo corner markings, pallet locating plate, threshold tread strip, briefing mat |
| Habitation / Cultivation | woven bedside rug, oval braided rug, plant drip tray, connected irrigation drains |

## Use

`sprites/` contains original-resolution RGBA cutouts. `manifest.json` declares
source regions, hashes, pivots, suggested sizes, departments and placement notes.
`floor_dressing.gd` caches PNGs and draws them with their aspect ratios intact.
Call it from the room floor pass:

```gdscript
const Dressing=preload("res://assets/floor-dressing-v1/floor_dressing.gd")
Dressing.draw(painter,"medical_bedside_mat",Vector2(-90,70))
Dressing.draw(painter,"linear_drain",Vector2(110,-40))
```

The default widths range from 32 to 66 units in the game's 384-unit room space.
Use nearest filtering. Place rugs under a bed/reading/seating activity, trays under
plant containers, service mats beside machines and markings around real work or
cargo positions. Avoid scattering them in empty floor simply to fill space.
These are decorative assets, not collision objects or resource-producing rooms.
No gameplay room placement has been changed by creating the kit.

## Production and review

The existing floor-utility sheet supplied pixel/material guidance. The exact
generation prompt and untouched RGB atlas are in `source/`; the requested
1536-square sheet returned 1254 square. `build_assets.py` extracts reviewed regions
using the project's connected light-neutral cleanup, preserving aspect ratio and
interior materials. This is source-derived cleanup, not painted replacement art.

The alignment ring needed five explicit background seeds: its open center and
four independently enclosed sectors between the rings. A single sector seed left
white wedges, caught in the native review and corrected. The cargo marking center
clears through its open gaps. Bright clinical panel surfaces remain intact.

`preview.png` is a native Godot gallery at recommended 1x placement size and 2x
detail size. `review.gd` checks all sixteen texture dimensions, layer metadata and
suggested scale bounds. It uses an isolated canvas without player saves. PNG
alpha, source/output hashes and hollow marking centers are also verified during
production. Evidence: `output/floor-dressing-v1.log`. Actual room placement still
needs local clearance/composition review; no packaged-game export is claimed.
