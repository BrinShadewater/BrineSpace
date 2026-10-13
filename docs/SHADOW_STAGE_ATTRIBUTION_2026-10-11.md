# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: separate structural shadow costs

## Objective and acceptance

Continue full performance/release plan. Attribute floor shadow costs before edits;
preserve selected pixels, owner layouts, timing and quality. No new production
optimization admitted in this pass. Previous turn was progress: scoped floor
timings changed the next profiling target.

## Accepted decisions and constraints

Muted secondary native debug=false tests, isolated profile/APPDATA, owner hashes.
No screenshots or runtime copies. Existing crew/zoom changes preserved. Do not
repeat rejected shadow-band, floor-slot or profiling-overhead trials unchanged.

## Current state

Private RoomLighting overlay times parts preparation, oversampling/key creation,
packet lookup/build, border commands, palette and submission. Eight-frame ring,
seven labels, metadata only. Diagnostic grid retains floor/shell/live labels.
Production rendering and gameplay files unchanged. Runner:
output/renderdoc-tools-2026-10-08/run-shadow-stage-attribution.py.
Evidence: D:/bs-release-crew-cache-20261009/benchmark-input-isolation/
shadow-stage-attribution/analysis.json, identities, source, logs, owner.json.

Initial candidate overlay failed parsing because an appended statement lacked a
newline. Corrected only the private file; failed log retained separately and
excluded from evidence. Existing clean reference result reused after checking
the same frozen production inputs. Runtime guards verify profile/control lanes.

## Verification

Completed two native 40-room traces/3240frames. Nine full phase states/cameras
and fifteen paired successful lighting/placement/demolition events exact at
1x/2x/4x. Six action-frame30 samples show aggregate room-shadow CPU costs:

| Stage | Range ms |
|---|---:|
| Prop feet/band preparation |1.215–1.334|
| Oversampling/geometry key |0.359–0.410|
| Packet lookup/build |0.125–0.171|
| Border commands |0.519–0.603|
| Palette |0.127–0.175|
| Shadow submission |0.614–0.804|
| Whole shadow calls |3.194–3.734|

Stages exclude most recording overhead; total includes nested measurements.
These are attribution counters, not saved time, FPS improvement or certification.

Prior evidence inspected before implementing contact-style memoization:
docs/FLOOR_TRACE_AND_GAIT_INPUT_2026-10-11.md and the actual private
shadow-band-preparation/candidate-lighting.gd. That rejected candidate already
avoided StyleBox work on unchanged light/geometry, with exact pixel/cache checks,
but three native large pairs worsened whole mean1.03% and >50 frames56→66.
Do not retest a weaker local style memo merely because preparation remains costly.
No new contact memo or duplicate packet cache was implemented.

Also inspected docs/PACKAGED_PROFILER_OVERHEAD_2026-10-09.md and
docs/RENDER_TIMING_SCOPE_AND_OVERHEAD_2026-10-08.md. Those matched draw/viewport
on/off experiments did not prove a consistent large profiler penalty. Do not
repeat them unchanged or attribute the performance gap to diagnostics by assumption.

Room configure2.272–2.739ms from the preceding floor attribution is the next
unresolved CPU target. Source shows existing Solar rotation snapshots and embedded
edge caches, with mutable owned copies; broad cache replacement is premature.
Separate configure/rebuild, edge copying and retired-prop filtering next. Avoid
skipping actor preparation without animation-state/visibility proofs.

Owner2938 unchanged in all guards. Jobs terminal, runtime override restored.
Completed JSON reports compressed with exact before/after content hashes;
no owner/runtime compression/deletion. Last freeC134.86/D68.70GiB. Full frame,
memory, loading, endurance, nine bugs, packaged Windows/M1 and signing gates open.

## Next action

Bounded attribution of room configuration versus prop filtering, using the same
guarded native structural workload and current accepted source. Choose a measured
change with exact owner-layout/geometry/pixel checks. Preserve existing caches and
mutable ownership until evidence supports altering them; no monolith refactor.
