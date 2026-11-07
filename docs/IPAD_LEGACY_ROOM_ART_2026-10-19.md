# iPad deferred legacy room art — October 19, 2026

Validation 2 build **brinespace-c6b21f6d546d4bd3**, based on `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus the accepted uncommitted integration/optimization work. Branch `codex/ipad-memory-placement-2026-10-17`. This pass changes only three selected production scripts; no assets added, removed or altered. No commit/push performed. Frozen/public Mac/Windows builds and protected monitor checkout untouched.

## Change

Tablet power/workshop constructors retain legacy prop registration and geometry without uploading old textures that current room layouts remove. Actual legacy draws load the original texture on first use. Machine bounds can decode the image for its used rectangle without creating a GPU texture. Desktop and layout-editor previews keep their prior eager policy. This reduces room-content texture residency; it does not reduce the number of ordinary room-content draw submissions.

## Verification

Separate native Mac processes with forced tablet layout and the same frozen synthetic 40-room fixture: eager **1085.511 MiB**, deferred **1033.525 MiB** in both repeats, a **51.986 MiB retained texture reduction**. Entire viewport pixels identical across all three captures (SHA256 `2ab4af303d869b02671b72ea05b6285c3dda103bef2217cc9d2ca0cf1875d841`). This is not whole-process RAM or iPad loading evidence. Native owner-profile fingerprints unchanged.

New native fallback regression passes, including four orientations, raw machine art, bench/tote fallback, carried tote and editor preview. Eleven exact-pack fixtures pass, including Hull UI 175 checks, RunSave, tablet controls, prior crew-storage and fog regressions. Asset audit 36,197 entries: no missing/changed/remapped/unexpected files. Selected script audit 437: no missing/changed/unknown scripts. Strict signature verification and signed PCK/export equality pass. Scoped independent review found no actionable issues. Whitespace check passes.

Source SHA256 `c6b21f6d546d4bd3fda55e761825bf6d6b4cfa3d98d4bc51d3ea8592b0f2e5f0`; PCK `71537f3da161a071002a129daed1db2363529644c982aa943382778733cf2106`; executable `5fab2868f480fb3ae84d0e3b5baeca8e89fcc75287d1f8b823ec96fad8df9bd9`.

## Physical iPad observations

Installed on iPad13,18 (A14, 4 GB, iPadOS 27.2), bundle `com.shadewater.brinespace.nativeoptimization20261017`. Same paused synthetic 40-room/four multi-cell/52-cell fixture; footprint-valid, not full-port-connected organic or multi-crew acceptance. Three one-second buckets sampled ten seconds apart after loading each build. No thermal/cache control or repeated A/B/A experiment.

| Measurement | Previous | Updated |
|---|---:|---:|
| Retained texture counter, all three samples | 1092.854 MiB | 1040.868 MiB |
| Draw calls, all three samples | 2965 | 2965 |
| Sampled FPS median | 24.95 | 35.69 |
| Process footprint peak in short capture | 2.206 GB | 2.173 GB |
| Process footprint at capture end | 2.158 GB | 2.120 GB |
| Station build | 6723 ms | 5572 ms |
| Interface/grid callback | 3830.534 ms | 2950.037 ms |
| Restore callback | 2018.366 ms | 1696.790 ms |

The **51.986 MiB retained texture reduction** matches the repeated native result. Other short before/after differences do not establish reliable process-RAM, loading or FPS improvement. Both captures zero logged game errors; no crash observed. Deliberate process stops triggered the existing last-session warning, which was dismissed. Rotation button and card-return drag clear placement controls on the disposable station; no new paid construction, pinch or two-finger gesture acceptance claimed.

## Owner preservation and final state

All five owner save/checkpoint files were backed up after Save Game, restored hash-exact before installation, preserved hash-exact through installation, then restored hash-exact after the disposable test. Save/title/Continue/Save passes **full gameplay-state and timer parity**: cycle 64, seven rooms, resources/cards/crew unchanged, timer `1.11834893097652`. Existing Continue speed reset to 1x was manually corrected to the original 4x before each save. Final Save 93.357 ms, result 0, errors 0. Differences outside gameplay state/timer: timestamps, event history, path, scroll and camera center; whole-file parity after UI testing is not claimed.

One immediate post-relaunch capture showed iOS's old application snapshot; excluded from acceptance. Confirmed fresh title explicitly showed cycle 64/seven rooms before Continue, followed by the matching station. Final app PID12302, paused at 4x, menu closed. Same two-hour helper xcodebuild PID72353 left connected. Initial helper attempt expired; the user approved the renewed helper, reused for all remaining tests.

[Portable evidence](ipad-memory-placement-evidence-2026-10-19/legacy-room-art/SUMMARY.json).

## Remaining gates

Initial loading pauses, active large-station performance, long-session memory growth, organic connected multi-crew station testing and iPad release readiness remain open. Do not infer release clearance or a reliable loading/FPS improvement from a texture counter reduction.

Full local artifact: `/Users/Shared/BrineSpace-ipad-optimization-20261019/texture-residency`. Private saves remain outside the repository.
