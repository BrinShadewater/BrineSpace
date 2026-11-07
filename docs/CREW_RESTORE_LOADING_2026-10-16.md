# Crew setup and checkpoint restoration — October 16, 2026

Scope: profile initial crew setup and checkpoint restoration on Windows, improve measured avoidable work, preserve appearance and crew behavior, and repeat the primary loading benchmark. Preserve the matching d3 Windows/Mac deliverables and the previous 3f Windows loading candidate. Evidence/helpers: `D:/bs-crew-restore-20261016/` and `output/crew-restore-20261016/`.

## Attribution

External clocks run over an overlay of frozen **3f477ebdff56bced** source, using the same 12-room Continue checkpoint and owner-layout fixture in scratch profiles. These are attribution measurements, not delivery timing or visual acceptance. The bootstrap verifies source hashes before instantiating the actual title/loading path. An initial missing bootstrap icon error was repaired; `profile-resume-1` is retained as a setup failure. Later clean runs and all original evidence remain available.

First-profile/repeat diagnostic observations:

| Work | First profile | Repeat |
|---|---:|---:|
| Manifest JSON read/parse | 119 ms | 119 ms |
| Manifest assembly | 847 ms | 681 ms |
| Batch finish, four crew | 1,632 ms | 1,729 ms |
| Final bank adoption | 24 ms | 24 ms |
| Apply checkpoint | 14 ms | 8 ms |
| Restore crew | 1,548 ms | 786 ms |
| Navigation room geometry | 1,381 ms | 615 ms |
| Local graph construction | 167 ms | 172 ms |
| Graph boundaries | 1 ms | 1 ms |
| Finish restore/UI | 298 ms | 141 ms |

Nested/overlapping clocks must not be summed. The checkpoint's active Bill graph has 3,167 points; small later rebuilds are about 4 ms. Room geometry includes first-use lazy room-view preparation and art reads, which explains much more of restoration than graph topology. One lazy-view trace found a **68.622 ms nursery initialization despite no nursery being placed**: the selector eagerly used nursery as a fallback before replacing it with the requested view.

The instrumented overlay's full crew signatures differ from the maintained production export for an unresolved reason. Consequently overlay signatures establish no pixel parity. Final acceptance must use the original primary fixture against the two maintained production PCKs. Clocks and local controlled experiments guide the changes only.

## Changes

- `scripts/crew_sprite_player.gd`: compute immutable manifest/clip values once rather than once per timing slot. Keep per-frame overrides, metadata setter order, independent wrappers, filtering, playback, furniture and mirrored poses unchanged. No retained cache is added.
- `scripts/grid_canvas.gd`: defer the nursery fallback until the selector actually needs it. Selected room views and unknown-room fallback remain identical.
- `scripts/crew_storage/worker_batch.gd`: prioritize compression/bounds jobs whose results are immediately consumed over speculative PNG prefetch. Keep the existing eight-job work window, 96 pending decoder limit, ownership and completion waits. No GPU operations move to workers.
- `tests/test_room_view_selection.gd` and paired UID, registered in `tests/index.json`: ensure representative room selection initializes only its chosen view and preserves fallback identity.

No art, navigation/AI algorithm, crew state, save schema/admission, gameplay flags or Mac deliverable changes. The candidate is a separate physical source selection over 3f; Git HEAD alone does not reproduce this dirty snapshot.

## Controlled checks

The selection regression fails two checks before the fix and passes afterward. A temporary initial fixture cleanup error is retained separately from that clean red/green result.

Metadata replay uses the actual 550-call manifest sequence, checks source JSON equality with frozen 3f, and compares **32,487 frame slots**, metadata, wrapper/filter type, timing, strides and gait groups: zero mismatches. Four alternating old/new passes give a median ratio **0.876** (12.4% lower assembly time); an original/original control gives 0.996 and correctly fails the local 10% improvement gate. This is a scoped headless experiment, not a CI speed budget or whole-game loading result.

Separate diagnostic priority trials reduce summed compression waits **469–573→93–103 ms**, with batch finish **1,632–1,729→1,512–1,556 ms**. Whole-load diagnostic differences are noisy; the final packaged comparison decides whether the combined candidate improves loading.

Five focused tests pass: room selection, sprite loading, image prefetch, run save and save integrity. Four native crew tests pass: texture batch (**76 checks**), router pixels, pose cache and loading progress. Native loading-transition coverage passes New Loop/Continue, exact restored reserves, gameplay pause during reading, explicit Continue and reduced motion/replay controls. Python release assertion safety passes 2/2. One fresh-context read-only review of the exact three-file difference against frozen 3f finds no actionable issues.

## Packaged comparison

