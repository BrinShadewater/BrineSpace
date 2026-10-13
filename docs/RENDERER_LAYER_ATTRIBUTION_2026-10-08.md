# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: attribute renderer layers and restore working disk space

## Objective and acceptance
Continue the complete PC/Mac performance/readiness plan. Identify substantial costs without lowering quality or treating hidden-layer diagnostics as an optimization. No normal gameplay/runtime changes admitted this milestone. Prior frame capture and draw-profiler results remain scoped to their recorded workloads.

## Accepted evidence
Thirteen fresh-process paired, uncaptured, debug=false native render-only experiments completed. Each loads the same deterministic40-room/four-crew candidate and owner-layout scratch copy, waits for observable discovery reveal completion, pauses simulation and disables grid processing, records90 settled frames before and after a single diagnostic ablation. Every initial baseline has5079draw calls, zero unfocused samples, same1549.510909MiB texture counter, exact crew snapshots before/after; logs clean. There are12 large-room canvases, spanning four types, not only four large rooms. Groups overlap; do not sum their deltas. Root whole-grid hiding also removes its children and cannot establish a component cost by subtraction against unrelated active tests.

| Hidden/cleared group | Draw-call delta | Normal → ablated median frame interval |
| --- | ---: | ---: |
| Whole grid | 4848 | 11.901 → 1.066ms |
| Twelve large-room canvases | 1574 | 11.724 → 8.477ms |
| Large-room bases | 1262 | 11.598 → 8.758ms |
| Large-room supporting props | 309 | 11.143 → 10.420ms |
| All environment layers | 1230 | 11.266 → 8.394ms |
| Floors/FloorsRest | 570 | 11.075 → 9.816ms |
| Terrain | 473 | 10.847 → 9.968ms |
| Walls | 427 | 11.105 → 10.243ms |
| Ordinary retained room contents | 387 | 11.215 → 10.180ms |
| Retained seabed still layer | 206 | 11.218 → 10.582ms |
| Non-grid branches | 188 | 10.972 → 11.226ms |
| Grid's own commands, children retained | 148 | 11.027 → 10.923ms |
| Animated water-wave pass | 1 | 11.158 → 11.083ms |

Wave pass removal reduces rendered objects by2820 but only one draw call: this path is already batched. No wave mesh rewrite justified by this result. Non-grid branches include external effects, not solely UI; timing noise means their one-pair delta is not a speed claim.

Frozen renders roughly11ms; prior active workload means31–41ms. This is a change of workload/clock/simulation state, not a matched estimate of simulation cost or a23ms redraw attribution. It motivates separating active processing/redraw from renderer submission. Existing active draw-profiler idle1x means include large_child_base575us, large_child_props420us, large_prop_retained856us, door_light_validation1341us, env_pass_lines978us, env_seabed894us, content_draw2151us, live_rooms5308us, station3422us. Scopes overlap and may nest: do not sum them; base draw-call volume does not mean it dominates script assembly. Engine process maxima are not per-frame CPU cost (earlier timing handoff).

## Diagnostic corrections and verification
The first two single-process multi-ablation runs did not recover the baseline:5079→3636 after visibility changes. The second explicitly failed its restoration gate. Preserve both as failed diagnostic evidence; their later layer deltas are unreliable. Fresh-process fixtures avoid reuse of altered renderer state and eliminate that confound. All13 fresh lanes start at5079, before/after crew equal, no missing art/error/warning logs. No claim that this establishes a production visibility bug.

Evidence `output/renderdoc-tools-2026-10-08/layer-census-{fresh,detail}/`, `layer-census-summary.json`; each group has log, full state result, source/EXE/bootstrap identity and isolated-profile mapping. Owners2936files unchanged in both sweeps; adapters restored byte-identically; runners99989/28450 and all native processes terminal. Earlier runners22519/84996 terminal too. No new visual acceptance: hiding layers is diagnostic only.

## Cleanup and current inputs
Disk fell to~0.52GB during this work; task-owned scratch shader cleanup reclaimed only18,938,400bytes across16 explicitly verified bs-bench-* profiles. Receipt `scratch-shader-cleanup.json`; logs, results, save copies, unique capture and archives retained. Unknown disk growth was not assigned to these caches or cleaned speculatively.

Both full release and QA PCK freshly hashed as `e05e7c0c2d009f83ea1ad93c951eb660bfa19c723f74d01cef06120330b748c8`, each3,623,023,191bytes. Reclaimed only that verified byte-identical QA PCK. Original retained release at `output/crew-release-2026-10-07/release/BrineSpace.pck` is unchanged. Before removal, both private deferred bootstrap loaders were retargeted to the retained path; their identity-with-icon.json files now record its location and actual new loader hashes. Historical identities/results remain historical. Normal source, EXE, frozen inputs, unique packs/art/archives and owner saves untouched.

`output/crew-release-2026-10-07/qa/PACK_RECOVERY.json` names retained source/hash/destination: ordinary QA executable requires copying that retained pack back before use. Current private diagnostic bootstraps load retained bytes directly. Cleanup receipt `duplicate-pack-cleanup.json`. Relocated control actualdebug=false fresh startup clean, budget268435456 guard executed, no SafeImage failures/router released/exit80.055112MiB. This is relocation/startup proof, not the active four-crew/memory/quality gate. Owner2936unchanged/proof process114520 and runner78949 terminal. Disk subsequently~4.16GB free.

## Next action
Use a matched active workload to separate simulation/processing, redraw preparation and retained rendering. The frozen baseline alone is already within16.7ms on this powerful GPU; draw-count reductions alone may not close the active gap. Keep large-room base batching as a measured GPU/backend lead, but avoid rewriting already-batched waves or treating575us base script work as the main CPU cause. Investigate high active live-room/content/door-light costs and preserve output clocks, pixels, layering and all simulation state. Any optimization needs matched uncaptured timing and relevant visual/regression checks. Integrate accepted memory/lifetime improvements into a newly frozen audited candidate afterward. Full target-PC/M1, loading, nine original issues, endurance, signing/notarization and delivery gates remain open.
