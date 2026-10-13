# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: bounded costly-sheet reuse

## Objective and acceptance

Continue full PC/Mac readiness. Reduce repeated large uploads while preserving original texture objects/pixels/dimensions/UVs/filtering/layer order, simulation and owner data. Require matched runtime, memory, visual and lifetime evidence before admission; no publication.

## Accepted decisions and constraints

Keep the one-sheet prototype private. The256MiB ordinary cache remains unchanged. Retain only the measured hot South mining body in its loaded session, using a2/3GiB scene limit and64MiB margin; no global cache enlargement, permanent visited-asset ownership, resampling, palette shader, compression or art change. Original source and trial pack preserved when creating a separate cleanup variant.

## Current state

Aligned upload cost ranking: South mining body5uploads/689MiB cumulative raw/69.322ms API in prior diagnostic, highest measured path cost; South effects next. New private `hot-sheet-motion.gd` holds the original ImageTexture, allowing existing weak restore to reconnect it after ordinary eviction. Owner exit uses a generation token so an older scene cannot clear a newer scene's lease. Additional stats record acquisition/reuse/drop/release without GPU readback.

Two actual matched pairs, same immutable candidate pack hash0cd2881f58db07ebdb904eb4e2fea2192f80b4a2865942c067dae3a924f62140:40rooms and synthetic12rooms (not historical reported station), four crew,9×180frames, explicit completed-driver upload indices. Early loader overlay ensures the actual module executes in both control and candidate. Only retention enabled differs per pair. Small fixture keeps normal placement/reserves/crew/drone flow but12rooms and8powered-room minimum; all fixtures' free-building/failure flags remain test-only.

## Verification

Native original prototype15checks/0failures: exact original texture/RID, no duplicate allocation, survival after lookup eviction, no new upload on restore, pixel/source immutability, owner release, newer-session protection, disabled control and insufficient-budget refusal.

40room: hot uploads5→1, raw722,534,400→144,506,880bytes (551.25MiB avoided), API76.703→12.934ms. All sampled uploads288→284; raw total9505545708→8927518188bytes; API898.980→868.104ms. Actual4reuses,1acquisition,0budget drops. Peak2348.739→2411.622MiB (+62.882MiB), below3072; exit228.259MiB equal, extra owner/reference released. Means7/9better/p955/9better, mixed/stillfails. All compared crew/drone/door/light/power-count/zoom states equal. Final4xzoom prop counters19214→19216advances and117531→117544live draws: familiar two/thirteen discrepancy unassigned, not closed or waived.

Synthetic12: hot uploads3→1, raw433,520,640→144,506,880bytes (275.625MiB avoided on that path), API47.000→19.355ms. Total sampled uploads183→183 because other paths offset counts; raw total5065777072→4873101232bytes; API496.694→488.668ms.2reuses/1acquisition/0drops. Peak1848.369→1971.445MiB (+123.076MiB), below2048; exit228.259MiB equal. All compared states and prop counters equal. Means5/9better/p958/9better but maxima55.321→58.324ms; stillfails. One pair per size does not establish robust FPS benefit, endurance, target hardware or Mac acceptance.

Further lifecycle audit found the prototype can leave its restored ordinary lookup alive after the memory guard drops the extra reference. Separate `hot-sheet-motion-drop-guard.gd` tracks the original texture weakly and releases its restored lookup on exit even after a budget drop; leaves an unrelated later texture untouched. New native19checks: old prototype1failure at this edge; corrected variant0failures. Initial fixture inferred WeakRef from Variant under warnings-as-errors; corrected explicit type, failed log retained. Corrected cleanup variant has not yet run the actual workload and must not inherit the predecessor's full runtime acceptance.

All accepted logs clean/jobs terminal. Every owner fingerprint2936files unchanged; actual adapters and early loaders restored byte-identically. Native source metadata/pixels unchanged. Large report legacy key `settle_budget_deferred` holds hot stats due runner-template reuse; comparison explicitly treats it as hot-before-exit. Small report uses `hot_before_exit`; no scheduling patch applied in these trials.

## Storage and evidence

Recovered32.736MiB from261 compiled `.cache` files in explicitly mapped completed scratch shader folders, with resolved-path/hash ledger. Original inputs, reports, layouts and captures retained. Later disk reached3MiB; verified obsolete ordinaryQA EXE equals retained release SHA7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76,109283328bytes, and reclaimed that duplicate only. `output/crew-release-2026-10-07/qa/PACK_RECOVERY.json` now explains restoring both EXE and PCK before ordinaryQA use. Private bootstrap, QA diagnostic engine, retained release and frozen sources untouched. Free space recovered to~105MiB before final native probes. No hardlinks/shared mutable release inputs.

Evidence under `output/renderdoc-tools-2026-10-08/{hot-sheet-native,hot-sheet-release-corrected,hot-sheet-small-trial,hot-sheet-drop-old-native,hot-sheet-drop-guard-native-corrected}` plus ranking/comparison/generators/source variants and storage ledgers. Initial release generator matched multiple scene insertions and stopped before launch/mutation; constrained initial scene insertion, corrected directory retained. No normal source/art change, export or upload.

## Next action

Run the corrected cleanup variant through actual12/40 workloads/lifecycle. Explain the final4xzoom two/thirteen redraw discrepancy with bounded room clock/visibility/caller events; previous intrusive observers' non-reproduction is not closure. Repeat matched performance after that, accounting for the memory tradeoff and unchanged upload-heavy first use. Broader drawing/preparation, all original bugs/loading/endurance/targetPC/M1/signing/notarization/package gates remain open.
