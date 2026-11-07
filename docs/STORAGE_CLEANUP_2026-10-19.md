# Workspace storage cleanup — October 19, 2026

## Approved template and LFS cleanup

Owner approved the recommended duplicate-template and remote-verified LFS cleanup. Third pass recovered **3.05 GiB of physical free space on C:**; current capacity **C:40.40 GiB /D:26.00 GiB**. Logical file sizes and drive-space gains differ; D: was unchanged.

Removed three SHA256-identical Godot4.7.2 export-template TPZ copies from old frozen snapshots, keeping the canonical archive in `output/export-tools/4.7.2-stable`. All four copies were rehashed before deletion, with absolute output boundaries/reparse points checked and copy-back markers recorded. `pass3_restore_templates.ps1` is read-only by default; `-Restore` copies missing template duplicates back from the verified canonical.

Ran `git lfs prune --verify-remote --verify-unreachable --when-unverified=continue --verbose`, with no force/recent flags, retention overrides or Git configuration changes. Installed CLI documentation confirms this mode deletes only verified objects and retains those that cannot be verified. **1,747 objects verified on origin were deleted;147 not found on the remote were retained.** Unreachable objects were explicitly included in verification. No shared `lfs.storage` configuration was present. Full operation/exit code and counts:pass3-lfs-prune.log, pass3-lfs-exit.txt, pass3-lfs-summary.json. No Git garbage collection or recovery-folder cleanup.

Seven third-pass verification checks pass. Canonical template rehashed unchanged; all three duplicates removed with restoration markers. `.git/lost-found` count/bytes match the original inventory; historical builds and animation audit captures count/bytes match the fresh pre-pass inventory. Live editor cache retained. All2,958 owner files, current trailer, Git index and existing tracked working state unchanged across deletion, before documentation. No game/source/art/footage changes, tests, builds, commits or publication. Evidence:pass3-template-plan.json, pass3-template-removals.jsonl, pass3-verification.json and pass3-protected-before/after.json.

## Additional cleanup requested by owner

Second pass recovered another **20.20 GiB on C:**. Verified free space is now **C:37.36 GiB /D:26.00 GiB**. D: was unchanged in this pass.

Removed four older extracted PCKs only after streaming their complete corresponding ZIP members, validating CRC and matching SHA256 to the loose files. The four retained release archives preserve the exact package bytes. Removed three byte-identical macOS export-template ZIP copies from old frozen snapshots, keeping the canonical template archive. Removed one rejected October7 export with recorded main.gd parse failures; failure logs and the successful later release remain. Removed2,433 regenerable compiler intermediates from the specifically validated local engine `bin/obj` directory; engine source, built EXEs and debug PDBs outside that directory remain.

Evidence is `pass2-plan.json`, `pass2-removals.jsonl`, `pass2-retained-guards.json`, `pass2-verification.json` and `pass2-protected-before/after.json` in the same cleanup folder. Affected directories contain `STORAGE_CLEANUP_2026-10-19-PASS2.json`. **pass2_restore.py** is read-only by default; `--restore` recovers missing archived PCK/template copies without overwriting existing files. The intentionally rejected export and compiler intermediates are not restored. Rebuild intermediates with the preserved source/configuration if that old engine build is needed again.

All six second-pass checks pass. Four retained release ZIPs, four engine EXE/PDB files and canonical SDK archives rehashed unchanged. All2,958 owner-profile files, current trailer, Git index and existing tracked working state remained unchanged across deletion, before this documentation update. Live editor cache retained. Restore script's no-change mode checked; full rehydration not performed. No source/art/save/footage changes, game runs, tests, builds, commits or publication.

## First cleanup pass

Owner requested workspace cleanup and more free disk space. Removed **143 exact duplicate obsolete QA runtime binaries** and **10 regenerable import caches in old output snapshots** (90,578 cache files). Kept canonical binaries, platform/delivery packages, source snapshots, reports, archives, artwork, source footage, current trailer/Resolve preparation and the live editor import cache.

Measured free space immediately before/after the removal window:

| Drive | Before | After | Net increase |
|---|---:|---:|---:|
| C: |3.930 GiB|17.157 GiB|13.227 GiB|
| D: |1.492 GiB|26.001 GiB|24.509 GiB|

About **37.74 GiB** recovered during that window. At the earlier inventory start C: had6.18 GiB free; capacity dropped before deletion began, so whole-task net growth is approximately35.49 GiB. Other disk activity/allocation can affect drive readings. Removed logical file sizes total37.60 GiB; those are distinct from physical free-space measurements.

## What changed

Duplicate deletion was limited to specifically inventoried `BrineSpace.exe`/`BrineSpace.pck` copies under the workspace's ignored output directory and named D: BrineSpace QA task directories. Each selected file matched a retained canonical by size and SHA256; canonical hashes and selected file hashes were checked again before removal. Unique binaries, Windows/Mac/deliverable folders and canonical copies were preserved. Each affected parent contains `STORAGE_CLEANUP_2026-10-19.json` with its copy-back source/hash.

Cache deletion was limited to old C: output snapshots' `.godot/imported` directories, including the separate9.284 GiB cache in `output/combined-release-v367/frozen-project`. The live workspace's `.godot/imported`, other `.godot` metadata, all D: candidate source caches, original artwork and source snapshots remain. Old snapshots need an import pass before editor/test reuse; continue using scratch APPDATA for Godot probes.

The complete deletion plan, per-file journal, hashes, guards, verification, cleanup script and restoration script are retained in [output/workspace-cleanup-20261019](</C:/Users/Alex/Documents/Brine Space/output/workspace-cleanup-20261019/HANDOFF.md>). **Restore-Duplicates.ps1** is read-only by default; pass `-Restore` to copy missing historical runtime files from the retained matching canonical. It never overwrites existing files. Source caches regenerate from the preserved snapshot sources rather than being restored from another cache.

## Verification and boundaries

- All planned removals confirmed; all28 retained binaries from the compared groups rehashed unchanged.
- All2,958 owner-profile files hashed unchanged; current trailer hash unchanged.
- Git index and existing tracked working state unchanged across the cleanup, before adding this documentation.
- Live editor cache retained. Restoration markers present and restoration script's read-only mode checked; full rehydration was not performed.
- Every final absolute target validated inside exact allowed roots before deletion; recursive deletion used native PowerShell `Remove-Item -LiteralPath`, with reparse points rejected.
- The broad metadata inventory encountered273 inaccessible long shader-cache paths in unrelated scratch profiles. Cleanup selection and validation had no access errors; those inaccessible paths were not touched.

No game/source/art changes, Git/LFS/recovery pruning, archive removal, save access by Godot, tests, builds, exports, commits or publication. No further removal of unique historical evidence was attempted. The pending Resolve connection and continuous audiovisual trailer review remain separate unfinished work.
