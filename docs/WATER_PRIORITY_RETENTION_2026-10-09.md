# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: verified worker scheduling and semantic drone retention

## Objective and acceptance

Continue the full PC/Mac performance/release-readiness plan. Resolve private worker
queue stalls and extra resource overlap without sacrificing pixels, animation
availability, simulation or owner data. Release gates remain unmet.

## Accepted decisions and constraints

All changes remain private. Normal gameplay source is unchanged. Higher worker
priority resolves one measured hitch but is not admitted as a general FPS fix.
Pose availability must be preserved while removing large animated-sheet overlap.
No asset edits, downscaling, frame reduction, renderer change or publication.

## Current state

Corrected reversed retention pair validates three instantiated inherited worker
scripts, 3000 trace rows and 5879 unique measured worker events per lane; event
coverage matches joined-counter deltas. All source identities, timestamp arithmetic
and current-output branches pass. Blanket one-frame memory gain repeats at 63.398 MiB,
but FPS/tails vary by order and a source-counter audit finds one extra 0.766 MiB
north cargo-pose upload. private_end.uploads=4074 is CREW presenter traffic, not drone
traffic. Raw reports are unchanged; the earlier handoff's label is corrected.

Worker timing isolates scheduling: typical builds take 1.6–2.4 ms; the rare low-
priority queue takes 32–36 ms and causes 26–29 ms joins. The largest gameplay stalls
remain large upload frames with tiny worker joins. Actual settings: 24 reported
processors, max_threads=-1, low_priority_thread_ratio=0.3, startup prefetch inactive.

A controlled four-thread/two-low-worker occupancy fixture exercises actual canvas
submission and unconditional joins. Low priority: 7 checks/1 expected failure,
28.595 ms queue. High priority: 7/0, 20 µs queue, 1 µs join and byte-identical commands.
Godot documents task priority and mandatory completion waits in its
[WorkerThreadPool API](https://docs.godotengine.org/en/stable/classes/class_workerthreadpool.html);
its [worker-pool settings](https://docs.godotengine.org/en/stable/classes/class_projectsettings.html#class-projectsettings-property-threading-worker-pool-low-priority-thread-ratio)
describe low-priority thread allocation. These describe the mechanism; runtime
measurements establish the effect here.

Two priority-only actual debug=false 1080p large-station pairs, opposite orders,
retention=1 both lanes, complete timing/readiness payloads:

| Metric | Low priority | High priority |
| --- | ---: | ---: |
| Worst queue, candidate-first / reverse | 32.962 / 33.548 ms | 0.482 / 0.167 ms |
| Worst join, candidate-first / reverse | 27.355 / 28.484 ms | 0.013 / 0.327 ms |
| Measured layer-readiness misses, first / reverse | 796 / 797 | 800 / 804 |

Mean/p99/max comparisons remain mixed; high priority worsens 2×/4× mean in both
orders. PNG availability changes slightly, and upload batches shift across frames.
The improved local hitch cannot be credited wholly to worker wait: the faster frame
also uploads fewer layers before asynchronous decoding completes. Keep private.

Synchronous PNG fallback was measured rather than assumed: 33 measured calls total
about 12.2 ms across 3000 frames, largest under 0.7 ms. It is not the sustained CPU
hotspot. Three queued requests exist before teardown, but actual scene exit drains
all three; post-exit pending count is zero. Existing main/drone-dock cleanup is
effective. No decode-job leak is established. No cleanup rewrite is justified.

The refined retention policy registers complete multi-frame sheet paths from
existing clip/wheel/rotor metadata. Only those use one-frame exemption; poses and
unclassified images retain the original two frames. Pose regression fixture: 8
checks, blanket policy red3, semantic candidate green0. Retained GPU pixel/RID/weak
reconnection/release fixture: 9/0 on the new policy.

Matched semantic-retention release pair, water priority LOW both lanes:

| Metric | Reference (two frames) | Semantic candidate |
| --- | ---: | ---: |
| Texture peak | 2408.880 MiB | 2345.481 MiB |
| Drone uploads before teardown | 486 | 486 |
| Crew presenter uploads | 4074 | 4074 |
| Mean, 1× / 2× / 4× | 38.667 / 39.342 / 40.683 ms | 38.990 / 39.421 / 39.888 ms |
| p99, 1× / 2× / 4× | 54.431 / 61.582 / 73.126 ms | 55.994 / 57.454 / 71.737 ms |
| Worst frame | 138.372 ms | 142.367 ms |

All per-source drone upload counts match. Gameplay phase/final endpoints match;
6238 jobs joined, peak2/active0, full navigation recovered, router released. PNG
readiness misses vary (794/799 measured), so full visual availability still needs
validation. This confirms the refined memory remedy, not general admission.

Worst 4× frame uploads mine-west and mine-west-effects, 137.812 MiB each: 36.5–39.9 ms
inside texture creation. Worst 2× batches 321.56 MiB and costs 47.1–52.2 ms inside
creation. Remaining grid draw work and independent full-navigation stalls also
persist. Avoid extrapolating this private RTX 4070 Ti workload to target hardware.

Evidence: D:/BrineSpace-performance/2026-10-08/moon-navigation-owner/ directories
drone-retention-corrected-reverse/, water-worker-priority-proof/, water-priority-runtime/,
water-priority-reverse/, drone-semantic-retention/, semantic-retention-runtime/.
Raw reports/logs, compiled identities, deduplicated events and analysis.json retained.
Checkout changes: private helper/probe scripts, this handoff, prior handoff correction
and CURRENT_STATUS.md. No normal gameplay implementation change.

## Verification

Actual release checks: debug=false, source/branch/capacity/timing/event-coverage guards,
clean logs, no missing-file failures, focused windows, all three natural missions
return/unload/full graphs. Owner 2936 non-log files unchanged in every pair/probe;
temporary adapters restored and processes terminal. Native/headless fixture checks
are scoped mechanisms, not packaged visual or target-platform certification.

## Next action

Profile remaining crew presentation and texture create/update costs separately from
other grid work. Investigate a bounded way to reduce allocation/upload bursts while
preserving original dimensions, formats, filtering, pixel output and resource-owner
identity. Admit a remedy only with matched timing, native pixels and lifecycle proof.
Do not replace the excluded synchronous-PNG or leak hypotheses with speculative
fixes. Reverse-test the semantic policy and exercise animation readiness during
transitions before integrating it. Full loading, 12-room memory, bug, UI, endurance,
save/Continue, target-hardware and Mac signing/native certification remain open.
