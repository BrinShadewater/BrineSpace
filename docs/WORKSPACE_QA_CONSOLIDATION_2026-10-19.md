# QA workspace consolidation — October 19, 2026

Owner authorized archiving the older QA build and consolidating duplicate captures
and caches while preserving source, saves, unique evidence, frozen releases,
current products and a complete rollback. No game code, device files or installed
apps were changed. The existing helper was left running.

## Retained and archived

Current complete candidate: `title-load-pass`, brinespace-efdb7ff32be59034.
Complete rollback: `card-png-staging`, brinespace-f9155b4334164440.
Both remain under `/Users/Shared/BrineSpace-ipad-optimization-20261019`.
Frozen notarized Mac alpha and Windows deliveries were not cleanup targets.

Older `card-region-demand`, brinespace-58324c425a8fc834: two4,077,450,095-byte
PCK copies were replaced by a7,143,681-byte recovery archive. The persisted archive
was reloaded and its complete reconstructed byte stream matched original SHA-256
`a0d82be8e0024aec1da96d7b8b4efb9dfa772f9ffe8f5263b9142f691e46b5c9`
before removing either pack. The historical app requires restoration before use.
Its binaries, signing data, source snapshots, logs, manifests and evidence remain.

Recovery archive and instructions:
`/Users/Shared/BrineSpace-workspace-cleanup-20261019-consolidation/README.md`.
Keep its scripts/archive and the immutable donor:
`/Users/Shared/BrineSpace-ipad-optimization-20261017/crew-loading-pass/export-final/BrineSpaceiPad.pck`.
Do not delete that donor; earlier recovery archives also depend on it.

## Consolidation and verification

Consolidated1,426 byte-identical files:1,399 bug-report ZIP copies,20screenshots,
and7large crew-cache files, representing2,992,255,631logical duplicate bytes.
Only selected captured files/inactive scratch caches of at least64KiB were
considered. Unique files and smaller caches were retained. SHA-256 and byte sizes
matched before and after each operation. APFS copy-on-write clones keep all
original paths and independent inodes; future writes do not change another copy.
No hard links or symlinks were introduced. Original modes, ownership, ACLs,
modification times and extended attributes were preserved. macOS can add its
provenance tag to new clones; additions were logged, original quarantine retained.

Final checks verified169save/checkpoint files,13,340other historical files,
39protected product/donor files and strict signatures of current iPad, rollback
and frozen Mac apps. Source/product/helper roots were excluded from mutation.
Open-file checks preceded operations. Clone failures0; unique evidence retained.
Raw file manifests, hashes, recovery plan and per-file journal remain in the
cleanup directory outside the repository. Initial read-only runtime/metadata
checks are retained; no original capture was replaced until validation passed.

Available space increased from15,530,344,448 to18,225,594,368bytes: about2.70GB
observed, with18.23GBfree at completion. Logical8.15GBpack removal plus2.99GBshared
duplicates does not mean11.14GBphysically reclaimed. APFS sharing/snapshots and
concurrent system activity affect this number.

[Portable summary](ipad-memory-placement-evidence-2026-10-19/workspace-consolidation/summary.json).
