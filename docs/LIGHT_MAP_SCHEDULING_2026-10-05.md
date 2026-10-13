# Light-map update scheduling

Updated: October 5, 2026 · BrineSpace · R7

## Objective and acceptance

Avoid rendering unchanged light-map contents while preserving the current map,
lighting transitions, view transforms and explicit effects choices.

## Accepted decisions and constraints

Enabled by default. `--reference-light-map` restores continuous viewport updates.
Schedule UPDATE_ONCE when existing content signature, viewport dimensions or scroll
offset changes. Do not disable a still-pending update on unchanged process calls.
Low effects quality disables the viewport and invalidates scheduling state; re-enable
requests a fresh render. Existing light-content signature and quantization remain.
No automatic quality changes, texture reductions or animation changes.

## Current state

Changed `rooms/whole-room/room_lighting.gd`; existing UID retained. Added native
`tests/test_light_map_scheduling.gd` and UID, registered in performance diagnostics.
The scheduling state is metadata on the scene-owned overlay; no permanent cache.
Evidence, frozen reference source and runner: `output/light-map-scheduling-2026-10-05/`.

## Verification

**73 new checks pass**, with actual station lighting required in every image:
18 byte-exact scheduled/reference comparisons and retained-map checks across zoom,
scroll, fades, blackout pulses, reduced motion, equipment, moving crew lamp,
effects re-enable and resize. Existing native light-map alignment and crew-lamp
tests pass against the enabled default. These tests do not certify OS focus,
minimize/restore, Mac Retina or packaged gameplay; those release gates remain open.

Three alternating stationary reference/candidate measurements, 60 frames each:
total render draw calls **1,372→1,370**. The continuously rendered map's median
reported cost was ~0.078 ms GPU / 0.112 ms CPU in this small paused fixture. This
is a small avoided pass, not an overall frame-time or minimum-hardware improvement.
Active moving lights, camera changes and blackouts still request map updates.

Important measurement correction: per-viewport counters/timestamps retain their
last rendered values; scheduled readings are stale, not fresh GPU work. Likewise
the SubViewport property can retain UPDATE_ONCE after the rendering server consumes
it. Do not interpret that property as proof of continuous rendering. The native
global draw-call comparison confirms the avoided pass. Engine mechanism checked
against primary [SubViewport source](https://github.com/godotengine/godot/blob/4.5/scene/main/viewport.cpp)
and [rendering viewport source](https://github.com/godotengine/godot/blob/4.5/servers/rendering/renderer_viewport.cpp).
These source references explain API behavior; local results use Godot 4.7.2.

Initial fixture errors were corrected: missing metadata needs a non-null default,
and camera placement/image-content checks must prevent all-white false acceptance.
The initial UPDATE_DISABLED property assertion also did not reflect server behavior.
Final test logs have zero engine errors. Guarded new fixture and scratch APPDATA
for existing suites; all run groups confirm **2,936 owner non-log files unchanged**.
Scoped whitespace/test-index validation passes. No exports, commits or uploads.

## Next action

R8: profile live props whose selected output is unchanged under inactive machinery
or Reduced Motion, preserving shader updates and continuous effects. Keep the
full-roster memory remedy and unresolved long stalls visible; viewport scheduling
does not resolve either. Include R7 in full moving station, focus/window, endurance
and packaged PC/Mac acceptance rather than extrapolating the stationary fixture.
