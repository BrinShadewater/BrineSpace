# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: shared ordinary/indexed residency policy

## Objective and acceptance

Continue full PC/Mac performance readiness. Attribute retained drone storage and test a combined cache budget without visible-layer eviction, corrupted held references or recurring reload stalls. A memory saving alone does not establish release readiness.

## Accepted decisions and constraints

Private physical provider/scene copies under `output/drone-activity-indexed-2026-10-06/residency/`. Both matched branches use the same twelve-source dock-sharing renderer. Normal source/art unchanged. Do not erase required layers to force a budget pass. Recent working-set excess remains explicit.

## Current state

Private `provider/motion.gd` sorts stale ordinary/indexed lookup entries by last-use frame and releases oldest until combined bookkeeping fits 256MiB, retaining all entries used within32 frames. Draw-command references remain valid after lookup eviction. At most64 small eviction metadata records, no textures in diagnostics. No permanent resource-retaining table. Physical control/candidate Main/Grid scenes and benchmark inspect actual source count, ordinary per-path bytes and both last-use maps. `prepare-residency.py` records current generation; refuses to overwrite existing evidence.

## Verification

- Real-allocation native probe17 checks, zero failures/errors/warnings/leaks. Four64MiB ordinary images plus selected indexed storage exercise actual pressure, cross-cache ordering, recent protection, held pixel/identity survival, exact counters and last-owner release. Owner2,936 unchanged. These tests do not establish gameplay hitch behavior.
- Aggressive two-frame variant: native registered-dock480 exact raster pairs/1,022 checks, zero errors/warnings/leaks; owner unchanged. Matched40 all six recorded crew/world phases equal, no missing art/errors/selected duplicates. Saved61.32MiB at2x,245.04MiB at4x idle; same final texture endpoint. However traced uploads30→35, bytes1,145,343,116→1,289,850,004; extra drive-West, steer-right-West, stop-West and two transparent effects. West stop reused15 process frames later; other sheets189/201 frames later. Aggressive policy unaccepted. Artifacts preserved in `station-results-aggressive`, `motion-aggressive.gd`, aggressive probe/content result files.
- Current32-frame variant: native17-check ownership probe clean. Matched40 all six recorded full crew/drone/door/light/power/zoom states equal, no art/engine errors/selected duplicates; owner2,936 unchanged. Processes terminal. Trace360 frames each; complete upload event metadata, same27 upload frames/30 uploads/1,145,343,116 bytes and identical per-path counts. Observed upload CPU90.871/98.806ms is one pair, not a reduction.
- Current texture endpoints control/candidate MiB: idle1 2300.243/2301.469; pan1 2453.642/2454.868; idle2 2514.892/2454.799; pan2 2515.064/2454.971; idle4 2760.472/2639.160; pan4 2715.226/2747.077. Thus mid-workload savings but final+31.85MiB; no peak/normal-release/aggregate improvement claim.
- Current p95 control/candidate ms: idle1 42.254/45.965; pan1 42.795/43.428; idle2 40.691/43.414; pan2 42.305/42.942; idle4 45.670/44.899; pan4 50.116/49.877. Frame gates remain failed; performance mixed, not admission evidence. Readiness12.138/11.910s, single observation.
- Path evidence attributes ordinary stale retention to idle/start/turn/stop sheets. Candidate releases stale ordinary storage as well as indexed storage, unlike previous indexed-only trim. Global GPU monitor differences also include held commands and other resources; lookup totals are not full residency.

## Next action

Keep both policies experimental. Complete dock flip/native/other-type/reuse/full-room/lifecycle and mode-off fallback acceptance; assess repeatability before admission. Investigate measured steady rendering separately: existing control quiet frame~6,500 draw calls, render CPU~13.3ms/GPU~11.6ms, live preparation~6.46ms and door/light validation~1.63ms (overlapping scopes, do not sum). Target the largest avoidable command/validation work with exact visual checks, rather than claiming cache cleanup reaches60FPS. All original loading/memory/frame/packaged bugs/endurance and Windows/Mac release gates remain open.
