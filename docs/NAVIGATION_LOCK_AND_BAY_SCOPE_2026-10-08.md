# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: current door locks and private bay navigation scope

## Objective and acceptance
Continue the full performance, bug closure and PC/Mac release plan, preserving selected pixels, clocks, gameplay and owner saves/layouts. No publication. Scope reduction must prove route/connectivity equivalence before actual gameplay performance acceptance.

## Accepted decisions and constraints
Normal source now refreshes locked_room_cells in the geometry collection pass before graph edges are emitted. Existing topology() refresh at completion retained. Shared geometry and historical save bindings preserved. Private bay scope is not admitted: only boarding/exit_bay with closed station pressure door can qualify; dispatch/approach/unload and general station movement must keep full graphs. Never falsely mark a partial graph current for full station navigation.

## Current state
Changed scripts/bill_npc.gd: clear lock map before collecting geometry, populate it from current occupied-room doors_locked flags before connection construction. Existing UID and unrelated work preserved. Extended tests/test_navigation_room_owner.gd with first locked and first unlocked rebuild cases for Bill and inherited Marsh; existing test UID/index retained. Private source, probes, failed evidence and logs under D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/{bay-scope,lock-refresh}/. No production scoped rebuild parameter or mission change.

## Verification
Initial private bay scope matches full routes/geometry but intended successful unlocked reference routes fail in15 cases. Observable cold/warm probe: first route after prior locked state empty, second rebuild restores it. Root cause: cross-cell segment_clear uses locked_room_cells before topology() refresh at rebuild completion. First locked rebuild conversely retains graph edges. Maintained normal regression red90 checks/four failures, green90/zero after three-line runtime correction. Clean isolated logs, no save writes.

Private full/scoped copies patched with the same lock correction: first unlocked routes now nonempty for boarding and exit_bay in all four rotations. 5,964 checks/zero failures:32 combinations of rotation, phase, hardware locks and room locks; exact smoothed endpoint routes, cold/warm parity, complete reachable component adjacency by world coordinates, proof reachable component remains inside bay, identical local geometry and invalidation of scoped signature for later full station updates. Fixture includes eight surrounding corridors and unrelated rooms. Graph count full5,387–5,399 versus scoped1,534–1,546; headless timings diagnostic only, not FPS acceptance. First failed source-patch assertion stopped edits; redundant probe ran unmodified, not treated as updated proof. Final corrected probe is authoritative. Initial/failed and prior-lock-fix evidence retained.

Owner fingerprints2,936 files unchanged for all runs; processes terminal. Normal lock correction needs packaged verification. Original indexed-links prototype remains private with mixed net performance and unresolved prop draw/advance counters.

## Next action
Prepare actual release reference and candidate with identical current lock correction. Private mission override should use scoped rebuild only for boarding/exit_bay when station pressure door closed and both actor foot and target belong to bay; otherwise full rebuild. Invalidate partial signature immediately; fall back to full graph on failed scoped route. Preserve movement/fire/locks and every side effect of rebuild. Extend coverage for layout revisions, demolition/cancellation, fire and save/Continue before admission. Measure same natural three-mission workload and exact phase endpoints, then decide. Full original release gates, combined exports, endurance, GTX1650/M1 and Mac signing/notarization remain open.
