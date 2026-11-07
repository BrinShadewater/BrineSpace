# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: shared indexed renderer real-map decision

## Objective and acceptance

Reduce texture/upload pressure while preserving pixels, gameplay and frame pacing.
Full PC/Mac performance/release goal remains open. This experiment is private.

## Accepted decisions and constraints

Do not install shared indexed renderer as an FPS optimization: all nine matched
mean comparisons worsen. Preserve accepted production changes. No art reduction,
automatic quality change, source refactor or owner data changes. Retain this
experiment as measured memory/stutter evidence, not release certification.

## Current state

New runner `output/renderdoc-tools-2026-10-08/run-shared-palette-real-map-repeats.py`
and summarizer alongside it. Current-source private Grid/Main fixture and hardened
Bank/Group/Session resource map in `shared-command-backend/`. Existing native
runtime reused. Artifacts at
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/shared-palette-real-map-repeats/`.
Production source unchanged. Source identities retained; no screenshots/art/runtime
copies. Additive diagnostics count unique shared banks/palette bytes per phase.

## Verification

18 actual debug=false native runs: three alternating pairs per reported 12-room,
current saved 10-room and deterministic 40-room station. Idle/pan/zoom/lighting,
1×/2×/4×, 90 measured frames/phase: 19,440 frames total. All 108 full gameplay
states/camera paths/action-speed labels exact. All candidate phases: enabled
provider, complete scan, no duplicate ordinary-cache sources, exactly one shared
Bank and 1,209,344 shared GPU palette bytes. No engine or missing-art errors.
First reference also passes selected-gait 10,224 samples/144 cases across 30/60/120
FPS and 1×/2×/4×; pause/restore preserved. Existing native pixel/input/lifetime
acceptance linked in [prior handoff](SHARED_DRONE_PALETTE_FEASIBILITY_2026-10-11.md).

Pooled matched reference→candidate values:

| Map | Mean ms | p95 ms | p99 ms | >50 ms | Peak texture MiB |
| --- | --- | --- | --- | --- | --- |
| Reported | 12.875→13.027 | 18.606→18.855 | 21.960→22.613 | 0→0 | 1558.872→1529.784 |
| Current | 11.981→12.077 | 17.271→17.290 | 25.757→22.452 | 0→0 | 1940.747→1912.633 |
| Large | 24.598→24.882 | 39.740→39.979 | 48.838→46.248 | 28→6 | 3028.007→2569.149–2630.399 |

Each mean pair worsens: reported +0.61–1.74%, current +0.53–1.14%, large
+0.63–1.53%. Large >50 counts improve in all three pairs (9→1,9→3,10→2),
but p95 and mean do not meet target. No frame >100ms in either lane. Large max
69.553→55.104ms; end texture 1924.488→2017.900MiB, so peak reduction is not a
claim of universally lower retention.

Profile attribution, not additive whole-frame accounting: large exterior callback
1.203→0.834ms and content drawing 2.496→2.118ms; render CPU 6.116→6.123ms,
GPU 4.559→5.233ms. Current GPU 2.119→2.577ms; reported 3.262→3.274ms.
Draw calls effectively unchanged. Evidence supports a CPU draw-work/GPU-time
tradeoff; it does not establish the shader's precise GPU bottleneck.

Owner fingerprint 2,938 files unchanged. Jobs terminal; runtime override restored.
Top-level generated evidence 52,710,944 bytes; C134.03/D68.20GiB free, above
20GiB floor. No destructive cleanup performed. Initial generated runner escaping
error occurred before any engine launch and was corrected; full run completed.

## Next action

Keep this renderer private. Focus next measured work on remaining frame costs;
inspect current door/light validation and dynamic room redraw invalidation against
the existing traces before changing code. Avoid unchanged palette/cache/paging
reruns. Any revisit of the indexed renderer needs a distinct measured remedy for
the GPU increase or explicit evaluation as a memory/stutter tradeoff. Full loading,
uncapped frame-tail, endurance, packaged bug/visual/UI/save, target hardware and
Mac/signing gates remain open.
