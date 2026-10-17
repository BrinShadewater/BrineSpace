# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: animated water rendering

## Objective and acceptance

Reduce animated-water CPU with identical appearance; benchmark average FPS and
placement hitches against the latest accepted frozen OpenGL candidate. Completed:
contained CPU reduction accepted, no dependable FPS/hitch or 60 FPS acceptance.

## Accepted decisions and constraints

Preserve animation, water levels, pumping, antialiasing, geometry/order, live crew,
doors/warnings, existing art/quality/OpenGL and owner data. Keep private LOD private.
Serial guarded native jobs and scratch APPDATA required. No export/commit/publication.

## Current state

Installed `scripts/water_stroke_triangles.gd`: prepare exact width/feather scalars
for the three literal water widths once; three static Vector2 values, generic
fallback unchanged. No new textures/buffers/growing cache. Existing paired UID
preserved. Added nearby-width/duplicate/tiny-segment coverage to existing
`tests/test_water_packet_assembly.gd`; UID retained. Status and
[report](ANIMATED_WATER_PERFORMANCE_2026-10-15.md) updated.

Installed-source actual release sweep saves 0.099–0.128 ms / 9.7–15.6% water CPU.
Whole-station normal idle: full series 50.62→50.06 FPS; focused series
50.91→51.14 FPS. Results mixed, no reliable whole-frame gain. Focused placement
normal 57.321/58.268→56.018/57.605 ms; 4× 81.754/78.733→76.778/85.398 ms.
The additional segment-length trial remains private; no established extra benefit.

## Verification

5,760 release frames, both orders at normal/4× across full/focused series, all
24 state/camera/path phase pairs exact. No foreign/duplicate game in 584 guard
samples. Actual Grid→Moonbay→Strokes source/width diagnostic confirms fast path.
720 installed-source release water image pairs exact, both orders/full/pumping;
12 station cross-process plus 12 repeat pairs exact. Installed 21,076 geometry
checks, native 180 stroke pairs, 493 water checks, 597 room pairs, 163 composition
checks: all pass. Water sample/chart visually reviewed. Thirty-three owner guards
preserve all 2,948 files; source/UID/whitespace checks pass. Independent review done.

Artifacts: `C:/bs-animated-water-20261015/`; helpers/chart:
`output/animated-water-20261015/`. Accepted helper SHA256:
`2a24f34f7be650a79c637b40e0c97faec9ec7e532b2b22e92516914dbced5228`.
`admission.json` records prior/helper UID hashes. Release adapter setup failures
are excluded and restored; accepted fixtures complete. No required check remains.

## Next action

Profile first-room canvas/private capture setup or atlas upload bursts. Native
editor timing overstates this saving relative to actual release: use release CPU
micro-measurements and preserve adverse macro results. Do not claim FPS gain from
this component result or admit the private length trial. Mac and real release
packaging still require their separate acceptance when requested.
