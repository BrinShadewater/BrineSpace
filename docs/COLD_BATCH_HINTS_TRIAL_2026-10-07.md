# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: first-launch selected-frame predecode

## Objective and acceptance

Reduce fresh-profile loading without loading discarded animation candidates, changing pixels/metadata/filtering/timing or increasing retained resources. Original complete PC/Mac/frame/memory/bug/endurance gates remain open. Single local sample is not loading certification or normal checkout admission.

## Accepted decisions and constraints

Private frozen image_prefetch.gd and crew_texture_batch.gd only. Sources before patch retained in cold-hints-source-before; patch hashes in cold-hints-patch.json. Existing32worker window/16MiB recent cache, selected-frame batching, runtime PNG paths and all prior experimental candidate changes retained. Warm recorded scheduling stays authoritative.

ImagePrefetch.hint_order appends deduplicated filenames only on active cold sessions. It queues no whole batch; take schedules the usual bounded lookahead. CrewTextureBatch.finish gathers pending surviving weak frame references, excludes already-live pooled source textures, and hints their existing paths before materializing. No frame references retained by hints, no new mirrored/composited storage policy. Cold partial hints keep indeterminate progress rather than imply a full known total. Additive scalar report fields: hint_calls, hinted_paths, using_previous_order. End clears the same startup path/index/image tables.

## Current state

Native fixed-site9062026 matched pair: first NewGame17,697.666→9,104.073ms; Continue5,595.161→5,593.996ms. Each142checks/clean exit. Native cold4hint calls/12,458paths, all12,458worker hits,32pending peak,11,059,200decoded peak bytes, zero unused. Warm0hints and95,415,252decoded peak/71unused match control. All six retained texture endpoints/sorted library source lists equal. Native is development evidence, not package acceptance.

Selection fixture19checks native and19actual debug=false passes with zero errors/leaks/warnings. Covers inactive retention, deduplicated lazy queuing, cold indeterminate progress, exact source pixels/independent returned images, warm order preservation, discarded weak frames, already-live source reuse, effective filtering, independent alpha-bound metadata and worker/storage release. This is narrow selection/pixel coverage, not every selected character frame/composition or motion acceptance.

Maintained export produces cold-hints-release/BrineSpace.exe and adjacent PCK under output/drone-compiled-2026-10-07. Build81365a7987632800, source SHA25681365a7987632800fe6e593c97c997def83c47d4bb2ff8a35650189c861dcd36. EXE109,283,328bytes/PCK3,646,718,023bytes. Broad outside-checkout audit36,288checked/55remaps/zero missing/changed/unexpected.

Actual debug=false fixed-site pair compares WINDOW32 baseline814e13b9914ed90a with81365a7987632800 using identical unprepared lifecycle fixtures. NewGame12,457.532→7,648.676ms (~38.6% faster); Continue4,932.296→5,118.747ms. Maximum loading draw gaps310.646→312.948ms and237.129→210.089ms. This reaches the10s fresh-profile time target in one small local workload, with fixture typing skip and uncontrolled OS cache. Continue is a different saved state, not a same-scene warm-load certificate. Required three runs,12/40rooms, responsive input/resize and target hardware remain.

Packaged cold4hints/12,458worker hits,32pending,11,427,840decoded peak (~10.9MiB), zero unused; no unused candidate frames were queued in this observed case. Warm0hints, same95,415,252peak/49pending/71unused/12,726submissions as control. Sorted library sources match at all six checked labels. Retained texture deltas0 at NewGame/game0/title states and−4bytes at two Continue labels; no cause established or full allocation-identity claim. No GPU-memory gate improvement claimed. Candidate NewGame capture inspected; full selected-frame native composition/motion checks remain.

## Verification and cleanup

Four lifecycle processes142checks each,19selection checks per native/release; all clean. Export/audit/test profiles isolated; owner fingerprints2,936 files unchanged. All handles terminal, temporary native override removed. Normal gameplay source unchanged; frozen trial retains hinted source for follow-up.

Space management: SHA256/recorded-identity verified obsolete qa-startup-prefetch PCK removed after identical retained17e0b0c package confirmed (3,646,716,489bytes reclaimed). Another WinError112 during new QA copying left only its EXE. Verified qa-helper and qa-normal-control PCKs against retained helper/current-release packages, removed these duplicates plus the partial EXE/empty QA directory, then recreated QA successfully (7,379,005,838bytes). No recursive deletion/running process/source/art/save/evidence removal. Those obsolete QA copies require reconstruction before reuse. Records: old-startup-qa-retired.json, cold-hints-qa-duplicate-cleanup.json and native PowerShell scripts.

Evidence: native-cold-hints comparison/resources JSON and per-lane logs; cold-hints-selection results/owner JSON; cold-hints export/audit/expected manifest; cold-hints-selection-release results; cold-hints-packaged-comparison/resources and per-lane session/gap/capture files; QA fixture identity. Source/UIDs and retained packages remain available.

## Next action

Repeat actual packaged fresh loading with identical accepted inputs and3runs; expand restored12/40-room cases, input/pause/resize ownership and observable retained-layer readiness beyond the provisional three frames. Add permanent selected-frame/metadata/filtering/early mirror/failed equipment coverage before normal source admission; preserve Bill historical bindings. Keep sustained frame/memory optimization, drone admission, original bug closure/endurance and actual PC/Mac certification active. No upload or release gate closure.
