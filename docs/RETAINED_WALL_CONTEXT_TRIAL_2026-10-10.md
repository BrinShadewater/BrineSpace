# Project handoff

Updated: October 10, 2026 · BrineSpace · Task: private retained wall dependency context

## Objective and acceptance

Reduce broad wall redraw bursts without the per-frame projection overhead that made
the earlier local-wall trials inconclusive. Full PC/Mac performance/release scope
remains open. Native visual and matched workload evidence are required for admission.

## Accepted decisions and constraints

Keep the existing wall slots, compositing order and neighborhood dependency projection.
Retain only the current immutable metadata context per grid; no image/mesh cache,
extra draw nodes, art changes or automatic quality changes. Context invalidates on
common/global/geometry/power/cell-list changes and relevant neighbors outside the
structural snapshot. Corridor shade retains only its latest nonzero key per room.
Preserve owner files, mute tests, use secondary display and bounded shared-runtime QA.

## Current state

Normal source unchanged this turn; accepted navigation reuse remains installed.
New private helper/test in `output/renderdoc-tools-2026-10-08/`:
`retained-wall-context.gd`, `test-retained-wall-context.gd`, and isolated unit driver.
Staged current-source Grid integration and identities in
`D:/bs-release-crew-cache-20261009/benchmark-input-isolation/retained-wall-context-unit/`.
Diagnostic reference switch retains original global wall-slot keys. Not mounted into
the game, admitted, exported or released. No full package/source copies.

Earlier local projection avoided >90% wall rebuilds but had mixed whole-frame means.
Its per-pass context reduced preparation overhead yet still rebuilt snapshots every
frame. The new experiment preserves those keys while retaining the last context.
Simply caching on visible/common state would miss offscreen neighbor mutations;
the new signature explicitly includes relevant external neighbors and power state.

## Verification

Pure headless fixture:8,004checks/0failures against fresh original per-pass projections
over200mutations/40rooms. Covers outside-snapshot neighbor rotation/live-only state,
power membership, global revision, changing shade, key immutability and bounded
current keys.41builds/660reuses including500unchanged timed passes.
Synthetic CPU preparation: fresh226,632usec /retained35,197usec for500passes,
about0.453->0.070ms/pass (84.5% lower). This is not game frame-time/FPS evidence.
It compares against prior per-pass local projection, not the normal global wall key.

Current private Grid/helper compile check passes with no errors. Parse-only copy
removes the global GridCanvas name to avoid the known raw-script collision; intended
PCK member retains it. Native rendering, input/event integration, all immediate
mutation pixels and actual station performance are not yet verified.
Both full owner guards2,938 unchanged. Jobs terminal; no game/native test active.
Small text/metadata outputs only; no asset batches or large duplicate runtime.

## Next action

Create a small current-source overlay including installed preparation/navigation and
the helper. Reuse shared QA package; adapt prior cached-versus-forced wall parity
without its old full runtime-copy path. Verify first-frame/settled placement/removal,
external neighbors, culling, pan/zoom, lighting/corridor fade, rotations/raised walls,
motion/crew/layering and lifecycle. Then compare actual normal global keys against
retained local context on reported12/large40 with identical accepted baselines;
measure preparation, rebuilds, complete frame tails and states before admission.
Continue independent drone-upload, memory/loading, original bug/UI/endurance and
native target-PC/Mac release gates. No public release.
