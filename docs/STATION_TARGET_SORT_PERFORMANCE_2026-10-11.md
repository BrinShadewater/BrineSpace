# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: reduce measured crew destination sorting cost

## Objective and acceptance

Continue the full performance/release plan. Reduce measured structural crew cost
without changing decision RNG, target ordering, routes, timing or selected art.
Full frame/loading/endurance/bugs/Windows/M1/signing gates remain open.

## Accepted decisions and constraints

Muted secondary native debug=false tests, isolated APPDATA/profile and owner
fingerprints. No screenshots/full runtime copies. Three matched alternating pairs
per map. Preserve exact full state/cameras/actions; no ignored warning history.
Test-only mining warning clock uses visual simulation seconds in both lanes;
production warning clock unchanged. Keep withdrawn point-map trial withdrawn.

## Current state

Installed only decision-local station target distances in scripts/bill_npc.gd.
_choose_goal calls _sort_station_targets after the same shuffle and station choice.
The helper calculates each target's squared distance once; comparator keeps the
same strict less-than and exact shuffled ties. Graph positions are read-only
during sorting. No permanent cache, graph sharing, deferred decisions or extra RNG.
Installed bytes equal measured private candidate, SHA256
6888fceaf6e24998d4e82bd6311240c9fa4d558825dff24183720bd83f99d193.

Maintained tests/test_navigation_prefix.gd now compares original/new ordering for
1152 cases/126528 targets: dense and sparse IDs, duplicate coordinates, shuffled
ties, varied centers and sizes0/1/2/16/128/512. RNG state unchanged. Existing UID
preserved. Earlier zoom scheduling source remains unchanged.

## Verification

Bounded profile (8-frame/64-label ring, private source) on large/current/reported:
six native runs/9720frames,27 exact full states/cameras and45 successful paired
action events. Large first placement James goal12.779ms includes sorting2.668ms;
six structural decisions sort2.099–2.837ms each. Across the workload, sorting
19.551ms/28calls within total goals77.496ms/8calls. Timers overlap; do not sum with
total goal/update. Candidate gathering1.502ms, station preparation1.256ms and
shuffling0.682ms over the workload. Current save uses primary work instead, with
no recorded station sorting. Reported sort2.801ms/4calls, total goals9.972ms/7calls.
All profiler/control state comparisons exact; production profiling not installed.

Isolated sorting check in debug=false executable/headless:1152cases,126528targets,
zero failures. Aggregate original289096us/new113105us (~61% less sort work), not
a gameplay FPS measurement. Fresh installed maintained-source check in the same
executable/headless:1262checks,zero failures,127892graph records,984routes,
126528sorted targets. Includes actual staged rebuild yields and final graph parity.

Gameplay comparison: eighteen native runs/29160frames; three alternating pairs
each for 40-room large fixture,10-room current save and12-room reported save.
Lighting/connected placement/successful demolition at1x/2x/4x,180frames/phase.
All81 full phase states/cameras and135 paired successful events exact. Runtime
guards verify the source lane/fixture clock, input disabled, muted secondary
display, no errors/missing art. Tested RTX4070Ti1080p; not target GTX1650/M1.

| Metric | Large before→installed | Current before→installed | Reported before→installed |
|---|---:|---:|---:|
| Structural crew mean ms (18 events) |32.241→30.969|13.895→13.889|13.634→13.434|
| Whole mean ms |24.510→24.579|11.975→12.001|12.882→12.830|
| p95 ms |40.554→40.595|17.431→17.716|18.833→18.774|
| p99 ms |52.883→52.353|27.698→27.075|21.791→21.649|
| Maximum ms |93.058→91.312|48.338→48.794|57.884→55.457|
| >50 frames |56→59|0→0|8→8|
| >100 frames |0→0|0→0|0→0|
| Texture peak MiB |3028.476 unchanged|1940.818 unchanged|1559.522 unchanged|

Large crew saving1.272ms (-3.95%), all18 events and all3 pair means improve.
Reported saving.200ms (-1.47%),12/18 events and all3 pair means improve. Current
effectively neutral (.006ms), with no recorded station-sort work in the profile.
Admitted as a small targeted crew-cost reduction with exact behavior, **not a
general FPS gain**. Whole mean large/current slightly worse0.28%/0.22%, reported
better0.40%; pair directions mixed. p99 slightly better on all maps but >50 large
count slightly worse. Every map still fails p95; large/current also fail p99.
Native scene coverage does not certify cold/warm load, physical input, normal
title/Continue, target hardware, Mac, visual review or endurance.

Stall review: reported >50 frames all demolition frame30, no sampled drone upload;
current none. Large includes both structural redraw/rebuild frames and recurring
upload frames. Largest reference placement93.058ms has floors6.784ms (includes
floor-rest5.031ms), detail-room setup5.290ms and live-room3.731ms. Counters overlap;
not an additive frame breakdown. Full hitch labels/timings/uploads retained in
comparison.json. Source inspection shows floor passes configure layered room
views; cost reduction there needs a scoped probe and exact rendering checks.

All owner guards2938 files unchanged. All jobs terminal and runtime override
restored. Completed profiling traces20201022→7704576bytes allocated; gameplay
traces59795030→22749184bytes. Every content hash checked before/after compression.
No owner/runtime compression/deletion; freeC134.83/D68.74GiB.

Evidence under D:/bs-release-crew-cache-20261009/benchmark-input-isolation:
goal-target-sort-attribution-v2/analysis.json and source/owner/logs;
station-target-distance-trial/candidate-bill.gd and native-parity.log;
station-target-distance-pilot/comparison.json, eighteen traces, identities and
owner.json. Runners/analyzers under output/renderdoc-tools-2026-10-08:
*goal-target-sort-attribution-v2.py, *station-target-distance*.py.

## Next action

Profile floor-only room configuration/setup work at placement/demolition, keeping
live animation and room layout application separate in the timings. Only remove
work proven unnecessary for floor output, with exact pixel/geometry checks on
owner layouts and actual native movement. Recurring uploads remain a separate
memory/pacing problem; do not repeat rejected larger-cache/indexed/atlas trials
unchanged. Keep full original PC/Mac release gates active.
