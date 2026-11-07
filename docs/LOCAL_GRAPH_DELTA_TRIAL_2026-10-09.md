# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: changed-section graph kernel

## Objective and acceptance

Reduce remaining full graph reconstruction while preserving exact IDs, weights,
ordered adjacency and selected routes. Full original PC/Mac scope/gates remain open.
Semantic parity and measured benefit are both required before normal integration.

## Accepted decisions and constraints

Current private kernel is REJECTED for normal integration: it is slower than the
same warm-cache full graph assembly. Do not package-test/adopt this form. Normal
Bill/UID remain unchanged at93e31c...; previous retained optimizations stay intact.
No graph sharing, mission timing deferral, art changes or broad refactor.

## Current state

Private static synchronous helper accepts actor-owned graph/global lookup/room ID
arrays plus old/new local templates and ordered boundary edges. Preflights equal
ordered ownership/per-cell counts, positions/weights/global map and valid endpoints;
disconnects old boundaries and changed local links, updates positions/weights/lookup,
then recreates local links and boundaries in original order. Disabled flags reset.
No persistent global cache; returns false before mutation on unsupported input.
Scene/layout/policy ownership and staged/lifecycle integration remain UNIMPLEMENTED.
This kernel alone must not be used as a general rebuild replacement.

Artifacts D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/local-graph-delta/:
delta.gd,current instrumented helper;delta-validated.gd,uninstrumented semantic form;
test.gd,timing-test.gd,red/green/timing-result.json,decision.json,logs and owner proofs.
Helpers output/renderdoc-tools-2026-10-08/prepare-delta-kernel.py,
run-delta-kernel.py,prepare-delta-kernel-timing.py. No normal code changes.

## Verification

- Fixture uses actual reported three Moonbays/cell sockets and copied owner layouts.
  Expected red1 failure proves equal-count update is absent. Corrected a diagnostic
  marker replacement before accepting red; no gameplay behavior changed.
- Native47694checks/0: exact graph IDs/order/positions/weights/ordered adjacency/
  selected paths through forward/reverse transitions,graph identity,read-only input,
  disabled reset,count-change fallback before mutation and untouched rejected graph.
- First preflight rejected native weight1.080000042915 versus GDS float1.08.
  A temporary diagnostic confirmed positions equal and exact native rounding;
  Vector2 float32 conversion now preserves the engine's stored weight in comparisons.
  Diagnostic indentation error was corrected; rejected runs are not acceptance.
- Warm derived-cache baseline,24 forward/reverse transitions with alternating pair
  order:63614checks/0 after timing,including final exact graph/routes. First trial
  full4-8ms/delta27-34ms. Bounded component repeat still much slower; decision.json
  retains medians. Last delta:preflight17.627ms/disconnect4.038ms/edit7.926ms/
  seams+disabledreset1.259ms. Repeated dictionaries,per-point validation and uncached
  link lookups outweigh local reuse. These are headless kernel timings,not FPS.
- Godot's documented APIs support updating point positions/weights and connecting/
  disconnecting edges; exact order/route parity is established by native tests,
  not promised by docs: https://docs.godotengine.org/en/stable/classes/class_astar2d.html
- All runs resolve scratch user data before writes. All2936ownerfiles unchanged;
  successful logs clean/processes terminal. No packaged performance claim.

## Next action

Revise the private design to prepare immutable packed local indices once and prove
actor/build/layout ownership with cheap state guards rather than revalidating every
point/link through dictionaries on every update. Profile those preparation costs
too; retain existing native parity/fallback tests. Do not weaken invalidation or
ownership merely to make a benchmark pass. If a faster exact update cannot be
demonstrated, pursue the measured boundary-check cost with equivalent collision
proof instead. Full-source package,broad workloads,original bugs,loading/memory/
endurance and Windows/Mac certification remain open.
