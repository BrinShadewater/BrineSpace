# Active drone texture memory

Updated: October 5, 2026 · BrineSpace release readiness

## Objective and acceptance

Identify storage outside the shared crew/room pools and choose a measured remedy
without changing selected art, animation timing, filtering or rendered pixels.

## Accepted decisions and constraints

Keep frozen candidates unchanged. Use isolated profiles and bounded diagnostics.
Do not force a cache limit that evicts images still needed by visible animation.
No runtime atlas repacking, frame removal, cropping or quality reduction accepted.

## Current state

A diagnostic-only explicit-root walker visits 49,172 values in 40.441 ms without
truncation. It excludes live pool images, unwraps CanvasTexture/AtlasTexture
references, and never reads GPU pixels or calls lazy room getters. It covers
named player banks and grid textures plus drone, library, floor, environment,
portrait, wreck, harvest and seabed caches. It is not a complete resource graph.
Figures below are RGBA8 base-size estimates except the independently verified
drone cache bookkeeping:

| Owner | MiB |
|---|---:|
| Drones | 1,148.99 |
| Room cards | 79.00 |
| Prop library | 71.77 |
| Floors | 59.99 |
| Wrecks | 32.00 |
| Seabed root | 23.99 |
| Door animation | 18.19 |
| Environment cache | 15.29 |

A second 40-room run records 18 drone cache entries and **1,204,798,352 decoded
bytes**, matching the estimate. Every entry was touched one frame earlier; zero
stale bytes under the existing two-frame criterion. The 256 MiB budget is soft
when the active set exceeds it. This observation does not justify an eviction
patch or identify a leak. Both current-source runs retain the same raw engine
total of 5,139.36 MiB; they are diagnostics, not frozen-release performance tests.

Offline full-cell RGBA hashing of 11 resident atlases finds **583.41 MiB of
duplicate cells**. The 120-cell `collect-south.png` has one unique image. Keeping
all animation steps and remapping this sheet to one full-size cell was tested
separately: **30/72 native comparisons match, 42 differ** across source-cell
indices, nearest/linear filters, scales and fractional/half-pixel positions.
The storage alternative is rejected under the pixel-parity gate. Potential
savings are not achieved savings. The cause of sampling differences needs a
specific explanation before another remapping approach is tried.

Added maintained report diagnostics in `scripts/drone_animation.gd` and
`scripts/performance_monitor.gd`: decoded cache bytes, soft budget excess,
recent/stale classification, upload counters and explicit completeness/scope.
Collection is report-time only, capped at 4,096 classified entries; it performs
no evictions, GPU reads or recency updates. Coverage added to
`tests/test_drone_runtime_animation.gd`. Runtime art/drawing behavior is unchanged.

Evidence and reproducible helpers: `output/pool-inventory-2026-10-05/`, especially
`nonpool-summary.json`, `drone-age-summary.json`, `drone-cell-audit.json`, and
`drone-repeat-render.json`. Experimental walkers/renderers stay in that directory.

## Verification

Native drone regression: 252 clips, 144 directional phase samples, dock boundaries
and new report accounting/integration checks; zero failures or engine errors.
All native runs retain 2,936 owner non-log files unchanged. No release export,
public upload or accepted memory/frame-time improvement in this milestone.

## Next action

### Sampling diagnosis and accepted empty-frame draw omission

Further October 5 inspection: the worst captured nearest comparison changes 278
pixels. Differences cluster at screen x=93 and y=166/239, mapping to exact source
boundaries 100/200/300 under the test transform. Linear differs by at most 1/255.
Exact engine GLES3 source normalizes region UVs by texture dimensions, interpolates
them, and clamps to half-texel limits before sampling. This supports a coordinate
rounding explanation, not missing or altered authored pixels. A control keeps the
**original atlas on both sides**, comparing equal-pixel cell zero to other cells;
30/72 comparisons still differ. Inspection captures and `sampling-differences.json`
are retained. These results do not establish a portable exact-remapping remedy.

Accepted a smaller rendering optimization instead: verified empty frames 0–44 and
135–179 in all four mining-effect sheets now omit their draw command. Frame
selection, timing, PNGs, UVs of visible frames, texture preparation, cache recency
and residency remain unchanged. Texture acquisition deliberately precedes the
skip, preventing new decode gaps or eviction churn before the next visible frame.

Changed: `scripts/drone_animation.gd`,
`assets/drone-runtime-2026-09-26/mining.json`, and new Python regression
`tests/test_drone_empty_frames.py`. The manifest differs only by four
`emptyFrameRanges` fields; all source image hashes match. No atlas conversion.

Verification: all 720 source cells checked (360 transparent). Native matched
before/after test covers four directions, both filters and six boundary frames:
**48/48 pixel-exact**, including the previously sensitive half-pixel position at
0.73 scale. Empty cases go from one draw to zero; visible cases remain one. Total
commands in this intentionally boundary-weighted test fall 48→16. Across a whole
180-frame mining effect cycle, 90 effect draws are avoided, not half the game's
draws. This establishes reduced rendering work, **not FPS or texture-memory gains**.
252-clip/144-directional-sample regression plus cache-report integration passes.
All 2,936 owner files unchanged. `empty-fix-summary.json` records the accepted scope.
Python source validation: `python -m unittest discover -s tests -p test_drone_empty_frames.py`.

### Remaining work

Measure this accepted draw omission in the next matched station/package comparison;
do not rebuild the release solely to imply the major memory gate is solved. Exact
storage remapping remains unresolved. Independently extend the
explicit inventory to nested seabed materials and room-owned wall pools, which
were outside this pass. Maintain separate raw engine and decoded byte figures.
Windows kernel trace, minimum hardware, native Mac certification and all failing
release gates remain open.
