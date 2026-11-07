# Project handoff

Updated: October 11, 2026 · Project: BrineSpace · Task: structural-action verification and placement stall attribution

## Objective and acceptance
Continue the full performance/release plan. Verify urgent lighting/placement/demolition after installed zoom scheduling, and investigate every >50 ms frame and the observed >100 ms placement stall. These checks do not certify the release.

## Accepted decisions and constraints
Muted secondary display, isolated profiles/owner fingerprints, reused debug=false runtime. Preserve real saves/layouts, gameplay, visual quality and UIDs. Dedicated fixtures alone use free building/disabled failures. No runtime copies or screenshot batches. Production logic unchanged this pass.

## Current state
New private action wrapper labels real success/blocked reasons for nine lighting toggles, three connected solar placements and three demolitions per run. Standard gameplay methods called once; no forced actor relocation or bypass of demolition blockers. Source fixture timing/inputs match in both lanes.

Pilot v1: current pair valid with nine exact phase states and fifteen exact successful action events. Large fixture failed before measurement because connected placement search applied to fixture generation too. Corrected v2 scopes that rule to the placement action. Failed evidence retained; owner guard unchanged. V2 large pilot valid and included once in completed three-pair set (cached pilot reports retained, not rerun). No historical result used to excuse the initial failure.

Private scripts in output/renderdoc-tools-2026-10-08: run-zoom-structural-actions-pilot[-v2].py, run-zoom-structural-actions-three-pairs.py, analyze-zoom-structural-actions.py, run-structural-crew-attribution.py. Evidence in D:/bs-release-crew-cache-20261009/benchmark-input-isolation/{zoom-structural-actions-pilot,zoom-structural-actions-pilot-v2,structural-crew-attribution}.

## Verification
Corrected current/large set: twelve native runs, three alternating pre-change/installed pairs per map; 19,440 measured frames, lighting/connected placement/demolition at 1x/2x/4x, 180 frames per phase. All 54 full phase states/cameras and 90 paired action events exact; every action succeeds (including all eighteen paired demolitions), no blocked action counted as coverage. No engine errors/missing runtime art. This verifies exercised behavior, not frozen structural pixel acceptance beyond the already passed maintained native visual test.

| Metric | Current before → installed | Large before → installed |
|---|---:|---:|
| Mean ms | 11.765 → 11.748 | 24.840 → 24.569 |
| p95 ms | 16.789 → 16.815 | 41.192 → 40.565 |
| p99 ms | 26.461 → 27.952 | 52.682 → 52.346 |
| Maximum ms | 47.864 → 47.906 | 94.769 → 100.481 |
| >50 / >100 frames | 0/0 → 0/0 | 69/0 → 57/1 |
| Texture peak MiB | 1940.818 → 1940.818 | 3028.476 → 3028.476 |

Whole means effectively neutral/mixed: current -.145%; large -1.093%, with two of three large pairs slower and the first accounting for the pooled improvement. Do not claim structural/FPS gain. Current p99 worse. Lighting/placement/demolition timings remain separate in comparison.json. Large placement p99 61.842→64.727; demolition p99 45.614→43.299. Frame gates remain failed.

Observed installed large placement at 1x frame30: 100.481 ms, action7.598 ms, update43.039 ms, grid drawing35.452 ms, zero sampled texture uploads. Other repeats same logical frame89.749/91.691 ms. Crew snapshot42.458 ms at the largest frame accounts for nearly all update cost. This is an observed >100 ms frame, not yet a reproduced >100 ms severity threshold; recurrent ~90 ms structural stalls are established and require remedy.

One bounded role probe, 1620 frames, keeps nine full phase states/cameras and fifteen action events exact. Method timings overlap: update contains rebuild/goal work. At 1x placement: James update24.400 ms, rebuild10.878, goal selection13.084; two generic companion rebuild calls total12.691 ms. At other structural events James rebuild~6.4–7.1, goal~7.2–11.4, two companions rebuild~12.2–12.9. Thus three navigation rebuilds plus James goal selection are concrete next targets. Do not add these nested totals or treat diagnostic overhead as acceptance. Ring8 frames/64 labels, metadata only; no overflow.

All owner guards2938 unchanged. Production grid still equals installed measured candidate. Native jobs terminal/shared override restored; no source changes from instrumentation. Free C122.07/D68.97 GiB. Accounted evidence54.41 MiB logical and scratch41.09 MiB via recorded profile locations; prior cached-profile remnants may add small storage. Twelve completed trace files explicitly compressed with NTFS, no runtime/PCK/player files touched: logical38.96 MiB→allocated14.91 MiB, saving24.05 MiB. Full comparisons rerun successfully after compression; compression.json records allocated sizes and current content hashes. Future report compression should happen only after a run is terminal.

## Next action
Attribute the three navigation rebuilds to their actual construction stages and James goal selection to route/target evaluation using current source. Preserve graph ordering, actor state, save bindings and exact behavior; do not replace synchronous work with unverified delayed behavior or assume graphs can be shared across actors. Seek a measured substantive reduction in these ~30–43 ms update spikes alongside ~30–35 ms structural drawing. Keep separate recurring GPU-image upload problem and all original endurance/loading/bug/UI/target PC/Mac/signing/package gates open.
