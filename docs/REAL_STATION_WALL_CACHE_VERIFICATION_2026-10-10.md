# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: real-station wall-cache verification

## Objective and acceptance

Verify the private retained wall context on saved station layouts using matched
native workloads, without changing selected visuals or the owner's progress.
The full PC/Mac release plan remains open; this is targeted optimization evidence.

## Accepted decisions and constraints

Reuse the physical QA executable/PCK with small source overlays. Actual debug=false,
RTX 4070 Ti, 1920×1080; muted secondary display, input blocked, isolated APPDATA,
copied owner layouts. Both lanes include current accepted navigation, preparation,
galley/shadow changes and the installed atmosphere-mask fix. Reference uses global
wall keys; candidate uses the private retained local context. No quality changes.

## Current state

Normal renderer and frozen PC/Mac packages remain unchanged. Private drivers under
`output/renderdoc-tools-2026-10-08/`: `retained-wall-motion.gd`,
`run-retained-wall-motion.py`, `run-retained-wall-mask-performance.py`, and
`analyze-retained-wall-mask-performance.py`. CURRENT_STATUS records this result.

## Verification

Saved reported 12-room station and deterministic 40-room extension of that save,
with active crew/drones/production: three alternating-order pairs per map, 12 native
runs, 19,440 measured frames. Lighting, card selection/connected direct placement,
demolition at 1×/2×/4×. All 54 phase-end gameplay states match. Scripted callbacks
and placement stress do not certify physical input or the normal construction queue.

| Metric | 12-room reference → candidate | 40-room reference → candidate |
| --- | --- | --- |
| Mean frame | 15.119 → 15.106 ms | 27.953 → 27.579 ms |
| P95 | 21.811 → 21.687 ms | 47.438 → 46.102 ms |
| P99 | 28.284 → 27.758 ms | 62.834 → 61.984 ms |
| Maximum | 78.267 → 81.389 ms | 124.688 → 106.432 ms |
| Frames over 50 ms | 12 → 9 | 124 → 111 |
| Frames over 100 ms | 0 → 0 | 17 → 13 |
| Construction frame mean | 51.953 → 49.219 ms | 111.336 → 100.533 ms |
| Construction grid-draw mean | 23.242 → 20.761 ms | 45.708 → 37.062 ms |

Large-map mean improves 1.34%; all three large pairs favor the candidate. Small-map
mean improves only 0.084%, with mixed pair results. Large construction shortens
10.80 ms (9.7%), with 8.65 ms less draw work. Texture peaks unchanged between lanes:
1,586.18 MiB small / 2,784.06 MiB large. Both maps still fail the lighting-inclusive
p95/p99 gates; large-map stalls over 100 ms remain. No general 60 FPS claim.

Slow-frame records retained. Candidate large-map frames over 50 ms: 71 lighting,
27 placement, 13 demolition. Its two longest frames are placement with zero sampled
drone uploads, ~47 ms step time and ~37 ms grid draw; these intervals overlap and
must not be summed as independent costs. Lighting and synchronous rebuild work
remain concrete targets, alongside the separately established drone-upload issue.

Native rendering: 23 exact RGBA edge/settled pairs plus 16 exact RGB cached/forced
crew-pose/light-fade pairs. Hidden-actor controls differ in visible station regions
at every step; selected image reviewed. Frozen clock with scripted visual poses,
not animation-rate/navigation simulation certification. Cache reuse exercised;
weak references confirm Grid and retained context release after scene exit.
Initial motion adapter assertions were wrong: Grid redraw alone does not execute
the retained wall pass. Corrected fixture queues that pass; original failures kept.

Every owner fingerprint unchanged (2,938 files); source hashes guarded, jobs terminal,
shared configuration restored. New evidence 118.68 MiB plus 317.23 MiB scratch,
including failed motion attempts; no full package copies or deletion retries.
C:127.00 GiB / D:79.67 GiB free; 20 GiB storage floor remains enforced.

Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`,
`retained-wall-mask-{reported,large}-performance/` (paired analysis, traces,
frames-over50, owner guards), corresponding inputs/runtime packs, and
`retained-wall-motion-lifetime-v3/` (native log, source identity, owner guard).

## Next action

Admit the narrowly scoped retained context with maintained regression coverage and
normal-source native verification. Then profile lighting-specific redraws and the
remaining synchronous construction/rebuild step; optimize measured work, preserving
visibility, simulation timing, and default effects. No repeat of unchanged full
batches just to seek better numbers. Full target-PC/Mac, endurance, original bugs,
latest-source packaging/signing and release certification remain outstanding.
