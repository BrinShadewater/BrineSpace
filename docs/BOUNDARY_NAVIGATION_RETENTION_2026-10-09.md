# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: boundary checks retained

## Objective and acceptance

Reduce measured navigation stalls without changing geometry, graph order/routes,
door/fire policy, mission timing or owner data. Full original release scope/gates open.

## Accepted decisions and constraints

Normal scripts/bill_npc.gd now retains synchronous boundary-only precomputed owner
blocker sweeps. Cache is local to each rebuild and discarded on return. Staged,
reference and sample-all builds keep the original path. Corridors,legacy shapes,
unknown cells/arbitrary endpoints/live route calls keep segment_clear. Reciprocal
open sockets,hardware/per-room locks,exact padded clipping and endpoints preserved.
General route smoothing is unchanged. UID untouched; no art/quality/timing change.
Broader FPS/p95 results remain mixed: retained for repeated targeted stall reduction,
not release acceptance. Shared private controls limit packaged certification scope.

## Current state

Reference switch --reference-nav-boundary-checks. Per-actor additive counters report
fast/fallback calls and aggregate cache preparation time. No retained geometry table.
Normal isolated edit captured in boundary-navigation/normal-boundary.diff alongside
before/after snapshots and source hashes in normal-integration.json.
Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
boundary-navigation/,boundary-runtime/,boundary-reverse/,boundary-summary.json.
Helpers prepare-boundary-navigation.py,test-boundary-navigation.py,
prepare-boundary-runtime.py,prepare-boundary-reverse.py,
integrate-boundary-navigation.py,validate-normal-boundary.py under
output/renderdoc-tools-2026-10-08/. All jobs terminal/adapters restored.

## Verification

Private and then normal299691checks/0:complete ID order,positions,weights,ordered
adjacency and sampled selected paths across4rotations,4Moonbay phases,locked/unlocked
hardware/rooms,connecting corridors,cold/warm builds and missing/arbitrary fallback.
Normal7344fast/81fallback calls;owner90/0normal and reference modes,clearancePASS,
stagger0failures. Previous5892synthetic/44160current geometry comparisons remain
supporting evidence. Staged shortcut explicitly disabled; no staged timing change.

Actual debug=false1080p40room,1000idle samples per1x/2x/4x,exact compiled inherited
Bill SHAa49dbe2ad6ca9ae8afcd6d093316ff84ea61e2fafe40290d0077d64d3fa1baf7;
same cold-template/point/link algorithms enabled both lanes. Probe bounded1256;
seam timing INCLUDES new cache preparation.

| Order | Branforth seams ref ->candidate | Marsh | Veld | Frame1256 crew | Frame1256 total |
|---|---|---|---|---|---|
| Ref first |11.902 ->5.171ms|13.650 ->5.829ms|11.817 ->5.013ms|128.193 ->119.602ms|168.254 ->160.839ms|
| Cand first |12.235 ->4.959ms|13.402 ->5.075ms|11.990 ->4.994ms|127.643 ->106.136ms|167.185 ->144.959ms|

Frame3086 crew74.951->55.051ms /66.243->55.360ms;total112.417->91.514 /
98.747->88.841ms. Nodes19695/cells76/template misses unchanged. No drone uploads
on these target frames. Full tables/component timings retained in boundary-summary.

| Order/speed | Mean ms ref ->candidate | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| Ref first1x |38.196 ->38.086|43.148 ->43.814|52.471 ->54.356|82.500 ->75.302|
| Ref first2x |39.445 ->39.299|46.380 ->47.372|61.385 ->57.079|168.254 ->160.839|
| Ref first4x |39.921 ->40.423|53.348 ->55.438|77.150 ->71.715|132.910 ->132.930|
| Cand first1x |37.650 ->38.088|43.038 ->43.796|54.401 ->54.196|79.587 ->91.674|
| Cand first2x |39.335 ->39.231|47.127 ->47.628|59.010 ->60.560|167.185 ->144.959|
| Cand first4x |39.946 ->40.396|53.693 ->54.665|70.941 ->67.789|154.011 ->136.130|

All phase crew/drone/mission endpoints and final mission histories/resources match.
Per-source drone uploads equal,crewuploads4074each,texturepeak2345.481MiB /
exit228.259MiB equal,pending0afterexit/routerreleased. Both pair owners2936same,
accepted logs clean/adapters restored/processes terminal. Normal regression owner
2936same. No full current-checkout export,3run certification or Mac acceptance.

## Next action

Shift sustained-FPS profiling toward grid drawing/room preparation. Ordinary first
candidate trace has roughly20ms grid draw versus~1ms station simulation; precise
under50ms-frame medians retained in boundary-runtime/ordinary-frame-costs.json.
Scopes overlap; do not sum them or infer a GPU cause. Profile expensive live-room
preparation and animation output invalidation with exact quality/behavior proof.
Navigation links still cost12-19ms in rebuilds,but rejected graph-delta forms must
not be adopted. Full-source package,broad workloads,original bugs,loading/memory/
endurance and Windows/Mac certification gates remain open.
