# Mixed New Loop and repeat loading investigation — October 16, 2026

The room-art candidate still has a reproducible **first-profile Continue benefit**. A general New Loop or repeat benefit is not established. No production code, artwork, crew behavior, source snapshot or playable export changed in this task. All earlier observations remain valid evidence of their own cohorts; none were replaced with better follow-ups.

## Builds and method

Compare frozen **A: brinespace-688bb7cf923bb512** at `D:/bs-crew-restore-20261016/windows` with **B: brinespace-53f5bf16534c2cf5** at `D:/bs-room-art-20261016/windows`. Their sole runtime difference remains the dressing-texture announcement described in [the room-art report](ROOM_ART_LOADING_2026-10-16.md). Matching **d3 Windows/Mac**, prior 3f/688 and current 53f sources/exports remain frozen. No release promotion or Mac rebuild.

Evidence: `D:/bs-loading-variance-20261016/`; orchestration: `output/loading-variance-20261016/`. Three independent profile pairs per mode/build, each with a first visit and repeat: **24 serial actual-release processes**, native OpenGL/Compatibility, 1600×900, screen 2, silent/Dummy audio. Lane order alternates and reverses between visits; fresh visits have A first twice/B first once, repeat visits the reverse. Primary title/button-driving fixture is byte-identical to the previous comparison. Timing is button action to the fixture observing `startup_complete`; intro is automatically acknowledged. Continue uses the same frozen 12-room checkpoint and owner layouts; New uses the normal one-core loop. Normal gameplay flags stay enabled. No minimized/overlapping runs were accepted; this cohort had no rejected launches.

Profile inputs/outputs and learned manifests are retained per run. Crew lossless sources, complete clip/metadata/timing/filter and historical bank signatures are checked **after timing**. External Windows memory/CPU/I/O sampling runs every 250ms; process accounting includes post-timing QA and is not isolated startup CPU or physical disk I/O. Fresh profile does **not** mean cold OS cache. Small samples are descriptive, without a significance, cold-boot, FPS, pacing or endurance claim.

## Primary results

Positive paired delta means B was slower. Report **median of matched-pair deltas**, with every pair retained; independent group medians are descriptive only.

| Entry | A range (s) | B range (s) | B−A for each pair (ms) | Median paired B−A | B faster |
|---|---:|---:|---|---:|---:|
| First-profile New | 5.526–5.815 | 5.574–5.994 | +179, −149, +111 | **+111ms / +2.01%** | 1/3 |
| Repeat New | 5.089–5.182 | 5.135–5.216 | +46, −46, +100 | **+46ms / +0.90%** | 1/3 |
| First-profile Continue | 7.977–8.053 | 7.619–7.754 | −222, −433, −363 | **−363ms / −4.55%** | 3/3 |
| Repeat Continue | 6.712–6.896 | 6.740–6.813 | +45, −156, +101 | **+45ms / +0.66%** | 1/3 |

First Continue restoration itself is **289–322ms faster** in all three pairs. New station-room preparation is **9–13ms faster**, but differences in the earlier `interface_and_grid` stage are **+207/−112/+92ms** and dominate the whole-New direction. The diagnostic prime transitions confirm B's extra New-room paths first appear in `station_rooms`, after those interface/grid differences. Repeat interface/grid differences also change sign. These data do not establish absence of a small regression; they do not support a general loading gain either.

The reporting pitfall is observable in this cohort: independent fresh-New medians are A=5.722074/B=5.636736s, which would suggest B is 1.49% faster. The matched pairs instead have median **+111.020ms**, with B slower in two of three. Added paired-effect reporting and three Python regression checks, including this actual sign reversal. Earlier two-pair reports retain their original method/results; this correction does not retroactively explain their mixed observations.

## Hypotheses checked

