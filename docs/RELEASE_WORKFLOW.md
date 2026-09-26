> September 24 takeover: [current status](CURRENT_STATUS.md), [Claude handoff](CLAUDE_HANDOFF_2026-09-24.md), and [asset pipeline/workflow](ASSET_PIPELINE_AND_WORKFLOW.md) provide the current continuation map. Dated evidence below retains its original scope.

# BrineSpace release workflow

Use this when making a playable build or certifying packaged assets. This is not
required for a portrait candidate or a documentation-only change.

## Mac test exports

Use `python tools/export_macos.py --godot <console-editor> --output <new-directory>`
for repeat builds of the local `macOS Game` candidate. It checks the official
template archive SHA512, embedded version and extracted Mac template identity,
then builds the named manifest, syncs raster import roles, waits for export and
checks bundle structure. Preserve the resulting expected manifest alongside the
build metadata for the separate exact-PCK audit. The first candidate predates this
wrapper; do not claim that candidate exercised the wrapper itself.
Use `--preflight-only` with the same arguments to check prerequisites without writing
manifests or starting an export. Verification resolves the release template from
the named macOS preset and hashes that actual file against the verified archive;
it must not merely check a conventional template path that the preset could ignore.
`python tests/test_macos_export.py` covers non-default selection and missing-template
rejection. September 21 real preflight passed against Godot 4.7.2.

Universal 2 requires ETC2/ASTC import support in project settings. The preset uses
testing distribution and ad-hoc signing, without notarization. A successful ZIP
export or Mach-O inspection does not establish Apple Silicon gameplay, signature
acceptance or readiness for public distribution. Follow `MAC_RELEASE_PLAN.md`.

## Select the revision and dependencies

Broad discovery omits `character/major-bill-v3/sources/` and the specific
`character/chief-engineer-branforth-v2/sources/locker-identity-2026-09-22/` study,
which contain authoring inputs. Exact/formatted file references and their transitive dependencies still
win. Other `sources/` directories can contain runtime art; do not generalize this
exclusion. Keep the sources for rebuilds. Collector tests and a source-byte delta
do not replace an exact PCK audit and actual release gameplay check.


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

For another platform, use `build_release_manifest.py --preset "<exact name>"`.
The default remains Windows Game. Preset selection is by name, not index; missing
or duplicate names fail before metadata writes. Only the selected preset's resource
filters/list change; platform options and other presets are preserved.

Check the template binary's actual version, not its folder name. The maintained
exporter compares the selected Windows template's `--version` with the editor
before export. Matching verified 4.7.2 templates currently live in
`output/export-tools/4.7.2-stable`. The old production-ten template was 4.6.1 and
produced an executable unable to read the newer PCK.

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
release (5.8 GB â†’ 1.2 GB pack). `.import` sidecars are local editor state; after
adding art or changing the manifest, rerun the tool and let the editor rescan.
The manifest crawler also no longer scans `addons/` (the export plugin's
`begins_with("res://rooms")` prefix test was read as a dependency), and
`scripts/swim_helmet_fit.gd` names only the fit table and `equipment/` subtree
instead of its whole source tree.

## Python checks versus Godot checks

`tools/run_tests.py` discovers Godot `.gd` tests only. Use direct Python commands
for release checks: `python tests/test_release_manifest.py`,
`python tests/test_release_assert_safety.py`, and `python tests/test_macos_export.py`.
An explicit `--only` selection now rejects missing or filtered-out names instead
of silently succeeding with zero tests. Three selection regressions pass in
`tests/test_test_runner_selection.py`; a valid Godot selection still lists normally.

## Checks that establish different things

- Import/parse and relevant regressions: run the changed subsystem checks. Include
  tests/test_release_assert_safety.py when runtime loaders changed, and
  tests/test_release_manifest.py when release dependencies changed. Read current
  invocation/scope first. Stop broadening once the relevant checks pass.
- Packed assets: tools/audit_release_assets.gd runs from an empty directory and
  mounts the PCK against its expected manifest. Verify missing/changed/unexpected counts,
  not just successful export. An editor with --main-pack can inspect packaged
  textures and render scenes, but it retains editor/debug execution behavior.
- Actual release behavior: use tests/release_new_game_smoke.gd through a temporary
  autoload override beside an isolated copy of the EXE/PCK. The fixture requires
  debug=false and uses explicit failure branches. Follow the override recipe in
  TEEGLY_PR_INTEGRATION_2026-09-09.md; give it isolated user data and remove the
  override before delivery. Exercise the normal title/New Game/dialogue/Resume
  path, confirm simulation advances and the station is visible without Fit/Locate,
  and check changed release-only behavior such as F8 reports when in scope.
  Wait for observable architect/dialogue/Continue state with bounded timeouts;
  frame-count waits can expire while the normal transmission is still typing.
