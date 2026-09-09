# Room editor performance, bug and polish pass — September 8

The editor rebuilt its complete asset tray and object list on every drag update, synchronously loaded all artwork previews before opening, re-read authored-layout JSON during runtime lookups, and repeatedly wrote the entire undo history into recovery files. Customized/raised lights bypassed the batched renderer. These costs grew with edits and room contents.

## Changes

- Asset previews decode one at a time on a worker; GPU textures are created on the main thread. The editor opens with usable named tray rows while thumbnails arrive. Shared sources reuse one texture. Closing drains pending work safely.
- Movement preserves unchanged tray/list rows, selection and scroll state. Idle hover redraws only when the highlighted object changes. Surface entities are reused within an editor revision, and validation no longer re-resolves details inside its comparison loop.
- Authored layout JSON is cached rather than read per prop/draw. Opening/reloading an editor room explicitly invalidates that cache. Local saved-layout reads remain isolated copies.
- Recovery only writes changed drafts and omits undo/redo snapshots. Undo is capped at 100 steps per orientation; recovery restores the current draft with a fresh undo history. Existing persisted recovery files remain readable.
- The game/title backdrop is hidden while the full-screen studio covers it and its prior visibility/pause state is restored on close.
- Moved and customized lights use a shared beam mesh: two mesh submissions for two fixtures instead of 56 separate band polygons. The unbatched reference remains available for comparison.
- Copied props display their source names, multi-selection shows a count, unsupported Duplicate actions are disabled, the tray is accurately labeled, and shortcut help includes box selection, groups, copy/paste and Alt snapping.

## Measurements and limits

Local Windows Godot 4.6.1 measurements on the same machine, isolated from owner layouts. Native profile uses a room with 40 extra props. These are bounded editor measurements, not a broad game FPS benchmark.

| Operation | Before | After |
|---|---:|---:|
| Time to open studio | 2,073 ms | 391 ms |
| Typical refresh, median | 0.863 ms | 0.298 ms |
| Populated refresh, median | 1.230 ms | 0.692 ms |
| Drag state update, median | 1.229 ms | 0.658 ms |
| Unchanged tray refresh, median | 0.364 ms | 0.009 ms |
| Authored-layout lookup, median | 0.105 ms | 0.001 ms |
| Complete rendered drag frame, median | 6.064 ms | 6.048 ms |

The initial isolated headless recovery stress check took approximately 24 ms when repeatedly serializing 150 undo entries. The optimized native check writes the draft once (1.36 ms maximum in this sample), with repeated unchanged checks taking 0.006 ms median. The earlier native baseline had pending recovery and is not used for the recovery comparison. Opening time measures when controls become usable; previews now finish asynchronously.

## Verification

- Existing 43-room editor regression suite passed.
- Workflow suite passed cross-room copy, presets, groups, selection, light edits, reload/recovery and in-game rendering.
- New performance guards cover retained tray selection, no duplicate recovery writes, bounded history/recovery, backdrop restoration and closing during thumbnail decoding.
- Batched-versus-reference light capture differed by at most one 8-bit color step (0.003922); the native image was inspected.
- Station operations and Save/Restore checks passed with isolated data.
- Evidence: `output/layout-editor/performance-native-baseline.json`, `performance-native-after.json`, `performance-baseline.json`, `performance-guards.log`, `perf-regression.log`, `perf-workflow.log`, and `game-checks/`.

No gameplay costs, failure conditions, discovery rules or owner saves were changed. Package acceptance is recorded separately beside the new Windows build.

## Windows package

`output/layout-performance-playtest-20260908/build/BrineSpace.exe` is the tested performance build. Its exported workflow and normal startup checks passed with exit code zero and no engine errors. Final EXE/PCK hashes were rechecked unchanged; `package.json` and `checks.json` identify this exact build. The packaged studio capture was visually inspected. Launch from the normal title screen and choose Room Layout Studio; keep the PCK beside the executable. Previous playtest packages remain untouched.
