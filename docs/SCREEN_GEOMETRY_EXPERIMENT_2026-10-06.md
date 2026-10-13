# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: screen geometry caching

## Objective and acceptance

Reduce measured room drawing cost without changing appearance, animation timing,
layer order, quality or owner layouts. Overall release performance remains open.

## Accepted decisions and constraints

**Do not admit either screen-cache prototype.** Reusing fixed geometry inside
existing slots preserves pixels but does not reduce measured station callback cost.
Normal runtime and permanent tests/index remain unchanged. No export or profile
writes outside verified scratch folders.

## Current state

Private frozen libraries/content, generators, direct tests, station fixtures and
rejected diagnostic logs in `output/screen-geometry-2026-10-06/`.

First version caches screen rectangles, inner bounds/grid lines, radar centres,
radii/blips, colour and width with per-draw input validation. Original native arc
API remains; no extra CanvasItems. Revision uses prop identity plus the existing
submit invalidation branch to avoid repeated value-key construction/comparison.
Dynamic commands and their ordering remain unchanged.

## Verification

First direct native version: 665 checks / 462 exact raster pairs. Revised final:
668 checks / 462 exact pairs, zero failures/errors. Coverage includes 179 current
metadata registrations dry/flooded; synthetic overlapping screens, operating state,
clocks, Reduced Motion, filtering, affine tint, mirroring, screen/colour/rect edits,
clock-only cache reuse and actual submit invalidation of same-object layout edits.
Not complete prop-artwork, Studio, lifecycle or packaged visual acceptance.

Rejected revision fixtures retained. Initial submit fixture inherited a legacy
copy-source ID; after fixing that, direct state inspection showed an empty view
snapshot because it preassigned `renderer` before first submit. Removing that
assignment lets the normal initialization path collect state fields. No runtime
code changed to satisfy a fixture.

Both matched 40-room station pairs explicitly preload physical candidate content;
runtime guards require populated caches and hits in every measured phase.
1080p idle/pan at 1/2/4x, 60 samples per phase, private compressed crew:

| Phase | Revision baseline content ms | Revision candidate content ms |
|---|---:|---:|
| Idle 1x | 3.077 | 3.295 |
| Pan 1x | 2.970 | 3.112 |
| Idle 2x | 3.074 | 3.223 |
| Pan 2x | 3.141 | 3.309 |
| Idle 4x | 3.946 | 3.354 |
| Pan 4x | 3.154 | 3.332 |

Five revision phases regress ~0.14–0.22 ms; one opposite outlier is insufficient
evidence of benefit. First version also slower in all six phases (~0.10–1.47 ms).
Revision 115 cached slots, 167→185 builds, 27629→62111 hits; cache execution and
reuse are proven, not inferred from green tests. Variant dictionary access and
additional routing remain potential costs, not separately attributed findings.
Do not claim the cache-key comparison alone caused the initial regression.

Frame results mixed and still fail: revision p95 37.544–52.051 ms versus 16.7 ms
target. No aggregate FPS improvement. Both pairs have all six actual crew/drone
snapshots, powered-room counts, zoom and texture counters equal; final 3168.333
MiB unchanged and above the large-scene budget. Successful logs clean and all
2936 owner non-log files unchanged, including rejected isolated fixtures.
All native processes terminal.

## Next action

Stop pursuing monitor preparation caches as the main remedy. Investigate the
larger measured room-content renderer cost: ordinary library body/contact-shadow
polygon submissions, with ordered mesh preparation where justified. Room lighting
already has its own contact-shadow batching; that is separate from library
silhouette shadows. Preserve exact blend/order/filter output and assert candidate
execution in matched workloads. No further general cache/refactor changes without
measured benefit. Memory/loading, lifecycle, original bug rechecks, endurance and
packaged Windows/Mac acceptance remain open.
