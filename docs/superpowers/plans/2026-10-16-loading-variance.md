# Loading variance investigation plan

> **For agentic workers:** Use superpowers:executing-plans for this bounded diagnostic investigation. One fresh-context evidence review at the end.

**Goal:** Explain the mixed New Loop/repeat observations as far as evidence allows, and benchmark the existing frozen Windows candidates again.

**Architecture:** Inspect profile and stage boundaries first. Compare the actual 688 and 53f release PCKs using the unchanged title-driving fixture, balanced run order, explicit input fingerprints and replicated fresh/repeat pairs. Add diagnostic-only controls only where needed; no speculative runtime changes.

**Tech Stack:** Godot 4.7.2 native Windows release, Python QA orchestration, SHA-256 identities.

**Spec:** Owner's current request; constraints and prior acceptance in docs/CURRENT_STATUS.md and docs/ROOM_ART_LOADING_2026-10-16.md.

## Global constraints

- Matching d3 Windows/Mac, all source snapshots and previous Windows candidates stay frozen.
- Preserve game appearance and crew behavior. No production edits without causal evidence.
- Every process uses scratch APPDATA and BRINESPACE_TEST_USER_DIR; fingerprint player files before/after.
- Serial native 1600x900 screen 2 runs; reject minimized windows or concurrent Godot processes.
- Maintain 20 GiB disk reserve; remove only verified task-owned duplicate binaries after QA.
- Fresh profile is not cold OS cache. Retain every valid observation, including slow runs.

## Review focus

- Repeat profile mutation: record exact input/output file fingerprints and learned-order changes.
- Build-order effects: alternate A/B and B/A, distinguish session drift from candidate differences.
- Phase attribution: quantify stages before the changed room-art code, target stages and residual time.
- Reentrancy/cache history: distinguish production observations from any instrumented diagnostics.
- Acceptance scope: preserve full crew signatures, checks, screenshots, frozen deliveries and player data; avoid statistical or visual claims beyond coverage.

### Task 1: Input and timing audit

- [x] Record owner/frozen identities and baseline process/storage guards.
- [x] Inspect old profiles, learned order and current startup boundaries; record hypotheses.
- [x] Set up two physical release QA copies with unchanged primary fixture.

### Task 2: Balanced actual-release comparison

- [x] Three matched fresh-profile pairs per mode/build, each followed by a repeat; 24 serial launches, alternating build order and visit order.
- [x] Record complete profile fingerprints before/after, all timings, crew identities and guard results.
- [x] Analyze paired deltas, within-build spread and phase attribution; use a bounded follow-up control only for an unresolved concrete hypothesis.

### Task 3: Review and handoff

- [x] Review representative saved native screenshots and all crew identity comparisons.
- [x] Request one fresh-context read-only evidence review; resolve material findings.
- [x] Verify owner/frozen identities; safely remove duplicate QA EXE/PCK files.
- [x] Record conclusions, limits, changed files and next useful work in CURRENT_STATUS and a concise report/handoff.

## Ledger

2026-10-16: Diagnostic work in task-owned output/loading-variance-20261016 and D:/bs-loading-variance-20261016. Existing dirty workspace retained; no runtime edit, source snapshot or export planned. Prior 20 observations remain evidence. Hypotheses pending profile audit: first-machine/session drift, learned-order differences, and pre-room setup variation. No attribution accepted yet.

Task 1 complete: 124 frozen delivery identities verified; player baseline 2,948 files. Old paired learned manifests byte-identical (New 12,762 requests /12,690 unique; Continue 13,360/13,286). Two physical canonical QA copies, unchanged primary entry fixture. No concurrent Godot process, reserve maintained. Scratch reports examined: post-timing identity scan triggers capture; no evidence it precedes timed completion.

Ruling: add four unchanged-fixture same-build fresh New controls after the 24-run cohort, because all three completed fresh New pairs have a slower second launch regardless of which build runs second. Then six external read-only draw/node-ready observer launches to attribute ~1–1.6s residual outside named stages. This is diagnostic follow-up to concrete unresolved concerns, not expanded release acceptance. Observer runs are separate from headline timings; no production script overlay or export.

Task 2 primary complete: 24/24 valid, all full crew identities and learned orders match. First Continue gains in all three pairs (222–433ms); New/repeats directions mixed. Same-build New controls second-minus-first A=-98.796ms/B=+195.929ms: a consistent order effect is not reproduced. Reporting now uses median matched-pair effects as primary; independent group medians remain descriptive. Three statistical regression checks red (missing helper) then green, including actual marginal/paired sign reversal.

Ruling: observer follow-up is eight rather than six runs, adding fresh Continue for an observed higher private-memory peak (B 2,710–2,812MiB vs A 2,632–2,643MiB in this cohort). Observer QA adds five seconds of normal simulation strictly after all timed measurements, original identity scan and original screenshot. This is a short residency diagnostic, not a leak/soak certification. Original primary fixture and all production PCKs remain unchanged.

Investigation complete: 36 valid launches, same complete crew identities within mode, common learned orders and frozen checkpoint/layouts. Observer gap New908–965ms/Continue1,586–1,626ms after setup and before render-pre; exact cause remains open. No production fix justified. Higher first-Continue private peak reverses in diagnostic fresh pair; original high samples retained. Native station/actual card crop review passes (whole-image viewer omitted A cards, actual PNG crop contains them). One final fresh-context review found no material issue; resolved minor audio wording to silent/Dummy `_ready` only. No new runs for documentation clarification. Final124 frozen hashes and all2,948 protected player files verified unchanged; duplicate cleanup in progress.

Finalization complete: task-owned duplicate binaries removed7,476,727,025bytes (6.963GiB), canonical sources/exports retained with restoration map. Final C/D114.982/41.252GiB, no game processes. Report, CURRENT_STATUS and D:/bs-loading-variance-20261016/HANDOFF.md updated. No production edit, commit, publication or new export. Remaining exact pre-render attribution, transient memory behavior, native Mac and release performance gates remain explicitly open.
