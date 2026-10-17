# First-use room art preparation — October 16, 2026

Owner request: improve first-use room art preparation, preserve visuals and crew behavior, benchmark loading again, and keep matching Windows/Mac builds frozen. Baseline is the separate loading candidate **brinespace-688bb7cf923bb512**. Matching d3 Windows/Mac and prior3f/688 source/Windows exports remain read-only inputs.

Evidence: `D:/bs-room-art-20261016/`. Helpers: `output/room-art-20261016/`.

## Cause and change

Native clocks over frozen 688 room code attribute most initial preparation to sequential image decoding. Seven representative views are BRINE, Storage, Thermal, Life Support, Hydroponics, Research and Salvage. The first direct trace has ~424 ms pool decode, 58 ms alpha bounds and 27 ms uploads. Inherited donor textures already share a cache; no inheritance/room-data refactor is warranted by this evidence.

First-profile image prefetch knows crew batch paths, but not dressing images. Each dressing profile already names its complete texture set before it loops over synchronous acquisitions. **`rooms/whole-room/room_dressing.gd` now announces that authored list to the existing `ImagePrefetch.prime()` before acquiring textures.** Same bytes, keys, acquisition order, uploads and owners; worker decoding overlaps. The existing loader bounds, copy-on-delivery, progress pumping, cache release and learned repeat order remain authoritative. No new cache or retained CPU image is added; outside active first-profile loading the call has no effect.

One controlled native pair, with scripts preloaded before room clocks and all views retained in a shared pool:

| Seven-room first initialization | Frozen688 | Trial |
|---|---:|---:|
| Combined ready time | 745.547 ms | 481.958 ms |
| Pool decode/wait | 400.943 ms | 127.439 ms |
| Announced/worker images | 0 | 22 |
| Peak pending jobs | 0 | 7 |
| Peak decoded image bytes | 0 | 32.993 MiB |

This pair is attribution evidence, not a loading claim: hidden direct views, no complete game/crew, official native editor with a source-clock overlay. The final maintained production comparison below is required. Initial clock setup attempts failed only source-hash guards (expected LF text versus Windows CRLF file bytes), before room timing. They are retained separately; clean clocks verify actual loaded source hashes.

## Correctness

`tests/test_room_art_prefetch.gd` fails two checks before the fix and passes afterward. It pins complete ordered announcement before acquisition, no eager work from announcement alone, unchanged learned repeat order, inactive construction, and cleanup. Native `tests/test_room_art_prefetch_pixels.gd` compares ordinary blocking acquisition with active first-profile prefetch: **117 checks /56 presentations**, seven rooms ×four rotations ×two operating/door-mask states, including omitted walls. Geometry/registration/bounds and rendered pixels are exact. Both default and frozen owner-layout fixtures pass. Room pool lifetimes and missing-art diagnostics are checked.

Both scripts have official generated UID sidecars, test-index registration, scratch-profile guards; the pixel test has an explicit native lane. The runner initially classified its headless-rejection guard as headless-safe, so that skipped attempt provides no visual evidence; the corrected native run passes.

Five focused loader/selector/save/integrity tests pass; existing native room-image sharing 22 checks and Python release assertion safety 2/2 pass. Fresh-context source review found no runtime issues and one minor fixed-name fixture-manifest rerun issue. Each test now resets only its own manifest after checking scratch isolation. The headless fixture passes twice in one profile, and the owner-layout pixel fixture also reruns in its same profile.

## Candidate and normal loading

Separate maintained-export Windows candidate **brinespace-53f5bf16534c2cf5**, full physical source and export at `D:/bs-room-art-20261016/source/` and `windows/`. Source selection **61,628 files**; relative to frozen 688, one runtime file and the test index change, plus four test/UID files. No excluded concurrent work is pulled from the shared checkout.

- Source fingerprint: `53f5bf16534c2cf5d72ea5e9cecfeba1c103d46722d3610a2e6fdbde2bb1ca4b`
- EXE SHA256: `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`
- PCK SHA256: `a7a4173c488be2648fe5d7132e5a46e48dd3f0e50ed694a89211f2720087c997`
- Base Git: `67e7db969f7c5d952a3c80830369715d703199c5`, dirty full-source selection; use `source-inputs.json`, not HEAD alone.

Exact package audits pass: same **36,430 dependencies**, **35,942 assets**, **431 selected scripts/shaders +421 additional frozen scripts**, no missing/changed/unexpected assets or source failures. Only `res://rooms/whole-room/room_dressing.gd` differs. Diagnostic clocks/overlays do not ship.

