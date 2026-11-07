# Storage cleanup — October 16, 2026

Completed without a game run or production code/art change. Figures below use
GiB, matching Windows drive-capacity measurements. Full evidence is in
`D:/bs-storage-cleanup-20261016/`.

| Drive | Free before | Free after | Net change |
|---|---:|---:|---:|
| C: | 26.835 GiB | 104.636 GiB | +77.802 GiB |
| D: | 142.743 GiB | 110.252 GiB | −32.491 GiB |

## Removed verified duplicates

Removed **27 obsolete physical runtime copies: 13 PCKs and 14 EXEs**, totaling
**48,659,839,018 bytes / 45.318 GiB**. Each file was fully SHA256-matched to its
retained canonical binary, then checked again immediately before removal.
Selection was limited to `C:/bs-*/runtime/BrineSpace.exe` and `.pck`.

The complete `C:/bs-crew-stall-20261016/runtime` reference remains. Its PCK is
the retained canonical for removed old PCK copies; the current Windows delivery
is the canonical for matching EXEs. Unique hashes/versions and already-hardlinked
copies were retained. Removing a hardlink name that still had a retained alias
would release no data, so those names were left alone.

All loose scripts, overrides, profiles, logs and result data remain. Fourteen
affected runtime folders contain `STORAGE_CLEANUP_2026-10-16.json` explaining how
to recreate missing physical binaries. Historical commands using those folders
need the copies restored before running; this is deliberate cleanup, not missing
source or a broken export.

The exact map and original file metadata are in `removed-duplicates.json`.
`Restore-Duplicates.ps1` defaults to a no-change summary. To recreate the recorded
physical copies, with canonical SHA checks and a 20 GiB free-space reserve:

```powershell
& 'D:/bs-storage-cleanup-20261016/Restore-Duplicates.ps1' -Restore
```

The restoration script's parser and no-change mode pass; a full restoration was
not run because it would recreate the duplicates just removed.

## Relocated complete historical benchmark archive

Moved **955 files / 34,884,200,385 bytes / 32.488 GiB** from:

`C:/Users/Alex/Documents/Brine Space/output/drone-compiled-2026-10-07`

to:

`D:/BrineSpace-archive/2026-10-16/drone-compiled-2026-10-07`

Every file's SHA256, file membership, empty-directory membership and stable source
metadata were checked before removing the C: tree. No unique content was discarded.
The original C: path is now a junction to the D: archive and remains usable. Before
recursive removal, absolute source/stage/destination boundaries and plain ancestor
trees were verified; reparse entries were rejected. The temporary C: stage was
removed successfully. Catalog and mutation records are preserved in the evidence
folder. The archive now physically resides on D: for future storage/timing scope.

## Preservation and verification

- **All 2,948 protected player files unchanged**, exact before/after fingerprint.
- Current Windows/Mac candidate **brinespace-b0b5d1b031c6ec29** preserved: both
  **11-file checksum manifests** pass, including EXE/PCK and the Mac ZIP.
- Main source, UIDs, room layouts/Studio marks, raw art, purchased packs, authoring
  generations, Git/LFS/recovery data and the open editor's import cache were not
  cleanup targets. The unique historical archive above was fully preserved.
- Final archive membership and junction resolution pass; retained canonical
  binaries match; all 27 removed paths are absent and restoration markers exist.
- Both drives remain above the 20 GiB reserve. Owner editor PID 46624 was preserved;
  no game, export or benchmark was started for this filesystem task.

The metadata audit encountered 273 inaccessible long shader-cache paths in other
old scratch profiles. None were selected or removed. Windows `DirEntry.stat`
did not provide reliable link counts, so large-file identities were refreshed
using `os.stat`; logical size totals were not treated as recovered disk space.

Files: `inventory.json`, `cleanup-plan.json`, `mutation-journal.jsonl`,
`removed-duplicates.json`, `archive-catalog.json`, `archive-result.json`,
`owner-guard.json`, `verification.json`, logs, scripts and concise `HANDOFF.md`.

## Remaining direction

Native Mac results are pending from the owner using the unchanged ZIP. Live-object
growth and existing Save/cold-loading/large-station pacing gates remain open.
See [current release QA](WINDOWS_MAC_RELEASE_QA_2026-10-16.md). Preserve the new D:
archive, retained canonical runtime and current release selection in future cleanup.
