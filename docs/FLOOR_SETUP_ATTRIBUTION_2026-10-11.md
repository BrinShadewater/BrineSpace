# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: attribute structural floor setup costs

## Objective and acceptance

Continue full performance/release plan. Identify structural redraw costs before
changing floor/room behavior. Preserve exact owner layouts, shading, layering,
animations and gameplay. No production optimization admitted in this pass.

## Accepted decisions and constraints

Muted secondary native debug=false executable, isolated profiles and owner
fingerprints. Reuse runtime; no screenshots or full copies. Accepted station
target-sort optimization included in both lanes. Test-only deterministic mining
warning clock unchanged. Keep full original gates open.

## Current state

Private grid overlay labels existing _draw_nursery timers by floor/shell/live.
No rendering branches, inputs or commands changed. Private trace adds the scoped
draw counters for each frame. Production grid and Bill hashes unchanged:
grid e4bdb79b4413bfdd21f4b0c3c9af51a8c8835cb158e8254d8cbb98d33fe966cf;
Bill 6888fceaf6e24998d4e82bd6311240c9fa4d558825dff24183720bd83f99d193.
Runner: output/renderdoc-tools-2026-10-08/run-floor-setup-attribution.py.
Evidence: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
floor-setup-attribution/analysis.json, scoped source, reports and owner.json.

## Verification

Two native 40-room runs/3240frames, lighting/connected placement/successful
demolition1x/2x/4x. All nine full states/cameras and fifteen paired successful
action events exact. Runtime source guards verify control/profile lanes.
These are attribution runs, not FPS improvement or release certification.

Six structural action-frame30 samples show floor-pass costs:

| Work | Range ms |
|---|---:|
| Equipment shadows |3.237–3.705|
| Room configuration |2.272–2.739|
| Room floor render |2.386–2.826|
| Door preparation |1.260–1.583|
| Light pools |0.696–0.873|
| Actor preparation |0.446–0.518|
| Companion preparation |0.106–0.129|

Aggregate counters include multiple rooms; timing scopes overlap broader floor
and frame counters. Do not add these to total draw time or claim saved time yet.
The largest measured target is shadow work, rather than actor preparation.

Source inspection: RoomLighting.draw_equipment_shadows already retains bounded
projected geometry and room packets. Every call still builds prop feet, visual
rise, contact bands, geometry key and palette; palette changes replace colors.
Therefore another cache or removing actor preparation is premature. Attribute
preparation/key lookup/palette/submission separately before choosing a remedy.
Live props, owner layout changes, lighting/StyleBox rounding and oversampling
fallbacks must remain valid. No broad renderer or art changes.

Owner2938 files unchanged; jobs terminal, runtime override restored. Two completed
trace reports11860466→5111808bytes allocated; content hashes before/after exact.
No owner/runtime compression/deletion. Last free-space checkC134.86/D68.72GiB.
Headless/manifest/pixel/target hardware/Mac/endurance gates not certified here.

## Next action

Bounded shadow-stage attribution in the same guarded native workload. Determine
whether cost is repeated prop/band preparation, nested-key lookup, tessellation,
palette rebuild or command submission. Then test a specific measured remedy with
exact pixel/geometry checks and matched real-station replays. Preserve the accepted
crew/zoom optimizations and keep frame, memory, loading and full release gates open.
