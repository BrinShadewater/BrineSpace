# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: normal navigation point verification and local-link prototype

## Objective and acceptance

Continue the full PC/Mac release-performance plan. Verify retained point helper with
exact normal navigation bytes, then reduce measured link assembly without changing
graph semantics, mission movement/timing or owner data. Full release gates stay open.

## Accepted decisions and constraints

Normal point optimization remains retained. Cached local links now retained after repeatable crew-cost gains and normal regressions.
Overall FPS/tail results remain mixed and do not meet release gates. No graph sharing, node reduction,
art changes, quality changes, broad refactor or public release. Shared private render,
storage, drone retention and water-worker controls limit certification scope.

## Current state

Normal Bill source SHA a8f34af94e70c5d734c89572366bab3ee86ed2ae92765f849c47b3dc54e13d16
copied byte-identically to normal-packed-nav-runtime/bill.gd and validated through
inherited actors in actual debug=false executable. Bay-scope/fast-local-template/
indexed-assembly navigation flags are absent and execution counters0 in both lanes.
--reference-nav-point-assembly selects the original point loop only for reference.

Cached link prototype derives PackedInt32Array local point-index pairs on existing
room-cache entries. Room node IDs remain independent per actor; connection insertion
order is retained. It avoids repeated Vector2i center additions/global dictionary
lookups per link. Template points/links stay unchanged; replacement drops derived data.
Prototype actual source SHA84c65494a59a26bc9c94b59706ed8135cb9823682fd528e9ff17fbfec18e35dc;
--cached-nav-links selects it. Packed points enabled both lanes; no other nav flags.
Normal scripts/bill_npc.gd now retains local link indices with a reference switch;
UID, template generation and boundary checks unchanged.

Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
normal-packed-nav-runtime/, cached-navigation-links/, cached-nav-links-runtime/,
normal-point-and-links-summary.json, cached-nav-links-reverse/ (completed), normal-navigation-cold-build/.
Helpers output/renderdoc-tools-2026-10-08/prepare-normal-packed-nav-runtime.py,
write-cached-navigation-links.py, test-cached-navigation-links.py,
prepare-cached-nav-links-runtime.py, analyze-normal-point-and-links.py,
prepare-cached-nav-links-reverse.py.

## Verification

Normal-source actual reference-first1080p40room,1000idle frames per1x/2x/4x:

| Speed | Mean ms ref ->point | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 35.928 ->35.808 | 38.562 ->38.107 | 48.194 ->48.678 | 74.935 ->74.151 |
| 2x | 36.668 ->36.630 | 42.627 ->43.009 | 51.503 ->51.220 | 229.116 ->218.613 |
| 4x | 38.057 ->37.772 | 49.485 ->49.369 | 78.833 ->76.449 | 173.581 ->169.000 |

Frame3086 crew88.373->83.728ms/frame119.816->117.461ms. Target source change works
in release; modest gain, not 60FPS certification. Normal nav lacks common private
navigation optimizations, so its larger spikes cannot be compared directly to earlier
scoped/indexed trials. New repeated largest crew-only frame1256:crew192.975->183.068ms,
no drone upload. Other large frames combine navigation and275.6/229.7MiB upload batches.
Packed point payload305360bytes per actor's67 referenced cache entries; sum may count
shared backing storage repeatedly. Not total CPU memory/RSS evidence.

Cached links native3916checks/0: four rotated sparse templates, exact ordered
connections/weights/selected routes, unchanged templates/cached indices, replacement
empty links and independent disabled-state/graph destruction. Initial fixture variable
inference error fixed with PackedInt64Array annotation; no behavior changed to pass it.

Actual link-only reference-first pair, same standard idle speeds:

| Speed | Mean ms ref ->links | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 38.323 ->38.297 | 43.989 ->44.158 | 55.036 ->54.336 | 86.011 ->78.598 |
| 2x | 39.088 ->39.347 | 47.596 ->46.229 | 62.222 ->62.949 | 215.881 ->199.284 |
| 4x | 40.767 ->40.309 | 54.215 ->54.178 | 83.551 ->79.745 | 189.375 ->181.421 |

