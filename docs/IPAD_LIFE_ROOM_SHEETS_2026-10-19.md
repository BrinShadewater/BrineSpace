# iPad life-room equipment sheets and longer test — October 19, 2026

Validation 2 **brinespace-f654e950d9f0ba36**, based on `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted integration/optimization work, branch `codex/ipad-memory-placement-2026-10-17`. Six selected scripts changed; no art/manifest additions or removals. No commit/push. Frozen/public Mac/Windows builds and protected monitor checkout untouched.

## Change and native evidence

Hydroponics, reactor, medical, underwater life-support and crew-hab constructors now give the inherited equipment-texture property a whole source path. On tablet, unused legacy equipment is uploaded on first read, after current layouts have replaced it where applicable. Explicit prop/wall/cap fallback draws get the same original source; desktop/editor previews stay eager. Direct assignment overrides a pending path, including assignment before first use and an explicit clear. This changes residency/first-use loading, not gameplay rules or ordinary room draw submissions.

Native red: five constructors each allocated 6,288,054 unexpected texture bytes. Green: zero added bytes for each. Four-orientation original prop images, original shell images and complete source bytes match; repeated access, assignment and preview checks pass. A mixed-tabs parse error in the initial implementation was corrected before green; it was not an accepted build.

Actual frozen 40-room station, separate Mac processes with tablet policy: eager **1033.525 MiB**, deferred **1009.538 MiB** twice; **23.987 MiB less retained texture memory**. All three full viewport hashes exactly `2ab4af303d869b02671b72ea05b6285c3dda103bef2217cc9d2ca0cf1875d841`. Native setup timing is mixed; no overall loading gain established. Scratch-profile runs preserve the Mac owner profile. A parse-only command used the project directly; it did not run gameplay or provide profile-fingerprint evidence.

Twelve exact-pack fixtures, Hull UI 175 checks, Save/controls/previous crew and rendering regressions pass. Asset audit: 36,197 entries, no missing/changed/remapped/unexpected. Selected script audit: 437, no missing/changed/unknown. Strict signature and signed-PCK/export equality pass. Independent six-file static review found no actionable issues; added assignment-before-first-access coverage afterward. Project/export metadata restored byte-exact after packaging.

Source SHA256 `f654e950d9f0ba36caf712cfefae0a697a69ef2c50c51ad05b4a06dae95f3614`; PCK `7f4ec03d9cbf3ce143047233b673399f17a0c5b69ab4e9005e4769042d69357f`; executable `a458ea4d806d4b1592b1e3ab113bbecb671ed50ef07d1e0f85d765c23689ad9a`.

## Physical validation

Physical device: iPad13,18 (A14, 4 GB), iPadOS 27.2. Installed build retains the GL compatibility renderer. A 20-minute synthetic station run completed, cycle 71→307, 40 door-connected rooms (four multi-cell, 52 occupied cells), one crew member, seeded fixture-only reserves and normal failure/build rules. All 41 sampled frame buckets were active; zero logged game errors and no observed crash. This is not organic multi-crew or paid-construction acceptance.

1,139 valid nominal 1 Hz footprint samples over 1,200 seconds: peak **2,337,935,144 bytes (2.338 GB)**, end **2,270,842,616 bytes (2.271 GB)**. Medians in the first/last 60-second windows increased **22,454,296 bytes**; this does not clear long-term memory growth. Frame buckets sampled roughly every 30 seconds: median **14.29 FPS**, minimum **7.62 FPS**, final **10.15 FPS**, sampled maximum frame **198.876 ms**. These are latest approximately one-second buckets, not full-run frame distributions. Rendering remains a release blocker; 36/41 sampled active buckets were below 20 FPS. Three automatic reports were captured; no extra Instruments recording ran during this measurement.

Earlier sparse synthetic fixtures exposed a fixture limitation: one ended through normal oxygen failure at cycle 226; another paused for low air around cycle 198. Neither was a crash. More reserves did not fix disconnected refuge paths. The final fixture was corrected and checked for door connectivity before its complete 20-minute run; production placement rules were unchanged.

Static original-fixture device texture counter: **1016.881 MiB**, versus the prior build's **1040.868 MiB**, matching the native 23.987 MiB difference. This is retained texture accounting, not a demonstrated whole-process RAM saving. First original-fixture station setup was 5.357 s, including interface/grid 2.889 s and restore 1.575 s; uncontrolled/cache-sensitive observation, no overall loading gain established.

Auxiliary 350-cycle headless simulation completed without in-run errors, but its shutdown reported live objects/resources. Explicit cleanup on current and prior signed packs matched the same four-object/two-resource exit warning in a two-cycle comparison. No clean full-suite/leak clearance is claimed.

A diagnostic native Mac M4 Metal trial reduced sampled frame median from 21.376 to 10.773 ms, but changed pixels and produced an invalid overflow-like texture counter. It was **not adopted** and is not physical-iPad evidence. A partial texture inventory found 18.573 MiB of duplicate pixels; that is a future sharing target, not an applied saving.

## Owner preservation and remaining gates

All five owner save/checkpoint files were backed up outside the repository, preserved hash-exact during installation and restored hash-exact before final owner launch. Save/title/Continue/Save then passed full gameplay-state and exact timer parity against the authoritative backup: cycle 64, seven rooms, speed index 2 (4×), timer 1.11834893097652. Cards, crew and resources are included in the full state equality. Timestamps, event history, path and camera/scroll metadata changed through UI use; whole files are not claimed identical after saving. Continue's existing 1× reset was manually corrected to the saved 4× while paused.

App PID 21610 is left paused at cycle 64, menu closed, Cold Store selected, with zero logged errors. Final save **87.051 ms**, result 0. Final repeated owner Continue station setup **3.553 s**, including interface/grid **2.592 s**; cache-sensitive observation, no causal loading improvement claimed. Existing helper PID 72353 was reused without a new authorization and left running; its two-hour lifetime still applies.

Initial loading pauses, active large-station frame rate, organic multi-crew tests and longer memory growth remain open. The iPad build is **not release-cleared**. Next useful targets are room-content submission cost and cross-cache texture sharing; any Metal backend trial needs separate physical-iPad visual, RAM, loading and stability validation. Frozen/public Mac/Windows releases and the protected monitor checkout remain unchanged.

Full local artifact: `/Users/Shared/BrineSpace-ipad-optimization-20261019/life-room-sheets`.
