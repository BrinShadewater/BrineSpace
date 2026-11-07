# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: duplicate PNG loading cost

## Objective and constraints
Reduce startup decoding while preserving selected pixels, frame identity, metadata,
runtime PNG loading and independent generated images. Backend remains experimental;
no normal loader or artwork changed in this experiment.

## Current state and verification
Private control: `output/compressed-crew-2026-10-06/bounds-cache/encoded-sharing/`.
One matched native cold-process loader comparison loads all three current replacement
banks without image prefetch. Both use compressed sources and cached alpha bounds.
Candidate hashes files before decoding, reusing live immutable sources for identical
PNG bytes under another path.

3,267 alias decodes avoided (Veld 1,140, James 1,666, Marsh 461). Unique source counts
remain 1,800/3,477/557. PNG work 5,578.734→3,323.060 ms, but extra file hashing takes
2,687.614 ms. Three-bank preparation **8,086.422→8,512.594 ms** (+426.172 ms).
Clean exits, no engine errors, owner 2,936-file fingerprints unchanged. Loader-only
timing: not scene readiness, warm-prefetch or packaged acceptance.

## Decision and next action
Reject this implementation. Separate `FileAccess.get_sha256` passes add more work
than they remove; do not promote them into preferred or normal loading. No broad
fidelity batch is needed for an unaccepted, unshipped timing experiment.

Next evaluate one encoded-buffer read/hash/decode path with bounded prefetch and
ordinary error handling. Avoid repeated reads/hashes for unique PNGs. Require matched
stage timings and exact pixels/metadata before admission. Frame budget, full memory
gates, original bugs, endurance and Windows/Mac release remain unfinished.
