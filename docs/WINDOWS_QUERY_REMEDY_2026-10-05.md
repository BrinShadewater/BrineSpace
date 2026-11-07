# Windows status-query remedy research

Updated: October 5, 2026 · BrineSpace PC/Mac readiness

## Objective and acceptance

Remove recurring Windows gameplay freezes while retaining screen-reader support,
Narrator detection, selected visuals and player preferences. Keep the accepted
Windows/Mac candidates immutable. A native prototype is not game acceptance.

## Accepted decisions and constraints

Investigate a targeted patch to the same Godot revision
`ed1daf0bf001b61586d9930840f2f1394092c079`, rather than upgrading the engine or
forcing accessibility off. Keep any custom engine experimental until matched
gameplay and accessibility validation passes. No public report or upload.

## Research and controlled results

The exact revision queries screen-reader status synchronously before its
accessibility-mode check and update throttle. A targeted upstream issue search
found the original AccessKit implementation but no verified ready-made remedy.
Microsoft documents settings-change notifications for refreshing cached system
settings, and separately warns that Narrator does not set the screen-reader SPI
flag. An event-driven cache must retain Godot's Narrator mutex fallback.

- [Exact SceneTree implementation](https://github.com/godotengine/godot/blob/ed1daf0bf/scene/main/scene_tree.cpp#L213)
- [Windows settings-change contract](https://learn.microsoft.com/en-us/windows/win32/winmsg/wm-settingchange)
- [Screen-reader flag and Narrator limitation](https://learn.microsoft.com/en-us/windows/win32/winauto/screen-reader-parameter)
- [Godot Windows build instructions](https://docs.godotengine.org/en/4.7/engine_details/development/compiling/compiling_for_windows.html)

A small MSVC Win32 program isolates the query from Godot and game content. Each
initial mode runs 45 seconds with the same window/pump and an 8 ms Sleep request.
Windows timer granularity makes ordinary frames approximately 16 ms; these figures
are diagnostic comparisons, not rendering benchmarks.

| Mode | Maximum frame | Maximum query | Maximum message pump |
|---|---:|---:|---:|
| Window only | 47.043 ms | None | 32.489 ms |
| Main-thread query each iteration | 422.696 ms | 400.245 ms | 36.299 ms |
| Background query every ~500 ms | 140.136 ms | 77.513 ms on worker | 124.659 ms |
| Initial query, then event-based refresh; live Narrator check | 46.850 ms | 0.237 ms Narrator check | 32.349 ms |

The periodic worker alone still exceeds the 100 ms limit and is not accepted as
a complete remedy. The event-based run receives no settings-change messages, so
it only establishes steady-state behavior. A separate functional run services
eight explicit local refresh requests and exits cleanly, with zero API failures.
It overlaps compilation and must not be used for performance acceptance. These
tests do not certify real screen-reader start/stop or notification delivery.

Wait-chain sampling during another slow synchronous-query run returns only the
sampled thread, without an external owner. This does not identify another app or
prove there is no wait: Windows documents that unsupported synchronization can
also return one node. [Wait-chain API behavior](https://learn.microsoft.com/en-us/windows/win32/api/wct/nf-wct-getthreadwaitchain).

## Current state

Evidence and reproducible helper sources:
`output/windows-query-remedy-2026-10-05/`. The two-file experimental engine patch
is `windows-screen-reader-cache.patch`, with before/after hashes in
`patch-hashes.json`. It initializes the SPI cache before gameplay, coalesces
WM_SETTINGCHANGE refresh requests through an event, refreshes on an owned worker,
retains the last known setting on a failed refresh and preserves the existing
Narrator check. Worker setup failure falls back to the existing synchronous path.
Thread cleanup and accessibility transitions require runtime validation.

Both experimental engines compiled successfully. Both local builds use
the same MSVC options and AccessKit 0.22.3, with debug symbols and a release target.
They enable the game's OpenGL backend; D3D12, ANGLE and Vulkan are excluded from
these diagnostic builds. This is not full release-template compatibility.
Source/archive and dependency hashes are recorded. No shipped runtime is changed.

## Verification and next action

Native control builds and executions pass; the initial Windows min/max macro
compile error was corrected before any control run. The unchanged build takes
8 minutes 33 seconds; the incremental patched build takes 15 seconds.

**The cache patch is rejected as a complete freeze remedy.** Matched 90-second
empty-scene runs with actual release targets and identical packaged assets show:

| Engine | p95 | p99 | Maximum | Frames over 100 ms |
|---|---:|---:|---:|---:|
| Unchanged local build | 8.453 ms | 8.897 ms | 988.599 ms | 8 |
| Patched local build | 8.487 ms | 8.948 ms | 901.539 ms | 10 |

Both owner checks retain all 2,936 files unchanged. The planned larger benchmark
matrix is not run for this rejected remedy. A slow status query is a real observed
stall location, but removing repeated polling does not remove the full freeze.

Additional native controls narrow the remaining path: a per-monitor-DPI-aware
window alone reaches 61.691 ms; adding OpenGL context creation, clearing and buffer
swaps reaches 392.728 ms without Godot or status queries. This rendering control
uses legacy WGL and is not a pixel/rendering equivalence test for the game. Further
native stack capture of the patched engine resolves the remaining waits to
`DisplayServerWindows::process_events` calling `PeekMessageW`, with instruction
pointers in `NtUserPeekMessage`/`NtUserMessageCall`. Six correlated captures fall
inside 415–915 ms frames; suspension overhead is 0.452–2.109 ms. An earlier
symbol-loading capture suspends for 217.781 ms and is excluded from causal timing
evidence. The probe's 50 ms message timeout itself takes 216–708 ms in these
conditions, so it is a detection aid, not a hard deadline or performance test.
All 2,936 owner files remain unchanged in both comparisons and the diagnostic run.

**Next required evidence is a CPU/GPU scheduling trace.** WPR can list the relevant
profiles, but starting them fails with `0xc5585011` (cannot enable the performance
profiling policy). A follow-up status confirms no recording is active. The current
process is not elevated. There was no attempt to bypass this restriction or stop
another recording.

Prepared local launcher:
`output/windows-query-remedy-2026-10-05/capture-stall-trace.cmd`.
Right-click it in File Explorer and choose **Run as administrator**. Its Python
helper checks for an idle recorder, verifies QA executable/PCK hashes, runs the
unchanged empty-scene reproduction for 90 seconds in scratch APPDATA, stops and
saves its own trace, and fingerprints owner data before/after. The trace remains
local. Preflight finds all required inputs and 61.7 GiB free; Python compilation
passes. Actual elevated capture and trace analysis are not yet performed.

The record will be under `kernel-trace-<timestamp>/brinespace-stall.etl` in that
same evidence directory, alongside PID, symbols location, frame timings and
profile checks. Analyze Windows message-pump scheduling and graphics submission
around correlated long frames before accepting another remedy. Do not repeat the
large game benchmark matrix merely to reconfirm this failed cache candidate.

Use isolated profiles and fingerprint owner data for every Godot run. Verify
real screen-reader transitions and exit during refresh before accepting a remedy.
GPU submission stalls, texture storage, native Mac testing and the other release
gates remain open independently.
