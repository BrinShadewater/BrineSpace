# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: large-base census and animated water batching.

## Objective and acceptance
Continue full PC/Mac readiness. Reduce actually executed room drawing work without changing pixels, animation clocks or selected effects. Private prototypes require real workload CPU/render comparison before admission.

## Accepted decisions and constraints
No art/quality/simulation changes or renderer upgrade. Frozen hiding experiments are attribution only. Extend existing credited WaterStrokes geometry, retaining native antialiasing/order. Scope geometry ownership to canvas/current water region, no visited-frame history. Preserve original prototype/evidence.

## Current state
New room-base-census.gd/run-room-base-census.py: four fresh actual debug=false40room experiments, one base type hidden per process. New private moonbay-dynamic-strokes.gd extends stationary WaterCommands path to advancing clocks/partial levels; separate moonbay-dynamic-current-strokes.gd owns current state per floor only. New native pixel/draw/ownership tests and runners under output/renderdoc-tools-2026-10-08. Normal game/art source unchanged.

## Verification
Frozen normal5079draw calls every process. Three Moonbay bases hide708calls/median1.230ms; threeTidal242/.088ms; threeHydro156/.214ms; threeStorage156/.552ms. Sum calls1262 matches earlier large-base total; timings are noisy/overlap and do not certify gains. All crews unchanged/unfocused0/errors0/owner2936same/adapter restored/jobs terminal. Reports room-base-census/summary.json.

Moonbay._draw_water uses cached/batched strokes only at clock0/full water; nonzero clock or partial water falls back to independent polylines. Native first extension288exact pixel pairs0fails; draw/cache extension864checks0fails. Separate current-state variant1152checks0fails:288exact pairs across levels.2/.7/1, clocks.17/1.23/38.9, pumping on/off, four rotations, scales.31/.73, nearest/linear, fractional positioning. Actual viewport drawcalls47-206 reference versus3 candidate in EVERY pair. One floor owns exactly one geometry entry despite changing clocks/levels/pumping, maximum16regions per canvas. No GPU texture/art modifications. Owners2936same allthree; clean terminal logs/results in moonbay-dynamic-native, moonbay-dynamic-draw-native, moonbay-current-native. This is water-only native proof, not full-room/gameplay motion or FPS acceptance.

Storage hit~0free during completed probes; reclaimed only checked generated scratch shader caches and equivalent copied JSON/PNG reports:143files18.727MiB (hot-shader-reclamation),41files5.444MiB (room-census-shader-reclamation),4copies11.952MiB (corrected-gate-copy-reclamation). Full hash/path ledgers preserved; primary reports/source/art/archives/packages unchanged. Free space remains volatile/critical; no full export or large capture.

## Next action
Run bounded actual animated40room old/current-batch comparison with module execution proof on Moonbay bases, CPU construction time, native/render time, textures/geometry lifetime and counters/camera state. Avoid claiming GPU draw reduction implies net gain: dynamic triangle generation might cost CPU. Require full-room motion/settled parity before admission, preserve pumping/flood/doors and reduced-motion choices. Then consolidate only measured improvements into normal source. Historical2/13zoom work issue remains open independently. Full original nine bugs, loading, endurance/transitions, targetPC/M1/signing/notarization/frozen packaging gates remain open.
