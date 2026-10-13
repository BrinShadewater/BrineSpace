# Floor invalidation, rejected shadow trial and world-position gait lead

Updated: October 11, 2026 · Project: BrineSpace · Task: PC/Mac performance readiness

## Objective and acceptance

Continue the full performance/release plan. This batch attributes larger redraw work,
rejects an ineffective optimization, and establishes a concrete animation-input error
to investigate against the indexed provider's strict-state blocker. No release gate
or broader platform requirement is closed.

## Accepted decisions and constraints

Keep shadow-band preparation out of production: local work decreases but the matched
whole-workload result worsens. No art, simulation, selected bank, save binding or
renderer-quality changes. Preserve floor/pool/seam order. The world-position gait
candidate is private until actual selected animations, state behavior, save/Continue,
zoom and all simulation/display speeds are tested. Do not waive the provider mismatch
with an epsilon or call its memory saving admitted.

## Current state

Production files unchanged. Private diagnostics/candidate under
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/`:
`floor-invalidation-trace`, `shadow-band-preparation`,
`shadow-band-preparation-pixels`, `world-gait-input`.
Runners in `output/renderdoc-tools-2026-10-08/` use those names, plus
`run-camera-gait-position-probe.py`. Current status and this handoff record the result.

## Verification

One current-source actual debug=false 40-room trace / 1,080 measured frames.
Idle/pan produce no floor-key invalidations; zoom requires nine floor-group repaints.
Lighting: 94 surface invalidations, 88 from room-state key index 5 and six initial
resets. Floor and rest passes total 1,191,783 us / 270 lighting frames = 4.414 ms/frame,
with 94 repaints each. These are instrumented CPU figures, not acceptance frame times.
Room-state includes fade levels; preserve narrow-corridor/wall dependencies and the
original interleaved pool/shadow/floor ordering.

Private trial derives band geometry/radii without StyleBox lookup and refreshes contact
colours/palette inputs only when a cached packet's geometry or light level changes.
Six actual debug=false native 40-room runs / three alternating pairs / 6,480 frames:
mean 25.632 -> 25.897 ms (+1.03% worse), p95 42.560 -> 42.707, p99 54.436 -> 54.260,
>50 ms 56 -> 66, >100 ms 0 -> 0, textures unchanged at 3,028.007 MiB. Shadow setup
345 -> 325 us (5.9% local reduction). One candidate pair worsens by 1.186 ms, two
improve; no useful overall performance gain claimed. All 36 state/camera phase pairs
exact. Reject the candidate; do not broaden benchmarks to real maps just to seek a win.

Candidate native validation still establishes its narrow pixel/lifetime behavior:
128/128 packet/fallback comparisons; 192/192 room/rotation/oversampling comparisons;
28 cache/alias/moved-footprint/budget/owner-lifetime checks with zero failures. Corrected
station visual pair 28/28 pixels/context checks exact, including visible case add/move/
remove. These passes do not override the worse performance result.

**Actual-engine gait input probe:** Main.get_chief_branforth_position returns
`(foot / 384 - Vector2(0, .038)) * get_cell_size()`. Grid supplies that position divided
by cell size to the player's distance-based gait. Twelve actual saved station feet,
12 zoom scales each: 9/144 projected/divided values differ from the unscaled canonical
value, 18 stationary zoom-to-zoom position changes, max 1.9073486e-6 cells.

Using the actual `crew_sprite_player.gd` frame method with a one-frame null-texture
walk bank, one-second loop and 0.12-cell stride, fixed physical foot and time advancing
at 1/60 sec: six feet accumulate false phases of 3.1789e-5 to 9.5367e-5 sec; canonical
world input stays exactly zero for all twelve. With time frozen, both phases stay zero
(the existing pause guard works). This proves a camera-dependent input/phase error in
that model, not selected-art acceptance or the sole cause of the provider mismatch.
No texture generation/loading or physics change is involved in the probe.

Prepared `world-gait-input/candidate-grid.gd`: three Branforth playback inputs use an
unscaled world-position helper; rendered coordinates and source anchors remain as
before. Candidate has not been run in gameplay. Do not claim it fixes the provider
until matched normal/indexed and selected-animation verification establish that.

All owner guards: 2,938 files unchanged. Native jobs terminal, QA override restored.
Evidence about 135.8 MiB added (6.82 trace, 28.09 trial/guards/probe, 100.89 visuals;
world-input source is small). C 124.65 / D 71.38 GiB free. Existing executable/PCK reused,
20 GiB floor enforced, snapshots bounded. No full source/package copies or deletion.

## Next action

Test world-position gait input against actual selected banks and saves, checking gait
under 30/60/120 FPS, camera zoom, pause/resume and 1x/2x/4x. Rebase the private indexed
provider onto the installed current source plus that fix; compare both providers at
matched canonical input, without ignoring phase or other saved-state differences.
If accepted, resume loader/filter/fallback/lifetime/endurance checks for the measured
~399 MiB large-scene texture saving. Larger frame-time work remains necessary; the
rejected shadow preparation saving cannot close the gap.

Keep the independently reproduced identical-input wreck rendering discrepancy open.
Actual target GPU/1440p, full workloads, endurance, packaged original bug closure and
Windows/Mac release certification remain outstanding; this batch does not certify them.
