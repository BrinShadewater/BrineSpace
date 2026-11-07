# Project handoff

Updated: October 15, 2026 | Project: `C:/Users/Alex/Documents/Brine Space` | Task: drawing and render submission

## Objective and acceptance

Completed private Windows drawing study without appearance or crew changes.
Water geometry CPU saves ~0.29-0.40 ms/frame. Normal idle 51.98 to 52.86 FPS,
4x idle 45.47 to 47.09, 4x placement phase 43.46 to 44.80. Action mixed:
58.738 to 57.009 / 57.024 to 57.903 ms. Following 4x mean/p95 improve, >50 ms
counts remain 1 per sixty-frame window. Normal pooled p95 worsens. 0/8 60 FPS gates.

## Accepted decisions and constraints

Keep V2 private; normal runtime unchanged. Reference already has private stable-ID
V3 and distant LOD/one spare; results are not against installed game. Preserve
geometry, blend order, clocks, colors, crew, doors, warnings and navigation.
Native retains counters only; absent extension/reference flag uses original script.
Batch parity accepted for finite generated 7/25-point paths; unsupported batch
lines pass through, oversized/nonfinite parity unproven. All native jobs serial,
every Godot job isolated. No normal native installation, export, Mac package,
commit or upload.

## Current state

[Results](DRAW_SUBMIT_PERFORMANCE_2026-10-15.md). Evidence:
`C:/bs-draw-submit-20261015/`; helpers `output/draw-submit-20261015/`.
V1/V2 source/build/DLL manifests preserved in `water-native/`. V2 DLL SHA:
`4e3dc0516744ac04d0599de5d8a5cd7c76e867ff349bd68c135a4a8d9c6cad74`.
Only two of 22 frozen scripts differ: Moonbay records raw commands for native
batch preparation; water-stroke helper adds optional native packet fallback.
Stable DLL/API3 unchanged. GPU draws remain ~2,117-2,196/frame; gain is CPU geometry
preparation, not demonstrated submission reduction. Static harvest retention
declined (~0.11 ms); drone atlas work remains ~2 ms at 4x.

Changed docs: results, this handoff, CURRENT_STATUS top milestone and
`docs/superpowers/plans/2026-10-15-draw-submit.md`. No installed game source/UID/test
change in this task.

## Verification

1,920 guarded production-lane frames / eight exact phase-state/camera-path pairs.
V2 packet oracle 21,079 assertions; batch 1,565 assertions over 109 calls;
extension-absent 21,076; native water 494 checks / 244 exact raster pairs. V1 packet
oracle also 21,079 pass. Seventeen cross-process station/first-placement pairs and
twelve repeats exact; representative image inspected. Independent read-only
water_batch_review found no blocker within stated domain. Final audit passes.
All 26 owner / twelve stable-binary / ten water-binary guards clean; final 2,948-file
fingerprint equals initial/prior protected baseline. Existing profile-incident
caveat persists. Engine memory counters equal; native transient/RSS and long-soak
acceptance unproven. Only owner editor PID46624 remained after jobs.

## Next action

Trace surviving draw calls/CPU submission separately, then test retained commands
or resources preserving blend order. Drone atlas bursts remain another large cost.
Before native integration: Mac/build/package, fallback lifecycle, longer pacing
and transient/working-set checks. Preserve every guard-valid run. Reuse frozen
reference/manifests; do not mix this stable-ID baseline with earlier dense studies.
