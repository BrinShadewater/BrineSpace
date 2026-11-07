# Initially visible artwork preparation — October 16, 2026

Separate Windows candidate **brinespace-3a0ae1af0283fa01** prepares the generated-site environment and opening companion room views while the existing startup decoder is active. The matching d3 Windows/Mac kit and previous53f remain comparison targets. No assets, draw routines, crew/navigation algorithms, save schema or normal gameplay flags change. This is scoped loading evidence, not release promotion, a 60FPS result or native Mac acceptance.

## Package and source

- Source: `D:/bs-visible-art-20261016/source`, **61,632 selected files**, based on frozen53f plus this task. Source/dependency fingerprint: `3a0ae1af0283fa01621fdeac2dc5519ed042894f7aa11e3a3b092ebf50ac4ac3`.
- Windows: `D:/bs-visible-art-20261016/windows`; PCK SHA256 `fdb06cdb4782730ab0a149eac05e86894542cf8ce65dd52b49174bd5463bbd7b`. Same release EXE `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`.
- Same **36,430 dependencies**, **35,942 assets**. Exact packed asset audit: zero missing/changed/remapped/unexpected. Packed source audit: selected431 +extra frozen421, zero unexpected/failures. Manifest delta is exactly `scripts/main.gd`, `scripts/grid_canvas.gd`, `assets/environment/seabed-v1/seabed_background.gd`; no added/removed runtime dependency.
- New focused tests +paired UIDs and index; existing decoder test switches four obsolete fixture images to maintained PNGs already in the package. Input/source-selection records and all raw results remain in the evidence folder.

## Preparation and boundaries

`main.gd` adds one measured `initial_art` stage before the existing startup-complete flag. The grid wrapper runs only while title startup decoding is active, preserving lazy direct/headless scenes. It calls the existing seabed factories, then prepares uncleared companion room views intersecting a predicted station-centered opening view with the existing half-cell margin. No draw is suppressed and no camera, container layout or simulation frame is advanced.

The seabed announces exact existing source paths to the bounded decoder, prepares the environment groups that the generated-site renderer already consumes, and preserves local placement RNG, geometry and animation clocks. Learned repeat manifests remain authoritative; this creates no second image cache. Legacy empty-layout studies stay lazy.

New Loop containers have **zero size during synchronous `_ready`**. Until layout resolves, the viewport supplies a conservative cover of the eventual scroll area. This can warm a companion just outside the final scroll area; eager room work remains bounded to the **three existing companion room types**. The final New captures show brine plus salvage workshop/storage/cryo views prepared before first presentation; the earlier prototype captured only brine. Existing draw-time configuration, doors, warnings and animations remain live.

## Actual release loading

**16 accepted processes**, two A/B pairs per entry/visit, order reversed in the second round. Same actual release title/buttons/dialogue adapter on both packages, native visible secondary display,1600×900, Dummy/silent audio. New uses the existing pre-ready `site_seed` metadata hook, **1928894317**; Continue restores original checkpoint **2808620329** on every visit, clears the task-owned comms sidecar and preserves learned image order on repeats. Critical profile inputs and complete crew identities match within mode. The ordinary randomized New path has a separate passing smoke visit.

Times start at the New/Continue action, not executable launch. Fresh profile is not cold OS cache; OS caching remains uncontrolled. New site geography is fixed for treatment comparison; this does not claim all gameplay RNG is fixed. Readiness and loading-screen disappearance are both retained. Table values are medians of two observations; percentages/deltas are medians of the paired effects.

| Entry | Startup ready A → B | Loading screen gone A → B | Paired uncover delta |
|---|---:|---:|---:|
| New / first profile | 5.616 → 5.634s | 6.740 → 6.384s | -356.1ms / -5.27% |
| New / repeat | 5.267 → 4.987s | 6.396 → 5.682s | -713.9ms / -11.30% |
| Continue / first profile | 7.618 → 7.037s | 7.650 → 7.065s | -585.5ms / -7.59% |
| Continue / repeat | 6.521 → 5.981s | 6.545 → 6.003s | -542.2ms / -8.28% |

All **eight paired uncover comparisons are faster**. First-profile New readiness changes direction between pairs: paired median **+18.0ms/+0.37%**, effectively mixed/flat in this small cohort. Repeat New readiness median−280.6ms; Continue first−580.4ms/repeat−539.8ms. No general fresh-New readiness gain is claimed. New uncover ranges A6.712–6.767s →B6.223–6.544s; repeats A6.259–6.534 →B5.141–6.223. Continue first A7.458–7.842 →B7.055–7.074; repeat A6.529–6.562 →B5.996–6.010.

Measured B `initial_art`: New fresh555–603ms/repeat308–367ms; Continue fresh144–145ms/repeat59–63ms. Moving work before readiness is not itself the gain: the uncover endpoint independently improves. Small two-pair cohorts and desktop variability limit generalization. No startup-bootstrap, audio-device, FPS, placement/zoom pacing or endurance acceptance is added.

## Memory and cleanup of startup work

