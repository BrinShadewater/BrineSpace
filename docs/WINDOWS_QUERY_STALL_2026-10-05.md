# Windows screen-reader query stall investigation

Updated: October 5, 2026 · BrineSpace PC/Mac release readiness

## Objective and acceptance

Resolve the long Windows frame stalls without reducing visuals or overriding
accessibility preferences. This report narrows the cause; it is not a fixed-build
acceptance or evidence about Mac performance.

## Accepted decisions and constraints

The paired build remains `brinespace-af8b5f00998283ef`. All game experiments use
physical QA copies, actual release executables (`debug=false`), isolated APPDATA
and owner fingerprints. Do not patch a shipping binary or silently disable
accessibility. No public bug report, upload or engine upgrade was performed.

## Current state

Added `tools/windows_screen_reader_probe.py`, a standalone read-only Windows API
timing probe with explicit output, bounded duration and failure reporting. It
requires only Python and does not load Godot, game art or a save profile.

```powershell
python tools/windows_screen_reader_probe.py --output output/windows-query.json
```

Raw evidence, QA fixtures and exact engine source extracts are in
`output/stall-attribution-2026-10-05/`. Selected runtime files and assets are
unchanged. Previous evidence is in `STALL_ATTRIBUTION_2026-10-05.md`.

## Verification and finding

The coherent sampler holds the main thread while obtaining context and unwinding,
then resumes it before resolving symbols. Sixteen captures took at most 4.603 ms
of suspension each. These remain diagnostic runs, not timing acceptance.

- `probe-coherent`: a 914.664 ms frame repeatedly samples the Windows system
  parameter query, then message handling. An 865.257 ms frame repeatedly samples
  message handling. Separate 281.820 and 295.210 ms frames sample graphics command
  submission through `nvoglv64.dll`. All 2,936 owner files unchanged.
- The stable query caller is executable RVA `0x15451`. Read-only disassembly
  shows `ecx=0x46` immediately before `SystemParametersInfoA`, followed by a mutex
  fallback matching Godot's screen-reader detection implementation. This resolves
  the call using machine code and exact source, rather than interpreting the
  unrelated nearest exported symbol `NoHotPatch` as a function name.
- `empty-scene`: a 90-second empty scene retaining the packaged reporting autoload
  has p95 8.497 ms, p99 8.918 ms and maximum 987.258 ms at a diagnostic 120 FPS cap.
  Nine frames exceed 100 ms. The large pauses cluster approximately 12.4 seconds
  apart. No station, crew or animation workload is needed. All 2,936 owner files
  unchanged. This does not prove the entire engine is otherwise fast under load.
- `bare-scene`: replacing the reporting autoload with an inert Node preserves
  the freeze. In 90 seconds, p95 is 8.494 ms, p99 9.049 ms, maximum 911.025 ms;
  12 frames exceed 100 ms. No game reporting implementation is running. The
  packaged engine, empty scene and timing fixture suffice to reproduce it.
  All 2,936 owner files remain unchanged and the run log contains no engine error.
- `screen-reader-query.json`: a separate Python process, without Godot, performs
  4,946 read-only queries over approximately 45 seconds. Six calls exceed 50 ms;
  maximum 385.320 ms, p99 3.778 ms, zero API failures. Slow groups begin around
  10.12, 22.57 and 34.96 seconds. All sampled screen-reader results are false.
  The query can therefore stall independently of game assets and rendering.

The maintained Python tool's one-second smoke run succeeds with 115 calls and
zero API failures. This checks the tool, not intermittent-stall acceptance.
Python compilation and scoped diff whitespace checks pass.

In the exact engine revision, `SceneTree::is_accessibility_enabled()` calls the
screen-reader query before checking the disabled mode. `_flush_accessibility_changes()`
calls that function before its own update-rate throttle. This explains why the
earlier `--accessibility disabled` experiment did not remove the query. See
[SceneTree source](https://github.com/godotengine/godot/blob/ed1daf0bf/scene/main/scene_tree.cpp#L213)
and [Windows implementation](https://github.com/godotengine/godot/blob/ed1daf0bf/platform/windows/display_server_windows.cpp#L3168).
Microsoft documents `0x0046` as the read-only
[SPI_GETSCREENREADER query](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-systemparametersinfoa).

This establishes a concrete main-thread stall source on this PC. It does not yet
explain why Windows delays this query here, attribute every part of the roughly
one-second pause, or prove an equivalent problem on another computer. The native
message-hook stack contains Windows components; no third-party culprit is proven.

## Next action

Follow-up: the same-revision event-cache experiment did **not** remove the full
freeze. Continue from `WINDOWS_QUERY_REMEDY_2026-10-05.md`, including the prepared
administrator-run scheduling trace. The query below remains an observed stall
location, not a sufficient explanation of all long frames.

Use the small reproduction on another Windows machine or a clean Windows session
to distinguish host-specific latency from broader engine behavior. Preserve the
current PC results for comparison. A narrow engine remedy should avoid synchronous
status polling on the gameplay thread while preserving accessibility changes;
an early disabled-mode return alone would only help users who explicitly selected
that mode. Do not ship a forced-disable workaround or accept an untested custom
engine build. Prepare any upstream report for review before sending it.

Continue investigating GPU submission stalls and texture memory independently.
After a justified remedy, repeat matched packaged workloads. Current frame,
texture, endurance and Mac native/signing gates still block release.