Separate maintained-export candidate **brinespace-688bb7cf923bb512**, with physical source at `D:/bs-crew-restore-20261016/source/` and playable export at `D:/bs-crew-restore-20261016/windows/`. Source selection: **61,624 files**, only three runtime changes, the test index update and two new test/UID files relative to frozen 3f. Same **36,430 manifest dependencies**; exact audits find **35,942 assets**, **431 selected scripts/shaders +421 additional frozen scripts**, zero changed/missing/unexpected assets and no source failures. Neither diagnostic clocks nor bootstrap ship.

- Source fingerprint: `688bb7cf923bb512268137d1495f63f142c08e420cc43238f26bed046829814b`
- EXE SHA256: `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`
- PCK SHA256: `ae46e3e4e9139895c62db235fe37278248b66f4ac888a14129c0f54a39a83e23`
- Base Git: `67e7db969f7c5d952a3c80830369715d703199c5`, dirty full-source selection; use `source-inputs.json`, not HEAD alone.

The unchanged primary fixture runs **12 valid actual-release title/loading cases**, two fresh profiles plus one repeat per lane/mode, 1600×900, visible screen2, normal gameplay flags. Both orders are represented. Times are actual button action to startup complete, before post-timing identities/screenshots; intro/transmission are automatically acknowledged. All primary samples are retained.

| Entry/profile | Frozen 3f | Candidate | Observation |
|---|---:|---:|---|
| New Loop, first profile | 5.661–7.062 s | 5.438–6.353 s | 7.32% lower median; two pairs |
| Continue, first profile | 8.090–8.191 s | 7.927–7.939 s | 2.55% lower median; two pairs |
| New Loop, repeat | 5.058 s | 5.114 s | 55 ms slower; one pair |
| Continue, repeat | 6.594 s | 6.803 s | 209 ms slower; one pair |

The slower repeat triggered a separate four-run Continue follow-up with reversed order, reusing primary profile1. Both additional pairs improve: **6.956–7.030→6.809–6.845 s**, **147–185 ms** lower. One preceding follow-up launch began minimized and was rejected before recording a timing; its failure log is retained. The primary cohort is unchanged. This does not establish a consistent repeat regression or a general warm-loading speedup. Keep the fast original baseline observation. The scheduling change stays in the separate candidate because both first-profile pairs per mode improve, the repeat regression does not recur in the balanced follow-up, and correctness/worker bounds hold.

Primary compression waits fall **455–1,127→37–94 ms**, while PNG wait/decode clocks increase **697–803→954–1,365 ms**. Priority trades queue waits rather than eliminating all of them; whole-load gains are substantially smaller than the compression-wait reduction.

All **six primary pairs and two follow-up pairs match complete crew-bank identities**, including lossless pixels, metadata, filtering, timing and historical banks. New/Continue's intentional Bill bank binding difference is preserved. Normal simulation advances, no artwork/errors are logged, and workers/decoded caches/path arrays are fully released after loading. Continue screenshots and actual PNG card crops match visually. Full-image tool previews again omitted cards in one displayed preview; the original PNG crops prove that the card pixels are present. No game defect was reproduced.

OS cache is uncontrolled; profile first use is not a cold OS boot. New Loop timing variance is material. Windows memory is sampled every 250 ms across the whole QA process, including post-timing identities/screenshots, so peaks are lower bounds. First-profile private peaks: New Loop **2,105–2,150→2,116–2,126 MiB**; Continue **2,642–2,675→2,668–2,695 MiB**. Primary repeat New **2,107→2,138 MiB**, Continue **2,685→2,627 MiB**. Continue early texture totals match at **1,543.075 MiB**; New Loop early totals vary with live presentation. No steady-state residency or memory-soak claim.

First-profile decoder peaks **31.29–31.99→23.00–31.78 MiB**. Primary repeat peaks: New **57.56→58.31 MiB**, Continue **235.58→214.23 MiB**; learned orders also contain larger non-crew artwork. Both builds reach the same 96-pending-job maximum; compression peaks stay at eight. The recent-image cache retains its existing 16 MiB budget. The pending window is a job-count bound, not a fixed byte cap.

## Preservation and next work

All probes use isolated APPDATA, copied fixtures and owner-folder fingerprints. All **2,948 protected player files are unchanged**, and all **112 preserved delivery checksums pass**, covering the matching d3 Windows/Mac files and the 3f Windows candidate. Original canonical/source/ZIP files remain untouched. Verified task-owned temporary QA binaries removed **7,586,009,276 bytes (7.065 GiB)**; C/D free **124.102/53.257 GiB**, no remaining game processes. Final records: `D:/bs-crew-restore-20261016/final-guards.json`, `runtime-restoration.json` and Windows `SHA256SUMS`. Canonical source, export, fixtures, per-run samples, invalid attempts and restoration map are retained. No commit, publication, Mac rebuild or expansion of release acceptance.

Next useful loading investigation is first-use room-view art/geometry preparation during restoration. Preserve the existing crew/door/warning behavior and prove any future caching with native geometry/pixel/state checks. Native Mac, large-station 60 FPS, frame-pacing and endurance gates remain open; this task establishes no average-FPS improvement.
