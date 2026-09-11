# BrineSpace release workflow

Use this when making a playable build or certifying packaged assets. This is not
required for a portrait candidate or a documentation-only change.

## Select the revision and dependencies

For owner-requested uploads after release validation, follow
[the saved Butler upload procedure](ITCH_UPLOAD_WORKFLOW.md).

Read CURRENT_STATUS.md and the relevant build handoff. Later source work does not
inherit an older executable's acceptance. In a shared checkout, freeze the selected
source and runtime bindings when other art/animation work is in progress; name any
excluded unfinished work. Record the build ID, source fingerprint and EXE/PCK hashes.
Use a new output directory or an explicitly selected replacement, preserving the
current accepted deliverable. No commit, publication or source deletion is implied.

Prefer tools/export_release.ps1 for Windows Game builds. It invokes
build_release_manifest.py, updates the dependency list, emits build_info.json,
checks source hashes through the raw export plugin, waits for Godot, and rejects
error logs. Supply ProjectRoot, Godot and a distinct OutputPath as needed. Preserve
other export presets and use no validation feature flags for a playable game.

Do not exclude directories by name without checking consumers. In particular,
tools/modular_room_geometry.gd is a gameplay and Room Layout Studio dependency.
Runtime PNG reads require raw bytes even when Godot also imports the image. Keep
JSON-relative frame paths, dynamic directories and imported control resources in
the manifest. Limit the shipped dependency set without deleting raw generations,
rejected candidates, prompts or review evidence from the authoring archive.

## Raster import roles (September 11, 2026)

Releases carry each tracked raster in one of three roles, assigned by
`tools/set_raw_png_import_keep.py` from `assets/runtime-release.json`
(`tools/export_release.ps1` runs it after the manifest build):

- Rasters referenced by `.tscn`/`.tres` keep the normal texture importer; they
  ship as imported `.ctex` through a remap, so the pack audit counts them as
  `remapped`, not `missing`.
- Manifest rasters get `importer="keep"`: no `.ctex` is generated and Godot's
  own selected-resources pass ships the raw file byte-identical. The raw-export
  plugin therefore no longer adds rasters itself (it still adds JSON/SVG/CFG/MD
  and still verifies every manifest hash).
- Every other tracked raster gets `importer="skip"`: never imported, never
  exported.

This removed ~2.4 GB of unread `.ctex` and ~3.4 GB of QA/source rasters per
release (5.8 GB → 1.2 GB pack). `.import` sidecars are local editor state; after
adding art or changing the manifest, rerun the tool and let the editor rescan.
The manifest crawler also no longer scans `addons/` (the export plugin's
`begins_with("res://rooms")` prefix test was read as a dependency), and
`scripts/swim_helmet_fit.gd` names only the fit table and `equipment/` subtree
instead of its whole source tree.

## Checks that establish different things

- Import/parse and relevant regressions: run the changed subsystem checks. Include
  tests/test_release_assert_safety.py when runtime loaders changed, and
  tests/test_release_manifest.py when release dependencies changed. Read current
  invocation/scope first. Stop broadening once the relevant checks pass.
- Packed assets: tools/audit_release_assets.gd runs from an empty directory and
  mounts the PCK against its expected manifest. Verify missing/changed counts,
  not just successful export. An editor with --main-pack can inspect packaged
  textures and render scenes, but it retains editor/debug execution behavior.
- Actual release behavior: use tests/release_new_game_smoke.gd through a temporary
  autoload override beside an isolated copy of the EXE/PCK. The fixture requires
  debug=false and uses explicit failure branches. Follow the override recipe in
  TEEGLY_PR_INTEGRATION_2026-09-09.md; give it isolated user data and remove the
  override before delivery. Exercise the normal title/New Game/dialogue/Resume
  path, confirm simulation advances and the station is visible without Fit/Locate,
  and check changed release-only behavior such as F8 reports when in scope.
- Visual acceptance: inspect the scenes actually exercised at native window sizes.
  Constructor values, a success marker or file hashes alone do not approve art.
  Preserve dated captures, logs and tested package identity.

A release EXE starting with --script does not establish that an external script ran.
Require the intended fixture marker, explicit failure count and debug=false. Never
put required loading, decoding, state mutation or verification only inside assert():
release templates strip assertions. Perform the operation first, handle its return
value, then optionally assert an invariant for debugging. Runtime artwork should
use the maintained safe-image helper where its consumer contract applies; a fallback
is diagnostic evidence, not visual approval of missing artwork.

## Camera and UI regression detail

Range changes can emit value_changed even if set_value_no_signal is used afterward.
Preserve and restore the slider's signal-blocking state across programmatic range
updates. Otherwise startup can queue an unintended zoom and invalidate the core
centering request. Keep normal camera processing active during the regression;
freezing _process immediately or manually centering before capture hides the bug.

## Deliver and stop

Wait for the final export/runtime processes, inspect exit codes and relevant errors,
and recheck only what changed after a failure. Windows GUI process launch returning
is not completion: use Start-Process -Wait/-PassThru with focused log excerpts.
Keep BrineSpace.exe and BrineSpace.pck together, plus README, rights notice,
build_info and SHA256SUMS. Update CURRENT_STATUS and a concise dated handoff with
actual scope and remaining limits. No need to rebuild after documentation-only
closeout. Package retention/cleanup follows the room skill's storage-retention
reference and needs its own authorized scope.

Evidence: WINDOWS_BUILD_2026-09-09.md records the initial dependency/camera fixes;
TEEGLY_PR_INTEGRATION_2026-09-09.md records the later release-only assertion failure
and actual-release harness; RELIABILITY_PERFORMANCE_2026-09-09.md records the newer
manifest exporter, safe loading, exact release IDs and optimized build. These are
distinct tested snapshots, not interchangeable acceptance claims.
