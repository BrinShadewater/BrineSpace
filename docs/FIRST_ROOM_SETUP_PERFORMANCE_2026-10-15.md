# First-time ordinary-room capture setup — October 15, 2026

The private distant-room prototype now has a tested one-spare capture-viewport
variant. Normal-speed placement falls from 58–60 ms to about 55 ms in both orders.
Idle remains about 50 FPS. This is a placement-peak improvement in the private QA
prototype; no production runtime, renderer, art, animation, export or quality setting
was changed. The existing distant-room prototype still needs separate acceptance
before shipping.

## Change and measured cause

The reference is the latest frozen animated-water candidate, including accepted
Moonbay prefix retention and Bill navigation lookup reuse. Nineteen overlay files
and the release runtime were frozen together in `C:/bs-first-room-setup-20261015/`.
Only `candidate-room_content_canvas.gd` differs from that reference. Normal source
`scripts/room_content_canvas.gd` has no private raster LOD and remains untouched.

The detailed release trace isolates placement-frame work. Ordinary slot creation
takes 53/60 microseconds at 1×/4×; triangle assembly takes 220/155 microseconds.
Creating the ordinary-room capture viewport/World2D/painter takes 2.586/3.402 ms.
These are nested scopes; they must not be added to their enclosing submission or
frame times. Instrumented whole-frame timings are diagnostic, not the FPS result.

The candidate keeps one empty, hidden, UPDATE_DISABLED capture surface per content
layer. Acquisition reparents it to the room and binds its painter owner. The
existing continuation still snapshots state, sets bounds/transform, clones the
ordered draw slots, requests UPDATE_ONCE, and uses the original readiness ticket.
No captured image or room data is recycled. A cold miss takes the original
synchronous allocation path. A process callback prepares one replacement on a
later frame and then disables itself. Scene release frees the pool and spare.
This covers the existing eight eligible ordinary room types; large-room capture
allocation is a separate path.

Instrumented acquisition falls to 0.062/0.049 ms; submission falls from
3.311/4.425 to 0.808/0.920 ms. Replacement allocation takes 4.361/3.761 ms on the
following frame: allocation is moved, not eliminated. Snapshot, classification,
capture admission, filtering and invalidation rules are unchanged.

## Uninstrumented release benchmark

Four serial processes, reference → candidate → candidate → reference, actual
Godot 4.7.2 release mode, OpenGL Compatibility, RTX 4070 Ti, 1920×1080. Mixed large
station, 180 warm frames, 120 measured frames per idle/zoom/placement/demolition
phase at 1× and 4×. Total 3,840 frames; all sixteen paired gameplay states, camera
endpoints and camera paths match exactly. The process guard has 337 samples, no
foreign Godot or duplicate game, no errors, maximum sample gap 0.637 seconds.

| Placement action frame | Reference | Candidate | Reduction |
| --- | ---: | ---: | ---: |
| Normal, forward order | 58.281 ms | 54.762 ms | 3.519 ms |
| Normal, reverse order | 60.397 ms | 54.974 ms | 5.423 ms |
| 4×, forward order | 76.972 ms | 70.176 ms | 6.796 ms |
| 4×, reverse order | 71.503 ms | 71.231 ms | 0.272 ms |

Normal placement has zero sampled atlas uploads in all four runs. At 4×, sampled
upload calls take 12.527→10.813 ms forward and 10.410→11.173 ms reverse; the full
4× frame difference cannot be attributed entirely to viewport preparation.

The immediately following frame increases from 22.315→26.821 ms and
22.479→25.211 ms at normal speed, and 24.386→25.393 / 24.536→26.792 ms at 4×.
No following sixty-frame window contains a frame above 50 ms in either lane.
Including placement, each sixty-one-frame window still has one frame above 50 ms;
its maximum is the placement frame shown above. All four window means improve,
but window p95 improves in only two of four pairs. This does not establish smooth
60 FPS or eliminate placement hitches.