All primary visits pass explicit checks that decoder tasks/results/recent images/path order are empty and inactive after loading. Maximum observed pending jobs remains96, compression window remains8 and recent-image budget16MiB. A job-count limit is **not a decoded-byte cap**.

There is a memory tradeoff in repeat New: decoded peak **56.8–58.3 →237.48MiB**; sampled whole-process private peak **2,134–2,147 →2,192–2,287MiB**. These private peaks include post-timing crew identity/visual QA, not just startup; no precise startup RSS delta or memory improvement is claimed. New fresh private peaks A2,120–2,157/B2,160MiB; Continue fresh A2,642–2,657/B2,603–2,673; repeat A2,655–2,660/B2,641–2,667. Continue repeat decoded peak remains214.23MiB. The short cohort is not a leak/residency soak.

## Verification and retained attempts

- New preparation regression red(two missing methods)→green, plus inactive-wrapper and zero-layout visibility regressions red→green. Idempotence, unchanged generated/recovery input, offscreen/cleared selection and job/cache release checked.
- Native environment **18 checks /12 exact-pixel presentations**: two sites, overview/close views, three clocks. Native loading transition passes; existing room geometry/pixels **117 checks /56 presentations** pass. Overview/detail artifacts inspected. Subsequent wrapper changes only gate/choose preparation; inner environment/room rendering is unchanged. Actual packaged screenshots are retained.
- Existing image-prefetch and room-art-prefetch checks pass; release assertion safety2/2. The decoder test intentionally exercises one missing image warning. Full crew lossless-source/clip/metadata/timing/filter/historical-bank identities match across the primary cohort within entry mode; normal simulation/flags and missing-art/engine/script checks pass.
- First focused fixture had a parse error, then an invalid manually attached scene emitted null-current-scene errors despite a PASS marker. Both are rejected; final selection tests use the real Grid with input-only state. Obsolete decoder fixture paths and same-profile fresh-manifest assumptions were corrected; failed records remain.
- Export254 was superseded before measurement by the inactive-wrapper boundary fix. Export186 has **16 valid environment-only comparisons plus normal New smoke**, but captured zero-size startup and missed companion preparation. It is retained under `environment-only-186` with raw results, package metadata, exact runtime fragments, inputs and rebuild provenance. Its median paired uncover effects were New fresh−8.29%/repeat−5.76%, Continue fresh−6.70%/repeat−8.24%. Those are a separate cohort, not a direct randomized comparison against3a. Obsolete fine diagnostics were explicitly skipped. Verified unaccepted intermediate binaries were removed; no protected delivery was included.
- Existing frozen-build RefCounted/ObjectDB exit warnings remain outside this patch; passing runtime error checks are not an overall leak-free claim.

## Drawing attribution and final integrity

Four corrected A/B observers use the same controlled New site and original Continue checkpoint. They reconcile monotonic/reset-aware cumulative grid counters and retain complete intervals; headline runs have the observer disabled.

| Diagnostic | Setup-last-ready → render-pre A → B | Instrumented grid methods A → B | First root seabed stage A → B |
|---|---:|---:|---:|
| New | 957.101 →291.144ms | 878.720 →216.580ms | 524.801 →1.090ms |
| Continue | 1,622.316 →1,032.847ms | 1,518.185 →933.564ms | 536.201 →1.418ms |

New observed-ready →uncover shrinks **1,088.545 →749.637ms**; its later derelict pass falls **808.799 →347.507ms**. Preparation therefore removes substantial first-use work but does not eliminate remaining material/geometry/render submission. Continue's tail is35.641 →24.661ms. Sampled newly appearing texture-cache entries after setup fall66→6 New /70→10 Continue; these are cache entries, not unique PNGs or residency bytes. Residual/unclocked UI/engine/observer work remains. Root substages overlap, counters include diagnostic overhead, and none measures GPU execution or isolates every decode/upload/mesh cost.

All **21 final visits** (16 primary +one ordinary New smoke +four diagnostic) have matching complete crew identities within entry mode and clean runtime/art/normal-flag/cache checks. Actual packaged New/Continue images were inspected. A fresh-context read-only reviewer independently reconciled the raw timings, diagnostic counters, crew identities and images and found no material issues. Review: `D:/bs-visible-art-20261016/review.md`.

Final integrity checks verify all **124 protected delivery hashes** and **2,948 protected player files unchanged**, with no game processes remaining. The separate candidate's EXE/PCK match its export identity. Verified task-owned QA duplicate removal recovered **7,476,730,545 bytes (6.963GiB)**; canonical source/Windows deliveries and evidence remain. Final free space: **C:115.681GiB / D:29.193GiB**. Results and cleanup records: `D:/bs-visible-art-20261016/final-guards.json`; concise handoff and retained helper copies are in the same evidence folder. No commit, publication, release promotion or Mac rebuild was performed.

The matching d3 Mac ZIP remains the owner’s native Mac validation target. Initial retained floor/wall drawing is still a separate measured loading cost; byte-budgeted decoding and longer memory sampling remain useful if repeat-New memory becomes a constraint.
