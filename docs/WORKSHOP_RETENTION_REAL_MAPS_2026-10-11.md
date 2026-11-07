# Workshop retention: real-station verification and handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Verify an invalidation-aware room setup optimization on actual station saves and the
40-room stress fixture. Full release frame, memory, visual, stability and platform
gates remain the objective. This is one measured batch, not release certification.

## Accepted decisions and constraints

Keep the workshop candidate private. It saves work on the expanded fixture but fails
exact zoom pixels; real-save improvements are marginal/mixed. No production edit or
new release export, commit or upload. Preserve selected art, crew timing/bindings,
normal economy and owner layouts. Tests muted, on the secondary display, with input
blocked, scratch APPDATA and read-only save copies. Reuse the existing runtime and
small overlay packs; enforce the maintained 20 GiB free-space floor.

## Current state

Trace attributed four live workshops to 649,404 us / 1,080 frames (~0.60 ms/frame).
832,539 door queries sampled at 0.84 us/call estimate ~0.65 ms/frame; these diagnostic
figures are not release frame acceptance. Workshop candidate permits existing retained
setup only without actors, companion/recovered sites or nonplain views. A deep snapshot
of the validated cosmetic floor-case payload joins the frame key, before its final
layout-serial field. Actor-containing rooms retain full preparation.

Private code and results: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`
`room-door-cost-trace`, `workshop-retention`, `workshop-retention-pixels`.
Runners/comparators: `output/renderdoc-tools-2026-10-08/` named `workshop-*`.
Production source hashes still match the measured inputs; only this note and current
status are changed for this milestone. Existing unrelated worktree changes preserved.

## Verification

18 actual debug=false Windows RTX 4070 Ti / 1080p native runs: three alternating pairs
per map, 90 measured frames per idle/pan/zoom/lighting phase at 1x/2x/4x. Total 19,440
measured frames. Maintained fixture uses dedicated free-build/failure overrides and
manual deterministic simulation; this does not certify ordinary unmodified gameplay.
Current normal source overlays and candidate overlays share the reused release PCK;
these are not freshly frozen complete release candidates. Strict state/camera checks
pass for all 108 paired phases; no SafeImage failures or unexplained engine errors in
the completed performance runs.

| Map | Mean ms before -> candidate | Mean change | p95 ms | p99 ms | Frames >50 ms |
|---|---:|---:|---:|---:|---:|
| Reported real station (12) | 13.031 -> 12.983 | -0.37% | 18.679 -> 19.313 | 22.495 -> 22.948 | 0 -> 0 |
| Frozen current station (10) | 12.515 -> 12.595 | +0.64% | 18.338 -> 18.409 | 27.653 -> 27.574 | 0 -> 1 |
| Deterministic expanded station (40) | 26.778 -> 25.926 | -3.18% | 43.895 -> 43.081 | 55.792 -> 55.267 | 69 -> 61 |

No measured performance frame exceeds 100 ms. Current candidate maximum 52.512 ms
needs investigation; no frames over 50 ms in its reference runs. Every 40-room pair
improves its mean, pooled 3.18%; reported station pooled mean 0.37% better but p95/p99
worse, so no claimed useful real-station win. Current station has no workshop and
identical skipped-setup counts, yet timings vary in both directions: pooled 0.64%
slower. Do not silently dismiss or advertise that as a gain. All p95 gates still fail;
current and large p99 gates fail. Texture peaks unchanged: reported 1,558.872 MiB,
current 1,940.831 MiB, expanded 3,028.007 MiB. No endurance/memory-growth claim.

Private headless guard fixture passes ten checks: empty/add/move/remove case keys,
deep snapshot nonaliasing, actor entry/exit and companion/recovered exclusions.
First attempt collided with the source GridCanvas global class; corrected only the
private guard copy and added can_instantiate. Failed log retained. An orchestrator
process-exit detection error and an overbroad fixture string replacement were corrected;
neither changes game code or invalidates completed native measurements.

Separate scoped visual pair: 15/24 exact; nine zoom captures differ by 26-42 pixels
with matched saved state/camera/clock/light levels. First mismatch max channel delta
48; no tolerance waiver. This differs from the older intermittent large wreck region,
so do not assume the same cause. Candidate withheld. Four extra case PNGs exist, but
were captured after report serialization and show zero add/move pixel differences in
both lanes. They do NOT establish case visibility/invalidation correctness. Fix capture
ordering, focus a verified visible workshop and inspect live slot/payload state before
accepting that fixture. No claim that this proves a production case defect.

All owner guards: 2,938 files before/after, no changes. Native jobs exited and original
QA configuration restored. Evidence 6.99 + 71.97 + 102.16 = 181.12 MiB. C 124.65 / D
72.00 GiB free. No full package/source-tree copies or broad deletion this pass.

## Next action

Locate the zoom pixels against workshop bounds and retained canvas transforms. Test
strict camera/scale invalidation for workshops before assuming it is the remedy;
existing generic room reuse normalizes the camera field during pan/zoom. Repair the
case visual fixture as described above. Rerun scoped visual checks on any correction,
then matched performance on both real saves and the stress fixture before admission.

Broader gates remain open: prior indexed-provider gait precision/loader/fallback/lifetime,
background-wreck discrepancy, remaining >50 ms frames and large-station frame budget,
full workload/1440p/target GPU, endurance/transitions and packaged original bug closure.
Actual Apple Silicon gameplay, Retina/input checks and signed/notarized downloaded Mac
candidate are still outstanding. Research alone or headless tests do not certify them.
