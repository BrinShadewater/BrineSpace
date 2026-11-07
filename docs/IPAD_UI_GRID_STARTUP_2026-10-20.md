# iPad UI/grid startup cache capacity — October 20, 2026

Accepted validation build **brinespace-7bf9bbc621fc24cc**, installed on iPad13,18 (A14/4 GB), iPadOS27.2. This is a scoped loading fix; not release clearance.

## Identity and rollback

- Checkout `/Users/Shared/BrineSpace-native-validation-20261017`; branch `codex/ipad-memory-placement-2026-10-17`; HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus preserved accepted dirty work.
- Source fingerprint `7bf9bbc621fc24cc66d6f2a2992101167cbddf62ca65911eed6b92a6370d1dde`.
- PCK `4f0ec60870b1b8a3830c786ffcfc7828835a6c6faf0c7ff4d40a63b7d4e01852`; signed executable `5c1e4871429e70b22def1d1278688cc0cfa399adbe211704f3d802c1bc91e930`.
- Full signed candidate/export/evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261020/ui-grid-startup/candidate`. Bundle `com.shadewater.brinespace.nativeoptimization20261017`, native sampler on-demand-vm-tags-v1 unchanged.
- Protected complete **f729 + VM1** rollback remains in `/Users/Shared/BrineSpace-ipad-optimization-20261020/floor-vram-trial`; its signed executable/PCK were rehashed and remain exact. Source, original artwork, saves, recovery donors and frozen Mac/Windows releases remain protected.

## Cause and change

Native inner timings and physical per-actor counters identify crew-frame preparation inside `interface_and_grid`, rather than button layout. The old file-count ceiling was8192 (8191 entries observed after trim), while four actor banks require8262 prepared files. The device index held142,462,092 bytes, below the192MiB budget. Sequential reuse evicted the next required files: an unchanged diagnostic repeat rebuilt all8262 PNG preparations with zero disk hits.

`prepared_cache.gd` raises only the file-count ceiling to16384. The192MiB disk budget,2MiB metadata index,4MiB entry/16MiB raw validation limits, checksum format, four-job decoder window and bounded writer remain unchanged. No additional decoded Images/textures are retained. Old builds can reject/rescan/trim this disposable cache; saves do not depend on it. `grid_canvas.gd` records per-actor manifest/finish/adoption times and scalar batch counters; `loading_transition.gd` includes them in the startup profile. No gameplay, original pixel, audio, save-schema or desktop loading-policy changes.

## Physical evidence

Same paused cycle69 checkpoint,56 rooms/four crew, normal costs/caps/hazards, same viewport and retained disposable cache:

| Load | UI/grid | Total station setup | Crew PNG rebuild jobs |
|---|---:|---:|---:|
| Old diagnostic repeat df7230 |9.011s|15.915s|8262|
| New first install load |3.579s|10.000s|70|
| New same-process repeat |2.499s|6.448s|0|
| New fresh-process load |2.795s|9.282s|0|

The new repeat and restart each hit all8262 files. Final index8262files/143,356,868bytes (~136.7MiB) fits the unchanged byte budget. Same-process repeat UI/grid72.3% lower; setup59.5% lower in this ordered comparison. OS-purged/first-ever cache still requires preparation. Fresh-process restore remains4.200s and surface staging1.529s; first redraw and title-return stalls are not cleared.

Latest sampled large-station footprint old repeat2.312GB, candidate repeat2.237GB/fresh2.224GB (decimal). These ordered samples are affected by allocator/cache history and do **not** establish a fixed RAM saving, growth/leak clearance or a new long soak. Pending decoded-image bytes remained0; decoder window4. Existing floor ETC2 policy remains enabled.

## Validation and owner protection

- New real-admission9000entry regression failed on the old limit (working set/oldest frame eviction), passes with this change. Restart/index recovery, checksum/corruption, exact pixel payloads, writer/worker bounds and independent byte-pressure eviction covered.
- Nine actual-PCK native suites pass: capacity, index, workers, writes, floor VRAM31checks, large art lifetime43checks, shared floors, session art26checks and material18checks. Isolated profiles/finally guards preserve the real Mac owner profile.
- Raster audit36191assets, source audit439selected/433extras: no mismatches; strict signing passes; signed PCK equals exported/audited PCK. Four temporary export configuration files restored exactly.
- Actual physical card select/return clears placement controls. Save→title→Continue→Save preserves full gameplay state and exact timer;4× manually reselected after Continue's existing1× reset. Final normal launch has errors0, cycle64/seven rooms paused4×, menu closed.
- All five original saves/sidecars restored SHA-exact after final launch and independently recopied/rechecked. Local private saves are under `candidate/immediately-before-install`; they are not committed as evidence.
- Harness corrections: initial parallel pack-test start raced scratch-directory creation; runner now creates its own directory. Owner acceptance originally demanded inspector text `No Selection`, but returned-card/terrain inspection can remain without an active blueprint; acceptance now checks actual placement controls. These were harness assertions, not product fixes. Intentional diagnostic process stops can produce the existing unclean-close notice; no spontaneous crash observed in these checks.
- Read-only scoped review reported no actionable findings. No new long active soak, empty-cache speed claim or release clearance. All older unrelated dirty work remains preserved.

Portable aggregate evidence: [ui-grid-startup](ipad-memory-placement-evidence-2026-10-20/ui-grid-startup). Next separate the remaining fresh-process restore (~4.2s), first redraw/upload and title teardown costs; maintain quality gates and measured memory attribution.