Unchanged primary **12-run actual-release title/loading fixture** against frozen 688, two fresh profiles plus one repeat per lane/mode, both orders, 1600×900, visible screen2, normal costs/failures. New Loop has one starting room; Continue uses the frozen 12-room checkpoint. Times are button action to startup complete, with intro/transmission automatically acknowledged. Full crew identities and screenshots run after timing. All samples remain recorded.

| Entry/profile | Frozen 688 | Candidate | Observation |
|---|---:|---:|---|
| New Loop, first profile | 5.641–6.641 s | 5.803–7.168 s | 5.61% higher median; two pairs |
| Continue, first profile | 8.164–8.330 s | 7.960–8.019 s | 3.11% lower median; two pairs |
| New Loop, repeat | 5.188 s | 5.356 s | 168 ms slower; one pair |
| Continue, repeat | 6.782 s | 7.055 s | 273 ms slower; one pair |

The targeted **first-profile restore stage improves 1,874–1,884→1,564–1,566 ms**, approximately 17%. New Loop station-room setup also improves **93–105→83–91 ms**, while interface/crew and interface-art work are slower in those primary New samples. The source/timers do not establish a cause for the broader variation.

Slower New/repeat observations triggered **eight additional reversed-order processes**, without replacing primary samples: two additional fresh New profiles per lane and two additional Continue repeats of primary profile1.

| Additional pair | Frozen 688 | Candidate |
|---|---:|---:|
| New first1 | 5.921 s | 5.726 s |
| New first2, reversed order | 5.653 s | 5.606 s |
| Continue repeat1 | 7.213 s | 6.793 s |
| Continue repeat2, reversed order | 6.844 s | 6.968 s |

Both follow-up New pairs reverse the primary direction; Continue repeats remain mixed. **Retain this as a scoped room-preparation / first-profile Continue benefit, not a general New Loop or warm-loading win.** No causal claim that other variations are regressions or harmless noise. This is a separate experimental candidate, without release promotion or an average-FPS claim.

All **20 valid runs /ten paired complete crew-bank identities match** within each mode, including lossless pixels, metadata, filtering, timing and historical banks. The intentional New/Continue Bill bank binding distinction remains. Normal simulation advances, no missing art/errors occur, and startup workers/caches/path arrays fully release. Actual packaged Continue station/card detail crops pass visual review.

OS cache is uncontrolled; profile first use is not an OS cold boot. Sampled Windows private peaks include post-timing identities/screenshots and are lower bounds. Primary first-profile New **2,145–2,148→2,149–2,242 MiB**; Continue **2,612–2,661→2,598–2,612 MiB**. Primary repeat New **2,141→2,139 MiB**, Continue **2,645→2,633 MiB**. One candidate early Continue texture snapshot is 1,420.575 MiB versus 1,543.075 MiB in the other Continue observations; retained as an early non-steady-state sample, not a residency saving. The previous loading investigation already recorded variability at this early sampling point. No memory-soak claim.

Primary decoder peaks **23.75–214.23→23.25–214.23 MiB**, including repeat learned orders with larger non-crew art. Observed maximum pending jobs stays 96, compression jobs stay 8, existing recent-image budget 16 MiB. New first-profile priming: New 12,508 paths vs 12,506; Continue 12,532 vs 12,506, with 25 extra hits and one unused result released at end. Job count bounds are unchanged; they do not imply a fixed total decoded-byte cap. No new persistent cache or image retention.

## Preservation and remaining work

Scratch APPDATA/fixtures and real-save fingerprints protect the owner throughout. All **2,948 protected player files are unchanged** and all **118 previous delivery checksums** pass again at closeout, covering the matching d3 Windows/Mac and both 3f/688 Windows candidates. Original canonical/source/archive files remain untouched. Verified task-owned QA binaries removed **7,476,727,025 bytes (6.963 GiB)**. C/D free **114.953/41.461 GiB**; no remaining game processes. Final records: `D:/bs-room-art-20261016/final-guards.json`, Windows `SHA256SUMS` and `runtime-restoration.json`. Canonical source/export, per-run data/screenshots, overlays and setup failures remain available. Restore only specified QA binaries before rerunning; comparison setup is not idempotent. No Mac export, commit, publication or release promotion. Native Mac acceptance, large-station 60 FPS, pacing and endurance remain separate gates.

Next loading work should use the phase timings to target remaining interface/crew setup and unpooled room image work, preserving this candidate and the primary/follow-up samples. Do not widen a local room-art gain into a whole-game performance claim. Owner Mac testing still targets the frozen matching d3 kit.
