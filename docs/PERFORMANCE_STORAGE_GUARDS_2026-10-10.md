# Project handoff

Updated: October 10, 2026 · Project: BrineSpace · Task: Performance with bounded test storage

## Objective and acceptance

Continue the PC/Mac performance work without filling the owner's drives. Release
performance and platform certification gates remain open.

## Accepted decisions and constraints

Use the retained physical QA runtime serially for private diagnostics. Do not make
full per-trial source/PCK copies. Keep current and rollback deliverables, art,
owner saves/layouts, and recovery/history. Native windows stay muted on the left
secondary display. Isolate profiles and fingerprint the owner's profile.

## Current state

`tools/run_release_benchmark.py` now refuses writes unless 20 GiB remains free
after the planned EXE/PCK copy. It checks evidence/temp volumes before startup
and evidence/profile volumes before each run. Its one physical QA copy is removed
in `finally`, including process timeout/failure, while identity, fixture, logs and
results remain. Both binary hashes must still match before either is deleted;
changed files are retained for investigation. This protects this maintained
runner; ad hoc drivers must call the guard and reuse the existing runtime.
Forced process termination/power loss can still leave a copy, and these checks
are between runs, not a live disk quota. Do not treat them as global protection.

Changed tests: `tests/test_release_benchmark_runner.py`.
Private probe: `output/renderdoc-tools-2026-10-08/check-navigation-prefix-mechanics.py`.
Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/navigation-prefix-mechanics/`.

## Verification

Seven runner tests pass, including insufficient-space refusal before copy,
hash-guarded cleanup, preservation of delivery/identity/modified QA files, and
cleanup plus owner verification on an interrupted subprocess. No native gameplay
run was needed for this Python infrastructure change.

Small headless Godot AStar2D mechanics probe: seven retained-prefix sizes,
504 ordered adjacency checks and 2,520 selected routes match fresh graphs;
available IDs equal each retained prefix length. Owner profile 2,938 files
unchanged. This tests engine mechanics, not actual station equivalence or FPS.
No release copy or screenshot generated. Latest free space: C 124.02 GiB,
D 82.09 GiB.

## Next action

Prove complete real-station graph equivalence for private prefix retention,
including connected/detached placement, demolition, layout invalidation, locks,
Moonbay and staged cancellation. Only then measure a private candidate against
the original rebuild in both orders. No production navigation change admitted
by this probe; the earlier station-resolution optimization remains accepted.
