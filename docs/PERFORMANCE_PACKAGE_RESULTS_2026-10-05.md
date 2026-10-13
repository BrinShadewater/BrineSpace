# Packaged performance comparison

Updated: October 5, 2026 · BrineSpace · **Release blocked**

## Objective and accepted scope

Finish the interrupted Windows comparison using visible, isolated native release
processes. Preserve selected pixels, animation timing, filtering and default
effects. No engine change, art reduction, upload or visibility change.

Baseline: `brinespace-7cefe63089abd67a`. Candidate:
`brinespace-124c70736fbfb879`. The candidate combines previously validated wall
retention, solar preparation caching and room-image sharing; these results do not
attribute the total gain to any one change. The five runtime-file differences
and unchanged selected artwork were recorded in the preceding diagnosis.

## Results

Twelve accepted `debug=false` runs: three baseline 40-room runs at 1080p, three
candidate runs each at 1080p and 1440p, and three candidate 12-room idle runs at
1080p. Each action has 180 measured frames at 1x/2x/4x. The current corrected Node
driver and identical workload were used on both packages. An external-process
monitor found no competing Godot/game process; minimized-window guards passed.
This is the owner's RTX 4070 Ti PC, not GTX 1650 or M1 certification.

Values below are the median of three per-run p95 values, in milliseconds.

| Workload | Speed | Baseline 1080p | Candidate 1080p | Reduction | Candidate 1440p |
|---|---:|---:|---:|---:|---:|
| Zoom | 1x | 56.86 | 54.32 | 4.5% | 54.02 |
| Zoom | 2x | 60.98 | 59.29 | 2.8% | 60.59 |
| Zoom | 4x | 60.94 | 59.54 | 2.3% | 57.70 |
| Lighting | 1x | 87.38 | 70.77 | 19.0% | 69.05 |
| Lighting | 2x | 86.10 | 69.17 | 19.7% | 69.94 |
| Lighting | 4x | 88.09 | 70.96 | 19.4% | 69.33 |

The modest zoom difference is observational, without a statistical confidence
claim. All 45 candidate phase runs fail the combined p95/p99/stall gate.
Candidate large-scene median p99 values remain 80.31–96.43 ms at 1080p and
81.83–92.38 ms at 1440p. The 12-room idle p95 values are 19.12/19.47/20.38 ms,
with p99 20.80/25.66/27.49 ms at 1x/2x/4x, also above acceptance.

Large-scene reported texture memory falls from median 4091.36 to 4035.40 MiB
at 1080p (55.96 MiB); candidate 1440p is 4047.71 MiB. The 12-room candidate
uses 3631.29 MiB. Both memory gates still fail. These packaged end states differ
from the earlier source-inventory sample, which isolated 50.989 MiB decoded
duplicates and about 68 MiB on the engine counter; do not combine those savings.
The previously documented counter discrepancy does not exempt these budgets.

Candidate scene-request-to-ready: fresh-profile runs 13.01–14.61 seconds; warm
runs 6.15–6.35 seconds. OS disk cache was uncontrolled, so these are not certified
cold-disk measurements. Large fixtures first restore the reported save, then
construct the synthetic station separately; this does not measure loading a
saved 40-room station. Normal title/dialogue loading remains a separate gate.

## Stall and visual findings

All 6480 candidate large-scene trace frames have complete render boundaries.
969 exceed 50 ms; eight exceed 100 ms. The worst is 116.648 ms: 2.191 ms manual
simulation, 101.432 ms before the render signal, 12.724 ms between render signals,
0.286 ms afterward. Reported GPU time is 10.632 ms; median GPU time across the
large-scene traces is 10.075 ms. These CPU boundaries and asynchronous GPU counters
are different measurements. Evidence prioritizes pre-render work; it does not
identify every nested callback or prove GPU headroom on target hardware. Full
per-frame records remain available. One automatic diagnostic report was saved in
each run; diagnostics were not disabled to improve results.

The 1440p capture initially suggested station-control/time-panel overlap with a
room selected. Subsequent actual packaged wheel-input testing confirmed expected
scroll clipping: all hardware controls become visible and the time panel remains
fixed. No layout fix is warranted for that observation; see the later
`PRE_RENDER_OPTIMIZATION_2026-10-05.md` handoff. A synergy notification also covers part of
the station in the final capture. These workloads include normal progression UI,
not an overlay-free station. The capture does not close all nine original bugs,
motion/layering review, enlarged-text or Retina acceptance.

## Test-runner fix and verification

The earlier r5 candidate warm run logged `shader_gles3.cpp:802` during startup
and was rejected despite completing its workload. It reproduced in that profile.
Its cache paths reached 293 characters; ordinary Python copying also failed on
those paths. Fresh and warm short profiles started cleanly. Copying the original
profile/cache with extended-path access to a short location also started cleanly.
Godot's [shader-cache initialization source](https://github.com/godotengine/godot/blob/ed1daf0bf/drivers/gles3/shader_gles3.cpp)
informed the directory-setup hypothesis; the controlled relocation is the local
evidence. No cache was deleted and no game shader was rewritten.

`tools/run_release_benchmark.py` now relocates deep Windows QA profiles into
short temporary APPDATA folders, retaining a location record in the requested
evidence directory and recording the actual profile in every result. The normal
player profile is untouched. `tests/test_release_benchmark_runner.py` adds a
relocation/recording regression; all three runner tests pass. Workflow notes now
explain this retention requirement. All twelve r6 runs complete with zero logged
engine/script errors and their per-batch owner fingerprints match.

## Evidence and next action

Evidence root: `output/release-stall-trace-2026-10-04/`.
Accepted data: `baseline-corrected-r6/`, `candidate-corrected-r6/`,
`candidate-reported-r6/`, `package-comparison-r6.json`, `timing-monitor-r6.json`.
Shader probes and rejected r5 data are retained separately. Candidate and rollback
packages remain unchanged; this continuation changed QA tooling and documentation.

Next: attribute the large pre-render interval to retained-layer preparation,
draw callbacks or engine submission with bounded timing inside those phases;
fix the measured largest contributor and repeat a matched comparison. In parallel
with that sequence (not concurrent native measurements), replace the slow 40-room
reflective inventory with a bounded source/pool inventory and investigate
pixel-exact transparent-padding removal. The sidebar observation is resolved by
the later input-path check; the Research source cache in that handoff awaits export.
Two-hour soak, ten transitions, full bug/save/upgrade matrix, target PCs, Mac
gameplay/signing/notarization and distribution notices remain open. The previous
34-object exit warning remains unattributed; this short benchmark is not a leak
or long-session stability certification.
