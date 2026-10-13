# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: navigation preparation and boundary costs

## Objective and acceptance

Reduce measured navigation stalls while preserving geometry, IDs, ordered routes,
door/fire policy, mission timing and ownership. Full original release scope remains
open. Actual packaged comparisons are required before normal integration.

## Accepted decisions and constraints

Packed delta remains private/rejected for this form. It improves the previous
kernel but still loses to the same warm full fixture and adds preparation costs.
Normal Bill/UID unchanged at93e31c...; no cheap guard replaces actual point checks.
Next measured remedy is boundary checking,not a broad graph refactor. Preserve
general route checks and all corridor/legacy/sample-all/live-fire fallbacks.

## Current state

Private packed delta compiles independent packed positions, float32 weights and
absolute link/seam IDs into forward/reverse plans. Plans are read-only by convention;
input templates are not mutated. Actual graph positions/weights/IDs/global lookup
remain checked on every apply. Scene/layout/policy lifecycle integration is absent.

Private boundary helper prepares the same grow0.05 owner-clipped blocker rectangles
once per geometry set. Only graph-assembly axis-aligned32px seams with known owning
cells and reciprocal open sockets use convex endpoint proof plus exact rectangle
sweeps. Hardware/per-room locks are retained. All other calls use segment_clear.
No general route validation or sampling policy change is implemented in normal code.

Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/:
packed-graph-delta/{delta.gd,test.gd,timing-test.gd,decision.json,logs,owner proofs};
boundary-kernel/{boundary.gd,test.gd,actual-test.gd,actual-result.json,logs,owner proofs}.
Helpers under output/renderdoc-tools-2026-10-08/:
prepare-packed-delta-kernel.py,prepare-boundary-kernel.py,
prepare-boundary-actual-test.py. All jobs terminal; no normal gameplay source edits.

## Verification

- Packed delta expected-red1 followed by native47694checks/0 and warm24alternating
  pair63614checks/0:exact IDs/positions/weights/ordered adjacency/routes,reverse
  transition,graph identity,disabled reset,count fallback before mutation.
- Full median3.617ms vs packed delta9.1195ms; previous unpacked median22.9565ms.
  Packed preparation9.955/10.885ms forward/reverse,reported separately rather than
  hidden. Last applypreflight2.343ms/disconnect3.092/edit2.679/reset+seams0.806ms.
  Not a full-station or packaged FPS result; current form is not admitted.
- Boundary expected-red1 then synthetic5892comparisons/0:four directions,closed
  reciprocal sockets,hardware/per-room locks,padded/clipped/half-open edge blockers,
  legacy/sample-all/live-fire fallbacks. Aggregate reference16.434ms/helper7.434ms,
  preparation0.068ms. Diagnostic accumulation,not matched gameplay speedup.
- Current three Moonbay component/socket geometries with copied owner layouts:
  four rotations × ten phase labels × both station door states =80geometry cases,
  44160boundary comparisons/0. Covers some unreachable combinations to test geometry.
  Aggregate reference788.815ms/helper331.246ms;preparation2.252ms across80sets.
  This proves tested seam boolean parity,not full graph or packaged acceptance.
- Each invocation verifies resolved scratch user data before writes. All2936owner
  files unchanged;successful logs clean/processes terminal. No art changes.

## Next action

Integrate boundary helper only into a private copy of the normal rebuild boundary
loop with per-build cache lifetime and a reference switch. Keep insertion order,
geometry/policy refresh and staged cancellation intact. Verify full graph adjacency/
chosen routes plus corridor and missing-cell fallback,then matched debug=false
frame1256 component measurements both orders. Admit only measured gains and normal
regressions; no FPS claim from these aggregate timings. Full-source packages,broad
workloads,original bugs,loading/memory/endurance and Windows/Mac gates stay open.
