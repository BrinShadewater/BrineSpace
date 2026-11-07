# iPad opening surface staging

Validation 2 **brinespace-4ec7bfc92e3b5e48** is installed on the physical iPad. Opening floor/wall PNGs now prepare behind the loading cover through bounded workers. Largest retained opening-grid frames measured **1.182/1.246 seconds**, against the previous first redraw **2.214 seconds**. Setup increased to **6.101/4.049 seconds** first/repeat. This spreads work; it does not establish shorter end-to-end loading or a whole-process memory reduction. Not release-cleared.

## Source and change

Checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch `codex/ipad-memory-placement-2026-10-17`, HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work. Starting installed source was **7675a83dea541541**, retained complete as rollback and recovery donor. Frozen Mac/Windows releases are unchanged.

Only selected runtime scripts `scripts/main.gd` and `scripts/grid_canvas.gd` changed from that build. The initial visible surface selector preserves finishes, rotation, wall visibility and culling; painted shells omit a redundant corridor base because corridors have their own wall art. Tablet opening preparation reuses the existing two-job/16MiB queue, decodes original PNGs on CPU workers and uploads at most one texture per main-thread frame. Missing, oversized or failed work retains the normal draw fallback. Gameplay processing pauses during preparation, restores its prior mode afterward, and drawing is held without hiding the grid Control or disturbing scroll layout. Desktop prewarm retains its synchronous path with the shared selector. Art bytes, gameplay rules and controls remain unchanged.

## Verification

- Native red/green regression (12 checks), existing initial-surface and loading tests pass. Original source pixels and seven-/forty-room viewports match exactly after equal camera/layout settling. Independent read-only review found no actionable issue.
- All **27 exact-PCK fixtures**, selected asset/source audits and strict signing pass. Actual main-scene startup in the exact pack verifies disabled gameplay processing during staging, restored processing/drawing, exact paused timer, unchanged gameplay state and released worker buffers. All four export configs are byte-exact restored; real Mac owner-profile guard is unchanged.
- Physical iPad13,18 / A14 /4GB /iPadOS27.2: same cycle64/seven-room checkpoint. First opening retained grid frames904.013/1181.700ms; repeat762.428/1245.688ms. Previous7675 setup4149/3051ms; candidate6101/4049ms, including staging1218/1025ms. A recorded construction frame remains4530ms. One ordered comparison; stage intervals overlap frame work and must not be summed into a whole-load duration.
- Normal1×56-room/four-crew soak completed its40-active-minute target; full terminal record and all crew survival fields are in portable evidence. Seeded initial reserves/support-room connectivity were fixture preparation; normal costs, resource caps and hazards remained enabled. No logged errors or app crash. This does not establish organic recruitment or faster-speed acceptance.
- Sampled process peak **2.442GB**, end **2.373GB**. First/last-minute medians change **26.182MB**; opening warmup affects the first window. Sparse active buckets: median **9.11FPS**, minimum **4.76FPS**, largest retained frame **366.571ms**. These are sampled buckets, not complete frame statistics. The large view remains slow; no leak clearance or controlled RAM gain. Previous7675 sparse buckets had12.17FPS median versus this run's9.11FPS; durations and simulation events differ, so this is not a controlled steady-render comparison and establishes no rendering speedup.
- Actual card return, pinch zoom, rotation button, Codex scrolling, background/reopen and Save/title/Continue/Save pass. Full saved gameplay state and exact timer compare equal. Continue's existing1× reset required manually reselecting4×. Two-finger tap/pan are not automated by this helper; paid placement was not retested against the original checkpoint.
- After final normal launch, all five original save/checkpoint files are SHA-exact. Owner station is cycle64/seven rooms, paused4×, menu closed. Final screenshot inspected. The current four-hour helper remains running.

## Next target and limits

A separate disposable native lifecycle probe found **40,934,676bytes (39.038MiB)** of engine texture accounting retained by the large-room static sprite lookup after registered owners reached zero. Manually clearing that lookup released the accounting in that probe. **No production change or iPad RAM saving is claimed.** Next test registered overlapping owners, Studio and reentry, then compare actual iPad title/load lifecycle. Initial interface construction, title return, intermittent stalls and process memory remain open.

## Artifacts and cleanup

Signed current app/export and raw evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261019/opening-surface-staging`. [Portable evidence](evidence/IPAD_OPENING_SURFACE_STAGING_2026-10-19.json), local `FINAL_VERIFICATION.json`, `full-device-pipeline.log`, `soak-summary.json`, `physical-loading-comparison.json` and `final-owner-restoration.json` contain receipts.

SourceSHA256 `4ec7bfc92e3b5e483d5a6173a4b80bb1cedd9919933020066dc0b9fef3d30959`; PCK `1382f60eeb88a8efb9a53f494689393a4b9ec90719703214d5e11c41729d7262`; executable `eaefb06d8c027247f67b16e3fa14a5bf30a14f742fe83d55e7b9c33f9900fe0d`. Build uses unchanged native sampler and generated C++ hashes recorded in portable evidence. No commit, push or release upload performed.

Cleanup preserves current4ec, full7675 rollback/donor, protected7bb root donor, recovery archives, source, all saves and unique evidence. The older Mac Esc QA pack is SHA-verified recovery-archived using7675. Old helper actions are fully hash-verified in a compressed archive; duplicate report paths retain exact bytes through APFS clones. Completed disposable crew caches were removed. An attempted rollback block consolidation retained complete exact signed copies but produced no measured free-space gain.

At explicit owner request, Chrome's4,269,932,544byte on-device AI weights plus component metadata were removed; profiles/history/passwords were untouched. Its receipt measured4,269,993,984bytes more free space. Free space changes with subsequent work; closeout reading is in portable evidence. Retain `DONOR_RECOVERY_ORDER.md` and every named donor.
