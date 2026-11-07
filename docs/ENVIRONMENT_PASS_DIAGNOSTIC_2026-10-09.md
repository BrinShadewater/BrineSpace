# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: live environment attribution

## Objective and acceptance

Identify a measured rendering target toward the original PC/Mac performance and release gates. Exclusions locate costs; they are not acceptable production quality changes or proof of an optimization gain.

## Accepted decisions and constraints

Retain default effects, animation pixels/timing and offscreen simulation. Original source renderer and accepted delivery packages remain unchanged. Tests use isolated profiles; the known idle editor remains open, so these are diagnostic results on this PC, not target-hardware certification.

## Current state

Private one-file Grid overlay excludes one environment pass at a time. Twelve actual `debug=false` 40-room idle runs cover 1×/2×/4× in forward and reverse orders: 6,480 sampled frames. The separate LIFE-over pass stays enabled.

Evidence: `D:/bs-release-crew-cache-20261009/environment-pass-diagnostic/workloads/analysis.json` and per-run JSON/logs/identity files.

| Excluded pass | Forward mean reduction | Reverse mean reduction |
|---|---:|---:|
| Exterior activity | 2.515 ms | 2.475 ms |
| Water lines | 1.426 ms | 1.643 ms |
| Foundation shimmer | 0.593 ms | −0.142 ms |
| Fog | −0.197 ms | −0.062 ms |
| Sea life below station | 0.578 ms | −0.041 ms |

Control means: 28.043 / 27.951 ms. Costs are not additive. The smaller inconsistent differences do not establish a remedy. Exterior is the strongest reproducible target in this fixture; water lines are second.

## Verification

All 30 captured gameplay/save-state pairs match, including crew animation playback. Expected excluded callbacks are absent. Each successful log has no engine errors or missing-art failures; owner fingerprints remain 2,938 files with no changes. This does not establish motion parity, action workloads, actual target hardware or release FPS acceptance.

## Next action

Timing-only private exterior overlay separates harvest sites, transitions, construction, drones and survey probes. Tools are `stage-exterior-timing-diagnostic.py`, `pack-exterior-timing-diagnostic.py`, `run-exterior-timing-diagnostic.py` and `analyze-exterior-timing-diagnostic.py` under `output/renderdoc-tools-2026-10-08/`. Follow-up launched only after the exclusion driver completed successfully; session 5936 is now terminal, exit 0.

The follow-up samples 540 frames and passes all six state comparisons against both controls. Owner 2,938 unchanged; no engine/missing-art errors. Drone CPU windows average 0.919 / 1.629 / 2.293 ms at 1×/2×/4×. Harvest is only 0.114–0.120 ms; each remaining substage is under 0.015 ms. CPU timings include timer overhead and exclude GPU work; nested parent times are not additive.

All seven captured >50 ms frames include current sampled-frame drone uploads: 91.875–275.625 MiB, taking 7.154–36.124 ms. Corresponding drone drawing windows are 10.297–50.914 ms. Frame times are 51.726–78.382 ms. This is direct current-run correlation, not proof that upload removal alone meets FPS gates. Evidence: `D:/bs-release-crew-cache-20261009/exterior-timing-diagnostic/workloads/diagnostic-none.json` (`hitches`) and `analysis.json`.

Next trace selected drone atlas residency, weak-reference reuse, eviction and upload paths. Target the large-upload bursts while retaining animation pixels/readiness and memory budgets; do not increase the global cache speculatively or prioritize the much smaller harvest-site path. Both diagnostic jobs are complete. No optimization installed and full release gates remain open.

Hitch upload events all name mining-rover assets: collection body/cargo, mining body/effects, wheel, steering, starting and carrying atlases. South collection body and cargo recur in captured 2× and 4× hitches, showing repeated uploads of the same sources within this run. Texture bookkeeping uses a 256 MiB atlas cache with weak retained-canvas reuse; a single mining effects atlas is 137.8125 MiB. Inspect these exact paths and eviction/reuse conditions before changing residency policy.
