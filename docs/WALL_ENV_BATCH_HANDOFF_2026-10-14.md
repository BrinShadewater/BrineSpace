# Project handoff

Updated: October 14, 2026 · Project: BrineSpace · Task: wall/environment ordered batching

## Objective and acceptance

Owner requested wall/environment batching toward 60 FPS with unchanged appearance.
Require exact native pixels and matched actual-release workload measurements; retain
original textures, region rectangle sampling, ordering, shaders and transforms.

## Accepted decisions and constraints

Final V2 source admitted; previous Windows delivery unchanged by this task. Muted,
input-isolated, always-on-top secondary-display QA; native/GPU jobs
serial. Scratch APPDATA with resolved-profile guards, owner fingerprints checked.
Existing accepted actor-cell optimization is common to both release lanes.

## Current state

Evidence: `C:/bs-wall-env-20261014/`; drivers: `output/wall-env-batch-20261014/`.
Final V2 batches polygon strips/corners inside each `tops()` call, flushing before
native rectangle branches, every closed-door draw and function end. Crown corners
combine their two triangles. Original triangulation, UV seams, textures, shaders,
transforms and order remain; no persistent cache or art changes.

V2 census: roughly 3,212 -> 2,877 calls (~10.4% fewer); wall contribution ~504 -> 198,
derelicts save roughly 30. Conditional hidden-layer counts are not additive.
Earlier corner-only V1 evidence is retained but superseded by V2 for admission.
Final V2 timing control uses the untouched original drawing implementation.

Native matrix: 768/768 visible exact pairs with fewer calls in each, covering three
materials, four rotations/scales, nearest/linear, tint, flood shader, raised/low walls
and closed-door boundaries. Whole-station parity: 12 exact adjacent comparisons at
three zooms, both directions, equal frozen states after settling drone textures.
Rocks/waves are unchanged: existing waves already instance rectangles, and earlier
wave/rock trials failed visual or pacing checks. Textured cliff/ridge alternation
prevents treating all rock sides as untextured geometry.

## Admission and final verification

V2 full clean-original comparison completes in both orders: 27.264 -> 26.595 and
27.422 -> 26.640 ms, saving 0.669/0.782 ms (2.45/2.85%). Delayed render CPU
7.226 -> 6.540 and 7.232 -> 6.531 ms. 15,120 measured frames; all 42 state pairs
exact. P95 improves 16/21 and 18/21, with no phase worse in both orders. Worst frames
93.414 -> 98.299 and 100.479 -> 92.237 ms; this is not a claim that stalls are fixed.
Settled textures exactly 1,946.07669 MiB in every lane. All 42 candidate gates fail.
Idle 1x means 24.666 -> 24.132 and 24.763 -> 24.273 ms (~40.4-40.5 -> 41.2-41.4 FPS).
`v2-full-analysis.json` preserves phase details.

Installed `rooms/whole-room/painted_shell.gd` is the measured V2 program after removing
trial identity/counters, renaming the diagnostic flag `batch_cap_polygons` /
`--reference-painted-caps`, comments/helper placement. Per-function source equivalence
verified in `production-source.json`. No cache, geometry, texture or rectangle change.
The existing script UID is retained.

New `tests/test_painted_cap_batch.gd` plus UID and `tests/index.json`: permanent native
matrix, explicit native lane because auto-classification mistakes its capture guard.
Red before admission exits 1 for missing packet API; green installed source passes
768 exact, visible pairs with fewer draw calls in every pair. Independent final review
finds no actionable issues; diff whitespace check passes. Owner guards remain unchanged.

## Windows candidate and packaging verification

Candidate **brinespace-2fb8e8659a3be093**: `C:/bs-release-wall-env-20261014/windows/BrineSpace.exe`.
Frozen snapshot derives from the previous physical candidate, with the current Grid
and wall runtime source plus regression support; previous delivery remains intact.
`windows/identity.json`, `build_info.json`, `SHA256SUMS.txt` record full provenance.
Source fingerprint: `2fb8e8659a3be093ac7a3a627baff6da22f509190697d06f547471ba742577b9`.

Clean full import and maintained export, 12 release manifest/assert-safety tests,
exact pack audit (35,790 checked; zero missing/changed/unexpected), actual debug=false
normal New Game/dialogue/simulation/F8 smoke all pass. Native screenshot reviewed.
Import wrapper initially rejected an empty error list because the old baseline had
known review-image errors; corrected subset comparison validates the existing clean
result without repeating import. All owner guards preserve 2,948 files.

Benchmark measurements use the equivalent frozen release-overlay renderer;
pack audit and smoke verify integration into this export, not a repeated full timing run.
`large-station-results.json` is copied alongside the new candidate directory.

## Next action

Requested batching and Windows candidate checks are complete. Full 60 FPS,
endurance/object growth, save/relaunch, target-PC and native-Mac release acceptance
remain open. Next gains need measured CPU/live-room work; rejected wave/rock
reorderings remain rejected. No commit, publication or Mac acceptance implied.
