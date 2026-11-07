# Reproduction and performance evidence

Use this reference for a reported runtime defect or measured slowdown, not for an unrelated art edit.
Start from current project guidance and the actual symptom: input, save/revision, runtime mode,
active phase, viewport/zoom, expected behavior and observed behavior. Dated notes are not a fresh run.

Choose the smallest reproduction that still catches the symptom. Predict an observable difference
between plausible causes before adding a probe. Use the project's existing diagnostics and verify
that a signal changes on the relevant success/failure path; a counter with no workload change proves
little. Do not require a fixed hypothesis count or block useful static investigation when runtime
access is absent. State what remains unverified.

For a fix, preserve the observed failing case, make the bounded change, rerun that case and return
to the original scenario. Add a regression check when it meaningfully protects the behavior.
Keep test fixtures isolated from real saves and external queues. Remove temporary instrumentation
or make intentional diagnostics explicit; do not enable free building or disable failures just to pass.

For performance work, record a baseline on the actual delivered runtime mode and compare the same
input, phase, viewport, workload and profile settings. Separate import/startup time from steady-state
frame time; inspect slow frames and relevant subsystem costs, not only an average FPS. Use repeated
samples only to resolve noise or a consequential uncertainty, not to fill a reporting quota.

Pair timing changes with behavioral and visual parity: active/pause/resume transitions, correct
invalidation after world/scene changes, visible actors/effects and pending work. Headless tests cannot
establish native rendering quality. Report regressions, measurement noise and whether the target was
actually reached; a smaller duration alone is not complete acceptance.

## BrineSpace application

Read current AGENTS.md and docs/CURRENT_STATUS.md. F7 exposes per-system times, path counts and
errors; F8 saves reports, and error_watch/stuck_watch/last_session breadcrumbs can answer specific
questions. Use an existing report when it contains the needed scope rather than scanning historical
logs. Tests/tools started with -s deliberately suppress automatic player-folder capture; no report
there does not prove the live automatic capture is broken.

Choose subsystem tests through tools/run_tests.py and tests/index.json. Native-only checks need a
real display; parse/headless success does not establish room/actor visibility. Use disposable saves
and explicit fixture flags, keeping normal costs/failure and owner Studio marks intact. For a
rendering optimization, preserve visible effective props, shader/material intent, pause/production
clock behavior, all affected rotations and real station integration. Never treat a missing resource
warning, placeholder or a filtered-out actor as a successful speedup.

Legacy and retired asset paths may be live dynamic dependencies. Preserve .gd/.uid pairs and the
owner's no-incidental-monolith-refactor decision. Scope searches to actual source/tests/docs and prune
output/ before walking it. Profile the actual requested change, not a broad art or test rollout.

Adaptation: Matt Pocock diagnosing-bugs and Addy Osmani performance/observability concepts, reviewed
2026-11-01. Reuse project diagnostics; no new monitoring service or universal benchmark threshold.
