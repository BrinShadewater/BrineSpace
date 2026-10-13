# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: reusable synergy circle geometry pilot

## Objective and acceptance

Reduce measured synergy drawing cost while preserving pixels, animation timing,
colors and ordering. Full release frame/loading/memory/endurance/Windows/Mac and
original bug gates remain open.

## Accepted decisions and constraints

Candidate remains private pending repeated matched runs. No production changes.
Use muted secondary-display native tests with isolated profiles and bounded disk
output. Do not interpret one-pair means as certified improvements.

## Current state

Private artifacts:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/synergy-geometry-trial/`
and `synergy-geometry-pilot/`. Builders/verifiers/analyzer live in
`output/renderdoc-tools-2026-10-08/` with names containing `synergy-geometry`.
Pilot comparison is `synergy-geometry-pilot/comparison.json`.

Candidate changes only filled circles inside `_draw_functioning_synergy`.
It stores one 66-point unit circle and 192 fan indices per Grid instance;
`Transform2D * PackedVector2Array` prepares current world vertices and
`canvas_item_add_triangle_array` submits the original fan order/current color.
Other draw commands, colors, radii, phase math and ordering stay original. No
persistent asset cache, extra textures, engine upgrade or quality reduction.

The fan follows [Godot 4.7.2's ellipse submission implementation](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/servers/rendering/renderer_canvas_cull.cpp):
64 segments, repeated circumference endpoint, final center vertex and center-first
triangle indices. Unit trigonometric values are generated with Windows float
functions, matching the tested Windows renderer. This does not establish Mac
math/raster parity; Mac remains unverified.

## Verification

Initial prototype used unsupported packed-array constant expressions and failed
to parse; its log is retained as `failed-constant-declaration.log` and excluded.
Corrected to instance-owned fields. Fixture now checks both scripts instantiate
before attempting any comparisons.

Actual debug=false native visual oracle: 576 image-byte comparisons, zero
failures. Six profiles, six sizes (including fractional), four times, two
directions and two coordinate origins, including `(8058.305,8099.799)` with
camera-like translation. Original background and a following overlapping line
are retained to test blending/order. No screenshots written to disk. The earlier
288-case passing log is retained separately. This is focused effect coverage,
not full packaged visual acceptance or 30/60/120 FPS gameplay certification.

Six native gameplay runs, one pair per large40/current10/reported12 map:
9,720 measured frames; lighting/placement/demolition at 1×/2×/4×. All 27 full
states/cameras and 45 successful paired actions exact. No runtime image failures.
Both lanes have the same additive synergy timing counter. Main/Bill fixture
inputs and deterministic idle-alert test clock match the prior accepted baseline.

| Map | Synergy CPU us/sample before → trial | Frame mean ms before → trial | p95 ms before → trial | p99 ms before → trial |
|---|---:|---:|---:|---:|
| Large40 | 653.498 → 524.115 | 25.599 → 25.357 | 42.775 → 42.453 | 55.390 → 54.839 |
| Current10 | 72.098 → 58.819 | 13.023 → 12.372 | 18.609 → 18.042 | 31.573 → 30.052 |
| Reported12 | 1.755 → 1.706 | 13.342 → 13.445 | 19.472 → 19.129 | 23.949 → 22.141 |

Large local drawing cost improves about 19.8%; whole mean improves about 0.94%
in this pair. Current whole-frame improvement is much larger than the measured
13 us local saving, so it cannot be attributed entirely to this change. Reported
map exercises negligible synergy work and has a slightly worse whole mean.
Require repeat pairs; do not claim a broad 5% gain from the current-map number.
Frames over50 ms large29→29/current2→0/reported2→3; none over100 in these runs.
All p95 gates still fail; large/current p99 fail. No release acceptance.

Owner fingerprints unchanged, 2,938 files, both pilot and visual verifier.
All jobs terminal, override restored, accepted Main/Grid/Bill hashes unchanged.
Six completed trace reports compressed in place with exact content hashes.
No runtime/source-tree copies or screenshot batches created.

## Next action

Run two additional alternating pairs per map with these exact candidate inputs,
then compare local savings and whole-frame tails. Admit only if repeated evidence
and relevant regression checks justify it. Keep Mac parity explicitly open.
Repeated drone uploads remain the stronger stutter target; rejected global
enlargement/crop/indexed-provider trials must not be repeated unchanged.
