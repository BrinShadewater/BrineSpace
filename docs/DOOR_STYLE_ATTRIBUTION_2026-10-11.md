# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: remaining door validation attribution

## Objective and acceptance

Identify measured CPU work to optimize after shared indexed rendering fails the
mean-frame acceptance. Preserve appearance, dynamic door/layout changes and current
accepted source. Full performance/release goal remains open.

## Accepted decisions and constraints

Keep indexed provider private; do not rerun unchanged renderer/cache trials.
Crew foot gathering is already cached by frame/owner/size. Existing connectivity,
port/frame/light/parts attribution remains useful; reuse it before new profiling.
Any cache candidate must preserve owner Studio layouts and dynamic updates.

## Current state

`run-door-style-attribution.py` generates a private instrumented current Grid and
uses the current Main benchmark clock fixture. Production unchanged. Actual native
release runtime reused, muted/secondary/isolated; no screenshots or art copies.
Outputs under `benchmark-input-isolation/door-style-total-attribution/` on D:.

## Verification

Corrected actual debug=false 40-room station attribution, 1,080 measured frames,
idle/pan/zoom/lighting at 1×/2×/4×: door style selection mean187.679us versus
door/light validation1094.447us (nested scope). Nonzoom33 style calls/frame,
206–214us; zoom mean19.067 calls and120–123us. Timer/instrumentation overhead is
included, and this is attribution, not an optimization/FPS comparison.

Initial `door-style-attribution/` used `_profile_draw_stage`, which overwrites the
per-frame label with its final call; its 5.589us mean is not total style cost.
Corrected probe uses `_profile_detail` accumulation and an explicit call counter.
Keep the first report labeled unusable for total-cost conclusions. Both successful
runs clean, owner2,938 unchanged; jobs terminal and runtime override restored.

## Next action

Prototype a paint-local ordered room-id/rotation pair→style lookup inside
`_door_light_state`; discard after each synchronous call. Original
DepartmentDoor.pair_variant remains authoritative on misses. No permanent cache,
new invalidation scheme or visual change. First verify all variants/rotations,
corridors, owner overrides and fresh-pass style changes; then matched real-map
timing. Accept only a measured benefit. Keep remaining broader CPU/render costs
and original release gates open.

## Paint-local pair lookup pilot

`build-door-style-reuse.py` now writes a private current Grid plus exact helper
in `benchmark-input-isolation/door-style-reuse/`. Lookup uses ordered id/rotation
keys and is discarded each `_door_light_state` call. No persistent resources or
invalidation rules added. Native helper oracle: 1,024,000 comparisons, zero
failures, 80 ids×all ordered pairs×16 rotation pairs×five layout contexts×miss/hit.
Includes corridor/default/unknown rules, copied position changes, owner layouts,
quarter overrides, invalid styles and wholesale Store.data replacement without a
revision bump. 100,820 entries change across fresh-pass contexts, proving overrides
are exercised. Native `door-style-reuse-checks/{probe.gd,native.log,owner.json}`.

Actual debug=false large-station pair, idle/pan/zoom/lighting at1×/2×/4×,2,160
measured frames: all12 states/cameras/labels exact, texture3028.007MiB unchanged.
Mean25.625→25.129ms, p9541.696→40.380,p9951.141→50.105,>50ms14→11.
However targeted door/light validation1065.889→1084.916us worsens by1.79%.
One whole-frame pair improving while targeted work worsens is insufficient
acceptance. Candidate remains private; no FPS claim. `door-style-reuse-pilot/`
retains identities/reports/comparison/owner guards. Production unchanged.

Both native runs completed before a reused runner's obsolete indexed-provider
postcondition failed. Removed that unrelated postcondition and finalized existing
identical-input completed results without repeating gameplay. Logs clean, owner
2,938 unchanged, processes terminal and runtime override restored.

Next resolve actual cache hit/miss distribution and lookup overhead before any
additional matched timing or admission. Consider per-room department reuse only
if the evidence supports it; do not install an unmeasured permanent cache. Full
performance/release objective remains open.

## Pair lookup rejected; workload coverage clarified

Native `run-door-style-hit-attribution.py`,1,080 measured frames: ordinary frames
have4 hits/29 misses (12.1% reuse); zoom mean2.311 hits/16.756 misses, same ratio.
Lookup timings are instrumented, exclude key construction/final value retrieval,
and include nested miss timing; not a matched optimization comparison. This
explains insufficient reuse to justify the prior pair lookup. Reject that
candidate; do not repeat its timing unchanged or install it. Owner2,938 unchanged,
jobs terminal/override restored; raw rows in `door-style-hit-attribution/attribution.json`.

Audited authoritative matched-state room lists from the18-run shared-palette
comparison: reported12, current10 and generated40 all contain only1×1 rooms.
None includes Moonbay, Tidal Power Plant, Hydroponics Farm or Storage Depot.
These tests remain useful standard/saved-station coverage, but cannot certify
multi-cell room animation/performance. Older multi-cell room attribution uses
different dated fixtures and is not current-source acceptance. Room census saved
to `door-style-hit-attribution/workload-rooms.json`.

Maintained `tools/release_benchmark.gd` now reports additive `room_composition`
with id counts, multi-cell room count and occupied cells once during preparation.
Actual debug=false native parser check succeeds with no engine errors, isolated
owner2,938 unchanged. Field execution awaits next gameplay benchmark; parser
success is not workload validation. No production renderer changes.

Next add a separate deterministic mixed-footprint workload with current large
rooms, connected doors/open-water requirements and active mission/crew/production
checks. Preserve the original three workloads. Then profile room preparation and
dynamic drawing in the actual populated scene, reusing existing evidence where
applicable. No blanket redraw suppression or art/quality changes.
