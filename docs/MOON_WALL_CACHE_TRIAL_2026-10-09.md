# Moonbay retained-wall prototype

Updated: October 9, 2026 · Project: BrineSpace · Task: rendering performance

## Objective and acceptance
Avoid rebuilding static Moonbay wall/window commands every frame while preserving water/sub/wall/gate/prop ordering, pixels and live mutations. Full PC/Mac release gates remain open.

## Accepted decisions and constraints
Retained after repeated controlled workload gains and normal native parity. The shell remains immediate because Common.begin also draws animated station ports. Internal walls/windows were previously measured at about 1 ms across three rooms. Do not claim the full earlier 1.48 ms shell-plus-wall scope as savings, or controlled-packet results as complete release certification.

## Current state
Normal rooms/large-rooms/moonbay.gd factors static walls and live gates/beacons into identical helper bodies. Normal scripts/moonbay_base_canvas.gd retains a wall child after parent water/sub commands; its live-gate child follows walls. Normal water implementation remains unchanged; private worker code was not ported. Wall key includes bounds, raw rotation, ocean side, raised walls and Studio revision; mission clock is excluded. Wall state retains only its three geometry fields, while complete base snapshots update live gates. Explicit nonwhite self_modulate uses the immediate full paint, recovering retention when white returns. Child canvases inherit material/filtering and report draw time through the existing slot profiler. Diagnostic --reference-moon-walls preserves immediate painting. Existing script UIDs preserved.

Added tests/test_moonbay_retained_walls.gd with paired UID and registered it in performance-diagnostics. Normal integration helper: output/renderdoc-tools-2026-10-08/integrate-moon-wall-cache.py; normal test helper test-normal-moon-walls.py. Pre-change bytes and source SHA records in normal-integration.json. No unrelated changes reset.

Helpers: output/renderdoc-tools-2026-10-08/prepare-moon-wall-cache.py and test-moon-wall-cache.py. Artifacts: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/moon-wall-cache/. Native-base source differs from packed base only in the direct Moon preload path; source hashes recorded in prepared-identity.json.

## Verification
Isolated native exact raster comparison against the frozen original Moon renderer: 579 pairs, zero failures, 65 wall redraws/513 reuse hits. Covers four rotations, two ocean sides, raised walls, fractional bounds/two sizes, partial/full chamber water, boarding/disembark/drain, gate/port states, two filtering modes, inherited shader/modulation, reduced motion, changing clocks and explicit self-tint fallback/recovery. First rendered state after each submission is compared. Accepted sample visually reviewed. Parse/native logs clean, all 2,936 owner files unchanged. No performance saving accepted from pixel parity.

## Next action
First matched debug=false pair completed. Reference -> candidate means at 1x/2x/4x: 37.210 -> 35.812 / 38.545 -> 36.871 / 40.318 -> 38.051 ms, savings 1.398/1.674/2.267 ms. p95 42.574 -> 41.952 / 46.456 -> 45.220 / 53.954 -> 51.759 ms. p99 mixed (1x 50.862 -> 52.117 ms); maximum candidate 139.686 ms. All frame gates still fail. Texture peak 2,345.481 MiB and crew uploads 4,074 unchanged. Each Moonbay rebuilt walls twice while live gates drew 2,869–3,120 times and wall cache hit 2,867–3,118 times. Phase crew/drone/mission/power/door/light state and final missions, texture exit, pending jobs, router release and decoded/upload counts match. Source/branch/worker proofs clean, adapters restored, owner 2,936 files unchanged. Evidence: comparison-summary.json and owner-pair.json.

Reverse comparison completed: mean savings 0.985/2.185/1.636 ms at 1x/2x/4x. p95 improves 1.425/4.507/1.945 ms; p99 mixed. Maximum candidate 149.304 ms. Both pairs match phase/final state and decoded/upload counts, texture/cleanup checks, source/branch/worker guards, owner fingerprints and restored adapters. Only retained-wall option differs between each matched pair. Summary: sibling moon-wall-cache-summary.json. Full frame gates still fail.

Normal native regression: 580 exact pixel pairs, zero failures, 66 wall redraws/514 hits. Explicit Studio revision invalidates walls; base/wall/gate weak references clear on observed scene destruction. Existing whole-room water/prop/offline/material composition regression: 135 checks, zero failures. Logs clean, all 2,936 owner files unchanged. Evidence: normal-native.log, normal-native-summary.json, normal-checks.json and test_moonbay_retained_walls.log/test_moonbay_water_batch.log.

Next freeze/export the complete accepted source with the maintained release workflow and measure cumulative normal changes in an actual debug=false candidate before more whole-game FPS claims. Private controlled water/storage fixture results do not substitute for that candidate. Continue targeted rendering work from its profile; original loading/memory/workload/endurance/bug/Mac certification gates remain outstanding.

Existing viewport-timing overhead control was checked in CURRENT_STATUS / RENDER_TIMING_SCOPE_AND_OVERHEAD_2026-10-08.md: earlier actual 40-room GPU-timing on/off pair did not reliably improve FPS. Do not repeat that control without a new concern or treat delayed viewport timing as current-frame additive cost.
