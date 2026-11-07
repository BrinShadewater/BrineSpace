# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: navigation repeatability and remaining room loading

## Objective and acceptance

Continue the complete PC/Mac performance/release plan. Demonstrate repeatable improvements with unchanged graphs, selected visuals, animation clocks, save state and quality. First large Continue still needs ≤6 seconds; gameplay, memory, endurance and target-hardware/Mac gates remain open.

## Accepted decisions and constraints

The prepared-local-edge candidate remains experimental. No normal runtime admission, art reduction or release upload. Profiles isolated and owner fingerprints preserved. Native attribution does not substitute for packaged performance certification. Avoid concurrent profiling during packaged measurements.

## Current state

Build `5760e46d67c3376b` retained in `output/drone-compiled-2026-10-07/navigation-edges-release/`; its physical QA copy and identity remain in `qa-cold-hints/`. Earlier packages preserved. Repeated comparisons add `navigation-release-pair2-*`, `navigation-release-pair3-*` and consolidated `navigation-release-three-pairs.json`. Diagnostic runner `run-navigation-geometry-profile.py` and separate `restore-geometry*` logs/JSON retain room, constructor/attachment and PNG attribution. Temporary Bill/Grid/SafeImage edits restore byte-exactly.

## Verification

- Three actual debug=false original/fast three-cycle pairs, 263 checks per process, all six clean. Pair two reversed order. First large Continue reference 7.706/7.612/7.573 seconds, fast 6.831/6.789/7.039; medians 7.612→6.831 (~10.3% lower), improvement in every pair. Later median 4.920→5.074 seconds, mixed. Local OS cache uncontrolled, not target-hardware certification.
- All 36 recorded full navigation graphs/crew snapshots and texture endpoints match; each process has 67,121 observed authored-edge parity comparisons with zero differences. Owner's 2,936 non-log files unchanged.
- Three native diagnostic processes pass 262 checks each with zero errors/leaks/warnings. First active Veld restore remains ~1.83–1.84 seconds with the edge candidate; later ~0.17–0.18. Ordinary room factories dominate cold geometry, especially life support, solar array, crew habitat, reactor, research and cryo. Large-room bounds/live props are much smaller in this fixture.
- Lazy-view split narrows factory latency to scene attachment/_ready rather than constructor: life-support attachment 112.827 ms, thermal 102.433, habitat 84.713, reactor 68.492, research 65.530, cryo 62.676. These are nested attribution, not additive gains.
- Scoped SafeImage trace inside navigation geometry records 47 distinct PNG paths / 52 calls. Thirty paths / 34 calls receive no prefetch hit and spend 548.286 ms in load_png; 17 paths fully served by prefetch spend 5.417 ms. This includes PNG handling and possible progress pumping, not isolated decode or GPU upload timing. Missing-order versus already-consumed/evicted cases remain unassigned; no claim all 548 ms can be removed.

## Next action

Inspect first-large-restore prefetch index/task/recent-cache state for these paths, distinguish unknown requests from repeated/evicted requests, and test bounded preparation of the actual selected room images. Preserve runtime PNGs, default pixels/filtering and session release; compare loading peaks/waste and complete gameplay state. Complete sample-all/layout coverage before normal edge admission. Continue title-retention investigation and the full original gameplay/memory/bug/endurance/PC/Mac release scope.
