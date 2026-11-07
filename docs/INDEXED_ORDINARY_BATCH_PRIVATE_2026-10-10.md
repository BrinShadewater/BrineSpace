# Project handoff — ordered ordinary commands in private drone provider

Updated: October 10, 2026 · BrineSpace · PC/Mac performance readiness

## Objective and acceptance
Keep measured indexed+prewarm memory/stall benefits while reducing extra renderer cost.
Accept only matching behavior/pixels and matched performance evidence. Previous turn
made progress by correcting/validating camera framing and action isolation. This turn
improves the PRIVATE candidate; ordinary game and final delivery remain unchanged.

## Accepted decisions and constraints
Current source overlays, corrected fitted camera, explicit zoom. Native debug=false
Windows/RTX4070Ti/1080p, muted secondary window, guarded scratch APPDATA, owner fingerprints,
20GiB refusal floor. No full release copies, asset re-encoding/deletion, source installation.

## Current state
Private group timing probe found about99slot draw callbacks per frame in final4xlighting
interval. Between phase snapshots:9,432slot draws/27,925us;9,432take-slot calls/10,559us;
3,874texture choices/5,806us;475end-update calls/12,464us including475trims/8,025us.
Interval includes90measured plus roughly5camera-settle frames. Instrument recording adds
cost; these are approximate attribution, not additive critical-path CPU times.

New private group batches consecutive ordinary textures/shapes into an ordered command
array in one canvas slot. Each palette-controlled texture remains a dedicated slot and
breaks the ordinary run. No sorting, altered transforms, new atlas geometry, reduced
frames/effects or changed filtering. Command arrays clear each update and on release.
Unused slots hide/clear; scene-owned pool retains no command history. Motion/prewarm,
asset encodings and all current normal optimizations unchanged.
D:/bs-release-crew-cache-20261009/benchmark-input-isolation/indexed-ordinary-batch-trial/
contains group.gd/resources.json/test.gd; existing20-source resources reused.

## Verification
Native actual release synthetic mixed-command checks:108checks/zero failures,
36exact raw RGBA pairs. Three scales(.613/1/1.6), mirrored/unmirrored, nearest/linear,
ordinary/flood/unsupported-material contexts, parent tint, texture regions/rects, lines,
arcs and twelve blended dust circles interleaved with palette draws. Linear and unsupported
contexts exercise original-texture fallback. Each case uses fewer slots and releases all
batched command references. This is sampling/ordering API acceptance, not all production
art/composition/motion/lifecycle or Mac acceptance.

Preliminary mean26.443->26.112ms; then three alternating actual saved40 pairs,
idle/pan/zoom/lighting at1x/2x/4x,90frames/phase:6,480measured frames.
Reference=unbatched PRIVATE indexed+prewarm, NOT ordinary RGBA game.

| Lane | Mean ms | p95 ms | p99 ms | Max ms | >50/>100 | Peak MiB |
|---|---:|---:|---:|---:|---:|---:|
| Unbatched provider |26.313|43.374|54.768|87.582|57/0|2629.926|
| Batched provider |26.127|42.997|52.936|79.321|48/0|2629.355|

Mean0.71%faster, all three pair means favor batching; p99 improves3.35%, >50count57->48.
Peak difference only0.571MiB; no substantial new memory reduction claim. All36full
matched gameplay snapshots and all camera start/end snapshots exact, including cached
playback. Native guards/logs clean. This supports using batching in further private tests;
no normal provider admission or FPS/PC/Mac release certification.60FPS gates still fail.

All jobs terminal/override restored; four owner guards2,938 files unchanged.265.27MiB
new evidence+scratch/no full PCK copies, C126.91/D78.08GiB free. Timing probe, preliminary,
native and repeated evidence under indexed-group-cost-* and indexed-ordinary-batch-*;
comparison.json and storage-summary.json in indexed-ordinary-batch-repeated.

## Next action
Compare batched indexed+prewarm against CURRENT ordinary RGBA game on saved12/expanded40
with corrected framing and explicit zoom, three runs/candidate. Do not treat this private-
provider comparison or legacy-camera results as that evidence. Verify whole-scene motion,
selected art, fallback/storage ownership, loader declaration preparation and transitions
before installing the provider. Continue other redraw/upload hotspots; all original cold/
warm/hardware/endurance/bug/packaging/nativeM1/signing/notarization gates remain open.
