# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: bounded drone upload diagnostics and repeated West comparisons

## Objective and acceptance

Identify every drone layer upload contributing to measured stalls, with bounded report overhead and additive fields. Continue original PC/Mac release/performance goals; no release acceptance claimed.

## Accepted decisions and constraints

Normal diagnostics change only; animation/cache/loading behavior remains unchanged. Record logical layer-upload operations, including bytes/time/max/largest payload; keep at most eight metadata events for one upload frame, no textures/images/RIDs. Preserve legacy lifetime counters and last_texture_upload. Current-frame report returns zero when stale; latest_upload_frame explicitly labels its actual process-frame number. Private West factory reports its combined index/palette operation through the same recorder.

## Current state

Changed scripts/drone_animation.gd; tools/release_benchmark.gd adds drone_frame_uploads and drone_latest_upload_frame to hitch/trace records. Existing performance_monitor cache report receives additive diagnostics automatically. New permanent tests/test_drone_upload_diagnostics.gd + unique paired UID, native render-perf index entry. Private West motion and physical benchmark mirror reporting. Evidence output/drone-upload-diagnostics-2026-10-06/ and output/drone-west-station-2026-10-06/{traced-repeat,completed-frame-repeat}/.

## Verification

Native test first fails for missing API, then12checks pass; explicit completed-frame snapshot test added, final13checks/zero failures/cleanexit. Checks all12sameframe uploads despite8eventcap, large payload before tiny last upload, lifetime/timing totals, defensive snapshot copies, readonly cache identity/storage, current-frame reset and independently timestamped previous upload frame. Unique UID and whitespace checks pass. Test registry helper initially used wrong top-level key; corrected lanes entry, no game change.

First traced pair confirms benchmark reads process_frame after the prior frame's draw: current-frame diagnostics correctly zero. Added explicit requested-frame/latest snapshot rather than labelling stale data current. Final actual trace captures32uploadframes/38logical uploads per branch, every captured event list complete; bytes/time sums verified, upload frame equals captured process_frame-1. No GPU readbacks or unbounded event history introduced; no quantitative reporting-overhead reduction claim.

Across three private matched mixed40-room pairs, all18phase fullcrew/drone/door/light/power/zoom snapshots equal; zero engine/missing-art errors. Third order reversed (candidate first); instrumentation evolved between pairs, so these are local prototype repeatability comparisons, not three identical packaged release candidates. Owner2936files unchanged for every run; all processes terminal.

West indexed uploads6.233/8.115/6.468ms; third original15.540ms vscandidate6.468ms. 4xidle p95 improves in allthree pairs72.474→61.165,63.504→58.178,62.521→61.656ms; pan mixed58.007→59.119,57.603→58.176,59.361→57.001ms. No universalFPS gain or normal source admission. Cache remains duplicate-free forWest and evicts afteruse. Fullframe gates still fail.

## New measured lead

Candidate third pair79.355ms frame/process531 has fouruploads in process530 totalling241647616bytes(~230.45MiB)/25.660ms: mine-south-effects144506880bytes/12.926ms, start-north48168960/5.270ms, wheel-layer-north48168960/7.213ms, northcargo802816/.251ms. Another69.991ms frame has Westeffects144506880/17.200ms +steer-right-west48168960/5.599ms. Southeffects and Southbody each upload again later in the same workload; cache churn is observed, not inferred from the last-event metadata. These are upload-call intervals within overall frames, not an additive complete CPU/GPU decomposition.

## Next action

Prioritize exact lossless storage for both measured mining effects sheets and repeated South body; inspect color/alpha counts and nonempty-cell coverage before choosing indexed representation. Preserve current full coordinates/hardware sampler, unknown-material/linear fallbacks and original clocks/layers; validate complete native frames. Track all related resources under shared pressure so reducing one atlas does not create duplicated caches or repeated decoding. Measure current-station upload aggregates and actual memory/wholeframe costs before admitting the rendering provider. Normal texture budget, loading, packaged bug checks/endurance and PC/Mac certification remain required.
