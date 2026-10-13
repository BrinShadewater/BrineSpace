# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: repeated circle-fan comparison

## Objective and acceptance

Reduce rendering cost with exact selected visuals and matched gameplay evidence.
Full release gates remain open; a component saving is not whole-game certification.

## Accepted decisions and constraints

Repeated evidence supports the geometry algorithm as a local Windows CPU
optimization, not a demonstrated broad FPS remedy. Keep private until the
platform guard and regression test are verified. Mac has not established float
or raster parity, so retain its original circle drawing unless native tests pass.

## Current state

Eighteen runs are complete under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/synergy-geometry-pilot/`.
`comparison.json` and `synergy-repeat-summary.json` hold the three-pair results.
Runner/analyzer names: `run-synergy-geometry-repeat.py` and
`analyze-synergy-geometry-repeat.py` under `output/renderdoc-tools-2026-10-08/`.
Existing six pilot results reused only after all source identity hashes matched.

No production edits. Separately prepared `synergy-geometry-trial/candidate-guarded-grid.gd`
uses cached geometry only on Windows and original `draw_circle` otherwise;
the frozen measured candidate remains unchanged. This new guard has not yet
been executed or benchmarked. `proposed-test.gd` contains an original-command
oracle intended for a maintained native regression check; not yet registered.

## Verification

Three alternating reference/candidate pairs for each large40/current10/reported12
map, 29,160 measured frames. All 81 full states/cameras and 135 successful paired
actions exact. Native debug=false, muted secondary display, isolated profiles,
no runtime image failures. Focused prior 576 pixel comparisons still apply to
the unchanged measured geometry candidate, not yet to the new guarded variant.

| Map | Mean synergy CPU us before → trial | Mean frame ms before → trial | p95 ms before → trial | p99 ms before → trial |
|---|---:|---:|---:|---:|
| Large40 | 664.302 → 532.838 | 25.873 → 25.836 | 43.932 → 43.199 | 56.678 → 56.743 |
| Current10 | 70.421 → 59.316 | 12.833 → 12.408 | 18.242 → 18.018 | 31.149 → 31.575 |
| Reported12 | 1.586 → 1.605 | 12.836 → 12.850 | 18.644 → 18.399 | 21.879 → 21.325 |

Large local saving 19.8%, current 15.8%; all six local pair means improve.
Large pair CPU us: 653.498→524.115, 679.343→540.255, 660.065→534.144.
Current: 72.098→58.819, 69.310→62.619, 69.856→56.510.
Reported has negligible synergy work and no useful local saving.

Whole means are mixed within each map; large aggregate saving only 0.14%.
Current mean difference exceeds the local saving and cannot all be attributed
to this algorithm. Large/current p99 slightly worsen. Frames >50 ms:
large94→95/current2→4/reported6→7; none >100. All p95 gates fail, large/current
p99 fail. No broad FPS, stutter or release acceptance claim.

Texture peaks unchanged on every pair: large3028.476/current1940.818/
reported1559.522 MiB. Owner fingerprint unchanged: 2,938 files. All jobs terminal,
runtime override restored. Eighteen terminal trace reports compressed, every
content hash unchanged. C:134.63/D:68.41 GiB free. No screenshots or runtime copies.

## Next action

Validate the guarded candidate against original-command pixels, exercising both
the enabled and fallback paths. Register/run the maintained native oracle and
check the final guarded source's performance before production admission.
Repeated drone uploads remain the larger pacing target; preserve the recorded
rejections of unchanged cache enlargement, cropping and indexed-provider trials.
