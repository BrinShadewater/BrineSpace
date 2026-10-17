# Performance work: orientation and limits

The list below records avenues investigated, not an assertion that every trial
shipped. The **d3 frozen source + manifest/PCK identity** define this candidate.
Historical reports often describe private overlays that were never integrated.
Do not combine FPS numbers from different maps, cameras, actors or builds.

## Latest confirmed changes in this source lineage

**e54 router lifetime cleanup.** Departed canvas registrations retained WeakRef
Objects until station exit. Node removal now clears registry/epoch/callback
records; re-entry registers correctly. Native exact-pixel/reparent/retained-peer
tests passed. The actual e54 Windows 12-room 4× two-hour run had zero expired
router references in 1,441 censuses, settled object/private-memory ranges and two
retained ≥50 ms hitches, none ≥100 ms. This acceptance belongs to e54/Windows.

**d3 Save fingerprint cache.** Capture repeatedly decoded and hashed the same
James cargo animation sources even with an empty active plan. Full two-gear bank:
26 bindings/24 unique frames. CpuFrame now owns one legacy hash plus an exact
compressed-byte/layout validity key, invalidated by replacement or in-place edits.
No decoded Images are retained. The loader prewarms after source adoption so the
first real Save is fast. Mutable/other textures retain fresh hashing; pivot/height,
gear/timing, stage/clock/plan and floor PNG/pixels stay fresh. Same save schema and
legacy digest encoding. Measured key copies: 490,230 bytes plus metadata overhead.

Changes relative to e54 are only `scripts/crew_storage/frame.gd`,
`scripts/james_cargo_checkpoint.gd`, and the prewarm line in
`scripts/grid_canvas.gd`. See `patches/minimal-runtime.patch` and the complete
[Save report](project-docs/SAVE_HITCH_2026-10-16.md). The cache runs in loading and
checkpoint paths; do not call it a general rendering FPS improvement.

## Earlier measured workstreams

| Area | What was investigated | What to preserve/check |
| --- | --- | --- |
| Cards/text | Zero glyph readability, frame layering, angled coloured edges | Retina text/AA, frame overlap and solid lines; preserve accepted design |
| Walls/environment | Retained geometry/batching, exterior passes, topology validation | Sorting, tint, seams, walls/doors/light identity and invalidation |
| Live rooms/surfaces/floors | Redraw work, retained prop/surface/floor submissions, structural batching | No disappearing props, stale power/hazard/water, masking or ordering changes |
| Animated water | Reused geometry/packets and live water handling | Same water appearance, clocks, pause/speed, overlaps and cargo rendering |
| Zoomed-out room images | Expensive-room prototypes and expanded cache reuse | Some private candidates only; crew, doors and warnings stay live; normal detail restores when close |
| Mining drones | Atlas upload pressure, partial/retained uploads, effect storage/material paths | Exact original pixels/filtering/tint, live exterior actors; memory lifetime/fallbacks |
| Crew CPU/navigation | Validation, batched graph construction, companion graph scope, stable-ID/private prototypes, idle regression | Same reachable paths, crew jobs/contacts/doors; no global renumber assumption or behavior change |
| Room placement | First-time setup/prewarming, deferred work, navigation and following-frame pacing | Preserve actual placement order/state; report action frame and following 60 separately |
| Render submission | Canvas/draw-call overhead, static props and structure | Lower draw counts alone do not prove whole-frame or tail improvement |
| Rare pre-render stalls | Scheduler/WPR stacks, interrupts and diagnostic I/O; report repair/longer soak | Root cause remains limited/unresolved; Windows ETW does not transfer to Mac |
| Memory/lifetime | Texture/canvas ownership, source banks, scene exit and long soak | Release counters can be unavailable; engine texture bytes are not physical GPU residency |

The optional source includes the full dated docs archive. Curated entry points are
in [REFERENCES.md](REFERENCES.md). In particular, old October 11 takeover notes and
October 14/15 private LOD/batching reports must not override later October 16
full-source export/validation. Old Windows absolute paths are provenance, not Mac
commands or files guaranteed to be in this kit.

## Renderer decision and rejected shortcuts

The measured Compatibility/OpenGL, ANGLE and Mobile comparison retained OpenGL as
the production default. Faster average FPS alone did not establish equivalent
appearance or better interaction tails. It used an earlier private candidate,
not this full-source d3 export, and cannot certify a Mac backend.

For the first Mac pass keep the shipped settings. Record what backend actually
starts; do not assume a Windows ANGLE option exists on macOS. A subsequent backend
trial must be separately identified, compare identical camera/state and visual
captures, and report zoom/placement/Save p95/p99/max and hitch counts as well as FPS.

No automatic global quality drop, resolution reduction, frozen crew/doors/warnings,
animation-frame removal, blanket disabling of lighting/physics or engine upgrade
is authorized. Do not revive a rejected indexed/material/large-cache experiment
unchanged just because an older mean FPS was better.

## How to choose the next useful target

First close native Mac launch/saves/input/visual/platform blockers. Then measure a
representative normal run and an explicitly labelled large fixture. Split actual
production work from diagnostic readback, tracing, screenshot and report overhead.
Profile the expensive path before editing it; narrow invalidation/ownership fixes
are preferred over speculative architectural rewrites. Retain first-load costs,
rare stalls, rejected runs and scope limits rather than filtering them away.
