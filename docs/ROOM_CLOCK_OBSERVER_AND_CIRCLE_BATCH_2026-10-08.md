# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: final zoom observer and exact circle batching

## Objective and acceptance

Continue the full PC/Mac performance/readiness plan. Explain the prior final zoom counter discrepancy before normal silt admission, and establish another exact geometry batching method. No reduced quality, renderer upgrade, art mutation, gameplay decision change or publication.

## Current state

Private benchmark observer records final4x zoom only, bounded2048 entries. Samples before rendering, after rendering and at the benchmark sampling point: twelve large rooms' clocks/context/view clocks, visibility, bounds, operating/water state, live-slot flags and prepare/advance/static/live draw counters, plus camera/preparation state and simulation step count. Copies scalar/state descriptors; no texture readback or mutation. Physical QA adapters restored after each run. Helpers: `room-observer.gd.txt`, `prepare-room-observation.py`, generated runners and `compare-room-observation.py` under `output/renderdoc-tools-2026-10-08`.

Private `circle-triangles.gd` builds ordered native ellipse fan triangles with explicit float32 rounding,64 segments and original centre/fan order, then submits one triangle array. Per-vertex colours preserve float precision; no mesh attribute quantization or primitive conversion. Adapted Godot source retains copyright attribution and existing MIT notice reference. Filled, non-antialiased circles only; not an admitted general ellipse/arc/antialias replacement.

## Verification

Two actual debug=false40-room/four-crew observer pairs using the same identified silt PCK as the three earlier performance pairs. Both pairs record542 entries/lane:181pre,181post,180sample. Extra pre/post at final label179 are preserved and documented; comparator uses the first observation per stage/action-frame. Every recorded room/global state and counter matches across the pair at all compared entries. Phase-end advances19216/live draws117544 both lanes, both pairs. Clean, zero missing images, focused, router released. Owner2936files unchanged; adapters restored byte-identically; runners/native processes terminal. Evidence: `silt-room-observation` and `silt-room-observation-repeat`.

These instrumented runs do **not** reproduce the earlier19216/117544 versus19214/117531 discrepancy. Do not conclude the difference was sampling noise, claim root cause, or close historical discrepancies. Allocation/collection overhead may perturb timing; observer runs are not new FPS acceptance. Prior uninstrumented three-pair mean improvements remain separately scoped. Silt stays private pending lower-overhead reproduction/assignment.

Circle native96checks/0failures/clean:48 exact pixel pairs plus48 draw-count assertions. Four radii(.55,1.15,3.7,15.3), four scales(.23,.73,1,1.7), three rotations, fractional positions, eighteen differently coloured circles including overlapping translucent circles, parent modulation(.8,.9,1,.7). Native reference18 draws versus candidate1 in every case. First fixture used the wrong argument order for current4.7.2 `viewport_get_render_info`; parse rejection retained, corrected against actual runtime signature (type before info), no gameplay rerun involved. Corrected evidence: `circle-batch-native-api-corrected/{result,owner,profile-location}.json`; screenshot files in resolved scratch profile. No actual-room integration, construction-cost or FPS gain demonstrated for circles yet.

## Next action

Reduce observer allocation while preserving meaningful frame labels/clock/visibility evidence, or compare a controlled counter reproduction before silt admission. Separately inventory actual contiguous circle groups (such as floor bolt runs) and prototype the measured hotspot with slot/session-owned geometry. Validate real-room pixels, invalidation and rebuild cost, then matched release workload before admission. The48 exact circle pairs establish a primitive method, not a whole-room or game acceptance. All original integration, nine bugs, loading/frame pacing/memory/endurance, target PC/M1 and signing/notarization/delivery gates remain open; goal active.

Primary geometry implementation: https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/servers/rendering/renderer_canvas_cull.cpp (`canvas_item_add_ellipse`).
