# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: navigation prefix reuse accepted in source

## Objective and acceptance

Continue the complete PC/Mac performance/release plan. Install measured construction
navigation savings with identical graphs, routes, save behavior and selected visuals.
This is a targeted improvement; large-map smoothness/release gates remain failed.

## Accepted decisions and constraints

Each actor owns its graph and retained metadata. Reuse only the unchanged leading
ordered room cells with identical geometry keys, layout revision and template point
counts. Remove old boundary connections and changed suffix; reset disabled flags;
assemble suffix and reconnect all boundaries in original order. Staged loading clears
old graph/keys immediately and retains full assembly/yield/supersession behavior.
No shared mutable graphs, art changes, simulation changes or quality reduction.

## Current state

Installed into `scripts/bill_npc.gd`; existing paired UID preserved. Removed only
private equivalence-check branch/function and its absolute external reference path
from the tested V2 candidate. Runtime reuse algorithm is unchanged. New maintained
`tests/test_navigation_prefix.gd`/UID `uid://b5xc3j2lhho4w`, registered beside existing
navigation room-owner coverage in `tests/index.json`. Original source backup and
private/installed hashes retained in `prefix-normal-install/source-identity.json`.
Source SHA256 `16d820f5d86ac4c06f705fc3f9521b42e17d35a680121f9aa1fcf697243a068a`.
Frozen PC/Mac packages unchanged; no export, commit, upload or itch visibility action.

## Verification

Final V2 comparison uses actual original navigation source as reference, not a disabled
prototype. Both carry identical timing wrappers and accepted current preparation,
galley and shadow overlays. No expensive graph verification in measured runs.
Actual debug=false Windows executable/RTX4070Ti/1080p, muted secondary display,
isolated saved12/copied owner layouts and deterministic40 extension. Three pairs each,
alternating order:12runs/12,960frames, all36paired phase-end gameplay states equal.
Scripted selection/direct connected placement/demolition at1x/2x/4x; physical input,
construction-queue acceptance and target1650/M1 certification remain separate.

| Metric | Reported12 reference / reuse | Large40 reference / reuse |
| --- | --- | --- |
| Combined actor rebuild mean |12.018 /11.381ms|38.261 /25.573ms|
| Construction/demolition frame mean |55.863 /53.993ms|125.802 /112.698ms|
| All-frame mean |14.759 /14.768ms|27.554 /27.499ms|
| P95 |16.542 /16.379ms|37.846 /37.499ms|
| P99 |22.497 /22.709ms|55.854 /55.604ms|
| Maximum |85.617 /81.794ms|145.828 /124.637ms|
| Frames >50ms |16 /15|46 /46|
| Frames >100ms |0 /0|18 /19|

Large rebuild CPU falls33.16%; construction frames shorten13.10ms/~10.4% on average.
Whole-frame means essentially unchanged (+0.06% reported12, -0.20% large40); individual
run means mixed. No general FPS gain or stall-resolution claim. Large candidate's
extra102.490ms frame is demolition1x/frame74 with46.468ms sampled drone upload call
time. Every >50ms frame retained with overlapping action/step/draw/render/upload
metrics; these must not be summed as independent costs. Phase texture peaks unchanged
1,586.306MiB/2,784.533MiB; these are not per-frame/driver peak-memory certification.

Prior final-V2 lifecycle verification87graphs/1,044,474point records/10,821selected
routes exact covers real saved prop moves/deletions, detached rooms, Moonbay phases
and rotations, immediate staged clear and synchronous supersession (see lifecycle
handoff). Installed maintained test red:4expected reuse failures before installation;
green76checks/0failures,99,360point records/888routes exact for Bill and Marsh. Existing
room-owner test90checks/0failures. Normal native galley passes paid construction,
deck/entrance, three hungry crew/meals, Save/Continue, frozen time/suspension,
104continuous movement samples and three native viewport sizes. Relevant source/index
diff whitespace check clean; new UID engine-generated in guarded isolated profile.

All owner guards2,938 unchanged; all jobs terminal/configs/fixtures restored. No full
source/package copies. This turn~83.77MiB evidence plus19scratch profiles~37.04MiB;
profiles retained following earlier automatic deletion rejection, no retry this turn.
C124.26GiB/D80.64GiB free;20GiB test storage floor remains enforced.

Evidence under `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`prefix-final-large-performance/`, `prefix-final-reported-performance/` (paired analyses,
traces and all>50ms census), matching small runtime overlays, `prefix-normal-install/`,
`prefix-normal-red/`, `prefix-normal-green/`, `prefix-normal-galley-gameplay/`.
Focused drivers/tests under `output/renderdoc-tools-2026-10-08/` retained.

## Next action

Profile/reduce broad room/layer redraw work remaining in construction frames while
preserving complete visible output; reuse earlier rejected wall/floor-cache evidence.
Address clustered drone uploads independently. Keep installed preparation and graph
reuse in future baselines. Continue original loading/memory/bugs/UI/save/endurance,
native target-PC/Mac, physical candidate freeze/audit, signing/notarization and final
readiness report. No public release while frame/stall or critical defect gates fail.
