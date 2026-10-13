# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: actual Windows release scene-loading warning

## Objective and acceptance

Determine whether the background scene-resource warning affects an actual debug=false executable. Preserve the full PC/Mac performance/release scope; this diagnostic does not certify gameplay, visuals, loading or release readiness.

## Accepted decisions and constraints

Freeze physical normal source/runtime inputs and use the maintained Windows exporter. Do not alter normal loading or admit experimental memory providers. Tests use isolated APPDATA, resolved-directory verification and owner fingerprints. No upload/publication or original-repository commit.

## Current state

Evidence: `output/scene-load-release-2026-10-06/`. `source-location.json` identifies the short-path physical snapshot and per-input hashes. A shared metadata clone with a populated, verified index supplies Git identity; runtime files are independent physical copies, not shared files. Snapshot selected ~36,600 files/3.59 GB. Required exporter plugin/config/paired UID were added after the first manifest attempt identified their absence.

Maintained `tools/export_release.ps1` runs against that snapshot and verifies editor/release-template 4.7.2.stable.official.ed1daf0bf. Build identity `brinespace-3429e7142ba143eb`; manifest 36,241 inputs/3,593,457,026 bytes. Runtime PNG roles retained: 63 scene-resource rasters, 33,804 raw rasters. Normal working-copy configuration/import roles remain untouched.

Diagnostic export: `release/BrineSpace.exe` 109,283,328 bytes; adjacent PCK 3,622,993,371 bytes. Physical QA copy and override/guarded adapter in `qa/`, created through maintained release-copy isolation. Identity records executable/PCK and actual diagnostic-adapter hashes. The adapter loads the normal gameplay scene resource but never instantiates it; it verifies debug=false and scratch profile before testing.

## Verification

- Exact PCK raw-asset audit from a separate empty directory: 35,779 checked, missing 0, changed 0, unexpected 0, remapped 0. This audits raw files, not full visual/gameplay acceptance or every compiled-resource mapping.
- Actual release executable: debug=false explicitly required and observed. Threaded normal scene-resource load reproduces 34 anonymous RefCounted objects at exit, each reference count zero. Synchronous resource load exits with no warning. No script/engine errors in these successful probes.
- This confirms the loading trigger survives a real release PCK/executable with the maintained current preset's script_export_mode=0. It is not a binary-token-mode comparison; such a case remains untested. Source/editor findings do not substitute for this release observation, and this narrow release observation does not certify normal entry/gameplay.
- Owner fingerprints remain identical: 2,936 non-log files before/after freeze, export, audit and runtime lanes. Processes terminal. No owner save writes, art edits, normal loader patch, renderer upgrade, experimental-provider admission or publication.

## Next action

Reduce the normal scene dependency/background-loading reproduction and test an approach preserving responsive progress. Investigate binary-token export mode as a measured diagnostic if it distinguishes source parsing from resource loading; preserve the normal preset until validated. Blocking synchronous loading and still-warning worker prototypes remain unaccepted. Continue larger frame costs and lossless provider composition/source integrity/admission; original memory/loading/packaged bug/endurance/Windows/Mac gates remain open.
