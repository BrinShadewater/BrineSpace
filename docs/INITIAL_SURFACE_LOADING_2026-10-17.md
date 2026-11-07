# Initial floor and wall preparation — October 17, 2026

Separate Windows candidate **brinespace-5dd3aea89a5b1c1f** prepares floor/wall images for initial retained room groups. Continue improves in all four primary paired comparisons. A single opening room stays lazy; New measurements remain variable, with one valid slow first-profile sample retained. This is loading evidence, not release promotion, a general New speedup, FPS acceptance or native Mac validation.

## Delivery and implementation

- Source and Windows: `C:/Users/Alex/Documents/BrineSpaceQA/structure-loading-20261016/source` and `/windows`; **61,634 selected source files**, based on frozen3a plus explicit task patches/tests. Release source/dependency SHA256 `5dd3aea89a5b1c1ff763cd1fd67994314cfc679cfed6455dca207240d3947185`.
- PCK SHA256 `cc05a0b90e6628f2f357d339372f2577457b3e8e2f301a21072d0b713b60ee55`. Same release EXE `7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76`.
- Same **36,430 dependencies /35,942 assets**. Exact asset audit: zero missing/changed/remapped/unexpected. Packed source audit: selected431 +extra frozen421, zero unexpected/failures. Manifest delta: exactly **two runtime scripts**, no added/removed dependency.
- `scripts/grid_canvas.gd`: prepare initial surface images inside the existing startup-art stage only while the startup decoder is active. Use the predicted opening view plus the renderer's existing three-cell retained join cover; deduplicate image requests and use existing texture caches. Require at least two eligible rooms. Extract existing hand image choices without adding per-room priming to steady play.
- `rooms/whole-room/painted_shell.gd`: retain hand-prepared images first, then use existing `SafeImage.raw_image` so wall PNGs can consume startup workers. Native PNG decoding and texture creation retain their original pixels.
- No mesh, draw command/order, camera, lighting algorithm, crew/navigation, save schema or gameplay-flag change. No second image cache. Owner finishes/rotations, disabled walls, offscreen selection and learned repeat order remain supported. Max pending96, compression8 and recent decoded cache16MiB are unchanged; a job-count bound is not a decoded-byte cap.

## Actual release comparison

**16 primary visits /eight pairs**: two observations per entry/visit, with A/B order reversed in round2. A is frozen **3a0ae1af0283fa01**, B is **5dd3aea89a5b1c1f**. Same title/buttons/dialogue adapter, native visible secondary display,1600×900, Compatibility/OpenGL, Godot4.7.2, RTX4070Ti, Dummy/silent audio. New geography uses existing pre-ready `site_seed` metadata1928894317; initial wrecks, room-view set, zoom and opening extent also match across all eight New visits. Continue restores the original twelve-room checkpoint2808620329 before every visit; learned startup-image order survives repeats. Critical profile inputs and complete crew identities match within mode.

Times start at the New/Continue action, not executable bootstrap. A fresh profile is not cold OS cache. Remaining gameplay RNG, desktop variability, silent audio and small cohorts limit generalization. Table values are medians of two observations; deltas/percentages are medians of paired effects. Positive change means slower. Both observed startup readiness and loading-screen disappearance are retained.

| Entry | Startup ready A → B | Loading screen gone A → B | Paired uncover change |
|---|---:|---:|---:|
| New / first profile | 5.917 → 6.302s | 6.532 → 7.941s | +1409.0ms / +21.46% |
| New / repeat | 5.179 → 5.084s | 5.908 → 5.694s | -213.2ms / -3.60% |
| Continue / first profile | 7.557 → 7.337s | 7.580 → 7.363s | -216.7ms / -2.85% |
| Continue / repeat | 6.603 → 6.121s | 6.628 → 6.192s | -436.0ms / -6.58% |

**All four Continue pairs are faster.** The measured `initial_art` stage grows from146–155 to246–266ms on first Continue, and59–68 to114–131ms on repeats. Total uncover time still improves; this is not a claim based only on moving work before readiness.

**First-profile New is inconclusive.** B's valid first sample is **9.546s uncovered /6.874s ready**, versus A6.562/5.946s. Its initial-art stage is1.240s versus0.583s, followed by2.671s ready→uncover versus0.616s. The second fresh pair reverses direction: B6.337s versus A6.502s uncovered. The slow sample is not discarded, and its cause is unproved; clocks do not isolate it to crew or to the new surface preparation.

Four separately labeled fresh New controls, A/B/B/A order, do not reproduce that outlier: A **6.314–6.467s**, B **6.133–6.149s** uncovered. Their initial-art stages are A562–568ms/B557–567ms. They are not pooled into the primary table or used to replace the slow sample. Both packages have empty floor/wall image caches at the New ready snapshot in all primary and control visits, and identical New startup worker-hit counts. The revised single-room policy is exercised in the actual package; no general fresh-New gain or stable regression is established by this small cohort.

Continue's `node.ready` snapshot occurs before asynchronous restoration completes; its early empty image caches are not evidence about final Continue preparation. Decoder counts, startup-stage clocks and post-setup draw traces provide that evidence instead.

## Drawing attribution

Four separately labeled corrected A/B drawing observers use the same controlled inputs. Primary timing runs have the observer disabled. Counters reconcile monotonic/reset-aware grid CPU totals; nested stages overlap and are not GPU execution times or a complete decode/upload/geometry split.

