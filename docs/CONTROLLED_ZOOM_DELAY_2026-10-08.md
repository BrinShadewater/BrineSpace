# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: controlled zoom-delay semantics.

## Objective and acceptance
Full PC/Mac readiness remains active. Establish whether controlled art waits alter expected camera/culling work without treating a small fixture as packaged acceptance.

## Accepted decisions and constraints
Preserve source art/gameplay/owner data. Controlled native test uses real inherited main._update_camera_zoom, grid.zoom_waits_for_cover, grid._rooms_in and grid._sync_large_room_canvases. Substitute only deterministic readiness, target/coverage state and UI zoom setter; no production patch. Independent fixture clock is not actual crew/needs simulation proof.

## Current state
Private zoom-delay-fixture.gd and run-zoom-delay[-host]-native.py in output/renderdoc-tools-2026-10-08. First50check fixture extended with native room hosts and explicit four-frame count-difference assertions. Results in zoom-delay-native and zoom-delay-host-native; maintained game source/art unchanged.

## Verification
Native30/60/120fps with zero/four-frame readiness delays:50checks first pass; stronger1733checks0failures, clean terminal. Delay holds camera exactly four frames, boundary rooms remain visible, camera reaches same1.0target and independent fixture elapsed clock2seconds. Actual room-host visibility follows complete room membership throughout. Visible-frame counts0/4 at30fps,1/5 at60fps,3/7 at120fps. Actual coverage gate independently holds until groups_left1 then permits movement. Both owners2936files unchanged. No fixed scene-start sleeps; render fences used for teardown only.

This proves expected asynchronous camera holds can change raw visible/draw opportunities while preserving final zoom. Does NOT prove exact historic2/13origin, full simulation speed correctness, real-art motion/joins/pixels, lifetime endurance or FPS gains. Historical issue remains open. Prior same-PCK gate trace showed an extra readiness hold with equal end counters; do not equate that with full attribution. Match future evidence by frame/camera/visibility state, report unequal opportunities explicitly instead of requiring every raw counter equal regardless of workload.

Reviewed existing throughput evidence without rerunning benchmarks: frozen large-room bases1262calls/~2.84ms ablation, environment1230/~2.87ms; overlapping attribution cannot be summed. Normal department_wall_material draws texture regions/rectangles, not the speculative circle hotspot, so no blind circle rewrite there. Silt candidate48pixel cases/threeactual pairs remains private; preserved existing evidence rather than rerunning it. Full original gates open.

## Next action
Return to large-base/live-layer submission attribution and pixel-preserving reuse/batching for actually executed high-cost code. Controlled delay fixture narrows interpretation; keep historical zoom defect separate and require motion/settled visual proof before admitting affected candidates. Do not repeat broad comparisons solely to chase equal counters. Memory/loading integration, original nine bug checks, endurance/save transitions, targetPC/M1 and signing/notarization/frozen packaging remain required.