Pooled normal idle is 19.9668→19.8953 ms, **50.08→50.26 FPS**, essentially flat;
p95 worsens 22.390→22.932 ms. Across all measured workloads, 44.29→44.44 FPS.
Forward whole-run mean is 22.6073→22.4715 ms; reverse 22.5456→22.5326 ms.
Whole-run p95 improves forward and worsens reverse; 0/16 candidate phases meet
both mean and p95 ≤16.667 ms. No material sustained FPS gain is claimed.

Other hitches remain. Normal demolition is 64.036→64.261 ms forward and
62.299→60.401 ms reverse. At 4× it worsens 71.891→76.139 and 71.758→72.224 ms.
The forward placement-phase maximum, 87.224→81.617 ms, occurs before the actual
placement action. Phase maxima must not be described as the action's timing.

Both orders retain the same 27 ordinary captured-room images at placement phase
end, plus exactly one candidate pool/spare. Warm takes reach 26 at normal placement
and 27 at 4×. Peak engine texture memory is 2,776.859→2,777.984 MiB, an additional
1.125 MiB in both orders. This counter is not total GPU/process memory, and the
short run is not an endurance leak test.

## Correctness and limits

- Native ownership/lifecycle/burst contract: 83 checks, zero failures. Warm reuse,
  simultaneous cold fallback, empty snapshots/slots, disabled capture, one-spare
  bound, reparenting and scene release are exercised.
- Actual-release private LOD contract: 30 checks, zero failures. Active James
  enters/leaves a room; occupied/fire interiors match full rendering. Fire/water
  fallbacks, geometry, flip, texture identity, slot kind/order/tail, operation,
  Reduced Motion, deep in-place mutation and one-capture-per-frame guards pass.
- Frozen station: twelve exact cross-process RGBA pairs and twelve exact repeat
  pairs, three zooms, interior lighting on/off, equal state/camera/visual sidecars.
  Fitted and close station images visually reviewed without a new visible defect.
- First-placement transition: five additional exact cross-process RGBA pairs,
  equal state/camera/readiness. Both lanes draw live slots with active=false,
  ready=false on the first rendered frame, then activate one completed capture
  on the next frame. Frames two through four retain identical pixels. No new
  blank frame or change in capture readiness was observed.
- Independent review found no actionable issue for current parented-canvas callers.
  The helper does not promise detached-canvas support. Crew, doors and warning
  paths retain their original ownership and live drawing.

Early setup attempts are excluded from acceptance: the expected red contract
fails without acquisition support; the first green attempt logged a missing-meta
error, corrected with has_meta; an older release fixture moved inactive Bill
instead of current active James and lacked its original scene freeze; a burst
assertion incorrectly expected the cold helper to hide the image before its
existing caller does so. Corrected accepted checks have no engine errors. No
production change was made to satisfy those stale fixture assumptions.

Every Godot job uses scratch APPDATA and fingerprints the owner's real profile.
Twenty-one saved owner guards preserve all 2,948 non-log files. Immutable overlay
identities are retained alongside the logs. Reference pack SHA-256 is
`f4d621425919e9a1d2685448a2a56823560fb4178587009035a2811d9b28c7b7`;
candidate is `4fa116fd6cb826268eda25754d70ab0c3347ddb47e79a4ee88315170d62f03ed`.
Candidate content source SHA-256 is
`bd3517eb52629f8989b95158be26df49434379836f030be5b6451301a0c789c0`.
These frozen Windows QA results do not certify a current-roster packaged
Windows or Mac early-access release, or all appearance states of the private LOD.

Evidence: `C:/bs-first-room-setup-20261015/`: `ab1-analysis.json`, four run JSONs,
source/PCK identity and owner guards, `trace1-placement.json`,
`trace2-placement.json`, `visual-parity.json`, `release-contract2.json`, native
logs and `first-paint-parity.json`. Reproduction helpers live in
`output/first-room-setup-20261015/`.

Next: retain this as a private placement-pacing variant. The larger remaining
costs are placement/topology/navigation and atlas/exterior drawing; profile those
against this frozen candidate before another change. Do not rerun this unchanged
series to seek a favourable FPS number.