| First post-setup interval | A | B |
|---|---:|---:|
| Continue floor-slot methods | 272.791ms | 116.789ms |
| Continue wall-shell methods | 183.584ms | 36.518ms |
| Continue north crowns | 30.885ms | 30.848ms |
| Continue total instrumented grid methods | 919.222ms | 576.855ms |
| Continue setup-last-ready → render-pre | 1,031.018ms | 692.024ms |
| New setup-last-ready → render-pre | 291.675ms | 300.792ms |
| New observed-ready → uncover | 611.747ms | 611.035ms |

Floor and wall-shell work falls by about303ms in this diagnostic. New's single-room presentation tail is effectively unchanged in this pair. Remaining retained-floor work, north crowns and derelict/presentation work are follow-up targets; this does not assign every remaining cost to a particular function.

## Memory observations

All final visits check that startup workers/results/recent decoded images/path order are inactive/empty after loading. Repeat New decoded peak remains **237.48MiB** and repeat Continue **214.23MiB**, equal to baseline in the primary cohort. Whole-process private peaks vary; repeat Continue is **30/98MiB higher in its two paired samples**. No memory improvement, exact startup RSS delta or endurance/leak acceptance is claimed. Private peaks include post-timing crew identity and visual QA.

| Entry | Sampled private peak A → B, MiB | Decoded peak A → B, MiB |
|---|---:|---:|
| new-fresh | 2127.1–2142.0 → 2125.4–2142.7 | 33.0–35.0 → 33.0–42.6 |
| new-repeat | 2287.5–2326.4 → 2284.8–2296.4 | 237.5–237.5 → 237.5–237.5 |
| resume-fresh | 2618.8–2656.1 → 2651.1–2652.1 | 34.5–39.8 → 34.2–35.9 |
| resume-repeat | 2613.4–2664.3 → 2694.6–2711.5 | 214.2–214.2 → 214.2–214.2 |

## Verification and retained revisions

- Focused missing-method regression and the later single-room regression each red→green. Final focused **16 checks** cover inactive laziness, single-room bypass, multiroom preparation, actual selected finish, rotated borrowed wall material, disabled walls, offscreen exclusion, idempotence, unchanged room input, source PNG pixels, learned repeat order and decoder cleanup. New script/UID paired and registered; existing visible-art fixture adds a hardware input.
- Core image/room prefetch checks, hand queue220, wall texture sharing73, floor keys164, wall context8006 and release assertion safety2/2 pass. Native room image/geometry parity **117 checks /56 presentations**, retained floors23, wall slots231 and loading transition pass. These native checks cover the same inner render/load implementation; the later change only selects whether startup preparation runs. Final focused and visible-art checks rerun after that gate; no redundant full native suite. Actual final package New/Continue screenshots inspected, coherent floors/walls/UI and no missing artwork. No full-frame pixel equality is claimed for moving gameplay.
- **25 final QA visits** (16 primary +four New controls +one ordinary randomized New smoke +four drawing diagnostics), plus one baseline investigation. Complete lossless-source/clip/metadata/timing/filter/historical-bank crew identities match within entry mode; art/runtime errors, normal simulation/flags and decoder-release checks pass. Final integrity and independent review completion are recorded below.
- First candidate **b5cf23fb16cf2ff5** has a separate valid16+smoke+four-trace cohort under `first-batch-b5`. Continue paired uncover−175.7/−416.9ms, New+16.6/+73.6ms. That measured one-room cost motivated leaving single-room preparation lazy. Do not compare cohorts as a randomized b5/5dd experiment. Exact source fragments, selection, package metadata, raw reports/images/inputs and revision decisions are retained. The offscreen test's stale expected image literal was strengthened before the final export. The first malformed test URI and failed deep-alternate Git clone are rejected workflow attempts, not accepted game measurements; cloning metadata from the root at the selected baseline HEAD resolved the latter while every physical file byte still came from frozen3a plus explicit task patches.

## Final integrity and continuation

Fresh read-only review found no material issues in the physical patch, manifests, raw paired results, diagnostic clocks, complete crew identities or four actual-package New/Continue images. The reviewer independently recomputed all eight pairs, retained the slow New sample and confirmed the limits above. Evidence is in `review.md`.

Final verification confirms **all130 protected delivery hashes and all2,948 player files unchanged**, all26 accepted records clean, the61,634-file source selection correct and the canonical EXE/PCK equal their export identities. No game processes remain. Byte/hash-verified task-owned QA duplicates and the superseded b5 binaries were removed; source, canonical final Windows package, historical metadata, raw evidence, helpers and restoration map remain. Total recovery across this task is **14,953,472,635 bytes /13.927GiB**; final C:/D: free space is **100.575/29.046GiB**. `verified-integrity.json`, `final-guards.json`, `runtime-restoration.json` and `HANDOFF.md` record the checks and cleanup.

This task is complete. No commit, publication, release promotion or Mac rebuild was performed. Matching d3 Windows/Mac and previous accepted candidates remain frozen comparison targets; d3 Mac is still the owner's native validation target. Remaining floor/crown and New derelict/presentation costs, the unreproduced New outlier, large-station60FPS, frame pacing and endurance remain separate work.
