# Companion rebuild spike attribution

Updated: October 11, 2026 · Project: BrineSpace · Task: performance release readiness

## Objective and acceptance

Identify the reproduced current-map 4x crew update spike before changing routing.
Preserve exact gameplay/camera state, route ordering, movement timing and graph
correctness. This is attribution; full release performance acceptance remains open.

## Accepted decisions and constraints

No production edits, navigation deferral, gameplay changes or broad refactor.
Private synchronous function wrappers and adjacent timing only. Staged rebuild
coroutine behavior stays unchanged; substage metrics apply only to synchronous work.
Muted secondary display, scratch profiles, input disabled and owner fingerprints.
Small script overlays/existing runtime; no art copies or screenshot output.

## Current state

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`crew-navigation-component-trace/`, `crew-update-stage-trace/`,
`companion-update-attribution/`, `crew-navigation-control/`,
`companion-rebuild-stage-trace/`. Corresponding runners in
`output/renderdoc-tools-2026-10-08/`.

Initial private diagnostic setup had incorrect step-label scope and mixed wrapper
indentation. Corrected before accepted measurements; parser evidence retained where
available. Failed launches provide no performance/gameplay acceptance. Production
source and owner data unchanged throughout.

## Verification

Six completed native debug=false runs: current/large navigation diagnostics, current
adjacent update stages, current companion attribution, large uninstrumented control,
and current rebuild substages. Idle/pan/selection/zoom-selection at 1x/2x/4x,
90 frames per phase, 6480 measured frames in total. Four current diagnostics match
the existing current control's twelve complete phase states/cameras each; the large
navigation diagnostic matches a new identical-workload control. **60 diagnostic
phase state/camera comparisons exact.** Instrumented timing is not FPS certification.

Navigation function trace reproduces current 4x selection logical frame 27:
crew 26.353 ms, Branforth update 6.563 ms. Measured route searches/clearance calls
do not account for the remaining time. Adjacent stage run locates 17.582 of
23.483 ms in `Companions.advance`, with 5.765 ms in crew/social work; hazards and
passage are small. Do not optimize AStar goal searches on that evidence alone.

Detailed companion run: same construction-completion frame, crew 25.208 ms,
companions 19.161 ms. Margot update 3.640 ms and River 15.420 ms; both navigation
build revisions change 1→2 in that update. Current roster is Margot/River. Source
shows active companions update directly after architectural crew, while architectural
crew already have a one-rebuild-per-frame guard. This identifies simultaneous
companion rebuilds as a trigger; no new deferral is introduced.

Rebuild-substage run: crew 25.190 ms, companions 18.918 ms. Synchronous timings:

| Stage | River ms | Margot ms |
|---|---:|---:|
| Geometry preparation | 0.791 | 0.394 |
| Point and local-link work | 12.137 | 2.619 |
| Boundary connections | 0.362 | 0.357 |
| Finalize | 0.082 | 0.073 |
| Complete rebuild | 13.379 | 3.449 |
| Complete actor update | 15.222 | 3.591 |

Rebuild total and actor update contain the substage times; route/clearance wrapper
metrics also overlap. No additive CPU claim across nested timings. The main target
is point/link work, not geometry preparation or boundary connections alone.

Another reproduced 1x frame has a ~9 ms Margot update without a build revision
change, including 2020 `can_stand` calls (~2.17 ms instrumented). Keep this separate
from the construction rebuild issue; it may involve passage/route-clearance work.

All five output-directory owner guards: 2938 files unchanged. Native/parse jobs
terminal; maintained runners restore the runtime override. Evidence ~21.33 MiB;
C 122.98 / D 69.78 GiB free. No production fix or release gate claimed.

## Next action

Split River's point/link stage into prefix retention, cache-miss template generation,
point insertion and cached-link assembly, including counts and cache-key reasons.
Use that evidence for a narrow remedy that preserves graph/route ordering and
exact movement timing. Do not add delayed movement or repeat old rejected cache
trials. Continue floor/lighting no-upload redraw work alongside this measured spike.
Full release workload, visual, memory/endurance and actual PC/Mac gates remain open.
