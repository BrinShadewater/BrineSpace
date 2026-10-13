# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: installed bounded circle geometry reuse

## Objective and acceptance

Reduce CPU drawing work with exact selected visuals. This admits a local Windows
optimization; it does not certify FPS/stutters or the broader PC/Mac release.

## Accepted decisions and constraints

Installed guarded circle geometry reuse. Windows uses the precomputed fan; other
platforms keep original `draw_circle`. No automatic quality changes or changed
effect clocks/colors/radii/order. One finite unit-circle/fan array per Grid instance;
no retained assets or extra textures. Mac native performance/visual testing remains
open despite the fallback path's successful Windows execution.

## Current state

Changed `scripts/grid_canvas.gd`, added `tests/test_synergy_geometry.gd` and its
engine-generated UID `uid://bt4bsftw5tldg`, registered it in `tests/index.json`
under render-perf/native. Existing Grid UID preserved; Main/Bill unchanged.
Installed Grid SHA256:
`03a46860e3eb626f31c31e165dc5b5e0ff4c3f4475b612646e306eae9f7b6072`.

Artifacts under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`synergy-geometry-final` (matched suite/comparison/attribution),
`synergy-geometry-control` (dormant-path verification),
`synergy-geometry-installed` (actual installed-source oracle).
Relevant runners/analyzers are in `output/renderdoc-tools-2026-10-08/`.

## Verification

Final guarded actual debug=false suite: 18 native runs, three alternating pairs
per large40/current10/reported12 map, 29,160 measured frames. All 81 full states/
cameras and 135 successful paired actions match. No runtime image failures.

| Map | Synergy CPU us before → installed algorithm | Whole mean ms before → trial | p95 ms before → trial | p99 ms before → trial |
|---|---:|---:|---:|---:|
| Large40 | 657.341 → 523.216 | 25.758 → 25.147 | 43.503 → 42.066 | 56.216 → 53.951 |
| Current10 | 68.150 → 62.742 | 12.488 → 12.780 | 17.868 → 18.575 | 30.652 → 30.106 |
| Reported12 | 1.626 → 1.669 | 12.993 → 13.269 | 18.825 → 19.497 | 22.237 → 23.127 |

Large local cost falls 20.4%, current 7.9%; all six active-map local pair means
improve. Large whole means improve in all three pairs, aggregate 2.37%. Smaller
whole means worsen, so this is not accepted as a universal frame-rate gain.
Frames over50 ms: large95→70/current0→1/reported6→7; none over100. Every map still
fails p95; large/current fail p99. Whole-frame observations do not certify release.

Focused reported-map control: 1,620 frames, zero optimized-circle calls across
all nine phases. States/cameras and 15 actions match its final-suite candidate.
Mean13.034ms vs earlier identical candidate13.269ms. Final-suite traces show broad
timing shifts in unchanged simulation, grid and render CPU work; current pair3
step1.238→1.372ms/grid5.338→5.722ms while local synergy still improves.
This supports environmental/run variation as an inference; its precise cause is
not established. The dormant control excludes new circle submission work as a
per-frame cause on that reported workload. Admission rests on repeatable local
CPU savings, unchanged memory and visual/behavior checks, not adjusted timings.

Texture peaks unchanged in all nine pairs: large3028.476/current1940.818/
reported1559.522 MiB. No global cache or additional image storage introduced.

Installed-source native debug=false regression oracle: 1,152 byte-exact image
comparisons, zero failures, optimized and fallback paths. Six profiles, six sizes,
four times, two directions, small and station-sized coordinates. Original-command
oracle includes overlapping subsequent drawing to cover blending/order. Test
loads the actual installed Grid through an early pack override; its source text
equals the final guarded canonical candidate (without diagnostic timing counter).
Native lane registration verified; index parses and scoped diff check passes.
The actual release executable test is distinct from editor/headless certification.

Owner fingerprints remain 2,938 files, zero changes in suite, control and installed
oracle. Muted secondary display, isolated profiles. All native jobs terminal;
runtime override restored. Nineteen terminal trace reports compressed with exact
content hashes. No screenshots or runtime/source-tree copies added.

## Next action

Return to repeated drone upload costs using the existing ranked paths and rejection
evidence. Choose a materially different bounded lossless storage/lifetime remedy;
do not rerun unchanged global cache enlargement/crop/indexed-provider trials.
Remaining full frame/loading/memory/endurance, original nine bug checks, save/UI
flows, Windows target hardware and Mac gameplay/signing/notarization remain open.
