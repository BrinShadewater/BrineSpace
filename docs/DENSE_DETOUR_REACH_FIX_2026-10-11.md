# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: companion passage spikes

## Objective and acceptance

Reduce the reproduced non-rebuild passage-wait CPU cost while preserving ordered
reachability, route/movement state, fire/disabled-node policy and sparse graphs.
Accept a targeted CPU improvement with matched native evidence, not a broad FPS claim.

## Accepted decisions and constraints

Muted secondary display, isolated profiles/input and owner fingerprints. Existing
debug=false runtime plus small overlays. No art/runtime copies, screenshots,
navigation deferral, gameplay/visual changes or architecture refactor.

## Current state

Changed `scripts/bill_npc.gd`: dense graph reach fill uses a temporary byte array
for visited/blocked status, while preserving output dictionaries and original
neighbor/BFS insertion order. Graph IDs are checked for density; arbitrary sparse
IDs use the original fill. Density facts cache only revision, graph instance ID,
point count and a boolean. Live disabled-point checks remain in each fill.
Changed `tests/test_detour_start_filter.gd`: retains original crew stand-off/search
checks and adds randomized fire/disabled/revision/order/sparse/replacement coverage.
Paired UIDs unchanged. No adjacency-list cache installed.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`companion-passage-attribution`, `detour-adjacency-trial`,
`detour-adjacency-attribution`, `detour-dense-trial`, `detour-dense-attribution`,
`detour-dense-workloads`. Scoped runners in `output/renderdoc-tools-2026-10-08/`.

## Verification

Fresh current trace: Margot idle 1x frame 40 has no navigation revision change,
update 7.373 ms, move 7.261, detour 7.258, reach 1.969, smoothing 2.746.
Nested timings overlap. River has similar ~2 ms reach cost. This is separate from
the already improved construction template rebuild.

Rejected lazy neighbor-list cache: 43,240 parity checks pass, but two cold fills
worsen reach by ~0.8–0.9 ms; three later fills improve little or worsen. Do not
adopt/repeat unchanged. It also retains ~2700 neighbor lists per exercised actor.

Dense candidate initial 43,241 comparisons pass; expanded fire/room/sparse/same-count
replacement differential 41,442 passes. All five instrumented reach events improve
0.281–0.686 ms; twelve full phase states/cameras and 54 UI snapshots match control.
Each diagnostic control/candidate replay preserves the same twelve full phase
states/cameras and 54 UI snapshots; coarse wrappers call original methods once.

Three alternating native current-map pairs / 6480 frames without private method
timers. Regular benchmark diagnostics remain enabled in both lanes. Idle/pan/
selection/zoom-selection at 1x/2x/4x, 90 measured frames per phase.
36 complete paired phase states/cameras and 162 UI snapshots exact.

All 15 preidentified passage events improve crew time: mean 6.1176→5.6707 ms
(-7.30%). Individual reduction 0.045–0.677 ms. Accept this targeted CPU result.

| Whole-run metric | Reference | Installed candidate |
|---|---:|---:|
| Mean frame ms | 11.363 | 11.315 |
| p95 ms | 18.627 | 18.817 |
| p99 ms | 27.685 | 27.743 |
| Maximum ms | 48.318 | 43.996 |
| Frames >50 / >100 ms | 0 / 0 | 0 / 0 |
| Texture peak MiB | 1945.262 | 1945.262 |

Whole-run means mixed, pooled -0.42%; tails essentially neutral/slightly worse.
No broad FPS improvement or release frame-gate acceptance. Renderer/animation
source untouched; no new visual certification claimed from navigation tests.

Installed maintained test: 41,442 dense comparisons plus original start-filter/
swimmer checks, zero failures/errors. Installed script bytes equal measured
candidate; source hash in `installed-verification.json`. All owner guards 2938
unchanged. A validation wrapper repeated full fingerprints inside its comparison
loop; stopped that specific read-only process after tests completed, then reran
the corrected final guard with one before/after fingerprint and tests. Final pass
evidence retained separately. Native jobs terminal/override restored.

Evidence 34.04 MiB plus 25.47 MiB scratch; C 122.94 / D 69.44 GiB free.
No cleanup-policy bypass attempted.

## Next action

Verify installed fill on reported/large maps, then split route smoothing and
detour-start join work before another remedy. Preserve live collision/facing checks;
do not infer a safe cache merely from repeated queries. Large rendering/upload
stalls, memory/loading/endurance, full bugs/visuals and PC/Mac certification remain
open. Indexed provider stays private.
