# Reliability and rendering handoff

Updated: September 9, 2026 · Project: BrineSpace · Task: artwork failures, release size, rendering, diagnostic snapshots

## Objective and acceptance
Handle missing/corrupt artwork without null textures, reduce the release asset set without removing runtime dependencies, improve measured station rendering, and add exact release identification plus a live diagnostic snapshot. Preserve paid gameplay, authored art/layouts and unrelated concurrent work.

## Accepted decisions and constraints
- No gameplay balance changes, main-script refactor or source-art deletion.
- Other work changed companion bindings to unfinished animation-expansion-v5 during this task. Validation and release use `output/reliability-performance/project`, with the pre-task script bindings plus this task's changes and their required assets. The working checkout retains the other task's edits.
- Reports stay local. Live snapshots are separate diagnostic files; they never replace the player's checkpoint. Editable source is labelled `unpackaged-source` instead of borrowing an outdated release identity.

## Current state
- `scripts/safe_image.gd` handles missing files and malformed PNGs, records a deduplicated path/error, and supplies a drawable diagnostic placeholder. Migrated 95 previously unsafe loader sites across 83 files plus the unchecked crew equipment overlay load. Existing successful PNG pixels are unchanged.
- `tools/build_release_manifest.py` follows scene/script/JSON-relative dependencies and retains dynamic asset-prefix directories conservatively. It generates ignored `assets/runtime-release.json` and `build_info.json`, and updates the Windows Game selected-resource list. `addons/brine_raw_export/plugin.gd` verifies source hashes and exports the listed raw assets. `tools/export_release.ps1` runs generation and rejects export error logs. Existing dedicated validation presets retain their broad raw-asset behavior.
- Exact source/config fingerprints, Git revision and dirty-state context identify a release. Reports add `diagnostics/live_station.save`, a checksum-protected RunSave capture, plus availability metadata and missing-art details. Snapshot size is capped at 16 MiB. `scripts/main.gd` exposes a guarded diagnostic capture without writing a save.
- The shared cryo renderer repeatedly switched between recovery and furnished layouts. `rooms/full-wall-v1/cryo_chamber_view.gd` now caches final geometry and dressing profiles by orientation/pod state, invalidated by layout revision; doors, actors, power and animation clocks still update. `scripts/grid_canvas.gd` culls offscreen wards with a half-cell art margin. Draw-stage instrumentation remains behind the existing profile flag.
- New tests: `test_reliability.gd`, `test_render_reliability.gd`, `test_release_manifest.py`; paired GDScript UIDs. Extended the actual-release smoke and corrected the large-station fixture's dialogue handling. CI runs the manifest and release-assert guards.

## Verification
- Source guard and dependency-manifest unit tests: four tests pass, covering multiline asserts, relative animation frames, dynamically loaded imported controls, excluded debug output and frozen script bindings.
- Native reliability fixture: zero failures. Missing/corrupt images remain drawable, failures deduplicate, valid pixels are identical, title reports explain unavailable snapshots, and an unsaved Metal change is captured while original checkpoint bytes remain unchanged.
- Native render fixture: zero failures. Cached and uncached layout/props/edges match for four orientations and real ward states, clocks and power remain live, layout revision invalidates the cache. Both close and wide native captures are pixel-identical and reviewed.
- Same frozen source, 1600x900 native profile, before/after using `--uncached-recovery-geometry --draw-all-derelicts` versus defaults. Large fixture is labelled 100 but actually contains 98 rooms: fitted view 111.66 -> 77.60 ms/frame (30.5% lower); close view 56.20 -> 22.44 ms/frame (60.1% lower). p95: 118.99 -> 79.34 ms fitted; 58.62 -> 24.12 ms close. Both runs finish with zero failures and no runtime errors. Dedicated profiling flags remain confined to the fixture. The fully fitted station still falls well short of 60 FPS.
- Earlier contaminated snapshot runs are retained as troubleshooting evidence, not acceptance. Final authoritative profiles are `final-before.log`, `final-after.log`, and `comparison.json` under `output/reliability-performance/`.
- Final release export completed without error lines. PCK shrank from 6,245,248,052 to 4,357,522,188 bytes (5.82 -> 4.06 GiB; 30.2% smaller). Native packaged-asset audit from an empty directory checked 10,300 raw assets: zero missing or changed bytes.
- Actual release New Game/Continue/Resume/240 frames/F8: zero failures, `debug=false`, no runtime errors or artwork fallback failures. The diagnostic ZIP contains the live snapshot and build fingerprint, and leaves the checkpoint untouched. Release report screenshot reviewed; temporary test override removed.

## Next action
Playable release: `builds/BrineSpace-2026-09-09-optimized/BrineSpace.exe`, with its PCK, rights notice, README, build_info and SHA256SUMS. Build identity: `brinespace-7ffe90b527116109`. Use `tools/export_release.ps1` for subsequent builds after concurrent animation work settles; it regenerates the dependency manifest automatically. Larger fitted stations remain a performance follow-up. Source changes are local; no new commit or online publication was performed.
