# Large-room props and Moonbay rendering

Updated: October 5, 2026 · BrineSpace · R6

## Objective and acceptance

Measure the actual large-room shell and prop paths before introducing retention
or culling. Preserve owner layouts, ordering, flood materials and selected art.

## Accepted decisions and constraints

Do not introduce dry-room child retention based on the prop-loop hypothesis alone.
Props are measurable work, but Moonbay's water generation is a larger individual
hotspot. Applied only a small equivalent arithmetic optimization: compute one
cosine offset per ribbon rather than seven times per ribbon. No cache, geometry,
timing, quality, UV or asset changes. Existing Moonbay UID unchanged.

## Current state

Changed `rooms/large-rooms/moonbay.gd` by hoisting the repeated expression. All
profiling/instrumentation source copies remain under
`output/large-prop-profile-2026-10-05/`; normal Library, Studio and wet-equipment
implementations are unchanged. Source hashes and copied owner-layout hash are
recorded in `inputs.json`.

## Verification

Native Godot 4.7.2: **64 cases / 768 sampled frames**, four room types × four
rotations × dry/flooded × online/offline appearance. Actual draw_live caller,
with owner layouts copied into a guarded scratch profile. Library instrumentation
includes deferred flooded prop drawing; submission alone would omit that cost.
First-use loading is warmed before samples. Medians across each room's rotations,
offline states and twelve frames:

| Room | Dry shell/machinery | Dry prop draw | Flooded prop draw |
| --- | ---: | ---: | ---: |
| Hydroponics farm | 0.198 ms | 0.328 ms | 0.337 ms |
| Storage depot | 0.211 ms | 0.423 ms | 0.435 ms |
| Moonbay | 2.077 ms | 0.215 ms | 0.210 ms |
| Tidal power plant | 0.250 ms | 0.274 ms | 0.283 ms |

These component times are command-building CPU, not GPU or complete frame time.
The selected supporting-prop sets contain 13/19/8/14 entries respectively; hidden
props and rotation variants affect visible call counts. Frozen Moonbay mission
clock is used in this profile; prop clocks advance. No station-wide saving inferred.

Focused Moonbay run: **16 cases / 192 sampled frames**. Inclusive component
medians: water **1.155 ms**, Common.begin **0.221 ms**, windows **0.161 ms**,
beacons **0.155 ms**, bay doors **0.135 ms**, wall corners **0.102 ms**. Common
floor tile timing is nested inside some work; do not sum every field as disjoint.

Water optimization: **144 exact pixel comparisons** across two scales, subpixel
offset, six water levels, six clocks and pumping on/off. Prototype large-water
median 981→922.5 us; final actual runtime versus frozen reference **939→889.5 us**.
These are paired fixture samples, not independent packaged benchmarks; about
50 us saved in the final fixture does not certify an overall FPS improvement.
Dry/wet Moonbay source capture visually inspected. No engine errors in final runs.
All run groups confirm **2,936 owner non-log files unchanged**. Scoped diff check
passes. No exports, uploads, commits or broad changes this interval.

## Next action

Profile/cache invariant water-ribbon preparation or retain unchanged Moonbay
output with complete mission, clock, water and geometry keys, then measure moving
mission phases as well as idle. Keep large-room per-prop retention open: multi-room
ordering, off-hull owner props, offline wash, crew crossings and culling require
native regression coverage before adding child slots. R7 light-map GPU scheduling
and full-roster memory remedies remain on the queue; release gates remain blocked.
