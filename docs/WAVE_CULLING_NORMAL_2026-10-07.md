# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: complete-motion wave culling

## Objective and acceptance

Continue full PC/Mac performance readiness. Avoid preparing waves entirely outside the view without changing visible pixels, animation clocks, quality or simulation. Accept only with native visual parity and a matched actual-station preparation saving.

## Accepted decisions and constraints

Normal live line pass now culls whole waves using all-clock bounds: cell x span and y centre .45 ± .12, padded by max(2 pixels, .02 cell size) for rectangle thickness, rotation and sampling. Existing cell-range selection remains. Static haze and combined `all` drawing stay unchanged. `--draw-all-rooms`, custom material and parent-material paths retain original drawing. No new textures, geometry caches, nodes or simulation changes.

## Current state

- `scripts/grid_canvas.gd`: five-line preparation/bounds addition, identical to the measured private candidate after removing its duplicate-class declaration.
- New paired `tests/test_water_wave_culling.gd`/UID `uid://d1p7m4q9v2s6k`, unique in scoped source; native render subsystem registration in `tests/index.json`.
- Existing water fixtures now explicitly provide broad view rectangles for their fake clock contexts: `tests/water_depth_fixture.gd`, `tests/test_water_wave_commands.gd`. Their original pixel scope remains.
- Evidence and preserved before/installed source hashes in `output/wave-culling-2026-10-07/`. Other dirty source preserved. No refreshed export or upload.

## Verification

Private/native and installed culling checks each pass486 exact nonblank image pairs across source/null/AtlasTexture, nearest/linear, custom/parent/default materials, three cell sizes, negative/fractional/distant views and three clocks. Installed existing command checks288 exact pairs and preparation147 checks/144 exact pairs also pass. Total918 installed exact pairs, zero errors/leaks/warnings. Selected native wave capture and actual station candidate capture inspected; low-alpha isolated wave capture is visually faint, machine equality establishes parity. JSON registration, scoped whitespace and unique UID checks pass.

Matched actual-normal/private candidate 40-room idle/pan at1×/2×/4×: all six full crew/drone/zoom/power/door/light states and texture endpoints equal. Wave callback1260.53→1096.98,1245.70→1039.60,1249.85→1053.17,1251.35→1072.65,1257.83→1047.53,1250.68→1062.53 microseconds. Consistent0.164–0.210ms/frame preparation saving. Effective renderer calls essentially unchanged: engine already rejects offscreen output; no GPU/batching benefit claimed. Whole p95 mixed37–55ms, frame gates fail. Ready12.51/12.60s and textures3.63–4.29GiB unchanged; loading/memory gates not closed.

Initial probe accidentally gave its Control a zero-sized clipping extent; both controls blank at positive origins.324 failures preserved as `probe-blank-fixture.log`, excluded. Set explicit5000×5000 grid extent and reran; all486 nonblank pairs pass. No production defect inferred from that fixture failure.

All2,936 owner files unchanged in private, station and installed checks. All process handles terminal. No packaged-game, endurance or Mac certification from these checks.

## Next action

Prioritize larger measured room preparation work and renderer submission rather than further micro-batching of water. Trace the6ms live-room preparation scope into state construction and repeated invalidations, preserving crew/dock/large-room behavior; test the largest measured avoidable work. Private memory-provider admission, full inventories, original nine packaged issues, long native endurance, refreshed Windows candidates and actual Mac certification remain open.
