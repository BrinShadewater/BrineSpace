# iPad companion pod loading — October 19, 2026

Status: installed and tested as Validation 2. Loading/runtime hitches remain; not release-cleared.

## Identity and scope

Active checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch `codex/ipad-memory-placement-2026-10-17`, HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted dirty work. Current candidate **brinespace-6c362d6f692b2d6f**, bundle `com.shadewater.brinespace.nativeoptimization20261017`.

- Source SHA-256: `6c362d6f692b2d6ff0ac97dd41b60cfcf2a6710c0c78eb46dd7ff38510f31644`.
- PCK SHA-256: `7d0fddf469ff9ddfb9b568195de2a357c88bdbc8a01d092bd998fcc5a4ea4f4e`.
- Signed executable SHA-256: `4c818b577cd4f7d31bea94f8f5f9371f05af052581781df5a039e501090fdce6`.
- Prior complete tested rollback **7bb44e16b7f164d3** in sibling `texture-residency-pass`; retain its PCK as the rejected-pack recovery donor. Frozen/published Mac and Windows builds unchanged. No commit or push.

## Diagnosis and change

A short physical self-sampling diagnostic used the unchanged 7bb4 PCK in a separate local wrapper. Its main-thread stacks include PNG decode in CanvasItem redraw during a 2545.791ms frame; grid redraw accounted for 2025.410ms. These are CPU wall intervals, not GPU timings. The observer requested10ms sampling and retained8571 samples over105.19s; suspend/unwind overhead and partial capture make it attribution evidence, not an uninstrumented benchmark. Two Apple recorder attempts failed to finalize and are retained as rejected evidence.

Native image-call tracing found349 Margot PNG loads/47,262,976 raw source bytes on first redraw: the frozen pod's nap pose invoked the ordinary companion getter and loaded locomotion, water and personality banks. Other first-draw floor, shell and environment loading remains.

Tablet pod rendering now uses only its demanded canonical clips. Full companion loading still supplies all ordinary art when requested and releases the subset aliases; desktop behavior stays eager. `load_manifest` keeps its original three-argument override contract, with a separate filtered `load_manifest_states` entry point. No artwork, density, animation clocks, navigation or simulation rules changed. Modified source: `crew_sprite_player.gd`, `companion_npc.gd`, `margot_cryo_art.gd`; new native fixture `test_tablet_companion_pod_storage.gd`.

## Evidence

- Native regression: three intended storage failures before the fix, zero after. Frozen/thaw/recovered pod pixels across both motion settings, demanded-clip residency, later full-bank pixels/metadata/clocks, and desktop behavior pass. Owner native viewport pixels exact: `ba7abac5864eff3821b9044bb76b75697a882d9bb15581b93f4aa05c8f4fbfa5`.
- Native texture counter799.682→740.478MiB; physical station peak texture counter811.967→752.763MiB: **59.204MiB lower** in each. These are texture accounting, not total-process RAM savings.
- Physical iPad13,18/A14/4GB/iPadOS27.2: fresh setup3984ms, repeat3241ms; first redraw hitch2382.095ms remains. Fresh cohort sampled process peak1,794,821,400 bytes/73 samples. Prepared crew disk cache retained. No controlled whole-load or sustained whole-process improvement is established.
- Sixteen actual-PCK fixtures, asset/source audits and strict signing pass. The first a62 package was rejected before installation for a parent-signature mismatch; corrected source preserves that API and received a second static review with no actionable findings. The rejected pack is recovery-archived under `rejected-a62`, with full-stream SHA verification. One native probe overlapped temporary export configuration and was rejected by the isolation guard; the corrected owner comparison was rerun after byte-exact configuration restoration.

The physical40-room/one-crew disposable fixture completed944.419s wall /910.993s conservative active time, ending cycle253 with crew alive and zero logged errors. Normal failures/caps remained enabled, with fixture-only initial reserves.903 nominal1Hz process samples peaked at2,157,448,808 bytes and ended2,115,423,824; first/last60s medians rose31,784,984 bytes.56 sampled active latest-frame buckets had median20.004FPS, minimum6.856FPS and maximum frame1400.622ms. These sparse buckets are not the full-run FPS distribution; this is not leak clearance or organic multi-crew acceptance. An initial normal BRINE dialogue pause was dismissed through the UI and excluded from conservative active accounting.

A separate copy of that disposable checkpoint was seeded to40metal (normal costs/failures retained). Actual UI rotated Cold Store once and placed at(25,19), deducting exactly8metal and adding exactly one queued order while paused. Save/title/Continue/Save preserved the order, tested gameplay fields and exact timer. This verifies queued construction acceptance/persistence, not completed drone construction under simulation. `paid-plan-used.json`, `verify-paid.log`, `placement-continue-parity.log` and before/after saves retain the proof. Native projection was adjusted by the measured physical saved scroll; an early menu-close OCR lookup missed its label and was corrected by tapping outside, without a game failure.

Actual device card return deselected placement, pinch zoom changed the saved zoom0.0708597375→0.2191083166, rotation button saved rotation1, Codex drag changed visible entries, and Home Screen/reactivation returned paused cycle64. Native readback verifies original gameplay fields and exact timer unchanged during those checks. Controlled owner Save→title→Continue→Save then matched the complete saved `state` dictionary and exact timer1.11834893097652, cycle64/seven rooms/speed index2. Only `_path`, event history and saved timestamp differed outside state. Both final manual reports logged zero errors.

All five original save/checkpoint files were restored and verified SHA-256-exact again after final owner launch (`final-owner-restoration.json`). Station left paused cycle64/seven rooms at4×, menu closed. No owner simulation was run. The existing authorized helper was retained; volatile PID/session details remain outside the repository.

## Limits and next work

Initial loading remains visibly slow. The next measured targets are the remaining first-draw floor/shell/environment preparation, followed by long growth and organic multi-crew play. Full companion activation still performs its ordinary full-bank load; its physical first-use latency is not cleared by these subset/pixel tests. Two-finger pan/tap are not supported by the helper; do not claim automated gesture acceptance. **Not release-cleared.**

Full local artifacts, logs, source snapshots, protected saves and raw diagnostics: `/Users/Shared/BrineSpace-ipad-optimization-20261019/station-first-frame`. Only18 obsolete generated scratch crew caches were removed (1,897,822,728 logical bytes); sibling profile files were hash-verified unchanged. Current/rollback builds, recovery donors, unique evidence, source and owner saves retained.
