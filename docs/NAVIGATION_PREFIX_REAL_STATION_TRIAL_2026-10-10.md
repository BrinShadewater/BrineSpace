# Project handoff

Updated: October 10, 2026 · Project: BrineSpace · Task: Real-station navigation reuse trial

## Objective and acceptance

Verify private graph-prefix retention against real station maps and measure its
placement/demolition benefit. Full PC/Mac release gates remain open.

## Accepted decisions and constraints

Independent crew graphs, unchanged point identities/weights/ordered connections,
paths, gameplay timing and selected art. Preserve owner saves/layouts. All native
tests muted on secondary display with isolated profiles. Reuse one physical QA
runtime; reserve disk space; no full source/game-package copies or screenshots.

## Current state

Private overlay retains the leading rooms whose ordered cells, geometry keys,
cache revision and template sizes agree. It removes old boundary edges and the
changed suffix, resets retained disabled flags, rebuilds suffix points/internal
links, and reconnects every boundary in original order. Layout invalidation and
staged work use full rebuilds. No mutable graph sharing or production script edit.

Entry drivers in `output/renderdoc-tools-2026-10-08/`:
`prepare-prefix-retention-trial.py`, `prepare-prefix-retention-performance.py`,
`prepare-prefix-retention-edge-verification.py`,
`prepare-prefix-stage-cancellation.py`, `analyze-prefix-retention-performance.py`,
`summarize-prefix-retention-trial.py`; generated run drivers retain exact inputs.

Evidence summary:
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/prefix-retention-summary.json`.
Per-run graphs, logs, phase states and CPU traces remain in the named sibling
folders. Original physical QA PCK hash e9d3f8460270b78b8eba5d29300349f1639ebd405965223e2b88f1be1ba6d297 unchanged.

## Verification

Reported 12-room save and deterministic 40-room expansion use copied owner Studio
layouts. Three successful verification runs compare 97 graphs, 787,712 point
records (positions, weights, disabled flags and ordered adjacency), room/point
maps and 8,361 selected cross-station routes against fresh reference rebuilds.
Connected galley placement and demolition retain 7,376/11,454 preceding nodes
in the large station. Hardware/room door locks and layout-revision invalidation
match; a yielded 40-room rebuild is safely superseded synchronously.

Review found the first prototype delayed clearing the old graph during staged
loading. V2 restores immediate clearing/full staged behavior. The cancellation
fixture on 12 rooms failed its yield precondition because that map rebuilt too
quickly; retained failure `prefix-retention-edge-v2-verification`. Corrected large
fixture `prefix-retention-edge-v3-verification` completes with the cancellation
marker and no engine/art errors. Do not classify the failed fixture as accepted.

Private V1 flag-off/on timing: four actual debug=false native runs, both orders,
4,320 measured frames, six placement/demolition phases per run at 1x/2x/4x.
All 12 paired phase-end gameplay states equal. RTX 4070 Ti, 1080p; this is not
GTX 1650/M1 target certification. Verification overhead is excluded from timing.
Both lanes carry the same prototype/profiling scaffolding; reference flag executes
full graph assembly. V2 staged correction is verified separately, not certified
by V1 performance results.

| Metric | Forward full / retained | Reverse full / retained |
| --- | --- | --- |
| Combined three-actor rebuild mean | 38.45 / 25.82 ms | 37.93 / 25.87 ms |
| CPU reduction | 32.84% | 31.79% |
| Affected action-frame mean | 129.70 / 120.48 ms | 129.39 / 117.46 ms |
| All measured frame mean | 28.668 / 28.743 ms | 28.567 / 28.732 ms |

Candidate >100 ms frames: 7 forward/6 reverse versus reference 6/6.
Candidate >50 ms frames: 21/21 versus reference 15/16. Average frame time has
not improved, and release frame/stall gates still fail. Targeted CPU savings are
useful evidence, not a global smoothness claim or production acceptance.

Candidate 1x placement/demolition trace still records 53.67/51.49 ms of grid
draw work with 15 redraws. These script draw times identify a remaining hotspot;
delayed renderer CPU/GPU query values must not be added as aligned frame costs.

All owner guards: 2,938 unchanged. Jobs 79472/17356/1598/85037 terminal0;
83912 is the failed cancellation fixture. Configs restored, no native jobs active.
Generated evidence ~41.1 MiB, zero new large package copies/captures.
Latest free space C124.03GiB, D82.03GiB.

## Next action

Keep prefix retention private until Moonbay/large-room phase changes, detached
placement, actual layout edits and final V2 matched timing are covered. Do not
ship it based solely on the scoped CPU gain. Profile the measured grid redraw
burst and coalesce only proven redundant room/layer invalidations, preserving
complete visible output. Full original bug closure, endurance and PC/Mac native
release certification remain open.
