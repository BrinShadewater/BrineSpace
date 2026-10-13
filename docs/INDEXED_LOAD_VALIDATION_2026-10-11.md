# Indexed renderer load validation

Updated: October 11, 2026 · Project: BrineSpace · Task: performance readiness

## Objective and acceptance

Fix the demonstrated private-provider release-build validation gap. Reject malformed
encoded storage and preserve ordinary PNG pixels, sharing and memory accounting when
fallback succeeds. Keep the renderer private pending its remaining acceptance gates.

## Accepted decisions and constraints

Preserve selected art and effects. No engine upgrade or art reduction. Reuse existing
runtime and asset packs; muted secondary-display runs, isolated profiles and owner
fingerprints. This reversible candidate work remains authorized.

## Current state

Private candidate files in
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/indexed-load-validation/`:

- `bank.gd`: runtime index format/dimensions/mipmap checks; palette decode,
  RGBA8 format, dimensions/mipmaps and byte checks. Cache weak references only after
  successful creation. Invalid indexed data loads the original PNG and records the
  fallback reason and actual decoded bytes. Missing original returns null with an error.
- `motion.gd`: empty failed-worker results go through bank fallback. Null creation
  does not enter the cache. Synchronous loading no longer relies on debug assertions.
  Cache records and upload diagnostics use actual fallback bytes; additional stale
  eviction considers larger fallback storage while respecting existing recent pins.
  Upload backend reports original-fallback explicitly; failed finish returns false.
- `validated-resources.json`: future private integration map using these two files
  and the unmodified selected catalog. `source-identity.json` fingerprints both files.

No production source changed this pass. Test packs overlay only small scripts on the
existing candidate; selected PNGs remain untouched.

## Verification

Actual Windows Godot 4.7.2 release executable, debug=false, RTX 4070 Ti:

- 42 checks, zero failures: previous 12 lifecycle checks; invalid index format,
  dimensions and mipmaps; invalid palette; exact fallback pixel SHA256 and byte count;
  shared live fallback identity; absent background result; malformed index through
  actual synchronous and worker loading; cache teardown; upload bytes/backend.
- 64 checks, zero failures: all 21 real selected catalog entries accepted as indexed,
  original dimensions and exact storage bytes retained, no fallback reasons.

Fixtures first exposed dynamic-script type syntax, read-only catalog mutation,
consumed worker-task IDs and mixed indentation mistakes. Fixed the fixtures using
script identity, a separate test-only catalog overlay, observable task completion and
consistent indentation. No production workaround for these fixture failures.

Two new upload assertions failed against the intermediate candidate, then passed
after byte/backend accounting was corrected. Final logs contain no engine errors.
Expected invalid input uses a separate catalog overlay; it is not the integration map.

Owner 2938 files before/after, zero changes for both final suites. Jobs terminal;
runtime override restored. New directories total approximately 0.124 MiB, without asset
copies or screenshots. C: 124.21 / D: 70.69 GiB free at completion.

Evidence: `indexed-load-validation/{native.log,result.json,owner.json}` and
`indexed-valid-catalog/{native.log,result.json,owner.json}` under the isolation root.
Runners: `output/renderdoc-tools-2026-10-08/check-indexed-load-validation.py` and
`check-indexed-valid-catalog.py`.

## Next action

Keep provider private. Verify failed PNG decode and missing-original behavior,
including ordinary-filter fallback in Display.original_texture; that path still lacks
a missing-image guard. Check filter inheritance, flood materials and representative
rendered pixels with the validated candidate. These tests did not certify arbitrary
palette content, all filtering, gameplay endurance or Mac behavior.

Then return to measured floor/lighting rebuild and upload hotspots for frame pacing.
Previous real-map performance results apply to the earlier provider, not this changed
loader. No FPS gain or new memory-performance acceptance is claimed here. All broader
release gates remain open.
