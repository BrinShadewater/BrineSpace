# Project handoff

Updated: October 6, 2026 · BrineSpace · Rendering layer attribution

## Objective and acceptance
Locate remaining frame costs before changing rendering structure. Diagnostics
must preserve gameplay state and restore all temporary masks; no quality cuts.

## Accepted decisions and constraints
Normal code/art/settings unchanged this interval. Native tests use verified scratch
profiles; all 2,936 owner non-log files unchanged. No performance/release admission.

## Current state
Private probes in `output/water-preparation-2026-10-06/attribution/visible/`,
`layers/` and `layers/surfaces/`. Current water function copied physically.
Layer probes reuse last frozen current-source 40-room station fixture including
accepted classification/water preparation; private compressed crew enabled.
Simulation stops after deterministic warm-up. Rendering visibility masks, rather
than gameplay flags or effects settings, suppress selected CanvasItems and their
children. Original masks restore after each phase. Script preparation may still
run; this separates rendering suppression from a rendering implementation change.

## Verification
Water: three repeats of 90 frames each redraw-frozen/retained-frozen/animated/hidden.
Six checks pass: visible nonblank output and exact retained/frozen pixels per run.
Clean exit, no errors. Median of per-run means: animated ~2.037 ms frame interval,
~0.214 ms viewport renderer CPU, ~0.038 ms GPU; retained-frozen ~0.355 ms interval,
~0.174 ms renderer CPU. Hidden ~0.202 ms interval, ~0.039 ms renderer CPU.
This is a small isolated viewport; not whole-station water cost or acceptance.
Viewport draw/primitive counters returned zero despite verified visible output:
unavailable for this 2D path, not evidence of zero draws. Full logs stored; initial
runner printed too much data, corrected to bounded summary for visible validation.

Whole station: three repeats / 21 phases, 60 samples each after 10 settle frames;
zero state-comparison failures/errors, clean exit. Median renderer CPU means:
baseline 10.441 ms; no-water 10.251; no-contents 7.872; no-surfaces 4.318;
no-environment 7.692; no-grid 0.836; repeated baseline 10.475.
Frame intervals baseline/repeated ~30 ms, no-grid ~20 ms. Frozen rendering masks
are diagnostic ablations and not viable gameplay optimizations. The surface group
includes LIVE room-content children, so costs overlap and cannot be summed.

Surface split: three repeats / 24 phases, same protocol, all crew/drone snapshots
remain equal. Median renderer CPU baseline 10.245 ms; no-live 7.652;
no-floors 8.613; no-walls 9.160; no-foreground 9.631; no-doors 9.914;
no-lights 10.108; repeated baseline 10.163. Largest individual leads are LIVE
contents (~2.59 ms renderer CPU difference), floors (~1.63), walls (~1.09).
GPU measurements vary with workload/power state; do not assume the differences
are additive causal estimates or promise equivalent gains in animated gameplay.

Global draw counter: baseline ~4805, no-live ~3626, no-floors ~3993,
no-walls ~4280. Whole-station no-water removed only ~17 reported calls despite
thousands of submitted textured segments. Command count is not GPU draw count.
Do not assume rebatching water offers a large GPU win from source loops alone.

Initial layer runner omitted benchmark's user-dir argument: isolation guard refused
before fixture writes. Failed log/fingerprint retained; corrected before evaluation.
All processes terminal. Results, summaries, logs and owner receipts retained.
Selected water output inspected; original low-alpha wave appearance retained.

Measurement API scope confirmed in [Godot 4.7.2 RenderingServer documentation](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/doc/classes/RenderingServer.xml).

## Next action
Investigate live room command/material/texture batching and unnecessary per-slot
preparation, then floor/wall command structure. Verify source ownership and effective
filtering before merging textures/material identities; preserve frame-object identity,
layer order, clocks and visuals. Use matched animated station comparisons plus exact
native raster/regression controls for any implementation change. Water remains a
CPU preparation opportunity but evidence weakens it as primary GPU bottleneck.
Remaining engine/script waits, uploads, memory budgets, Windows/Mac packages and
original visual/endurance/release gates remain open. No goal completion claim.
