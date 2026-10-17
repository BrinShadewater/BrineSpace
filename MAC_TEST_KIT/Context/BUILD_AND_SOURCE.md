# Exact build, source and archive provenance

The app is **brinespace-d3cfa1890bafefe7**, Godot 4.7.2 official templates,
Universal 2 arm64/x86_64. Windows source fingerprint:
`d3cfa1890bafefe7e5b1a8c4e3f4f01f52e19d1e250701c27832d52b675e7514`.
Runtime PCK:
`49a95db92f2382f52b56034a5af4515746a464d2695e2aa1e150ca83d0c09b12`.

`build_info.json`, `expected-manifest.json`, `platform-parity.json` and
`bundle-audit.json` accompany the app. Windows/Mac runtime manifest, PCK and build
metadata must match exactly; the Mac executable is naturally a different platform
binary. The original app files and executable modes are preserved when documentation
is added **outside** the .app. Native `codesign`/Gatekeeper/launch checks remain pending.
Local testing distribution uses ad-hoc signing, not Developer ID/notarization.

`FILE_SHA256.json` verifies the extracted game package, excluding that manifest's
self-hash. The external `ARCHIVES_SHA256SUMS` anchors the final game/source ZIP
hashes. To check both ZIPs in the transfer directory on Mac:

```sh
shasum -a 256 -c ARCHIVES_SHA256SUMS
```

## Optional editable source

Extract **BrineSpace-source-d3cfa1890bafefe7.zip** separately. It contains the
selected physical source/assets/tests and paired UIDs, plus `MAC_TEST_KIT/` with
this context. `project.godot` is the project entry. Read `MAC_TEST_CONTEXT.md`
before opening it in Codex. `SOURCE_FILES_SHA256.json` verifies archive payload;
`SOURCE_PROVENANCE.json` records selected count, explicit omissions, metadata/docs
overlays and runtime identity. Example from the main game kit:

```sh
python3 Context/tools/mac_qa.py verify-source --source-dir /absolute/path/to/BrineSpace-source-d3cfa1890bafefe7
```

This is **not just Git HEAD**. Base commit is
`67e7db969f7c5d952a3c80830369715d703199c5`; accepted working-tree changes from several
sessions and the d3 Save patch are part of the frozen selection. Cloning that commit
or a newer main branch alone does not reconstruct this build. The archive is not
a Git repository; it has no hidden dependency on a Windows shared Git object store.
All selected raster files are real bytes, not LFS pointers.

All runtime inputs listed by the Windows manifest are verified against the archived
source. Current handoff documentation and the post-freeze native router pixel test
with its UID are overlaid where recorded; these do not change runtime dependencies. Source build ID
hashes selected runtime inputs, not the entire ZIP or documentation archive. Import
sidecars are retained; `.godot/` cache is omitted and must be regenerated on this Mac.
Do not copy a Windows import cache into native acceptance.

The five platform export-tool files under `output/export-tools/4.7.2-stable/`
(official template archive, Mac template ZIP, two Windows executables and checksum
file) are explicitly omitted to avoid shipping ~1.5 GiB of SDK binaries. Other
generated output, Git history, live owner profiles, vendor art and private trace
directories are not this source payload. Runtime dependencies are not omitted.

Godot is unnecessary to play the exported app. To test/edit source, install/select
official **4.7.2**, confirm its actual `--version`, complete imports in the QA account
and preserve graphics settings. Source tests use the maintained runner, after
native isolation proof. To re-export, install/verify matching official templates;
the project presets contain historical relative custom-template paths. The maintained
`tools/export_macos.py` expects verified files in output/export-tools/4.7.2-stable.
Do not bypass template version/hash checks or change runtime art to make export pass.
See the [release workflow](project-docs/RELEASE_WORKFLOW.md) and
[official Mac export guidance](https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_macos.html).

Keep the frozen app unchanged when experimenting. Any source fix gets a separate
build ID/export and affected validation; do not claim the old package tested new
code. Preserve NOTICE/LICENSE and bought-art rights. No signing credentials or
publication authorization are included.