- Visual acceptance: inspect the scenes actually exercised at native window sizes.
  Constructor values, a success marker or file hashes alone do not approve art.
  Preserve dated captures, logs and tested package identity.

When adapting a dated QA harness, derive its fixture and log paths from the driver
directory (`$PSScriptRoot` in PowerShell). Freeze expected pixels for the selected
source, and inspect the generated autoload path before running: a copied absolute
path can silently run an older fixture against the new package. Preserve failed
setup evidence separately; do not count that run as new-art acceptance.

Some room families apply authored layouts in render_into, after configure_embedded.
Presence/position fixtures must exercise that production render step before inspecting
effective props. Power-room checks first reported absent supports because they stopped
at configure; invoking render_into through a native preview resolved the false failure.
Preserve the failed fixture evidence and distinguish it from a missing packaged asset.

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
centering request. After transmission Continue, wait for the loading overlay to leave and gameplay
process mode to be restored; a fixed count of process frames can race the covered
rendered frame even after the button becomes available.

Keep normal camera processing active during the regression;
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


## Enabled autoload and package evidence lesson - September 12, 2026

The dependency collector must normalize enabled autoload paths such as `*res://scripts/example.gd` before resolving them; otherwise minimal exports can omit startup dependencies. Keep the regression in tests/test_release_manifest.py. For the Windows release template tested in the Bill/airlock session, use the actual packaged EXE/PCK and an isolated QA harness rather than assuming `--path` redirects the release. Require the fixture marker, explicit failures and debug=false. See docs/BILL_AIRLOCK_RELEASE_2026-09-12.md for the tested package; the later accepted deck sources are outside that package's evidence.

### Migrated runtime art bindings

After moving art, run `tests/test_runtime_room_art.gd` as well as release manifest
and assertion-safety checks. It initializes the Grid and forces directional room
loaders that saved layouts may hide. Concatenated and formatted paths can survive
a literal-path migration unnoticed. Confirm those originals enter the dependency
closure even when stored under `legacy/retired`. The regression also checks the five null-returning foundation loads, but does
not replace full environment rendering or actual release gameplay checks.

Run `tests/test_runtime_environment_art.gd` for the migrated seabed, biome, scenery,
wreck and basalt loaders. It checks expected textures, including those historically
skipped by existence guards. Their selected PNGs must enter the dependency closure;
follow with powered native/executable station review so fog does not mask evidence.

## JSON dependency coverage

Parse JSON structurally when collecting paths: apostrophes and escaped quotes in
labels must not change dependency discovery. Run tests/test_release_manifest.py
after collector changes and check registered source coverage independently.
An exact-PCK match proves agreement with the manifest, not manifest completeness.
For isolated release diagnosis, Godot 4.7.2 supports Logger plus
debug/settings/gdscript/always_track_call_stacks=true in an external override.
Keep that diagnostic override out of playable deliverables.

The actual-release smoke registers a Logger and fails on engine/script/shader
errors as well as fixture assertions. Keep the external log review: early startup
errors before the fixture registers and warnings also need inspection.


JSON fixture comparison lesson (September21): Godot decodes JSON numbers as floats.
Nested-array equality against integer literals can reject correct packaged values.
Print actual values/types before changing product data; compare normalized numeric
components or float literals. Preserve failed harness logs and rerun in a fresh
isolated profile after correcting the fixture.

Use a new isolated application/config/name for every actual-release attempt. A
forced stop after a fixture parse error can leave a genuine session lock; reusing
that profile opens the previous-session recovery overlay and invalidates startup/
F8 assumptions. Verify no recovery overlay is present, rather than disabling crash
recovery or forcing tree.paused=false. For decoded PNG byte hashes in GDScript,
use HashingContext.start(HASH_SHA256), update(bytes), finish().hex_encode();
PackedByteArray has no sha256_text method. See ANIMATION_RELEASE_2026-09-21.md.

## Checkpoint presentation after staged loading

For playable checkpoints, exercise actual release Continue at a nondefault zoom
and verify BRINE is centered after the viewport is visible, alongside crew,
resources and room state. Check subsequent normal-clock progress separately.
The September22 test build brinespace-fb99bc56643b745a includes the Continue camera
fix and Fit preparation scheduling change. Actual Windows Continue/Fit checks
pass; this does not establish native Mac execution, a full expedition or100-room
release performance. See CAMERA_POLISH_TEST_BUILDS_2026-09-22.md for packaged
evidence, CONTINUE_CAMERA_FIX_2026-09-22.md and FIT_BUTTON_PROFILE_2026-09-22.md
for the underlying changes. Re-run relevant release checks when their inputs
change, not merely because an older handoff calls them pending.

Load QA checkpoints from disposable working copies. RunSave.read records _path;
Continue adopts it and conclusion can delete that active file. Keep a separate
frozen evidence copy, fail explicitly on empty reads, and verify the expected run
ID/state so new-loop fallback cannot masquerade as successful restoration.
