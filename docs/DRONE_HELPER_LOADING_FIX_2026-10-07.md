# Targeted drone helper preparation

Updated: October 7, 2026 · Project: BrineSpace · Task: performance/release readiness

## Objective and acceptance

Admit the lossless drone integration only after actual release lifecycle, loading, visual, behavioral and matched performance checks. Preserve responsive progress and selected quality. Original PC/Mac release gates remain open.

## Accepted decisions and constraints

Keep text-script export mode and the station's threaded loader. Do not preload the whole scene synchronously, switch quality or upgrade the engine. Experimental changes stay in the physical frozen candidate; owner checkout, layouts, archives and previous Windows delivery remain unchanged.

## Current state

`output/drone-compiled-2026-10-07/` records the following actual debug=false candidates:

- Normal-path text candidate `brinespace-7a35d34088274fba`: maintained export succeeds, EXE 109,283,328 / PCK 3,646,714,814 bytes. Broad outside-checkout audit **36,288 checked, 0 missing/changed/unexpected, 55 loadable remaps**, including scripts, shaders, scenes, audio/fonts and selected text notices. Main, title and main scene bytes equal the accepted baseline; experimental Grid uses the normal runtime path. Parallel-copy package's unexpected originals are resolved by this selection.
- Binary-token trial `brinespace-9d92632c6cf0449b`: same game source/assets, preset mode 1 only; EXE 109,283,328 / PCK 3,652,001,566 bytes. Broad audit **36,288 checked, 0 missing/changed/unexpected, 468 remaps**; remap destinations recognized explicitly for selected script sources. Source availability false confirms token export exercised. Threaded load-only takes **80.139 seconds** with 35 exit leaks/one warning; synchronous 1.289 seconds clean. One outlier, cache uncontrolled, not a general loading estimate. Token mode does **not** fix warning and is rejected; frozen original preset restored byte-for-byte.

Text candidate load-only: threaded 1.366 seconds / 35 leaks; synchronous 1.345 seconds / none. Fresh physical QA copy of the previously accepted **normal package** reproduces 32 leaks with threaded 1.426-second load-only; synchronous 1.308 seconds clean. Thus the warning is not unique to the drone optimization; earlier normal lifecycle acceptance had a different warmed dependency scope. No engine root cause or safe warning dismissal claimed.

## Verification

Actual packaged two-cycle New Game → Studio → save/title → Continue:

- Normal package: **100 checks, no failures/leaks/warnings**.
- Experimental text candidate, normal loading/crew/flood and no prewarm: **142 functional checks, no failures, four exit leaks/one warning**. Required factory/jobs/textures, actor/fleet restores and weak owner releases pass; not a clean lifetime acceptance.
- Same experimental package, **only eight small provider scripts** prepared on main thread with a rendered frame between each; Main is not preloaded: **150 checks, no failures/leaks/warnings**. Normal intro, Studio ownership, restores and last-owner cleanup retained. Preparation totals **44.234 ms**; slowest room-content script **23.124 ms**. This proves a targeted remedy in the QA lifecycle fixture, not yet production-loader certification or full loading/endurance acceptance.

Eight provider files also pass the existing release-assert loading-side-effect scanner; no required PNG load hidden in stripped assertions. All completed runs preserve all 2936 owner files. Native processes above are terminal.

## Next action

The targeted remedy is now written into **frozen** `scripts/loading_transition.gd`: after the opaque loading UI is rendered, load the eight whole named helper paths sequentially with rendered frames between; then retain normal threaded Main/scene loading. No helper resource cache added to permanently retain visits. Original frozen loader preserved as `loading-before-helpers.gd`; patch hash and scope in `loading-helper-fix.json`. No accepted checkout change yet.

The first patched export attempt found its two frozen template copies missing and terminated before export. Cause not established; restored copies from maintained local 4.7.2 templates, recorded hashes and preserved failure log. Retry **verified live unified session 55202** runs maintained text export to `helper-release/` then broad audit. Poll the same handle; do not restart after observation timeout. All earlier packages/evidence retained.

After the patched package succeeds, prepare actual QA against it and run an **unprepared** lifecycle adapter: helper preparation must come from the packaged loading screen, not the QA script. Measure loading-frame gaps/progress and stage duration, then matched actual large-station memory/uploads/p95/p99 and motion/behavior. Fix residual issues before normal admission. Two-cycle small fixtures do not replace two-hour large soak, ten transitions, full bug/UI/hardware/Mac checks or three measured benchmark runs. No publication or performance gate closure.
