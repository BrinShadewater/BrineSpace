# Project handoff

Updated: October10,2026 · Project: BrineSpace · Task: authorized duplicate-package cleanup

## Objective and acceptance
Owner explicitly authorized removing unneeded files after the disk audit. Reclaim
space from verified duplicate test binaries while retaining unique evidence and
current/rollback deliveries. Original performance/release objective stays active.

## Accepted decisions and constraints
Only SHA256-identical generated QA PCK copies deleted; no recursive directory
deletion. Resolved paths checked against allowed test roots before deletion.
Engine-process guards checked before each deletion. Preserve selected art, source,
Git/recovery archives, bought packs, owner data, logs/captures and unique packages.
Use the retained reusable QA runtime for subsequent serial diagnostics; avoid
another complete PCK copy per experiment. Frozen release inputs still physical copies.

## Current state
D:23duplicate PCKs removed,77.609GiB. C:37duplicate PCKs removed,122.186GiB.
Total60files/199.794GiB logical bytes; measured net free gain197.94GiB during
passes (other filesystem activity affects free-space delta). Latest free-space
reading C:124.03GiB,D:82.09GiB. Sessions69646/59580 terminal0.
No blanket output/temp/history deletion; unique C:packages have retained canonicals.
Current shared QA remains at D:/bs-release-crew-cache-20261009/floor-slot-trial/
prepare-diagnostic/workloads-v2/runtime/. Current and rollback source/windows/mac
delivery folders under both D:release roots retained.

## Verification
Both cleanup owner guards2,938files unchanged. All60deleted paths absent, all
retained restore sources exist, current QA PCK matches expected e9d3f846... hash.
Both frozen project.godot, WindowsEXE/PCK and MacZIP present. No game launch/test
needed for file-only duplicate removal. The removed binaries can be restored from
retained identical files; original report/script locations remain available.
Removed test runtime paths are no longer directly runnable until their PCK is
restored. Do not recreate every historical runtime automatically.

Ledger and verification under output/renderdoc-tools-2026-10-08:
qa-pack-cleanup.json,c-pack-cleanup.json,cleanup-verification.json. Each deleted
entry records absolute target,size,SHA256 and retained restore_from path.
Drivers cleanup-redundant-qa-packs.py,cleanup-c-duplicate-packs.py;
c-output-pack-usage.json is a pre-cleanup inventory, not current file existence.
The earlier disk-usage-audit.json likewise predates deletion.

## Next action
Resume private navigation-prefix correctness prototype using the retained QA
runtime once needed. Preserve muted secondary-display testing. Review further
obsolete generated snapshots only with their provenance established; no need to
touch owner art/history or rebuild eliminated copies. Full PC/Mac gates remain open.
