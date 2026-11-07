# Door/light validation: call-local light reuse

Updated September21,2026. Broad objective remains active.

## Objective and constraints
Reduce repeated work in the previously measured door/light validation stage without
changing lighting, door state or room layout. Preserve frame-to-frame fades and
power updates. No broader render/FPS claim from this scoped measurement.

## Installed change
scripts/grid_canvas.gd::_door_light_state now reuses each room's light level in a
local dictionary for that invocation only. The current room level already used by
the lighting key also feeds its door pairs; neighbor levels are evaluated lazily
and reused when their own rooms are visited. Neighbors outside static_draw_rooms
still receive a fresh lookup when a visible door needs them. Nothing is retained
across calls, so same-frame changes on the next call are not hidden by a cache.
Door geometry, depth, flicker, power rules and invalidation logic are unchanged.

## Verification
Native100-room fixture compares the production method against an output-only copy
of the original method. Normal, blackout, interior-off, partial-fade and restored
snapshots produce identical complete door/light keys. Each lowers light queries
280 to100. Inputs include synthetic per-room light levels; these are not a native
fade-duration or autonomous crew-crossing test.
Paired before/after/after/before blocks,10 warmup and100 calls each: original
3469.07/3467.74 us, installed3030.52/3077.66 us. Means3.468 to3.054 ms, about0.414ms
(11.9%) for this validation call. Wrapper/counting overhead is shared. Forced native
setup, paused simulation, fixed snapshot: not FPS or whole-render savings.
Initial output-only probe also passed; installed-native.log is the final run,
exit0 without logged errors. Evidence, exact source hashes and original method:
output/door-light-memo-2026-09-21. No unrelated benchmark reruns.

## Next action
Include this change and Biomass in the next maintained Windows/Mac release checkpoint;
current packages predate both. Full expedition and native Apple Silicon acceptance
remain open. Broader live-room rendering cost is not resolved by this optimization.
