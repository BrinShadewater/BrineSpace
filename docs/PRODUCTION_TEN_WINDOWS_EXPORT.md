# Windows validation export

The official Godot 4.6.1 non-Mono template archive was downloaded from
`godotengine/godot-builds` release 4.6.1-stable and SHA-512 verified against its
published SHA512-SUMS.txt. Only Windows x86_64 debug/release templates were
extracted locally. Archive, checksums and verification record are under
`output/production-ten/export-tools/`, excluded from Git.

`export_presets.cfg` adds Windows Room Validation, with custom local templates,
raw PNG/JSON inclusion and selected actual game scenes/room fixtures. Output is
local, unsigned and not published. `output/.gdignore` prevents local evidence
and downloaded tools being imported as game content.

The first all-resource export returned zero but logged broken references in an
older animation study. V2 uses selected-resource roots and has no ERROR/SCRIPT
ERROR entries. Evidence: `windows-export-v2.log/.err`; executable and PCK are in
`windows-validation-v2/`. It preserves the current title-screen entry point.

The standalone executable launched from a fresh external directory with
`--quit-after 120` and exited zero without resource/script errors. Evidence:
`windows-title-v2.log/.err`. This proves a real template-based executable starts;
it does not certify the room batch in that executable.

The official template rejects scene path overrides and does not run the editor
SceneTree test harness through the attempted --script invocation. That first
process was stopped; the explicit scene-path attempt exited with the template's
path-override error. Exported-room verification therefore needs a dedicated
runtime validation entry point and isolated save behavior, rather than treating
the earlier editor/PCK tests as executable acceptance. That work remains pending.

## Exported station verification (v6)

`tools/build_room_export_fixture.py` mechanically adapts the existing SceneTree
fixture base to Node and copies the mixed-station fixture body unchanged. Source
SHA-256 values are stored in `tests/runtime_generated/sources.json`; UIDs are
preserved on regeneration. The bridge hands current_scene to the actual game.
The `room_validation` export feature selects this scene through a project feature
override. Ordinary builds retain the title screen. The fixture uses its existing
process-specific isolated save and removes it afterward.

The first working runtime bridge exposed missing raw PNGs: the executable's
fixture could print PASS with empty room interiors. The normal PNG include filter
retained imports but not every source byte. `addons/brine_raw_export/plugin.gd`
now explicitly adds raw PNG files from known runtime art roots alongside imported
textures. No runtime loading behavior or source art is changed.

V6 export and standalone mixed-station execution both exit zero with no
ERROR/SCRIPT ERROR entries. All fifteen rooms are visited through 303 valid walker
transitions. The actual exported 1600x900 station image was inspected: all ten
subjects, furniture, hulls, doors and draft cards are present. Evidence:
`windows-export-v6.log/.err`, `windows-runtime-v6-1600.log/.err`, and
`windows-runtime-v6-1600/`. This supersedes the earlier pending exported-room smoke.

This is a local debug validation executable, unsigned and unpublished. It is not
an installer, release-signing test, all-driver compatibility claim or complete
exported game playthrough. Raw Image.load warnings may remain despite readable
source bytes; logs are assessed for actual failures separately.

## Explicit exported-asset assertions (v7)

The mixed-station fixture now verifies every selected source SHA-256 against the
manifest (including v2 revisions) and decodes both raw source and card PNGs. V7
passes ten hashes, twenty PNG decodes, all fifteen visited rooms and 303 walker
transitions. Export and positive runtime logs have no ERROR/SCRIPT ERROR entries.
A deliberate `--negative-source-check` run exits 1 with asset-check failures,
proving the harness rejects wrong source hashes. It does not modify source files.
Evidence: `windows-export-v7.*`, `windows-runtime-v7-1600.*`,
`windows-negative-v7.*` and corresponding captures.

## Repeatable checked command

Run `tools/export_room_validation.ps1 -Godot <Godot executable> -OutputDirectory
<new absolute directory>` from PowerShell. The verified custom templates referenced
by the preset must already exist. The command rebuilds the generated fixture,
exports, checks stdout/stderr as well as process status, runs outside the checkout,
requires asset and mixed-station result markers, validates complete room coverage,
and records executable/PCK SHA-256 in verification.json. Each process has a
60-second timeout. Existing destinations are rejected; evidence is never deleted.

The command itself passed at `output/production-ten/windows-helper-check/`: ten
source hashes, twenty PNG decodes, fifteen visited rooms and 303 transitions.
This is the preferred reproduction path over manually chained invocations.

## Additional underwater adaptations

The station fixture and checked export command now accept additional manifests.
Thermal Power Control, Acoustic Communications and Hull Integrity Control were
included in `output/production-ten/windows-validation-adaptations-v1` using the
`-AdditionalManifest` array of their three `res://rooms/underwater/.../manifest.json`
paths. No extra manifests retains the original ten-room default.

The exported executable ran from an empty external working directory. Thirteen
selected source SHA256 checks and 26 raw PNG decodes passed; the dynamic fixture
uses seven trunk rooms plus thirteen subjects. All 20 rooms were visited in 295
valid production-walker transitions over 2,000 simulated walker seconds. This is
not 2,000 seconds of economy simulation or a real-time performance measurement.
Export/runtime checks passed with no SCRIPT ERROR/ERROR lines; executable/pack
hashes and coverage are in `verification.json`. The native start overview was
visually inspected and all three new adaptations render. The objective overlay
obscures part of the old Lounge at this overview; no claim of complete art review
is made from that frame. Individual-room captures remain the detail evidence.

Fixture source loading falls back from optional `selected_source` to `source`,
rejects duplicate identities and computes trunk capacity from the batch size.
The runtime summary defers scope to subject-specific assertion output instead
of claiming inherited rotation coverage. Signing/distribution remain out of scope.
