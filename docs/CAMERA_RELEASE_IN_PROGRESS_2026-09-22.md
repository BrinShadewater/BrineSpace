# Camera/Fit test build in progress

Updated September22,2026. This is not an accepted build handoff.

## Selected source and constraints
Candidate build ID brinespace-fb99bc56643b745a, source SHA256
fb99bc56643b745a8c2d58b6b2aaeb6fa764ab3336629707a6f50e1615246549.
Includes local Continue core-focus and Fit preparation scheduling changes.
Preserve accepted b0d1640cfe18c6fc packages and owner data. No publication requested.

## Active operation
Windows maintained exporter started for
builds/BrineSpace-camera-polish-2026-09-22/BrineSpace.exe.
Unified exec session87703 was confirmed running; output/release-export.log shows
active savepack progress. Re-poll this handle; do not restart from this note alone.
Wrapper log: output/camera-release-2026-09-22/windows-export.log.
Do not run the Mac exporter concurrently with Windows manifest/export mutation.

## Prepared QA, not yet executed
output/camera-release-2026-09-22 contains frozen windows-expected-manifest.json,
release-smoke.gd, run-release-smoke.ps1, both expected pixel lists, package.py and
empty/. Harness extends prior accepted release smoke with actual disk replacement-
scene Continue at0.55zoom, exact crew/resource preservation, core focus<2pixels,
and real toolbar Fit-button settlement/visibility. No claim of pass until run.
QA remains outside deliverables. package.py expects both platforms/audits; do not
run it as proof before the prerequisites exist.

## Next action
1. Wait for session87703 and inspect both logs/exit. Freeze Windows export log.
2. Run actual-release driver and audit_release_assets.gd from empty/ against the
   Windows PCK and frozen expected manifest. Inspect rendered restored/Fit images.
3. Export Mac to builds/BrineSpace-mac-camera-polish-2026-09-22 using maintained
   export_macos.py. Verify matching source identity, extract/audit its PCK, then
   package instructions/hash sums using prepared package.py. Native Mac remains open.
4. Only promote CURRENT_STATUS package identity after all claimed checks pass.

## Windows verified; Mac export active
Windows exporter session87703 completed exit0. Frozen engine log is
windows-godot-export.log. Exact Windows PCK audit passes15216assets, all discrepancy
counts0. First actual-release attempt failed external QA indentation before tests;
isolated process was stopped, logs preserved as failed-harness*, indentation fixed.
Fresh-profile retry session91101 completed exit0: actual release debug=false,
zero failures, empty stderr,49bunk+49polish samples match. Disk Continue preserves
crew/resources, core focus error1.41399pixels; Fit starts/settles with visible station.
Native release-restored.png and release-fit.png inspected. No package-side source
fix was needed. These are core-scene camera/Fit checks, not a100room timing claim.

Mac exporter session26145 remains active, last verified progressing through scan.
Log: builds/BrineSpace-mac-camera-polish-2026-09-22/export.log and QA/mac-export.log.
Re-poll this exact handle, then inspect errors/structure and matching build metadata.
Extract Mac PCK using package.py --extract, audit from empty/ with Mac expected-
manifest.json, then run package.py to finalize instructions/hashes/checklist.
Do not promote the matching pair until Mac audit is finished. Native Mac execution
remains unverified regardless of export/audit success.

Completed: Mac exporter session26145 exit0; exact Mac PCK audit passes15216assets
with all discrepancy counts0. package.py completed instructions/NOTICE/checksums
and release-checklist.json. No live export sessions remain. Current final handoff:
CAMERA_POLISH_TEST_BUILDS_2026-09-22.md. Earlier active-operation notes are historical.
