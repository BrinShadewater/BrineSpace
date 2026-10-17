# Initial drawing and deferred UI investigation plan

> Use superpowers:executing-plans and systematic-debugging. One final read-only fresh-context review.

**Goal:** Attribute the 0.9–1.6s post-setup gap and benchmark loading without changing appearance/crew behavior or any frozen build.
**Spec:** Owner's request and docs/CURRENT_STATUS.md / docs/LOADING_VARIANCE_2026-10-16.md.
**Architecture:** Start with external CanvasItem/node/render observers on the exact frozen53f release PCK. Compare counters within the same performance-monitor epoch so resets cannot produce false costs. Calibrate notification ordering on this native engine. Use source clocks/one narrow candidate only if the observation justifies it; diagnostic timings never replace actual-release headline runs.

## Constraints and review focus
- Scratch APPDATA/user-dir for every Godot process; owner fingerprint before/after, no concurrent Godot and no minimized timing.
- Matching d3 Windows/Mac, all previous candidates/source snapshots stay frozen. Preserve prior124 delivery identities, 20GiB disk reserve and normal gameplay flags.
- Whole-path raw-art loading, crew behavior and visuals unchanged. No speculative refactor, commit, publication or Mac rebuild.
- Draw-signal spans include callback/engine overhead; only same-epoch grid counters are draw-method attribution. Root profile stages can overlap nested work and are not GPU timings.
- Deferred markers establish ordering, not function CPU costs. Probe overhead and Dummy audio limit scope. Repeat/fresh profile and order must be explicit.

### Task1: Fine attribution
- [x] Preserve identities/owner and prepare one physical53f QA copy.
- [x] Calibrate native draw signal order, then run fresh/repeat New and Continue observers.
- [x] Locate expensive passes/functions; distinguish draw counter time from residual/deferred UI work.

### Task2: Evidence-led action and loading comparison
- [x] Apply only a justified narrow optimization in a separate candidate, or record why no runtime change is justified.
- [x] Run actual-release title loading again with unchanged primary fixture and explicit fresh/repeat inputs; report paired effects only if comparing builds.
- [x] Verify full crew signatures, normal simulation, cache release and representative actual screenshots; add focused regression/visual checks if production changes.

### Task3: Final review and handoff
- [x] One fresh-context evidence/code review; address material findings.
- [x] Verify124 frozen files and all player fingerprints; remove only verified task-owned QA binaries.
- [x] Record accepted conclusions/limits and next action in CURRENT_STATUS, report and concise handoff.

## Ledger
Task-owned output/first-draw-20261016 and D:/bs-first-draw-20261016. Existing dirty workspace retained. No runtime edit planned before evidence. Reuse immediately preceding124 frozen delivery hashes for initial stat baseline; final hash verification required. User's matching d3 pair and53f remain immutable. No full-source copy/export unless a justified change needs one.

Task1 complete: native calibration confirms draw signal precedes scripted _draw. Two calibration attempts stopped before capture at scratch-path guard (fixed empty-project custom name); all owner fingerprints unchanged. First game probe excluded by legacy guard's empty-path row for its own PID120800 (scratch report confirms). Four fine2 protocol-valid probes retained but superseded for attribution: monitor.frames resets each bucket, and retained terrain children were missing from draw callbacks. Fine3 stopped on diagnostic-only indentation parse error before timing; fixed and check-only passed. Corrected fine4 uses monotonic monitor.last_usec, adds consumed last_draw_timing across observed resets, observes all grid descendants, and reconciles cumulative gap counters. Four corrected traces valid. New gap932–962ms /draw853–888ms; Continue1596–1600ms /draw1498–1499ms. Residual74–101ms includes untracked UI/engine/observer work. Root seabed524–532ms; Continue first retained floors270ms/walls181ms. Extra New-ready-to-uncover1.09–1.19s includes798–803ms derelict pass. Cache inventories add66/70 entries; this does not isolate decoding versus geometry/upload.

Ruling: no production fix/export this profiling pass. Targets are now specific initial environment/structure/derelict preparation; moving the startup timer, suppressing draws or speculative UI changes would not demonstrate a real gain. Source initialization work still needs bounded preparation/decoder design and pixel-parity controls before changing it.

Task2 loading: eight unchanged-primary-fixture runs on frozen53f, two fresh/two repeat per mode. Six passed legacy guard; seventh excluded for another own exiting PID129416 empty-path observation. Kept those six valid runs, retried rejected fresh profile in a new scratch directory and ran final repeat. Task-local monitor now binds actual Popen Windows process handle and rejects every other Godot PID (including second copy inside QA directory); four pure guard regressions red→green. Two native bound-guard runs pass without a missing-path observation, so exact native race reproduction remains unclaimed. Original failed records retained. Original8 schedule and final schedule both saved. New normal site seeds vary per launch; Continue restores seed2808620329. Do not describe New fresh/repeat as identical geography. No performance gain comparison in this unchanged-build task.

Task3 complete: full crew identities/normal flags/simulation/cache/error checks pass for all12 final-cohort visits, actual station and card-crop visuals reviewed. Fresh reviewer independently reconciles four counter traces and eight raw primary reports/crew data, no material findings. All124 frozen delivery hashes and2948 protected player files verified unchanged; main/grid/dressing working-source matches frozen53f. Verified owned duplicate cleanup removes3,738,363,642bytes (3.482GiB); canonicals/evidence/helpers/restoration map retained. Final C:/D:115.593/41.150GiB free; no game process, no production edit/export/commit/publication. CURRENT_STATUS, detailed report and concise D:/bs-first-draw-20261016/HANDOFF.md record accepted conclusions, limitations and bounded initial environment/derelict preparation as the next target.
