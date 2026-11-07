# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: verify circle batch reachability and crew transfer costs

## Objective and acceptance

Continue full PC/Mac performance readiness. Require actual workload execution and matched evidence before admitting a drawing optimization. Preserve default art/clock/settings/layout/save behaviour; no publication or normal source admission in this pass.

## Current state and decisions

Floor bolt batching was rejected before implementation: current `draw_floor` calls `_draw_material` only for `wet`; the steel/technical bolt branch has no other callers in scripts/rooms/tests. Frozen release and current floor/library source file hashes agree. Do not revive an intentionally unused visual path to demonstrate an optimization.

Private radar prototype caches three blip circles' geometry per Prepared screen and updates only float colour arrays. Native120checks pass:60 exact raster pairs plus60 geometry-retention checks, varied time/scale/rotation/modulation and Reduced Motion. Actual40-room9phase matched pair reports candidate module available but radar builds/batches0 throughout, with no meaningful draw reduction. Reject it as a workload performance fix; runtime timings are not a gain caused by an unexercised branch. Candidate root module availability alone does not prove every renderer's preload references that same module instance.

Private specimen prototype caches three glow-ring geometries and one origin-centred mote circle per painter/area. Native Transform2D identity translations produce drifting mote positions; ordered triangles and float colours retain original nine-circle drawing order. Native120checks pass, geometry builds3/batches63 across60 pixel cases plus warmup. Early optional PCK loading precedes Motion/BugReport/fixture preloads, avoiding late library preload ambiguity. Actual40-room candidate counters again builds/batches0, no meaningful draw reduction. Reject as a current workload fix; no further FPS repetitions warranted without proving caller execution. Existing helper experiments remain private; normal scripts/art unchanged.

## Hitch and transfer evidence

Later correction: the private adapter's current-frame drone upload bucket queried
the sampler frame, one after the completed driver. Its zero at idle4x146 does not
exclude coincident drone uploads. Aligned October8 probe confirms229.6875MiB in two
mining atlas uploads at that point. Crew transfer event matching remains separately
indexed; raw evidence below is retained. See
`docs/EXTERIOR_UPLOAD_ATTRIBUTION_AND_ACCOUNTING_2026-10-08.md`.

Specimen control has108.549ms idle4x/frame146 stall; same candidate point89.283ms. Control simulation step3.614ms; wall intervals before render90.070ms, between render signals14.575ms, after render.273ms. Drone upload diagnostics are zero there. These are CPU wall intervals, not GPU attribution; this one>100ms observation remains a release concern, not proof of a reproducible>100ms stall.

New private `crew-transfer-slots.gd` records bounded8192 events: frame/owner/bytes, lossless image-decode interval and texture create/set/update API-call interval. Original slot/lease semantics unchanged; original helper/PCK preserved. Identified actual40-room diagnostic captures all4297 transfers (no truncation), total decode397.786ms and API calls196.253ms including setup/warmup. At ten slowest observed frames70.533–88.048ms, matched sampled-frame crew decoding.188–.355ms and API calls.093–.191ms. Thus measured synchronous decoding/API submission is small in those frames. Deferred backend transfer work, GPU completion and other readbacks are not covered. The earlier idle4x146 stall is not in this probe's ten largest events; do not claim this measures its exact earlier cause.

Collected per-frame ownership and sampled process-frame alignment follow the existing sampler-1 convention. The added diagnostic may perturb timing; no new FPS acceptance or worker/cache optimization justified by these small measured intervals. Next attribution should cover remaining canvas preparation/notifications before `frame_pre_draw`, and separately queued renderer/driver work.

## Additional capture evidence

Bounded retained RenderDoc replay locates eight evenly-spaced samples from188 default polygon draws with192 indices. Post-VS buffers are indexed with66 vertex records; complete buffer reads confirm earlier66-record prefix was complete. Recorded screen bounds include a30×14px shape and several subpixel/tiny shapes. This is a location/geometry lead, not source-function attribution or proof all192-index draws are circles. No GPU timing counters or new live capture. Tool config restored; full capture preserved.

## Safety and evidence

All native/release/controller/runner jobs terminal. Every owner fingerprint2936files unchanged; adapters restored byte-identically, specimen loader also restored byte-identically. Root source unchanged apart from documentation; original private slot router unchanged. Native logs, source/PCK identities, states, scope summaries and owners: `output/renderdoc-tools-2026-10-08/{radar-batch-native,radar-release-trial,specimen-batch-native,specimen-release-trial,crew-transfer-probe}`. Helpers under that same directory; `circle-locations.json` plus initial prefix report retained. Source-generated prototypes use existing Godot MIT attribution in the circle helper. No image edits, archive cleanup, export or upload.

## Next action

Add bounded current-frame draw/system work snapshots to a diagnostic workload at the repeated slow frame locations, using the already validated timing scopes. Confirm the actual source/module/caller producing expensive geometry before another candidate. Keep silt admission and historical two-advance/thirteen-draw discrepancy open; two observer pairs did not reproduce it. Full integration, original nine bug reports, loading/memory/FPS/stutter/endurance and target PC/M1/signing/notarization/delivery requirements remain open; full goal active.
