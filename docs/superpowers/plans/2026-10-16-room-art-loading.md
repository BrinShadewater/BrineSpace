# First-use room art loading implementation plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task. Execute inline with one final fresh-context review.

**Goal:** Reduce first-use room art preparation and benchmark normal Windows loading while preserving all rendered pixels, room geometry and crew behavior.

**Architecture:** Attribute preparation over frozen688 source, select a narrow redundant operation, and preserve lazy view ownership/reentrant publication. Freeze a separate physical source selection and maintained Windows export. Compare against688 with the unchanged primary12-run title-loading fixture and full crew identities, adding room geometry/pixel parity for the changed art path.

**Tech Stack:** Godot4.7.2, existing raw PNG loader/room texture pools, Python/PowerShell release helpers.

**Spec:** Owner's current request and docs/CURRENT_STATUS.md; previous evidence docs/CREW_RESTORE_LOADING_2026-10-16.md.

## Global constraints

Keep matching d3 Windows/Mac pair and both3f/688 Windows/source candidates frozen. Every test/probe uses scratch APPDATA and owner fingerprints. Native work serial, visible screen2, silent and no physical input. Preserve visuals, room collision/door geometry, crew AI/poses/timing, save admission/schema and normal gameplay flags. No unrelated source edits, refactor, Mac export, commit or publication. Keep20GiB free; remove only verified task-owned QA binaries after testing. Use actual maintained exports for acceptance; diagnostic overlays establish attribution only.

## Review focus

Preserve first-use and repeat behavior, all rotations and operating states, owner layout/Studio overrides, reentrant loading draws, and scene/cache lifetimes. Keep essential art ready under the existing loading overlay; do not move a loading cost into the first uncovered play frame. Retain slower/outlier samples and sampled-memory limitations.

### Task1: Measure and choose

- [x] Verify original delivery hashes, baseline-related source equality and real-save fingerprints. Attribute decoding/upload/bounds and redundant inherited/view art setup on representative expensive rooms using existing source/evidence.
- [x] Select one measured avoidable operation; write a failing meaningful regression or controlled parity/performance experiment before changing production.

### Task2: Implement and validate

- [x] Make the narrow change. Verify structural state/geometry and native pixel parity including rotations, lights/doors/operating states and owner-layout cases relevant to the path. Run focused loader/save/lifetime checks and one final fresh-context source review.

### Task3: Package and measure

- [x] Freeze selected full source over688, maintain .gd/.uid pairs, export separate Windows candidate, audit exact assets/scripts/dependencies, and run unchanged12-case loading comparison. Follow up only a new failure/unresolved regression.

### Task4: Close out

- [x] Verify owner/delivery hashes, remove verified task-owned QA duplicates, record candidate identity/results/limits and next action in CURRENT_STATUS/report/HANDOFF-template fields.

Evidence: D:/bs-room-art-20261016/. Helpers: output/room-art-20261016/. No efficiency.csv entry for this routine task.

Ledger:118 preserved hashes pass. Six relevant current source files match688 before edits. Direct native seven-room trace attributes most preparation to sequential decoding (~424ms pool decode versus58ms bounds/27ms upload). Existing parents cache shared donor images; do not redesign inheritance or skip geometry. Ruling: announce each small authored dressing texture list with existing Prefetch.prime before acquisition; first-profile only, repeat learned order unchanged. No new cache, task scheduler or asset format.

Regression fails2 checks before the change and passes afterward. Controlled active-prefetch room initialization745.547→481.958ms, pool decode/wait400.943→127.439ms;22 worker images,7 pending,32.99MiB decoded peak. Scripts preload outside initialization clocks. Clock-only overlays are attribution, not canonical loading acceptance. Initial clock setup rejected expected-LF/actual-CRLF hash differences; exact on-disk hashes fixed the guard, and setup failures are retained.

Five focused prefetch/selector/save/integrity tests pass. Native default layouts117checks/56presentations exact geometry and pixels; frozen owner layouts same117/56 pass. Existing room image-sharing22checks and Python assertion safety2/2 pass. New pixel test needed explicit native-lane override because the runner's headless-guard heuristic initially skipped it; rerun native passes. One fresh-context review and canonical export/cohort pending. Full-source copy in progress; no timing samples overlap it.

Review completed: no runtime findings; one minor fixture rerun issue fixed by resetting only each test's own manifest after scratch verification. Owner-layout pixel test reruns successfully in the same profile; headless fixture runs twice in one profile, both pass. Source freeze complete61,628 files; only one runtime file and index change plus four new test/UID files. Maintained export in progress, manifest36,430 entries unchanged. Canonical loading/identity/audits remain pending.

Completed: candidate53f5bf16534c2cf5 maintained export/exact audits pass (36,430 dependencies;35,942 assets;431+421 scripts). Primary12 actual-release runs show first-profile Continue3.11% lower median, restore~17% faster, but New/repeat observations slower. Ruling: run eight additional reversed-order processes to investigate those new concerns, retaining primary data. Both additional New pairs reverse the primary direction; Continue repeats mixed. Accept scoped room-preparation/first-profile Continue benefit only; do not claim a general New/warm/FPS gain or promote release. All20 valid runs/ten paired crew identities exact. Native station/card crop review passes. All2948 owner files and118 prior delivery checksums unchanged. Verified QA duplicates removed7,476,727,025 bytes; C/D114.953/41.461GiB free, no games. Report ROOM_ART_LOADING_2026-10-16.md; D:/bs-room-art-20261016/HANDOFF.md records continuation. No Mac export/commit/publication.
