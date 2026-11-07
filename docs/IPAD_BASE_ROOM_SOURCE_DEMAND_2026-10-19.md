# iPad inherited room source demand — October 19, 2026

Installed and tested as **brinespace-dd897919d092e022**, Validation 2. Memory accounting improved; initial loading and intermittent stalls remain open. Not release-cleared.

## Identity and change

Checkout `/Users/Shared/BrineSpace-native-validation-20261017`, branch `codex/ipad-memory-placement-2026-10-17`, HEAD `81b2f9a4a36eb0e3162d86ccfb4e9ef735836122` plus accepted uncommitted work. No commit/push or public delivery; frozen Mac/Windows releases unchanged. Bundle `com.shadewater.brinespace.nativeoptimization20261017`; physical device iPad13,18 / A14 / 4 GB / iPadOS 27.2.

- Source SHA: `dd897919d092e0227bb951ef7caf01bfbf9f851bfa5026b5e12947933d798ea1`.
- PCK SHA: `a98c686a06cc3d9ed9b49f560d82310e10db7b5ce562bea4e0d3431141176e60`.
- Signed executable SHA: `ec7a2b24c35e6e43de28aad2531bfb132e4d965dfa37ff7af6d695d388dcec3a`.

Only `nursery_whole_view.gd` and `connected_rooms_view.gd` changed in the runtime manifest; paths/assets unchanged. Tablet setup now defers two inherited default sheets that current layouts replace. The nursery property retains the existing shared-source loader on demand; explicit assignments (including null) remain authoritative. Connected rooms use the established lazy life-source policy. Desktop/editor preserve their original eager shared-loader branch. No artwork, geometry, simulation, navigation or renderer change.

The regression failed on five intended eager-upload assertions. An initial implementation also failed desktop cache ownership; preserving the original desktop branch corrected it. New base-source, equipment and legacy-room native tests pass. Independent static review found no actionable production issue; an editor assertion was strengthened to check its own field rather than a previously warmed shared cache. Twenty actual-PCK fixtures, asset/source audits and strict signing pass. Four temporary export configurations restored byte-exact.

## Measurements

| Observation | Tested da3 baseline | dd89 candidate |
|---|---:|---:|
| Native station texture counter | 722.488 MiB | 710.495 MiB |
| Physical station peak texture counter | 734.773 MiB | 722.779 MiB |
| First setup | 4.083 s | 4.133 s |
| Repeat setup | 3.133 s | 3.121 s |
| Initial redraw frame | 2.310 s | 2.288 s |

Native and physical texture accounting are **11.994 MiB lower**. Fresh paired native station pixels are exact (`ba7abac5864eff3821b9044bb76b75697a882d9bb15581b93f4aa05c8f4fbfa5`). An older historical viewport differed in a small actor region and was superseded by this fresh pair.

No useful loading-speed or sustained total-RAM gain is established. This is one ordered comparison with prepared crew cache; candidate first startup order came from the rejected experiment and normal loading replaced it. Candidate 73 nominal 1 Hz process samples peaked 1,768,885,480 bytes, versus baseline 71 samples / 1,786,350,848 bytes. Both reports logged zero errors. Initial long frames survived in bucket history after the recent-hitch list evicted them.

## Longer tests and restoration

Synthetic workload: nine phases / 5,400 frames, idle/zoom/placement at 1/2/4×; phase ends retained all 40–43 rooms in view. Measured-frame sum 276.983 s; maximum 516.353 ms. Process peak 1,994,640,856 bytes / end 1,964,477,912 over 312 nominal 1 Hz samples. Zero logged errors or missing-art failures. Heavy draw profiling, free building and failure bypass belong only to this method-driven fixture; it is not ordinary play acceptance. Five original files restored SHA-exact and QA marker removed afterward. Its raw pre-restoration comparison also includes intentional earlier loading-UI saves.

Normal rules: **20.228 endpoint-counted active minutes** / 21.982 wall minutes at **1×**, cycle 65→129, 40 rooms and one crew alive; no pending orders/unpowered rooms at saved end. Normal caps/costs/hazards retained with fixture-only initial reserves; heavy profiling off. Opening dialogue pauses were dismissed through actual UI and excluded from endpoint accounting. Zero logged errors. 1258 nominal 1 Hz samples: peak 2,176,224,872 bytes / end 2,162,314,856. First/last minute medians rose 156,827,816 bytes; the first minute includes opening pauses. This is not leak clearance. Seventy-six sampled active latest-frame buckets had median 22.871 FPS / minimum 12.788 FPS / maximum frame 116.811 ms. Fifteen-second snapshots are not a full-run frame distribution or faster-speed clearance.

Actual UI card return, pinch zoom, rotation button, Codex scrolling and background/resume passed; saved gameplay fields and exact timer unchanged. Complete-state Save → title → Continue → Save parity passed. All five incoming original files were then restored **SHA-exact after final launch**. Owner station: paused cycle 64, seven rooms, 4×, timer 1.11834893097652, menu closed. No owner simulation. Two-finger pan/tap are unsupported by this helper and were not retested. Volatile final PID 39445; retain the authorized helper session.

## Rejected evidence and retention

The first experiment kept bounded PNG workers through a covered station draw, suppressing nested progress redraws. Its tests/audits/signing passed, but device redraw 2340.632 ms versus baseline 2309.809 ms showed no useful gain (covered phases 2531/2490 ms also include scheduling). Both production loading scripts were restored byte-exact; its new test/UID moved out of the live index into rejected evidence. Sibling `startup-draw-prefetch` retains it. The existing loading-flow test was repaired to wait for the observable overlay after deferred tap feedback; the initial failed lookup remains recorded.

The final-device coordinator initially lacked one copied helper and stopped before device action; copying the maintained helper fixed the controller only. Failed logs retained; no production change.

Complete tested rollback **da3** remains in `legacy-equipment-demand`; complete **7bb** in `texture-residency-pass` is a protected recovery donor. Superseded **6c** and rejected **de42** packs are recovery-archived with full reconstruction SHA verification; historical apps need pack restoration. Instructions remain beside them and in `/Users/Shared/BrineSpace-workspace-cleanup-20261019-consolidation`.

106 byte-identical immutable libraries in inactive exports were hard-linked after hash, ownership/mode and xattr checks: all original paths/content retained, original mtimes recorded; 19.511 GB logical duplicates consolidated. Physical free space rose about 1.4→7.4 GiB before the next export. Source, saves, current/rollback/helper products, frozen releases and unique evidence were outside that target scope.

Next: attribute remaining first-use draw/upload/driver work and runtime cache growth on the physical iPad. Sparse counters, synthetic coverage and a prebuilt one-crew soak do not certify organic multi-crew growth, all gestures or release readiness.

Full evidence: `/Users/Shared/BrineSpace-ipad-optimization-20261019/base-room-source-demand`.
