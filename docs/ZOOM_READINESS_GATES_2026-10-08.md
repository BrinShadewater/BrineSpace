# Project handoff

Updated: October 8, 2026. Project: BrineSpace. Task: bounded zoom gate attribution.

## Objective and acceptance
Continue full PC/Mac readiness. Determine gate/viewport cause of historical two-advance/thirteen-live-draw difference before admission. Diagnostic timings are not FPS certification; no publication.

## Accepted decisions and constraints
Original readiness check called exactly once; wrapper records its result without extra prefetch calls. Preserve simulation/art/owner data. Candidate remains private. Cap256gate/view records, direct room events4096per room.

## Current state
New private direct-gate-grid.gd based on actual candidate/grid.gd; hooks zoom_waits_for_cover and sync membership. Records art/cover/bypass/covered, current/target zoom, asks/groups, viewport/scroll and edge room membership. New run-hot-guard-gating[-corrected].py and compare-zoom-gates[-corrected].py in output/renderdoc-tools-2026-10-08. No normal code/art change.

## Verification
Initial pair clean but baseline gate/view fields null: startup early overlay was overwritten by later crew-storage pack. Fixed lane loaded late overlay and recorded19gates/181views. Comparison rejects null evidence; cannot use initial baseline for gate comparison. Corrected runner reloads identical instrumented pack after crew pack in BOTH lanes. Corrected pair18gates/181views each, nine art waits/three cover waits, all gate fields and viewport/membership fields equal. All final prop counters equal19216advances/117544live draws/2196prepares/29467static draws. No gate/view cap reached. Owner2936same/adapter+loader byte restored for both jobs; all terminal/clean.

Same-PCK fixed-lane cross-run comparison proves readiness variability: initial art wait atframe3 versus corrected cover wait atframe3; initial starts cover at4. Initial total10art+3cover waits versus corrected9art+3cover waits. Pack SHA equal, output in corrected/cross-run-readiness.json. Despite this one-frame hold variation, both fixed runs have same final counters and edge membership. Therefore actual async art readiness changes zoom progression, but this is NOT sufficient attribution of exact2/13 difference from the prior direct trace. Do not close mismatch based on non-reproduction. Prior direct trace still proves bounds/membership-related work localized to Tidal(16,16)/Storage(24,16); total simulation clock match remains.

Corrected peaks2348.739/2411.622MiB, exits228.259MiB both; instrumented timings still fail and are not acceptance. Reclaimed8verified duplicate scratch reports23.732MiB; ledger direct-gate-report-reclamation.json, primary evidence retained. Initial metadata/null comparison failure retained. No full export.

## Next action
Controlled native zoom fixture with observable delayed art readiness and viewport-boundary assertions, plus compact target-frame tracing if needed; distinguish expected bounded camera hold from incomplete visible output before admitting reuse. Avoid repeated whole workload runs without a new discriminating check. Broader drawing throughput/preparation optimization remains necessary. Full original bugs/loading/endurance/targetPC/M1/signing/notarization/frozen-package gates remain open.
