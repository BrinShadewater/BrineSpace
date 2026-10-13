# Real-map inspector verification and indexed-material checks

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Verify installed preview retention on real saves; close specific private lossless
renderer validation gaps. Preserve the full release frame, memory, stability,
visual, platform and endurance gates; these checks do not certify release readiness.

## Accepted decisions and constraints

No additional production changes. Tests are muted, on the secondary display,
input-disabled and scratch-profile isolated. Reuse the physical release runtime;
only small overlays, reports and tiny synthetic images are added. Owner saves,
layouts, archives and selected art remain unchanged. Lossless renderer stays private.

## Current state

Installed inspector-preview body tested against the prior implementation with
the same installed grid renderer. Candidate main differs from installed source
only by two fixture-only notification-tween pauses; both lanes manually step the
same notification and survey clocks. No profiling injection in the real-map mains.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`inspector-preview-real-maps/`, `indexed-parent-material-validation/`,
`indexed-missing-both-validation/`. Runners/comparator in
`output/renderdoc-tools-2026-10-08/`; source/upload summary also retained in the
previous `inspector-preview-retention-trial/` directory.

## Verification

Twelve native debug=false Windows RTX 4070 Ti 1080p runs / three alternating pairs
each reported 12-room and frozen owner-current 10-room save / 12,960 measured frames.
Idle, pan, ordinary selection and zoom-selection at 1x/2x/4x. All **324 selection UI
snapshots**, **72 full paired phase states and cameras** match; 648 handler selection
applications verified. Only save timestamp omitted from gameplay capture comparison.

| Map | Mean ms before → after | p95 ms before → after | p99 ms before → after | >50 ms before → after |
|---|---|---|---|---|
| Reported 12 | 12.025 → 12.027 (+0.023%) | 19.427 → 17.492 | 34.341 → 34.635 | 0 → 0 |
| Current 10 | 11.741 → 11.540 (-1.712%) | 20.185 → 19.245 | 30.146 → 30.795 | 0 → 1 |

No >100 ms frames; textures unchanged at 1559.51 / 1945.26 MiB. Reported pair
means improve in two of three; current improves in one of three, dominated by the
first pair. Overall FPS gains are small/mixed, not a universal speedup. Ordinary
selection handler means fall 5.786→4.281 / 5.903→5.006 ms; zoom-selection handler
5.565→3.356 / 5.391→4.110 ms. Frame means by action retained separately.

One >50 ms frame inspected: current candidate 4x selection, frame 27, 50.536 ms;
no sampled upload, action 0.003 ms, simulation step 25.611 ms, grid draw 17.254 ms.
Durations overlap; this does not prove preview retention caused the isolated tail.
It reinforces that uploads are not the only remaining stall source.

Private indexed provider: **31 native checks pass**, ten rendered R8/RG8 material
cases exact. Inherited flood uses indexed storage; direct custom shader, inherited
custom shader, two-level parent inheritance and CanvasItemMaterial preserve ordinary
fallback pixels. Reuses the existing 21-asset candidate PCK with hardened loaders.
Tiny missing-original display test retains expected placeholder warning/accounting.

Additional **14 native checks pass** when both original and indexed artwork are
missing: synchronous and actual worker paths return no texture safely, do not count
nonexistent GPU storage/uploads, consume worker jobs, record fallback reasons and
close the session. Exactly two expected missing-art errors are required and verified;
no other error is allowed. These intentional missing-art fixtures do not relax the
release gate against missing packaged art or unexplained engine errors.

Previously measured large-station upload source summary confirms mining body/effect
and cargo atlases dominate; those sources are already in the 21-asset lossless map.
This is prioritization evidence, not a new lossless-renderer FPS result.

All three owner guards: 2938 files unchanged. Jobs terminal; runner finally blocks
restore runtime override. Evidence ~52.85 MiB; C 123.02 / D 70.03 GiB free.
No copied runtime/assets or screenshot batches. All performance release gates remain
open, including p95/p99 and target-hardware/Mac acceptance.

## Next action

Advance private lossless-provider moving-station/animation-join verification and
remaining PNG payload-corruption coverage, then measure the latest loader/provider
with installed UI/grid changes. Keep redraw and 4x simulation spikes in scope.
Do not repeat the unchanged rejected forecast or cache-budget trials. Broad
gameplay/visual/endurance, same-input packaged candidates and PC/Mac certification
remain required before a release readiness claim.