- **Different learned order:** ruled out for the inspected old profiles and every new paired visit. Old New manifests have 12,762 requests/12,690 unique paths; Continue 13,360/13,286. New repeat observer inputs were additionally cloned byte-for-byte, including shader cache and profile state. Repeats prime zero new paths in both builds and request the same worker count. The changed announcement returns without replacing the learned order.
- **Consistent second-launch penalty:** all three primary fresh-New pairs had a slower second lane, irrespective of build. Four additional unchanged-fixture fresh New controls using the *same build twice* give A **5.598113→5.499317s (−98.796ms)** and B **5.542544→5.738473s (+195.929ms)**. A consistent ordering cause is not reproduced. Variation of comparable size exists without changing the build. This is evidence of variability, not identification of OS caching, thermal, scheduler or driver causation.
- **Reports interfering with the measured load:** scratch automatic reports capture the post-timing crew-identity work. Their capture triggers follow timed completion/uncovering; loading itself is suppressed by the existing monitor. Reports remain inside scratch profiles. Whole-process memory/CPU totals still include that diagnostic work.
- **Large station-audio `_ready` cost in this fixture:** eight separate diagnostic runs add a read-only node/render observer plus five seconds of ordinary simulation after the original timed checks, identities and screenshot. Main station audio `_ready` takes only **13.9–15.2ms under silent/Dummy audio**. This does not rule out real-device initialization/mixing costs or earlier audio resource preload outside that interval. No production source overlay is used.

## Remaining loading boundary

The eight observers consistently locate a gap from the final station-audio ready event (after the startup flag is set) to the first subsequent `frame_pre_draw`: **New 908–965ms; Continue 1,586–1,626ms**, in fresh and repeat profiles. Main setup has returned before this gap. Existing automatic-report counters record substantial grid redraw work in startup frames, but those cumulative counters overlap named stages and must not be added to them.

This localizes a useful target to **initial drawing/deferred scene work before the render signal**. It does not identify the responsible engine function, prove the whole gap is grid drawing, or measure GPU time. Node/render observation did not resolve the exact cause of the broader interface/crew variation. Next useful investigation: finer clocks around initial grid redraws, deferred interface layout and first presentation, followed by a controlled comparison if a specific fix is justified.

Observer loading times are kept separate from the 24 primary runs: additional callbacks and a changed post-timing fixture tail make them diagnostic evidence, not substitute headline timings. See `followup-analysis.json` and the per-run `*-draw-observer.json` files.

## Memory, appearance and integrity

Primary first-Continue sampled private peaks were **A 2,632–2,643MiB/B 2,710–2,812MiB**. Retain this higher B observation. Diagnostic first-Continue follow-up reverses it (**A 2,650/B 2,632MiB**); early Continue texture totals are 1,543MiB in both diagnostic lanes and after five further seconds span **1,560–1,563MiB** across fresh/repeat lanes. Dynamic presentation caches continue to populate. No stable private-memory regression, leak, exact-residency equality or memory improvement is established by this short check. One original early B texture point of 1,359MiB remains recorded.

All workers/caches release after startup. Maximum observed decode queue **96**, compression queue **8**, repeat decoded-image peak **214.23MiB**; the decoder has a job-count bound, not a strict byte cap. The 16MiB recent-image cache releases at the end. Memory peaks are sampled lower bounds and include QA overhead.

All **36 processes /18 matched or same-build control comparisons** have full crew signatures consistent within entry mode; New/Continue Bill binding remains deliberately different. Complete guards check normal simulation, default gameplay flags, missing artwork and engine/script errors. Representative saved native station/card screenshots are reviewed; prior exact pixel/geometry tests still apply to these unchanged PCKs. The full-image preview again omitted A's cards in its display; inspecting actual PNG hand crops confirms the cards are present and match B. This is a preview issue, not a reproduced game change. These loading fixtures do not replace release gameplay or native Mac acceptance.

Final integrity verification passes: **124 frozen delivery checksums** and **2,948 protected player files unchanged**, checkpoint/layout fixtures unchanged, no Godot process remains. The matching Windows/Mac pair and all prior candidates/sources are preserved. Verified task-owned duplicate EXE/PCK cleanup removes **7,476,727,025 bytes (6.963GiB)**; canonicals, QA overrides, evidence and restoration map remain. Free C/D **114.982/41.252GiB**, above the 20GiB reserve. See `final-guards.json` and `runtime-restoration.json`. Fresh-context review finds no material issue; the minor Dummy-audio scope clarification is incorporated. No commit or publication.

## Changed files and retained work

Only this report, `docs/CURRENT_STATUS.md`, the task plan and ignored diagnostic/report helpers change. No runtime/gameplay files change. Plan/ledger: `docs/superpowers/plans/2026-10-16-loading-variance.md`. The matching d3 Mac kit remains the owner's native validation target. Large-station 60 FPS, pacing/endurance and broader release gates remain open.
