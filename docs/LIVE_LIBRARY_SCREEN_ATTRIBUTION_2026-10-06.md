# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: live library prop painting attribution

## Objective and acceptance

Continue the full PC/Mac performance plan. Identify live prop painting costs after installing the large-room preparation key improvement. Preserve default animation quality and exact output.

## Accepted decisions and constraints

No normal source change this milestone. Keep monitors animated at their existing clocks, movement and simulation speeds; no frame thinning or automatic quality reduction. Attribute cost before introducing a cache or alternate renderer.

## Current state

Private profiling replacement of the current Library script wraps live drawing, station screens, ordinary screens and registered effects. Counts screen categories and effect kinds, accumulating numeric metadata only. Runs through actual normal Main/Grid and the installed large-room key optimization. Original source file remains unchanged. Artifacts: `output/library-live-profile-2026-10-06/`.

## Verification

Native mixed40 six phases complete. All recorded full crew/drone/door/light/power/zoom states match the preceding current-source fixture; no missing art. Owner2,936 files unchanged; process terminal. Timing includes instrumentation overhead and nested totals overlap; not a performance improvement or certification run.

Per frame, approximately146 live prop calls:143 station-screen calls and3 ordinary-screen calls. Active station output is112 bar screens plus41 waveforms (153 screens); no radar or registered specimen/field/hologram effects observed in these workload phases. Station screen drawing totals1.304–1.349ms, ordinary screen drawing0.151–0.159ms, inclusive live drawing1.794–1.857ms. Screen routines are the measured lead; optimizations targeting registered glowing/holographic effects would not address this standard workload.

Station screen drawing repeatedly parses colour and computes screen boxes, widths, aspect categories, inner rectangles and related static geometry, followed by dynamic clock-dependent waveforms/bars. Waveforms generate25 points each;153 screen outputs remain intentional default visuals. Geometry inputs depend on registration, source mirroring, prop rectangle/scale and layout changes, not only the room clock.

## Next action

Private prepared-screen geometry, owned by retained slots and cleared on their existing changed-item path. Preserve exact arithmetic/clock order, colour, mirrors, inheritance and unknown-material fallbacks. Validate actual submit/invalidation behavior, not only manually populated slots, including resized/moved/replaced/hidden props, operating/reduced-motion changes and lifecycle. Then compare matched workloads before admission. Full normal performance/memory/loading, provider admission, packaged bug checks, endurance and actual Windows/Mac certification remain open.
