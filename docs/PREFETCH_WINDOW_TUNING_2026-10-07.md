# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: bounded startup worker window

## Objective and acceptance

Reduce the extended loading decoder's temporary peak/waste while preserving loading responsiveness, pixels, resource ownership and gameplay. Original frame/memory/loading/bug/endurance/PC/Mac gates remain open. No normal checkout admission.

## Accepted decisions and constraints

Only private frozen ImagePrefetch.WINDOW changes96→32; UID and art unchanged. Earlier loading/library changes and experimental sixteen-source drone provider remain in this candidate. No permanent cache or quality reduction. Worker image-count window is not an absolute decoded-byte cap. Cold first launch without a saved order still uses zero prefetch workers; do not attribute its timing difference to worker scheduling.

## Current state

Four native debug=true fixed-site9062026 lifecycle trials:96,32,16,96. Each142checks/zero failures/errors/leaks/warnings. Both candidate/repeated controls match all six retained texture endpoints and sorted prop-source lists. Temporary Continue decoded peak:242,243,576bytes at96;95,415,252 at32;59,485,088 at16. Pending peak167→49→31; unused169→71→41. Native Continue times5,364.487/5,559.812/5,677.880/5,344.859ms.32 has~205ms/3.8% penalty against mean96;16~323ms/6.0%. NewGame native17.3–17.5s and variable large gaps are development evidence, not packaged loading certification or worker-attributed changes. Select32 as the lower-memory/lower-penalty packaged trial. Native32pixel fixture285checks/69exact uploaded-image comparisons clean.

Maintained export creates physical startup-window32-release/BrineSpace.exe and adjacent PCK under output/drone-compiled-2026-10-07. Build814e13b9914ed90a; source SHA256814e13b9914ed90abd21fb2821166551161c176d3b5bf76a1007d6be0d7d6ab9. EXE109,283,328bytes/PCK3,646,716,489bytes. Broad outside-checkout audit36,288checked/55remaps/zero missing/changed/unexpected. Actual debug=false pixel fixture285checks/69exact pairs, all23warm source requests served, startup storage released; clean exit.

Actual packaged fixed-site pair compares prior17e0b0c67184deaf WINDOW96 against814e13b9914ed90a WINDOW32 with identical unprepared fixtures. Both142checks/clean exit. Maximum gaps NewGame212.926→238.098ms, Continue265.700→247.524ms: shorter handoff pauses preserved within this fixture. Elapsed NewGame12,369.525→13,375.866ms (slower, neither launches workers), Continue4,947.010→4,871.687ms, single pair only. No repeatable speedup or cold/warm loading certificate.

Packaged worker peak exactly reproduces native242,243,576→95,415,252bytes (~231.0→91.0MiB; ~60.6% reduction), unused169→71, submissions12,854→12,726. All six retained texture counter deltas zero, sorted library source lists equal. Candidate Continue capture inspected; not full motion/UI acceptance. End releases decoded storage; no whole-system peak RAM/driver VRAM or endurance claim.

## Verification and cleanup

All native/export/audit/pixel/comparison profiles isolated; owner fingerprints2,936 files unchanged. Native temporary override removed; only selected32constant retained in the frozen trial. All tool/process handles terminal. Normal gameplay source unchanged; prior candidate packages retained.

QA physical-copy preparation failed with WinError112 (disk full), before gameplay. Native PowerShell verifies actual SHA256 equality to preserved packages and recorded identities, then removes only obsolete qa-inplace/BrineSpace.pck, qa-tokens/BrineSpace.pck and the partial qa-startup-window32/BrineSpace.exe. Removes the now-empty partial QA directory, then recreates the complete test copy. Reclaimed7,407,999,708bytes. Source/art/saves, fixtures, identities, logs and retained packages preserved; obsolete two QA copies require reconstruction from their retained packages before reuse. Details: verified-qa-duplicate-cleanup.json and cleanup-verified-qa-duplicates.ps1. No recursive deletion or running test process was involved.

Evidence: native-prefetch-windows.json, native-prefetch-window-summary.json, native-window32-pixels-results.json, prefetch-window32-source.json, startup-window32 export/audit logs/expected manifest, window32-pixels-results.json, startup-window-comparison.json, startup-window-resource-comparison.json and per-lane session/gap/capture files; corresponding owner fingerprints. QA fixed-seed fixture identities preserved.

## Next action

First-load stage remains large and serial without a prior request order: investigate bounded hints from the selected animation manifests before their PNG loops, keeping existing selected-animation/runtime PNG behavior and byte/pixel ownership intact. Also replace provisional three covered frames with observable preparation acceptance and test restored12/40-room/layout/resize/input/clock workloads. Three matched packaged loading runs and larger/motion/resource coverage remain before admission. Continue larger sustained frame-time, GPU memory, drone admission, original bug and PC/Mac/endurance certification work; no release upload.
