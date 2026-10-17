# Initial Windows loading — October 16, 2026

Separate **brinespace-3f477ebdff56bced** reduces first-profile loading by **37.10% for New Loop** and **33.44% for Continue** in this comparison. The existing matching d3 Windows/Mac deliveries remain frozen; no promotion, commit, upload or new Mac export.

## Measured cause and change

Normal startup already had bounded image prefetch, but it depended on the previous launch's `startup_images.txt`. A fresh profile therefore decoded crew PNGs on the main thread even though each completed crew batch already knew its surviving paths. Compression-worker waits were tiny compared with PNG loading.

An unchanged d3 PCK experiment isolated this: fresh profiles without/with a scratch pre-seeded order took **9.985→5.654 s New Loop** and **12.362→7.176 s Continue**. Summed crew PNG-loader wall time fell from about 5.55 s to 0.86–0.88 s; compression-worker waits rose from 13 ms to 741–781 ms as work overlapped. This experiment is attribution evidence, separate from the candidate results below.

Only two runtime files change:

- `scripts/image_prefetch.gd`: accept a batch's deduplicated surviving paths only when there is no learned order. Priming performs no decoding or synthetic requests. Keep the first-launch indeterminate loading indicator; retain the learned order on repeat launches.
- `scripts/crew_storage/worker_batch.gd`: announce surviving paths before the existing bounded worker loop. Do nothing extra during ordinary gameplay or when a learned order is available.

No asset list, texture format, sampling, animation, AI, checkpoint schema/admission, normal costs/failure flags or room drawing changes. `tests/test_image_prefetch.gd` adds the regression, including the actual compressed-batch caller; its existing UID stays paired.

## Actual packaged comparison

Windows Compatibility/OpenGL, Godot 4.7.2 official, i7-13700KF (16 cores/24 logical processors), RTX 4070 Ti / driver 616.92, 1600×900 visible secondary display. Serial actual release processes, physical viewport input disabled, Dummy audio/silent. Use the shipped intro/title, actual New Loop/architect/Continue button signals and loading transition. Skip intentional film/transmission reading and acknowledge Continue automatically. Normal gameplay advances afterward, with free building and failure-disable flags false.

**12 valid runs:** two new scratch profiles per mode/build, then one repeat of profile 1. Alternate the fresh pair order. New Loop has one initial room; Continue restores the frozen reported 12-room checkpoint. This is not the synthetic 40-room FPS fixture. Scratch layouts and checkpoint are frozen copies. First-profile means no learned image order; OS filesystem caches were not controlled, so these are **not cold-boot certification**.

Button action to observable `startup_complete`, seconds:

| Entry | Profile | Frozen d3 | Startup candidate | Median reduction |
|---|---|---:|---:|---:|
| New | first | 10.142–10.208 | 6.120–6.680 | 37.1% |
| New | repeat | 5.442–5.442 | 5.349–5.349 | 1.71% |
| Resume | first | 12.304–12.938 | 8.214–8.587 | 33.44% |
| Resume | repeat | 7.128–7.128 | 6.968–6.968 | 2.25% |

Repeat rows have one observation per build, not a statistical performance claim. They exercise the unchanged learned-order path. No average-FPS or 60-FPS gain is claimed.

Until the station is uncovered (including automated Continue/render handoff), first-profile New Loop is **11.324–11.390→7.281–7.893 s**; Continue **12.324–12.964→8.235–8.618 s**. Timed loading stops before the full crew-identity diagnostic and screenshot work.

The largest measured difference is the grid/interface construction stage: first pair New Loop **7.466→3.361 s**, Continue **7.757→3.391 s**. Other first-pair work stays similar: New Loop interface artwork **0.462→0.468 s**, first room **0.142→0.146 s**; Continue restoration **1.896→1.882 s**. Summed crew PNG-loader wall time across fresh comparisons **5.56–5.79→0.72–0.84 s**. Source loading, manifest/metadata assembly, restoration and first presentation still cost time.

## Pixels, crew and memory

All **six paired comparisons** match complete crew-bank identities: compressed lossless source bytes, dimensions/format/mipmaps, frame order, wrapper metadata/filtering and timing/stride data, including both equipment and retained historical cargo banks. There are **8,262 immutable source objects across the four actors**. All repeats match within each entry mode. New Loop and Continue legitimately select different live Bill banks/timing in both builds: `bill_carry_player.restore_snapshot()` selects the saved binding, while a new loop selects the current master. Historical banks and the other actors match across modes. The initial analyzer incorrectly required cross-mode equality; its failed assertion is retained, and the corrected comparison requires equality within each mode.

