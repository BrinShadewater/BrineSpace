# Project handoff

Updated: October 6, 2026 · BrineSpace · Current-source station and actual exterior comparison

## Objective and acceptance
Validate the private drone storage provider against current source and actual
surrounding exterior art before admission. Performance/release goal remains open.

## Accepted decisions and constraints
Normal game/art/settings unchanged. Every native run isolated; all 2,936 owner
non-log files unchanged. No export, normal admission or published requirements.

## Current state
`output/drone-coordinate-2026-10-06/prepare-current-station.py` rebuilds physical
Main/Grid from current UTF-8 source. Explicit narrow private crew/player/bank/router
and drone emitter substitutions preserve current animation selection/load order.
Removes global class_name from private Grid to avoid redefining normal GridCanvas.
Other supporting private crew/benchmark files retain their recorded revisions.
Normal source fingerprints and private source hashes retained in `station-current/`.
This is a current-source development fixture, not the frozen release inputs/PCK.

## Verification
First preparation failed on global class declaration position in private copy.
Only the verified failing fixture process was stopped. Failed log/owner fingerprint
preserved; diagnostic check identified class_name conflict and copy was corrected.
Both subsequent 40-room native runs finished cleanly without engine errors or
SafeImage failures. Six crew/drone snapshot comparisons equal, equal warm-up count.

Same workload as earlier experiment: 1080p, 180 warm-up frames, 60 frames each
idle/pan at 1/2/4x, VSync disabled, Godot 4.7.2 Compatibility / RTX 4070 Ti.
Memory deltas remain first four phases 0 MiB, South mining -91.817 MiB,
final +0.058 MiB. End 3168.333/3168.391 MiB; both above 3072 MiB budget.
Baseline p95 39.251–50.419 ms; candidate 38.858–53.937 ms. No FPS gain established.
Ready 12.692/12.598 s; one uncontrolled loading pair, no cold/warm certification.

Two additional native actual-exterior tests: eight exact raster comparisons total,
zero failures/errors, clean exits. Original redraw-repeat controls also exact.
Current Grid EnvPass drawing in offscreen viewport with frozen actual 40-room Main:
overlapping South mining and loaded driving actor, actual dust/harvest art, admin
grid on/off, inherited nearest/linear. Extended fixture adds actual half-complete
solar construction and an active scanning survey room. Indexed and fallback paths
both exercised. Native viewport output visually inspected; actual construction,
survey and surrounding deposits/grid are present. Forced test actors/orders are
post-measurement fixtures and never applied to normal gameplay or owner layouts.

This establishes complete exterior-pass composition at the tested frozen state,
not every heading/frame/scale, scrap fade, full station-floor/crew occlusion, motion,
scene lifetime, zoom workload or all effects settings. Existing 120 exact drone
transform/material pairs and lifecycle checks retain their earlier scope.
Current full-window screenshot inspected: normal UI punctuation restored; discovery
notification still overlays station. No whole-window pixel-equivalence claim.

## Next action
Measure current native frame hot spots and preparation/upload costs with complete
CPU attribution before adding more rendering structure. This experiment improves
one atlas's active residency but does not solve gameplay pacing or memory budgets.
Extend measured lossless storage only where it gives net benefit; retain original
filter/material handling, resource identity and current visual quality. Actual
scene transitions/zoom/lighting/other atlases, three-run benchmarks, release asset
encoding/hash audits, packaged Windows/Mac and full release gates remain open.
