# Station visual gate and zoom attribution

Updated: October 11, 2026 · Project: BrineSpace · Task: performance readiness

## Objective and acceptance

Check the hardened private renderer on reported/current/stress station replays,
preserving complete checkpoint state and pixels. Attribute remaining frame stalls
without changing quality. Keep the full PC/Mac release objective open.

## Accepted decisions and constraints

Provider remains private. No production gameplay or renderer changes this pass.
Muted secondary display, isolated profiles, owner fingerprints and bounded output.
Reuse runtime and existing art packs; no new multi-gigabyte package copies.
Do not repeat the rejected per-room floor-slot or row-strip candidates unchanged.

## Current state

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`hardened-indexed-station-pixels/`, `zoom-redraw-stage-trace/`.
Private fixture/runners under `output/renderdoc-tools-2026-10-08/`.

First six native debug=false runs: 80/80 captured pixel hashes and complete contexts
exact (28 reported, 24 current, 28 large), with all 36 phase checkpoints/cameras
exact. Visual inspection of saved current/large witnesses found a synergy notification
obscuring rooms. This is partial crop evidence, not unobscured station acceptance.
Current map lacks an actor-free workshop; reported/large show case add/move/remove.

Second six-run fixture hides the notification and portrait. Portrait refresh later
sets itself visible again. Result: 60/80 captures exact across all contexts, all 36
phase checkpoints/cameras exact. Five reported, eight current and seven large context
mismatches retained in `visible-comparison.json`. One large capture has equal pixels
but `/comms/seen` differs by the pending `discovery/breathable_quarters` entry.

Saved reported zoom repaint witness: 6567 differing pixels, bbox [2,8,129,79], entirely
over the compact portrait; maximum channel difference 203. This localizes that witness,
not every unsaved image difference. No provider-specific defect or acceptance inferred.

Root causes in current UI source:

- `crew_portrait_panel._process` refreshes and sets visibility from active IDs.
- Notification tween completion calls `_finish_center_toast`, which releases a held
  crew comment and modifies saved comms state. Real-time tween steps can cross that
  boundary at different fixed-step capture times. Comms automatic processing was
  already disabled by the benchmark; the notification callback was still active.

Prepared and started third station-only fixture: disables portrait processing while
capturing, asserts portrait/notification stay hidden, and uses a small fixture-only
main overlay that pauses notification tweens. Replay step manually advances the tween
by 1/60 second; gameplay source remains unchanged. Actual release probe: six checks
pass for paused stability, exact manual property steps and a single completion callback
on a subsequent replay step. Initial exact-duration callback expectation was corrected
after testing the actual engine boundary behavior; no checkpoint epsilon introduced.

## Verification and active work

Third run currently active: terminal session **30842**, Python PID **438628**. Confirmed
live native child PID **436556** when checked. Serial comparator session **53687** waits
for that exact runner. Do not restart while it is live. Next poll these handles, then
inspect `station-comparison.json` and `station-owner.json` after completion. Runtime
configuration is temporarily owned by this test and will be restored in its finally.

Drivers: `run-hardened-indexed-station-only.py`,
`compare-hardened-indexed-station-only.py`, `finish-station-only-comparison.py`.
Earlier `comparison.json` and `visible-comparison.json` retain their distinct scopes.
Capture speed labels 0/1/2 are speed indices; phase labels report actual 1x/2x/4x.

Both completed visual batches and completed diagnostic preserve 2938 owner files.
Pending third batch has not yet supplied its final owner guard. Evidence currently
155.74 MiB visual + 4.85 MiB trace; will grow modestly while reports finish.
C: 124.18 / D: 70.49 GiB free at last check. Existing packs reused for repeats.

## Frame attribution

Reused three-run 40-room traces, no additional benchmark: normal has 15 frames >50 ms
without sampled drone uploads, 13 zoom/2 lighting. They average 34.421 ms grid redraw
work. Earlier indexed variant has 13 such frames, all zoom, averaging 37.337 ms redraw.
This is correlation and sampling-window evidence, not causal proof that uploads never
occurred elsewhere. Script/render timings overlap and must not be added blindly.

New private per-read draw-stage counter trace: one actual debug=false 40-room run,
540 measured zoom/lighting frames. Eight >50 ms frames without sampled uploads,
six zoom/two lighting. Mean stage work in those frames: floor 6.857 ms, floor-rest
1.477 ms, live rooms 4.748 ms, terrain cells 1.869 ms, walls 1.349 ms and door/light
validation 1.279 ms. Instrumented diagnostic only, not a matched optimization result.
`attribution.json` and `existing-frame-attribution.json` retain measurements/scope.

## Next action

Finish the live corrected station-only pass and investigate any remaining exact-state
or pixel mismatch; no broad visual claim until it passes. Then profile a changed floor
submission or zoom rebuild strategy using the measured per-frame stages. The previous
floor-slot trial regressed large-station performance, so merely reinstalling that cache
is not the next move. Preserve pool/shadow/floor ordering, interactive completeness
and selected pixels. No FPS gain accepted this pass. Full release/Mac gates remain open.
