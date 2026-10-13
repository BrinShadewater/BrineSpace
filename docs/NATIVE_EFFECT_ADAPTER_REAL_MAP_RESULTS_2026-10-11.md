# Project handoff

Updated: October 11, 2026 · BrineSpace · Task: native effect storage real-map results

## Objective and acceptance

Reduce memory and upload stalls without changing selected animation pixels,
timing, frame identity, filtering or simulation. Full PC/Mac release gates remain
open. This is diagnostic release-runtime evidence, not a freshly exported full
candidate, target-hardware certification or Mac acceptance.

## Accepted decisions and constraints

Original-pipeline LA8 effects adapter remains private pending selected-source hash
guard validation and integration checks. No extra palette shader/Group/look-ahead,
lossy changes or original art edits. Three native alternating pairs per scene;
muted secondary display, physical input disabled, isolated saves/user directory,
bounded reports and 20 GiB free-space floor. Reuse the existing runtime.

## Current state

Eighteen native debug=false RTX4070Ti/1080p runs complete, 19,440 measured frames.
All 108 complete gameplay states/camera paths/action-speed labels match exactly;
all input source hashes unchanged. No missing runtime art or engine errors.
Three repeats retain the same memory values in each lane.

| Scene | Mean ms, original → trial | p95 ms | p99 ms | Peak engine texture MiB |
| --- | ---: | ---: | ---: | ---: |
| Reported station | 12.700 → 12.788 | 18.685 → 18.912 | 21.902 → 22.606 | 1558.872 → 1558.872 |
| Current owner-copy station | 12.553 → 12.550 | 18.440 → 18.515 | 27.039 → 27.646 | 1940.747 → 1880.470 |
| Original 40-room fixture | 25.707 → 25.658 | 41.737 → 41.732 | 50.464 → 50.970 | 3028.007 → 2844.258 |

Average frame speed essentially flat: reported +0.69%, current -0.026%, large
-0.19%. No sustained FPS improvement claim. Large >50ms frames 36→38; maxima
76.545→74.604ms. No >100ms frames in either lane on these three scenes. Current
max47.045→43.685ms; reported27.280→30.045ms. Settled end memory unchanged in each
scene: reported1558.872/current1819.183/large1924.488MiB. Peak current saving60.277
MiB and large183.750MiB. Engine accounting is not physical GPU residency.
All scenes still exceed p95≤16.7ms; current/large exceed p99≤25ms. Do not certify
release performance from these results. Mixed large-room workload remains separate.

## Verification

Existing rendering/lifetime proofs are recorded in
[mixed results](NATIVE_EFFECT_ADAPTER_REPEATS_2026-10-11.md).
Owner2,938 files unchanged; original-map job terminal, runtime override restored.
Evidence: `D:/bs-release-crew-cache-20261009/benchmark-input-isolation/native-adapter-original-maps/`
including `comparison.json`, `identity.json`, `owner.json` and 18 run reports/logs.
Maintained private summary: `output/renderdoc-tools-2026-10-08/summarize-native-adapter-original-maps.py`.

Separate revised adapter now verifies selected original PNG hash before derived
selection. Native21 fallback/identity/accounting/explicit cleanup checks pass,
including stale original metadata, invalid derived SHA and missing derived file.
No errors, worker jobs0, owner unchanged. Its576 actual-draw pixel pairs now pass
exactly, including nearest/original fallback selection and accounting checks.
Updated-revision station/loading timing remains pending.

Existing mixed traces now have a bounded offline upload attribution. Original
slowest zoom frames in pairs1/2 are117.553/113.541ms with47.916/52.064ms upload work.
Candidate maxima73.347/77.134ms still upload both full RGBA body sheets in26.929/
28.426ms. Pair3 original130.850ms stall includes four collection/cargo uploads,
72.466ms total; that work is outside the three selected effect sources. This is
observed work within stalls, not exclusive attribution of their entire duration.

Deduplicated sampled/current-frame upload snapshots show159–162 unique observed
events per run and34 source paths uploaded repeatedly in each lane. Original
observed decoded upload volume5757.75–5895.57MiB; trial5619.94–5665.88MiB. Excludes
startup/warmup and is upload traffic, not retained memory; incomplete snapshots
would undercount. Artifact: mixed directory `upload-attribution.json`. No claim
that each large effect repeatedly uploaded: five observed effect paths each occur
once per measured run. Do not repeat the rejected larger global cache unchanged.

## Next action

`bill-update-attribution/runner.py` now runs on unchanged simulation to measure per-actor
topology-signature and fire refresh costs. Validate/tune only measured hotspots.
Selected-source guard revision still needs matched station/loading checks before
normal integration. Continue actual gameplay transition/endurance, original-nine
bugs, complete-source packages, GTX1650/M1 and Mac signing/certification separately.
