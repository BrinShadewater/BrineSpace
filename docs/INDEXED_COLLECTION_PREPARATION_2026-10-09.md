# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: bounded preparation for predictable mining collection

## Objective and acceptance

Reduce repeated collection-transition upload bursts without altering fleet state, pixels, playback, default settings or session lifetime. All original PC/Mac release gates remain open; no normal source admission.

## Accepted decisions and constraints

Keep the same twenty-source indexed representation/cache budget and all ordinary fallbacks. Prepare only selected indexed resources ≤64 MiB within two simulation seconds before the known work-to-collection transition. At most four speculative decode jobs and one prepared atlas per engine frame. Required current-frame readiness is unchanged. Skip unpowered, blocked, other drone kinds/phases and unsupported effective filters/materials. No permanent extra texture table.

## Current state

Private overlay `D:/bs-release-crew-cache-20261009/indexed-collection-preparation/`, copied/hash-verified from the twenty-source candidate. New `scripts/drone_trial/upcoming.gd` predicts paths using a copied dictionary and the original sampler; private Motion adds preparation plus bounded scalar diagnostics. No original source/art/package edits.

Tools under `output/renderdoc-tools-2026-10-08/`: `stage-indexed-collection-preparation.py`, `test-indexed-collection-prediction.py`, `pack-indexed-collection-preparation.py`, `prepare-indexed-collection-pair.py`, `run-indexed-collection-pair.py`, `analyze-indexed-collection-pair.py`.

## Verification

Isolated headless predictor contract: 216 checks/zero failures, exact source order across eight headings, three work durations and explicit window boundaries; no fleet mutation; disabled/interrupted/non-mining phases return no forecast. Pack succeeds, both owner fingerprints 2,938 unchanged. These checks do not prove native scheduling quota, resource pressure or performance benefit.

## Next action

Four actual debug=false 40-room idle runs complete with the same twenty sources, both orders, 180 samples per speed (2,160 frames total). Session 24805 terminal 0. Runtime source count20/factory/duplicates/fallbacks correct; candidate prepares three atlases, 144,606,208 cumulative bytes. All six captured states exact, no engine/missing-art errors, owner 2,938 unchanged. Evidence: `paired-idle/analysis.json` plus raw preparation snapshots.

At 4× means improve 30.703→29.966 /30.663→29.677 ms, maxima 62.803→53.023 /61.598→54.787 ms; p95 forward essentially unchanged/slightly worse, reverse improves. At 1× means regress 26.514→26.641 /26.284→27.048 ms, p95 worsens both orders and each candidate has one >50 ms frame versus controls zero. 2× means regress both orders, tails mixed. Earlier phase texture endpoints add 122.561/122.500 MiB; final 4× endpoint essentially equal. All FPS gates fail. This two-second window is not admitted.

Half-second private copy `D:/bs-release-crew-cache-20261009/short-collection-preparation/` completes four runs/2,160 samples and six exact state pairs, zero errors, owner unchanged. Initial means/p95/p99 improve all six, but 1× prepares no images, so the timing gain cannot be credited to upload scheduling. 2× prepares five atlases and adds 76.623 MiB at its endpoint; 1× endpoint matches. No acceptance from this first comparison.

Stricter `collection-same-pack/` uses identical source pack in both lanes, early enabled flag, tagged preparation events and equal tracing. All four runs terminal 0, owner unchanged. Trace proves five prepared atlas events per candidate, all at 2×, one per sampled frame, each ≤64 MiB; control events zero; complete metadata. Each paired body/cargo preparation is on successive frames. Collection overhead maxima 182–246 µs, outside timed frame samples. No job-peak or driver-bandwidth proof from these counters.

Same-pack forward pair preserves all three states but means regress ~0.100/0.760/0.883 ms at 1×/2×/4×. Reverse has exactly three differences: saved hover cell at each speed; all other compared fields match. Candidate means also higher, but reverse is contaminated and cannot certify behavioral parity. Failure retained in `paired-idle/state-diff.json`; strict comparator failure preserved, not waived by dropping hover. Reject current preparation version rather than promote earlier favorable timings.

Next benchmark input isolation was reproduced and repaired; see [input isolation](BENCHMARK_INPUT_ISOLATION_2026-10-09.md). Further renderer/upload remedy requires a materially different measured approach. Broader actions/material/motion/cleanup/lifetime and full release gates remain open. No production gameplay or delivery changes.
