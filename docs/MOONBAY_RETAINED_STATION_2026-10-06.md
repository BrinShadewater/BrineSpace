# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: retained large-room station integration

## Objective and acceptance

Reduce measured large-room redraw overhead without changing visuals, animation, ordering or gameplay. Full release performance and PC/Mac certification remain open; this is a private prototype, not normal admission.

## Accepted decisions and constraints

Private Grid integrates ordered large-room containers behind the LIVE parent, keeping each base before its live props. Moonbay base retains native commands with the previously tested complete state key; other large bases still redraw. Flooded equipment remains on its original shared LIVE-parent layer, above the complete base sequence. Room replacement rebuilds base/prop children; obsolete/out-of-view slots are hidden or removed. No detail/AA/quality changes.

## Current state

Evidence and physical fixtures: `output/moonbay-retained-station-2026-10-06`. Accepted experimental revision under `revision/`, including `large_slot.gd`, explicit physical Main/Grid copies, runner/comparison and native overlap probe. Normal runtime and test index unchanged this turn.

First station integration hid/shows every slot every frame: cache hits rose but Moonbay redrew every frame, saving little. That behavior is rejected. Revision only hides rooms leaving the visible set. First overlap probe passed eight dry cases but failed eight flooded cases: wet equipment was drawn in per-room layers. Corrected prototype keeps wet equipment on the original parent; both corrected 16-case composition runs pass, final run also swaps room types at existing slot positions.

## Verification

Revised native matched mixed 40-room pair: 12 multi-cell rooms including three Moonbays, idle/pan at 1/2/4x, 60 measured frames per phase. Actual retained execution verified: 12 slots, three Moonbays, hits 715→1615, base redraws constant at seven in all phases. CPU live-room preparation including new child base/prop callbacks falls by 6.82–7.22 ms/frame, from 17.06–17.92 ms to 10.16–10.80 ms. Excluding child callbacks would falsely inflate the saving.

| Phase | Baseline p95 ms | Candidate p95 ms |
|---|---:|---:|
| Idle 1x | 64.069 | 52.553 |
| Pan 1x | 65.678 | 53.470 |
| Idle 2x | 61.329 | 50.564 |
| Pan 2x | 65.559 | 52.396 |
| Idle 4x | 73.456 | 69.272 |
| Pan 4x | 78.172 | 63.951 |

One matched pair is promising, not repeatable release acceptance. All crew/drone snapshots, power/zoom and complete door/light entries equal. Texture counters equal first three and final phases; intermediate candidate counters ~61.25 MiB lower, cause unassigned. Final both 3036.131 MiB. No memory-saving claim. These fixtures use private compressed crew/drone changes, debug=true and synthetic fixture reserves; neither packaged acceptance nor minimum-target hardware certification.

Native overlap checks: all four large-room types, four rotations, deliberately overlapping bounds, dry/flooded, offline overlays and inherited modulation. Corrected initial 16 exact pairs and final replacement 16 exact pairs pass. Previous standalone complete-base check remains 385 checks / 256 exact pairs. All successful processes terminal and clean; each isolated run preserves 2,936 owner files. An early overlap test ran while the first station candidate was starting; do not use that pair for loading acceptance. Revised pair ran without concurrent native visual testing.

## Next action

Before admission: verify actual mixed-station composition including ordinary retained rooms and parent-drawn BRINE signals; complete pan/continuous zoom/filter/material checks, active Moonbay mission clocks, layout mutation, demolition/replacement/culling/show recovery, wet-equipment ordering and scene release. Add permanent native regression coverage and account child callback cost in normal diagnostics. Repeat a matched workload only after these integration changes/checks justify it. Investigate texture counter history separately. Keep the full 16.7-ms p95 target and all PC/Mac release gates; prototype still substantially exceeds them.
