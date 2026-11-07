# Project handoff

Updated: October 6, 2026 · BrineSpace · Ordinary library live drawing context

## Objective and acceptance
Reduce measured live room preparation work while preserving pixels, state,
filtering, layering and runtime behavior. Overall release gates remain open.

## Accepted decisions and constraints
Narrow normal room-content change only; no texture/material merging, batching,
quality cut or animation change. Verified scratch profiles; all 2,936 owner
non-log files unchanged. No export, release certification or goal completion.

## Current state
`scripts/room_content_canvas.gd`: guarded ordinary `library_live` path supplies
a small reusable context containing painter, operating and machine_clock. These
are the current library screen/effect functions' entire room-field contract.
It avoids rebinding/restoring every shared room field. Painter reference clears
after drawing; prop ID normalization still uses an independent shallow copy.

Missing snapshots/cached flip, mirrored layout transforms, custom artwork,
portable views, drone docks and aquariums retain original room-state path.
Registration mirroring still works through original library source-UV functions.
Original live/static redraw counters preserved. Optional additive
simple_library_paints counter collected only with profiling enabled.

Permanent `tests/test_library_live_context.gd` and paired UID, render-perf index.
Oracle embeds original paint implementation; no dependency on disposable output
fixtures. All other item kinds and normal room/editor drawing paths unchanged.

## Verification
Bounded private per-kind profile of actual 40-room fixture: 118 library-live slots,
7080 callbacks per 60-frame phase, 182.7–187.1 ms inclusive (~3.05–3.12 ms/frame).
Only three crew slots; no materials/shaders assigned to visible room slots in this
dry scene. Material merging therefore unsupported as first remedy for this cost.
Profile overhead is diagnostic; no release frame-time claim.

Initial context prototype: 48 exact raster pairs. Expanded counter test exposed
live/static reporting mismatch; failed log/fingerprint retained and corrected.
Final permanent test against actual normal code: 510 checks / 406 exact raster
pairs, zero failures/errors, clean exit. Synthetic radar/trace/bar screens and
all three effect kinds across clocks, operating state, Reduced Motion, inherited
nearest/linear, tint, fractional translation, nonuniform scale, flipped fallback;
179 current station asset registrations in dry and current submersion shader.
Metadata-only registration coverage, no full PNG batch. Shared renderer state
remains unchanged/restored, painter not retained, excluded-case guards and redraw
counters pass. Guard tests verify eligibility, not every special path's pixels.

Matched native 40-room prototype pair, 1080p, 180 warm-up frames, 60 idle/pan
samples at 1/2/4x, Godot 4.7.2 Compatibility / RTX 4070 Ti. All six full crew/drone
snapshots equal; texture end equal 3168.333 MiB; zero errors/missing art, clean
exits. Content callback means 4.151–4.368 ms → 3.081–3.301 ms: paired saving
1.005–1.183 ms. Prototype full workload differs from normal admission only in
helper names and profiling-counter gating; actual normal implementation separately
passes permanent native raster/state test above.

Whole-frame p95/p99 mixed; candidate p95 37.919–49.170 ms still fails 16.7 ms gate.
One pair does not establish aggregate FPS gain. Loading/memory/release acceptance
not established. The frozen experiment uses private compressed crew, distinct
from normal release gameplay.

Evidence: `output/room-slot-profile-2026-10-06/` and
`output/room-live-context-2026-10-06/` (initial/rejected tests, actual-assets,
normal-source, permanent-test and station comparison). Test-index JSON and UID
uniqueness checked. Successful processes all terminal.

Renderer texture/filter behavior consulted in [Godot 4.7.2 GLES3 canvas source](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/drivers/gles3/rasterizer_canvas_gles3.cpp);
this does not prove texture RID changes are this scene's bottleneck.

## Next action
Investigate continuous library screen/effect command generation and floor/wall
rendering with current source and matched animated workloads. Any geometry or
batching change must preserve exact native output and command order; do not infer
GPU benefit from submitted command count. Broader Studio/lifecycle/zoom/lighting
and packaged Windows/Mac, endurance, memory/loading/performance gates remain open.
