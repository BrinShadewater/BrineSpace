# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: correctly attribute drone uploads to measured frames

## Objective and acceptance
Continue the full PC/Mac release/performance plan. Diagnose actual stalls with bounded additive reports; retain selected pixels/timing/default quality and all original gates. This milestone repairs attribution, not frame rate.

## Accepted decisions and constraints
Keep historical fields unchanged; add sampled-frame diagnostics. Full atlas copies retain pixel fidelity. Earlier naive cropped-frame backend fails358/416native comparisons including nearest/linear; do not retry without solving recorded sampling issue (DRONE_ATLAS_REUSE_SAMPLING_2026-10-06.md). No larger permanent GPU cache or lossy/downscaled art admitted.

## Current state
Normal changes: `scripts/drone_animation.gd` adds monotonic start/end microseconds to upload events using the existing upload timer; `tools/release_benchmark.gd` records the actual FrameDriver process index (or current index for signal driver) and adds sampled_process_frame/sampled_drone_uploads to hitches/traces; `tests/test_drone_upload_diagnostics.gd` adds interval consistency and explicit completed-frame assertions. Existing fields/counters/collection caps retained; UIDs unchanged. No rendering/cache/simulation behavior changed.

## Verification
Isolated normal benchmark compile passes; native upload test16checks/0failures/clean. Owner2,936files unchanged. Actual private debug=false release dbe44a995a5708be, active40-room1080p uncapped pan/zoom1/2/4x60frames/phase; additive diagnostic adapter only. PCK is unchanged and does NOT contain the normal new upload timestamp fields. Actual FrameDriver attribution is tested here; timer fields are validated by normal native test separately. Adapter's exact hash stored in report identity. QA adapter restored; process terminal; owner2,936unchanged. Evidence `output/drone-sampled-frame-2026-10-07/` and `output/drone-sampled-frame-release-2026-10-07/`.

All360samples observe process_frame=sampled_process_frame+1. Every legacy current-frame upload field is zero; explicit sampled-frame fields reveal35upload frames/54uploads,2,024,388,988bytes (~1.89GiB),182,183us total GPU image-create calls. Upload-frame median38.602ms versus32.109ms without uploads; workloads differ, so not a causal matched performance comparison. Thirteen measured frames>50ms, six contain uploads and seven do not; both paths remain relevant. One230MiB three-atlas burst costs19.483ms in62.553ms frame. Worst upload-frame69.241ms has91.878MiB11.331ms upload. P95 still fails; no measured frame>100ms in this360-frame lane, not whole-session stall certification. Endtextures3037.838MiB; no missing art/routes/errors/warnings/leaks.

Latest previous cap-control worst89.673ms frame has atlas upload index531 while sampler index532; its exterior-actor stage50.458ms includes36.039ms uploads. Earlier full-workload90.428ms worst has last upload640 vs sampler643, so it still has no same sampled-frame upload (sample642). Correct the attribution only where indices prove alignment; do not generalize every redraw stall to uploads.

## Next action
Measure atlas CPU source preparation/worker waits separately from GPU image creation on repeat paths before choosing another memory-safe remedy. Large repeated mining body/effect and tyre atlases dominate transfer; require session-bounded lifetime and exact sampling. In parallel priority, redraw-only frames still need live-room/environment attribution. Minor cap cache stays private; compressed crew remains private. Packaged FPS/peak-and-lifetime memory/12room/loading/endurance/original bug/UI/targetPC/Mac/signing certification all remain open.
