# Drone material retention trial: rejected

Updated: October 10, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Test whether repeated shader, uniform and canvas-material assignments explain the
lack of an average-frame gain from private indexed drone storage. Both lanes use
indexed21, current construction/Solar fixes, and the same 40-room fixture. Accept
only a measured gain with equivalent state, pixels and resource lifetime.

## Accepted decisions and current state

Reject conditional material retention: it removes repeated assignments but does not
improve performance. Keep the existing indexed provider private and unchanged. No
production gameplay, renderer or art edits were made. No quality or animation-frame
reduction, export, commit, release upload or certification.

Private group code retains slot-owned shader/material bindings and changes palette
or flood parameters only when values change. Ordinary art and unsupported-filter/
material fallback restore inherited material; release clears added references.
Review caught an omitted ordinary-slot reset before acceptance. The known test
process was stopped, the runner restored configuration/profile guards, and the
corrected candidate was rerun. The rejected pre-correction script remains as evidence.

## Verification

Six debug=false Windows native performance runs, three alternating pairs, 6,480
measured frames. RTX 4070 Ti, 1080p, isolated saves, muted secondary display,
physical input disabled, bounded trace collection, no captures in measured phases.
The unchanged first reference run was reused after the interrupted candidate.

| Metric | Existing indexed21 | Conditional retention |
| --- | --- | --- |
| Mean frame ms | 28.715 | 29.409 |
| p95 ms | 46.999 | 47.801 |
| p99 ms | 60.234 | 62.833 |
| Frames >50 ms | 96 | 117 |
| Frames >100 ms | 1 | 0 |
| Maximum ms | 101.685 | 96.057 |
| Peak texture MiB | 2629.355 | 2629.355 |
| Renderer CPU ms | 6.905 | 7.097 |
| Renderer GPU ms | 4.595 | 4.737 |

Mean regresses 2.41%. Pair means: 29.065 -> 29.046, 28.619 -> 28.953,
28.463 -> 30.226 ms. No consistent gain; worsening p95/p99 and >50 ms counts.
All 36 captured state and camera comparisons are exact. Complete backend scans
observe 21 sources, no original indexed-source duplication and no fallback.

Counters summed at each run's final phase (include warmup/camera resets as well as
measured work): shader assignments 23,697 -> 96; uniform assignments 23,697 -> 713;
canvas-material assignments 164,890 -> 1,611. Palette draws 23,697 -> 23,694.
Removing writes does not establish a performance gain; keep the measured rejection.

A separate scoped station-art fixture passes 24/24 exact RGBA image pairs at matching
state, camera, animation clock and light levels across idle/pan/zoom/lighting and
1x/2x/4x. It uses the established fixed-light/synchronous-camera capture method,
completes pending decoding, drains background redraws, refreshes portraits and hides
hand/discovery overlays. It does not certify all filters/materials, full UI, native
asynchronous pacing or session lifetime. Visual results do not replace timing gates.

Private runners/comparators: `output/renderdoc-tools-2026-10-08/` names
`run-indexed21-material-retention*` / `compare-indexed21-material-retention*`.
Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/` directories
`indexed21-material-retention` and `indexed21-material-retention-pixels`.
All 2,938 owner files unchanged; 76/77 source-resource identities unchanged;
processes exited and runtime configuration restored. Evidence totals 235.46 MiB.
Free space C 124.75 / D 72.49 GiB; existing runtime reused and 20 GiB floor enforced.

## Larger measured target

Reanalysis of the previous three normal-source large-map traces, without new runs:

| Action | Frame ms | Manual simulation step ms | Grid callback ms | After step, before render ms | Render signal interval ms |
| --- | --- | --- | --- | --- | --- |
| Idle | 29.323 | 2.901 | 12.673 | 17.968 | 8.196 |
| Pan | 27.780 | 2.778 | 11.153 | 16.616 | 8.120 |
| Zoom | 30.539 | 2.600 | 13.183 | 19.737 | 7.973 |
| Lighting | 34.716 | 2.595 | 17.816 | 23.753 | 8.005 |

Grid callback totals include nested rendering preparation and uploads; they overlap
other scopes and are not independently additive. These figures identify a much
larger CPU target than material assignment. `work-split.json` records the analysis
in the previous `indexed21-current-normal-real-maps` evidence directory.

Current source `_surface_state()` keys fading room lights globally, invalidating both
floor halves; `_paint_surface()` then reconfigures and redraws the layered floors in
room order. The comments require preserving per-room light-pool/seam ordering.
Do not remove the fade dependency or change layering to make a benchmark pass.

## Next action and remaining work

Trace floor-only room configuration/drawing, distinguish static geometry from
changing light-pool/seam output, and test bounded command retention or reuse only
where measured costs justify it. Preserve ordering and selected pixels, owner
layouts, structural invalidation, doors, water and zoom behavior; compare real maps.

The prior normal-vs-indexed tiny Branforth gait-phase discrepancy remains open;
this trial's exact indexed-vs-indexed state result does not resolve it. Loader,
filter/material fallback and lifetime validation still precede provider admission.
All performance, endurance, bug-closure, Windows target-hardware and Mac release
gates remain open. Keep the original readiness objective active.
