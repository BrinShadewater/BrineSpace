# Performance diagnostics handoff

Updated: September 12, 2026 · Project: BrineSpace · Task: monitoring and bug-finding pass

## Objective and acceptance

Make playtest slowdowns observable and attach useful evidence to the existing local bug report. Implemented and tested in the editor project; no release export or owner playtest acceptance claimed.

## Accepted decisions and constraints

- F7 toggles a mouse-transparent performance overlay without pausing. F8 opens the bug reporter. F9 opens Room Layout Studio, resolving its previous F8 collision. These keys are reserved from gameplay remapping.
- Sampling runs while the overlay is hidden. Retention is bounded to 120 approximately one-second buckets, 32 recent frames at least 50 ms long, and 2,048 percentile samples per bucket. Counts and means continue beyond the percentile sample cap, which is explicitly recorded.
- Manual F8 bundles include `diagnostics/performance.json` alongside existing logs and a separate live station save. Reporting does not overwrite the player's checkpoint. Collection makes no per-frame disk writes and does not enable the heavy draw profiler.

## Current state

New `scripts/performance_monitor.gd` collects wall-clock frame intervals, mean/p95/peak, hitch counts and pause/focus markers. Once per bucket it samples draw calls, process timing, static engine memory, object count, window/vsync/FPS settings, room counts and retained floor/wall rebuild counters. F7 shows the compact subset.

Integration changes: `scripts/bug_report.gd`, `scripts/main.gd`, `scripts/settings_panel.gd`, `scripts/title_settings.gd`. Coverage: `tests/test_performance_monitor.gd`, `tests/test_performance_reporting.gd`, paired UIDs, and the `performance-diagnostics` group in `tests/index.json`. README documents the shortcuts.

## Verification

- Headless collector checks passed: mean/nearest-rank p95, peaks, pause/focus counts, bounded retention, sample cap, independent snapshots, invalid inputs and JSON serialization. Final log: `output/test-runs/20260912-214729-headless`.
- Native integration passed using actual key events: F7 visibility, F8 routing without Studio, running and already-paused restoration, F9 Studio, real ZIP readback with timing history and diagnostic save, unchanged checkpoint, and omission of new-process timings from previous-crash reports. Final log: `output/test-runs/20260912-214701-native`.
- Overlay captures visually reviewed at 1600x900 and 960x540: `output/performance-monitor-20260912/overlay-1600.png` and `overlay-960.png`. Test ZIP lives in the same directory. Fixture timings include loading Studio and switching focus; they are not a gameplay benchmark.
- Synthetic `observe()` cost was about 0.19 microseconds/sample in the initial unit run. This measures only sample accumulation, not total monitoring or rendering overhead.

## Limits and next action

Frame intervals include vsync, focus changes, pauses and startup work; bucket context is sampled at its end, not averaged. Memory is static engine allocation, not total process/GPU memory. Timing history is current-process memory only: it cannot survive a crash, and an automatic report on the next launch deliberately excludes that launch's timings.

During the next ordinary expedition, press F8 soon after a slowdown or gameplay error and describe the action, expected result and actual result. The report can connect timing spikes to room counts, cache rebuilds and a reproducible station snapshot. This pass does not identify a new dense-station bottleneck or claim improved game FPS. Persistent crash breadcrumbs or action replay remain possible follow-ups if these reports prove insufficient.
