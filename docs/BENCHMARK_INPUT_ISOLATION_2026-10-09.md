# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: deterministic performance input

## Objective and acceptance

Prevent physical input from changing automated station state while retaining scripted workload actions. Preserve report compatibility and physical-input gameplay certification as a separate requirement.

## Accepted decisions and constraints

Only benchmark infrastructure changes, not the game UI/input defaults. Saved hover is retained in comparisons. Do not erase differences to obtain a pass. All Godot probes use isolated profiles and before/after owner fingerprints.

## Current state

`tools/release_benchmark.gd` now disables viewport input before scene loading, checks it remains disabled in `visible_for_measurement`, and adds `benchmark_input_disabled`/`input_scope` report fields. Existing UID unchanged. Scripted actions still call game methods. This prevents the observed real-pointer `_gui_input` hover mutation; it does not certify physical keyboard/mouse/trackpad interactions.

Godot documents the public viewport input setting as blocking received events: [Viewport input documentation](https://docs.godotengine.org/en/4.5/classes/class_viewport.html#class-viewport-property-gui-disable-input). Native behavior was checked against installed 4.7.2 rather than inferred from the 4.5 docs alone.

## Verification

`output/renderdoc-tools-2026-10-08/test-benchmark-input-isolation.py`: red missing isolation API, one expected failure; green eight native checks/zero failures. Enabled `_input` and `_gui_input` receive a pointer event; disabled handlers do not; scripted property changes still work; restored input receives events again. Both runs preserve owner 2,938 files. Evidence `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/{red,green}/`.

The motivating same-pack collection comparison has three reverse differences, all `/state/hover_cell`; other compared state fields match. Source `_gui_input` emits `cell_hovered`, whose Main handler edits hover and queues redraw. No gameplay-state defect attributed to preparation. The uncontaminated forward candidate was slower at all speeds, so it is rejected independently of the reverse mismatch.

## Next action

Actual original physical `debug=false` PCK/EXE smoke completes, session 99894 terminal 0, `benchmark-input-isolation/packaged-smoke/`. No renderer overlay. 540 samples; disabled-input report true, hover `(19, 18)` identical at 1×/2×/4×, empty missing-art failure dictionary, clean log, owner 2,938 unchanged. Mean 26.288/28.048/28.733 ms and p95 30.213/38.111/41.339 ms still fail FPS gates; this is harness validation, not a new optimization gain or hardware certification.

Future renderer comparisons should use this corrected infrastructure. Keep benchmark fixtures and physical-input gameplay certification distinct. Do not re-benchmark the rejected preparation variant solely to seek a favorable result. Retain original renderer and accepted delivery; continue measured steady-rendering/system work plus the full release workload/bug/endurance/Windows/Mac gates.
