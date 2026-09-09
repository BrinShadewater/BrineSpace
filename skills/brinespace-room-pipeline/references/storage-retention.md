# Storage and generated-build retention

Use this during asset-pipeline closeout or an authorized storage cleanup. Keep
source-art preservation separate from generated-binary retention.

- Preserve accepted art, raw generations, exact prompts, selection manifests,
  source snapshots, screenshots, logs and rejection reasons. A v1/v2 suffix or an
  old modification date does not prove an image is unused or visually bad.
- Record each retained accepted package's location, hash and tested scope. Retain
  the current deliverable and any explicitly required historical baseline. A
  source change does not inherit an older package's acceptance.
- Treat redundant isolated EXE/PCK copies and explicitly rejected/superseded test
  binaries as cleanup candidates. Do not delete all of output: it mixes binaries,
  unique source material and evidence. Deleting a binary ends direct replay of
  that exact snapshot; keep its manifest and test records and mark it removed.
- For an authorized cleanup, enumerate exact files and sizes, resolve each path
  within its approved root, reject reparse points, recheck modification and active
  use, and preserve logs/README files. Prefer file-only removal. Record the actual
  deleted-file manifest, failures, reclaimed space and protected-package checks.
  Disk-pressure guidance is not blanket permission for future deletions.
- Do not manually delete Git/LFS objects, remove unique source art, or clear an
  active Godot cache as part of generated-build cleanup.
- During future export-tool maintenance, give temporary copies an explicit
  lifecycle: release successfully completed isolated copies after evidence has
  been saved and processes have exited. Retain failed-run diagnostics, and retain
  failed binaries only when needed for a recorded investigation. Keep a deliberate
  package retention list instead of a full executable for every visual iteration.

Observed failure: tools/validate_environment_export.ps1 creates a new
BRINE-environment-validation GUID directory under TEMP, copies EXE/PCK files into
it, and its finally block only restores the working directory. The September 8
audit found 23 copies totaling 34.96 GiB. Cleanup removed these and older build
binaries; the export script itself was not changed. Automatic cleanup remains a
separate implementation task, not an installed capability.

See docs/STORAGE_CLEANUP_2026-09-08.md in the maintained project for dated evidence.
