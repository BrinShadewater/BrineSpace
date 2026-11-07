# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: lossless drone dock admission gaps

## Objective and acceptance

Continue full PC/Mac performance readiness. Close actual dock integration, flip/type/reuse/fallback and lifecycle gaps before admitting the lossless drone provider. Preserve original pixels, clocks, source art and default quality; no performance gate closure from visual tests alone.

## Accepted decisions and constraints

Sixteen-source provider remains private. No normal runtime/art/export/owner-data change. North start and wheel sheets are already encoded; no duplicate encoding needed. The previous goal turn made concrete progress through the frozen/audited actual Windows release baseline.

## Current state

Evidence `output/drone-dock-admission-2026-10-07/`: generated retained dock probe, actual room-content probe, explicit no-session probe, original/fixed logs, private before-source copies, input/encoding/patch hashes and current two-cycle lifecycle results.

Private fixes in `output/drone-normal-cache-2026-10-06/provider/`:

- `motion.gd`: `uses_indexed_storage` requires an active palette factory. No-session requests/finishes/texture reads delegate to ordinary storage; a selected encoded image cannot be cached as ordinary pixels without the resolving session.
- `dock.gd`: preparation readiness uses the same backend selection; pending-job cleanup drains ordinary and indexed jobs.

Original provenance retained; current before/after hashes recorded separately in coverage.json. These are prototype fixes, not defects asserted against the shipped normal game.

## Verification

Retained registered docks:2,625 checks/1,300 exact native nonblank pairs, zero failures/errors/leaks/warnings. All mining/construction/salvage types, dock/launch/return poses, three elapsed values, four flip axes, nearest/linear inheritance, normal/flood/unknown materials, provider-present versus missing-session fallback, repeated use of one slot across types and hide/restore. Corrected renderer context enables actual flip bounds. Parent transforms/modulation and complete dock layers retained.

Actual full-wall bay views:446 checks/216 exact native full-room pairs, clean exit. Native mining/construction/salvage view configuration and sorted retained-content submission, all four rotations, actual legacy dock IDs, surrounding floor/wall/furnishing layers, flips, dock/launch/return, nearest/linear and normal/flood/unknown materials. Shared candidate canvas reused across actual room types; dock execution and final provider release asserted. Candidate room capture inspected.

No-session regression first reproduces6failures/11checks: index-format textures returned without palette resolution, ordinary identity lost and indexed caches/jobs created. After private fix11checks clean. Added shutdown case reproduces1failure/13checks: delegated ordinary job left pending. Cleanup fix13checks clean, no indexed jobs/caches, original RGBA and immutable texture identity, serial/parallel readiness, both backend queues drained. Failed logs retained; successful results supersede them. Repeated1,516 visual pairs after the loader/readiness fix remain exact; final cleanup-only change tested through its targeted probe and lifecycle.

Actual private two-cycle save/title/Continue+Studio fixture rerun after fixes:244checks,0failures/errors/leaks/warnings. This still uses existing private crew support and does not certify drone-only normal admission, long endurance or packaged gameplay.

Catalog coverage versus actual Windows stalled-frame uploads:7of8substantial paths already encoded, including North start/wheels. Missing substantial path is West right-steering48,168,960bytes; two other unmatched paths are already four-byte transparent placeholders. All16selected original PNG hashes match the frozen Windows build inputs;32encoded file hashes preserved. No art regeneration. All owner checks2,936files before/after, zero changes. All handles terminal.

## Next action

Stage a drone-only current-source integration (preserve current crew backend) and compare against the accepted normal Windows baseline with normal flood code. Resolve combined residency tradeoffs and source-to-encoding build validation before normal admission; include West steering only if census/native evidence warrants it. Refresh actual release candidate after an accepted integration, measuring upload stalls, steady frames and memory separately. Full benchmark matrix/three runs, original nine packaged reports, endurance/target hardware and Mac certification remain open. No public upload.
