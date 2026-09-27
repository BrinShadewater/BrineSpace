# Project handoff

Updated: 2026-09-26 · Project: BrineSpace · Task: Playable build after drone installation

## Objective and acceptance
Continued the owner's installation request into a new local Windows build. Delivered `builds/BrineSpace-2026-09-26-drone-runtime-r2/BrineSpace.exe` with its PCK, build metadata, expected manifest, rights notice, README and SHA256SUMS.

## Accepted decisions and constraints
Preserve previous builds and owner saves; no commit, push or publication. Existing gameplay costs/timings remain. Selected source inputs were physically frozen before the successful export because concurrent River artwork edits invalidated the first manifest during export. Build identity, not the current moving workspace, defines this evidence.

## Current state
Build `brinespace-073f851880d1bda9`, source SHA256 `073f851880d1bda980dfbedcf0b2e7bd59f285fd168f11df24ee72f961e25624`. Maintained exporter used verified Godot 4.7.2 templates against `output/drone-release-2026-09-26/frozen-source`. That snapshot holds 15,676 manifest inputs (about 2.20 GB raw); original commit identity is recorded in build_info.json, with working-tree modifications. Later edits are outside this build.

Fixed `tools/set_raw_png_import_keep.py`: newly added manifest rasters now receive raw keep rules, newly added unused studies receive skip rules, new scene resources retain the normal importer, and absent working-tree files are ignored. Targeted regression added at `tests/test_raster_import_inventory.py`. No raster art changed for this fix.

## Verification
- Manifest tests: 8 passed. New raster-role regression passed.
- Frozen runtime assertion scan: zero failures. The broad repository assertion scan reports eight historical preview-only scripts; none enters this package. Their failure evidence is retained separately.
- Maintained export succeeded without error-log rejection. Post-export hashes confirm zero frozen source changes.
- Exact-PCK audit: 15,304 checked, zero missing/changed/unexpected, zero remapped.
- Actual release template: New Game, transmission Continue, Resume/simulation, visible station and F8 report checks passed; `debug=false`, zero engine/script errors. All three production drone/dock renderers exercised at four phase samples. Native startup and drone captures visually inspected.
- APPDATA was isolated under the evidence directory, and the autoload fixture guards that resolved user-data path before running. QA EXE/PCK were hardlinks used read-only. The delivery has no override.cfg or QA fixture.

Evidence, logs, hashes and captures: `output/drone-release-2026-09-26`. Rejected concurrent-change export retained as evidence, not a deliverable. Successful exporter log is `export-frozen.log`; actual-release marker is in `actual-release.log`; full hash inventory is `validation.json` and the delivery SHA256SUMS.

## Next action
Owner playtest and visual acceptance. This is an actual-release startup/animation smoke test, not full-expedition/balance acceptance. No further rebuild is needed for these documentation-only updates.
