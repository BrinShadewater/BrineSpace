# Workshop retention with exact camera invalidation: installed cleanup

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Continue the full performance/release plan. This milestone installs a small measured
CPU cleanup, closes its workshop zoom regression and repairs a visual fixture. It does
not meet the frame gates or certify a new export. All broader requirements remain.

## Accepted decisions and constraints

Reuse actor-free workshop contents only while camera/scale, layout, doors, power,
flooding and validated cosmetic case payload remain unchanged. Do not normalize away
workshop camera fields during pan/zoom: scaling old commands changed prop-edge pixels.
Actor entry, companion/recovered sites and nonplain views still force preparation.
Preserve art, timing, cargo mechanics, save bindings, default quality and owner data.

## Current state

Installed `scripts/grid_canvas.gd` and `scripts/james_cargo_workshop.gd` match the
measured strict candidate; only two explanatory comment lines differ in grid source.
New `tests/test_workshop_retention.gd` and paired UID provide ten ownership/invalidation
checks, registered as headless in `tests/index.json` render-perf. Existing script UID
pairs and unrelated dirty worktree changes preserved. No export, commit or upload.

The first camera-normalizing candidate remains rejected. This correction gives up most
of its apparent 3.18% mean gain; admission is a CPU-work reduction, not a major FPS win.

## Verification

18 actual debug=false Windows RTX 4070 Ti / 1080p native performance runs, three
alternating pairs per real reported save, frozen current save and deterministic 40-room
fixture. 19,440 measured frames: idle/pan/zoom/lighting at 1x/2x/4x, 90 frames/phase.
All 108 paired state/camera phases exact. Textures unchanged at 1,558.872 / 1,940.831 /
3,028.007 MiB respectively. No measured frame over 100 ms. Source overlays share the
reused release PCK; dedicated fixture economy and manual stepping apply. These are not
fresh frozen candidates, target-hardware tests or complete workload certification.

| Map (rooms) | Mean ms before -> installed | Change | p95 ms | p99 ms | Frames >50 ms |
|---|---:|---:|---:|---:|---:|
| reported (12) | 13.008 -> 12.925 | -0.63% | 19.000 -> 18.839 | 23.038 -> 22.524 | 0 -> 0 |
| current (10) | 12.001 -> 12.045 | +0.37% | 16.988 -> 17.376 | 26.038 -> 25.706 | 2 -> 0 |
| large (40) | 25.764 -> 25.658 | -0.41% | 42.389 -> 42.444 | 54.888 -> 54.146 | 59 -> 59 |

Large means improve in two pairs and worsen in one; pooled gain 0.41%, p95 slightly
worse, >50 ms unchanged. Large setup/configure timing 461 -> 416 us, skipped setups
123,105 -> 134,103. Reported means improve in all three pairs, pooled 0.63%. Current
map has no workshop and equal skip counts: 0.37% pooled slower, mixed pairs; no claimed
improvement there. All p95 release gates fail, current/large p99 also fail. Investigate
remaining >50 ms frames; no endurance or memory-growth acceptance.

Installed-source isolated regression test: ten checks, zero failures. Case add/move/
remove keys, deep snapshot ownership, actor entry/exit and companion/recovered guards.
Runner list recognizes the new headless test. Diff whitespace checks pass. New UID
created with the engine; no existing UIDs regenerated.

Visual fixture repaired: prepare the surface pass as well as repainting existing child
slots, focus a visible workshop for case changes, and capture before JSON serialization.
Cases really alter pixels: add 533, move 1,052; removal restores the original exactly.
Original candidate with repaired fixture: 18/28 exact, nine workshop zoom mismatches
plus the initial case focus. Strict candidate: workshop differences gone, 27/28 exact,
one previously observed background-wreck mismatch. Exact-transform/last-painted-size
trace: strict 28/28 pixels and terrain contexts exact; forced wreck repaint changes
zero pixels in both lanes. No intentional pixel tolerance introduced.

**Independent baseline discrepancy confirmed:** reference-versus-reference overlay PCKs
are byte-identical. Yet their 2x zoom frame 89 differs by 8,879 pixels at bbox
[1240,149,1327,253], max channel delta 8. Saved state, camera, clock, lights, terrain
keys, exact transform bits and last-painted sizes match. Within-run forced wreck
redraw changes neither image; cross-lane difference remains. 27/28 control hashes
match. Therefore workshop reuse is not required to trigger this discrepancy. Root
cause is still unproven: do not claim a GPU/engine/texture defect without further
command, material and pixel evidence. It remains an open release visual issue.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`workshop-retention-pixels-trace`, `workshop-retention-strict-pixels`,
`workshop-terrain-redraw-trace`, `workshop-retention-strict`,
`workshop-baseline-pixel-control`. Runners/comparators in
`output/renderdoc-tools-2026-10-08/` use those names. This batch adds 400.40 MiB,
including only suspect PNGs for the identical-source control. Runtime reused, no full
package/source copies. C 124.65 / D 71.54 GiB free; maintained 20 GiB floor enforced.
All owner guards 2,938 unchanged. Jobs terminal and QA configuration restored.

## Next action

Use the identical-input wreck reproduction to compare actual texture pixels, draw
rect/UV bits and inherited material/filter state at the suspect boundary; exact node
transforms alone did not explain it. Avoid repeating uninstrumented full visual batches.

For larger performance gains, return to measured grid/content/floor-light preparation
and the indexed provider's zoom/gait precision blocker. The installed workshop cleanup
is too small to meet the frame target. Preserve floor/pool/seam order and actual actor
calls. Indexed loader/fallback/lifetime, broad workload/1440p/target GPU, endurance,
packaged original bug closure and full Windows/Mac certification remain open. No
Apple Silicon gameplay or notarized Mac candidate has been certified by this work.
