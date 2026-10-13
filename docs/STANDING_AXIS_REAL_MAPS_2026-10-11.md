# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: standing-axis real-map verification

## Objective and acceptance
Verify the installed direct socket collision checks on the reported 12-room and deterministic 40-room stations. Full PC/Mac release gates remain open.

## Accepted decisions and constraints
Muted secondary-display, isolated profiles, owner fingerprints, shared debug=false runtime. Preserve art, gameplay timing, layouts and saves. No screenshot batches, runtime copies, source refactor or automatic quality reduction.

## Current state
No production logic changed in this pass. Private paired runner and analyzer in output/renderdoc-tools-2026-10-08; evidence in D:/bs-release-crew-cache-20261009/benchmark-input-isolation/standing-axis-other-maps/comparison.json. Reference restores the pre-change four dot comparisons; candidate uses installed bill_npc.gd. Three alternating pairs per map, twelve phases per run, 90 frames per phase: 12 native runs, 12,960 frames. Actions idle/pan/selection/zoom-selection at 1x/2x/4x. Frozen reported checkpoint and copied owner layouts; this does not cover every release workload.

## Verification
| Map | Mean before → after ms | p95 before → after | p99 before → after | >50 ms before → after |
|---|---:|---:|---:|---:|
| Reported 12 rooms | 12.080 → 12.072 | 17.556 → 17.706 | 26.307 → 26.220 | 0 → 0 |
| Large 40 rooms | 25.111 → 25.210 | 36.774 → 36.978 | 51.115 → 50.425 | 36 → 35 |

Reported mean -0.065%; large +0.391%; mixed pairs on both maps. Effectively neutral whole-workload result, no broad FPS gain. Large maximum 89.629→92.814 ms; neither lane has a frame >100 ms. Texture unchanged: reported 1559.506 MiB, large 3028.686 MiB. Large memory fits initial 3 GiB budget but frame gates fail. Reported p95/p99 also exceed gates. RTX 4070 Ti evidence is not GTX1650/M1 certification.

All 72 full phase states and cameras plus 324 UI snapshots exact. All logs free of engine/script errors and safe-image failures. Owner fingerprint 2938→2938 with zero changes. Native process terminal, runtime override restored. Evidence 36.82 MiB; scratch profiles retained. Free C 122.68 / D 69.23 GiB. No large capture or runtime copy generated.

Room paint attribution collected separately: 1080 frames, no missing frame dictionaries or label overflow. Category measured paint averages: live library 1.565 ms/frame, props 0.449, prop passes 0.341, crew 0.256. Largest individual groups mining ROV docks and BRINE chamber. Instrumentation has overhead. Its older fixture omitted the expected selection actions (post-run validation failed) and matched only one phase against the newer control; do not use it for parity, FPS admission or causal conclusions. Owner unchanged/override restored. Scope and limitation recorded in attribution-summary.json.

## Next action
Correct attribution fixture to use the current deterministic selection/zoom/UI workload before matched drawing experiments. Separate room renderer context setup, dock animation and continuously changing screen/effect command generation. Preserve animation pixels/timing and default quality; do not freeze continuous effects. Existing direct collision check optimization remains a small equivalent CPU primitive improvement; this evidence provides no reason to claim broad station speedup. Full loading, endurance, bug/UI coverage and packaged Windows/Mac hardware/signing certification remain open.
