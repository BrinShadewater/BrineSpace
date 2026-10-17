# Project handoff

Updated: 2026-10-15 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: placement graph invalidation/retention

## Objective and acceptance

Explain both companion graph rebuilds, reduce unnecessary work while preserving
appearance and crew behavior, and compare average FPS and 4× placement pacing.

## Accepted decisions and constraints

Keep current runtime. Two native retention prototypes are correct within tested
scope but slower; neither is admitted. Preserve exact canonical IDs, neighbor
order, routes, graph identity, locks/water behavior, resets and update schedule.
Scratch APPDATA/test-dir override and owner fingerprints remain mandatory.

## Current state

4× fixture placement at `(24,17)` opens Life Support `(23,17)`: 307→310 local
nodes. Three inserted nodes shift later canonical IDs; each companion retains
8,580 of 14,382 old nodes and rebuilds a 5,802-node suffix. Fifty-two existing
local room templates are unchanged, but their global IDs are not all unchanged.

Private native V1 patches the full graph; V2 patches only the affected suffix,
reusing numeric slots and endpoint-consistent ordered edge prefixes. The final
4× patch keeps only 478 suffix edges while adding/removing ~18,000. Its extra
inspection/update work outweighs that retention. Normal source remains unchanged.

Only this handoff, results and CURRENT_STATUS are new project-source edits.
Evidence: `C:/bs-nav-retention-20261015/`; helpers:
`output/nav-retention-20261015/`. V1 source/DLL archived; V2 DLL separate/hashed.
No installed extension, export, Mac binary or commit.

## Verification

V2 warmed connected rebuild 10.263→15.034 ms; middle edit 13.244→16.644 ms.
Guarded release comparison: 1,920 frames, eight exact state/camera/path pairs,
0/8 60 FPS gates. Idle 53.33→53.04 FPS. 4× action
69.767/70.664→80.287/79.759 ms; crew 26–27→37 ms. Following-window pacing gives
no dependable gain; >50 ms counts remain 1→1 in each order.

13,424 final graph/route checks, 1,474 native primitive assertions and 1,488
extension-absent checks pass. Seventeen cross-process image pairs plus twelve
repeat pairs exact. V2 read-only review found no production blockers. All 26
profile guards clean; final 2,948 files equal task-initial/prior post-recovery
baseline. Source/UID/test hashes unchanged; only owner editor PID 46624 remains.
Retain the [earlier incident caveat](TEST_PROFILE_INCIDENT_2026-10-15.md).

## Next action

Do not rerun unchanged wrappers or install these prototypes. A larger retention
gain needs a design that avoids global node-ID shifts and preserves routing's tie
order and actor-specific restrictions. Propose that design before a navigation
restructure. See [full results](NAV_RETENTION_PERFORMANCE_2026-10-15.md).