Frame3086 crew85.662->70.397ms/frame121.330->104.581ms. Target local-link gain15.265ms;
max better3/3, broader means/tails mixed. Largest1256 crew179.584->162.642ms, no upload;
still199.284ms frame. Link payload495584bytes per actor's67 referenced entries, not
unique or total memory. More reconstruction work remains; don't shift stall later.

Both actual pairs pass compiled-source/branch/execution/nav-return/mission/endpoint
and worker-event coverage guards. Phase/final crew/drone/mission histories match;
texturepeak2345.481MiB/exit228.259MiB/drone486/crew4074 equal; pending3->0 at exit,
router releases. Owners2936unchanged/logs clean/processes terminal/adapters restored.
No full current-checkout export, 3run certification, broad workload or Mac acceptance.

## Reverse link result and normal integration

Actual candidate-first reverse, same compiled prototype/source/control guards:

| Speed | Mean ms ref ->links | p95 ms | p99 ms | Max ms |
|---|---|---|---|---|
| 1x | 38.545 ->38.468 | 44.611 ->43.860 | 56.669 ->55.506 | 81.470 ->97.333 |
| 2x | 39.463 ->39.389 | 46.670 ->48.634 | 61.237 ->58.879 | 241.390 ->195.269 |
| 4x | 39.968 ->40.679 | 53.469 ->54.524 | 82.466 ->80.433 | 190.559 ->169.711 |

Frame3086 crew84.467->65.700ms/frame116.798->99.129ms. Target CPU gain repeats
15.265/18.767ms in both orders. Frame1256 crew198.265->158.179ms, no GPU upload,
frame241.390->195.269ms. Mean/p95/max mixed, p99 better reverse3/3; not universal FPS.
All existing endpoint/history/source/branch/memory/worker/cleanup/isolation checks pass.

Normal source now uses append_cached_room_links and --reference-nav-link-assembly
for the original lookup loop. Normal3916kernel/0, room ownership90/0 in optimized,
reference-link and full-reference modes, rebuild-stagger0failures. Owner2936 files
unchanged/logs clean/processes terminal. Normal-source.diff records only this edit;
existing UID untouched. Helpers integrate-cached-navigation-links.py and
validate-normal-cached-links.py; source hashes in normal-validation.json.

## Larger remaining normal-navigation stall

Bounded17frame actual debug=false probe on current normal point/link code, around
engine1256, validates inherited base SHA
41c8a8e5591e41a2654a3bb10518251d71408514f66a7b264016ce4b3d1344f2.
No behavior changes, just component timing. Existing fixture/ownership/mission/
branch/memory/cleanup and owner protection guards pass; max205ms stillfails gate.
Artifacts normal-navigation-cold-build/build-components.json/candidate.json and
prepared-identity.json retain timings, normal baseline hash and isolation proof.

| Actor | Full cells/nodes | Template misses | Template generation | Points | Links | Boundaries | Total |
|---|---|---|---|---|---|---|---|
| Branforth | 76 /19695 | 0 | 0.029ms | 3.655ms | 11.724ms | 11.769ms | 31.355ms |
| Marsh | 76 /19695 | 0 | 0.030ms | 3.630ms | 12.229ms | 11.839ms | 31.685ms |
| Veld | 76 /19695 | 6 | 53.418ms | 4.388ms | 14.442ms | 11.616ms | 88.773ms |

Thus frame1256 builds three full graphs; one pays substantial cold-template cost.
This is different from earlier scoped/indexed frame3086 with zero template misses.
Do not apply that earlier attribution to this frame. Timings include probe overhead;
no precision/performance-gain claim beyond measured components.

## Next action

Reduce cold authored-room template construction: compare exact clipped blocker sweeps
against original segment checks with correct corridor/legacy/fire/closed-socket guards,
actual room/layout/rotation tests and matched native/release evidence. Preserve current
mission timing, geometry and graph ownership; do not simply defer crew exits. Links
and boundaries still cost substantial time; independent full-graph retention/changed
cell updates need their own invalidation proof if pursued. Current point/link normal
code remains; full-source package, broad workloads, original bugs, loading/memory/
endurance and Windows/Mac certification gates still open.