The same **35,942 packaged assets** pass exact byte checks. Native loading/transmission and station/card captures were reviewed. A full-image preview appeared to omit cards; inspection of a crop from that same saved PNG confirmed all three were present. This was not a reproduced game defect. The extra short Continue follow-up matches all recorded hand-node geometry/visibility states and crew identities in both builds. Original captures and the diagnostic crop are retained.

No prefetch limit is enlarged: 96 images ahead, existing stale-window handling, eight crew compression jobs, and the existing **16 MiB/128-image recent cache**. Actual candidate first loads peak at **96 pending decoder jobs / 32.34–32.70 MiB decoded worker results**. Existing repeat Continue peaks at **235.58 MiB** in both builds because that order includes larger non-crew images. Every run explicitly verifies that workers, decoded results/recent cache and path lookup arrays are released after loading. Only diagnostic counters remain.

Windows private-memory sampling every 250 ms covers the complete QA process, including post-timing bank hashes and screenshots, and provides sampled lower-bound peaks rather than allocation-complete loading peaks:

- Fresh New Loop: **2127–2135→2148–2175 MiB**. A small temporary increase accompanies first-launch parallelism.
- Fresh Continue: **2594–2653→2587–2631 MiB**.
- First-profile texture-memory samples are equal within both modes: **1071.462 MiB New Loop / 1543.075 MiB Continue**.
- Retain the unequal primary repeat-Continue point: **1359.325 MiB baseline / 1543.075 MiB candidate**. These early samples are not settled residency measurements. A separate six-observation follow-up starts at **1543.247 MiB in both**, ending about five seconds later at **1562.007 / 1562.351 MiB** while gameplay continues. This is a short observation, not a memory-growth soak.

## Verification and limits

- Expanded prefetch regression: expected failure for the missing feature, then PASS. Exact pixels, independent returned images, live batching, deduplication, source sharing, pivot/alpha extent, learned-order preservation, scheduling limits and cleanup.
- `test_run_save`, `test_save_integrity`: PASS.
- Native `test_crew_loading_progress`, `test_crew_pose_cache`, `test_crew_router_pixels`: PASS. The generic native runner classifies `test_loading_transition` as headless-safe and skipped it there; a separate direct native invocation **PASS**, including reading/Continue resource freeze and replay behavior.
- Release assertion-safety Python checks: **2 PASS**.
- Maintained Windows exporter: PASS. **36,430 runtime dependencies**, only the two runtime scripts changed, no additions/removals.
- Empty-project exact PCK audit: **35,942 assets / zero missing, changed or unexpected**. Source audit: **431 selected +421 additional frozen scripts**, zero failures/unexpected.
- All 12 primary entry runs and the two settling follow-ups: zero captured engine/script errors and zero missing-art placeholders. Forced QA exits retain the same 34-ObjectDB warning in both builds; this fixture warning is not a new lifetime acceptance claim.

Initial fixture/setup parse failures and the cross-mode analysis assertion are retained separately. No timing sample was discarded. No new two-hour soak, large-station FPS/placement benchmark, physical input/audio certification, Mac run or signing/notarization check was performed. Prior release gates remain open.

## Frozen artifacts and safety

New full physical source and Windows candidate: **D:/bs-startup-20261016/**. Base Git commit `67e7db969f7c5d952a3c80830369715d703199c5` plus the recorded dirty source selection; Git HEAD alone does not reproduce this build.

- Build: `brinespace-3f477ebdff56bced`
- Source SHA256: `3f477ebdff56bced174334bee4e2df9e0551a36cc33bc7bd53ae95b3f81854dc`
- EXE SHA256: `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`
- PCK SHA256: `8cc744850b88af82c3e7a141d19961c6117c45c77d6e5bab707608ea3f2d835e`

All **2,948 protected player files unchanged**. All **106 files** in the matching d3 Windows/Mac checksum sets reverified unchanged, including both Mac archives. That preserved pair remains the owner's Mac comparison baseline.

Two verified task-owned QA EXE/PCK duplicate pairs removed (**6.963 GiB**); both canonicals, fixtures, profiles, captures, logs and `runtime-restoration.json` retained. Free space after cleanup: **C: 124.243 / D: 65.063 GiB**. No game left running. No owner assets/saves or prior release binaries deleted.

Evidence: `D:/bs-startup-20261016/loading-analysis.json`, `comparison-fixture.json`, `compare-*.json/.log/.png`, `settle-*.json`, `manifest-comparison.json`, exact audits and `final-guards.json`. Helpers: `output/startup-20261016/`. Primary fixture is preserved as `primary-entry.gd` beside each cleaned QA runtime; `entry.gd` contains the later settling observer. Restore only the mapped binary pair before reusing a QA folder, and select fresh output/profile names.

Next useful loading work is attribution of the remaining scene/script loading, crew manifest/metadata assembly and restoration costs. Keep the d3 Windows/Mac pair frozen; any Mac test of this new startup change requires a separate matching export and native validation.
