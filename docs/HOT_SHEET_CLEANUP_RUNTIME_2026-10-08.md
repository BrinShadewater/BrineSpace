# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: corrected texture cleanup runtime.

## Objective and acceptance
Continue full PC/Mac release readiness; verify actual debug=false cleanup without changing art/simulation. Candidate stays private, no publication or FPS certification.

## Accepted decisions and constraints
Original South mining texture only, session-scoped, ordinary256MiB cache unchanged,2/3GiB scene limits/64MiB margin. Preserve previous evidence and owner data. Synthetic12 is not historical reported station.

## Current state
New run-hot-guard-release.py, run-hot-guard-small.py, run-hot-guard-forcedlookup.py and compare-hot-guard.py in output/renderdoc-tools-2026-10-08. Corrected hot-sheet-motion-drop-guard.gd loaded before initialization. Normal source/art unchanged. Evidence folders hot-guard-release, hot-guard-small, hot-guard-forcedlookup.

## Verification
40room matched pair hot5 to1 uploads/API82.754 to13.038ms; peak2348.739 to2411.622MiB; exit228.259MiB both. Four restores/exit release1. Means9/9 and p956/9 improve. Synthetic12 hot3 to1/API41.910 to10.708ms; peak1848.369 to1971.445MiB; exit228.259MiB both. Means6/9/p957/9 improve. All compared states AND prop counters equal both pairs. Historical2/13difference unexplained, not closed. FPS still fails: corrected large means31.7-41.6ms/max96.059ms; small means17.3-21.7ms/max58.124ms. Same corrected pack in both pairs, single pairs insufficient for robust FPS benefit.

First forced post-measurement drop freed original before scene exit, making release counter0 valid; initial verifier wrongly expected1, no game error. Focused follow-up explicitly restores original lookup after measurement, verifies present, forces limit1/trim (held144506880 to0/drop1), then exits: lookup absent/release1/ownerfalse/228.259MiB. lifecycle-verification.json confirms actual edge. This extra restore is outside measurements and is not natural reuse evidence.

All three jobs terminal/clean; owners2936files unchanged each, loaders/adapters restored byte-exactly. Initial documentation write encoding error corrected with explicit UTF8. No full export.

## Next action
Direct bounded caller/frame attribution of historical redraw discrepancy; repeat before admission. Broader rendering/preparation reduction still required for60FPS. Original bugs, loading, endurance/transitions, targetPC/M1, signing/notarization and frozen packages remain open. Critically low disk: avoid large captures/exports, reclaim only verified disposable duplicates with ledger.
