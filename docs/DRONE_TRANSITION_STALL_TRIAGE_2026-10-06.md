# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: 4x slow-frame investigation

## Objective and acceptance

Explain remaining slow frames from recorded evidence before another optimization. Full PC/Mac smoothness, memory and release requirements remain active.

## Accepted decisions and constraints

Use existing paired native benchmark evidence; no new run is needed for this triage. Preserve animation pixels/timing/root offsets/layering/filtering and runtime PNG compatibility. Do not hide transitions or reduce animation detail. Normal source unchanged this turn.

## Current state

Saved-frame analysis: `output/drone-stall-triage-2026-10-06/saved-frame-summary.json`, from `output/prop-triangle-submission-2026-10-06/normal/station/{reference,candidate}.json`. Inspected current `scripts/drone_animation.gd`, `scripts/drone_dock.gd` and exterior drawing call path.

## Verification

Recorded >50ms frames at4x: reference21/candidate20. Median explicit simulation step4.329/4.301ms; median exterior-actor draw callback8.770/11.118ms, maxima32.348/33.358ms. Largest recorded texture upload13.804/20.892ms. Candidate slowest77.627ms frame has exterior callback33.358ms, simulation4.255ms; another75.622ms frame has exterior32.709ms and simulation4.314ms. These stage intervals overlap broader drawing/process counters; do not sum them or attribute all elapsed time to GPU.

Mining West `mine-west.png` upload metadata:2688×13440RGBA,144,506,880bytes (~137.81MiB),20.892ms upload. Metadata identifies most recent upload, not every upload within the current frame, so a small last upload does not rule out an earlier large upload. Slow adjacent transitions also show large exterior preparation with1×1 transparent effect uploads. Exact decode/wait/invisibility stage durations are not currently collected; do not infer those durations.

Current loading already decodes ordinary atlas requests in WorkerThreadPool and skips a not-yet-ready layer. Completed jobs upload the entire Image through ImageTexture.create_from_image on the drawing/main path. Dock preparation has a4ms scheduling check before work, but cannot cap one upload that itself takes~21ms. This is an observed remaining stall mechanism, not proof of an effect caused by the new triangle renderer: both paired branches show it, and snapshots match.

No new source changes, probes or owner writes; existing isolated run receipts cover the analyzed evidence. No additional performance/FPS acceptance or closure of4xregression from this analysis alone.

## Next action

Prototype bounded GPU residency/upload of exact currently needed drone frame regions rather than entire large sheets. Keep selected PNG decoding, current source coordinates/root offsets and ordered layers; preserve ready/transition behavior, filtering and texture lifetime. Avoid introducing repeated decoding, redundant ordinary/palette caches or uncontrolled prefetch. Validate exact native frames including region-edge sampling, transparent cells, cargo/effects/heading transitions, dock/exterior views, multiple drones and scene shutdown. Measure upload bytes/time, cache residency/churn and matched active4xtransition workloads. Background decode alone does not remove the measured full-image upload cost. Private South palette work remains separately unadmitted; do not assume it solves West/other headings or normal release memory.
