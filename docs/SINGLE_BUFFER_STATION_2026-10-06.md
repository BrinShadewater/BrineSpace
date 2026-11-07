# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: full-scene single-buffer loading

## Objective and constraints
Validate the loader improvement in a matched native station workload without changing
pixels, gameplay, default quality or owner data. Normal backend remains unchanged.
Both variants use the compressed private bank, cached bounds and current camera
lifetime guards. Only the single-buffer decode/share flag differs.

## Current state
Generator: `output/compressed-crew-2026-10-06/prepare-single-buffer-station.py`.
Evidence: `bounds-cache/single-buffer/station/` under that directory.
Three matched 1080p pairs, one candidate-first and two reference-first, each in a
new guarded scratch profile. Forty rooms, Veld/James/Marsh active, powered production
and drones; 60 fixed simulation steps per action at 1x/2x/4x across idle, pan, zoom,
lighting and interface. These are native debug diagnostics, not release executables.
Fresh scratch profiles have no recorded startup prefetch order; OS disk caches were
not flushed. The previous dedicated bank cold/warm lane remains separate evidence.

## Verification
| Pair | Reference ready | Candidate ready | Saving |
|---|---:|---:|---:|
| 0 | 14,117.062 ms | 12,824.339 ms | 1,292.723 ms |
| 1 | 14,346.363 ms | 13,563.229 ms | 783.134 ms |
| 2 | 13,908.453 ms | 12,696.006 ms | 1,212.447 ms |

Median paired saving **1,212.447 ms**. Median readiness 14.117→12.824 seconds.
Readiness excludes initial scene-resource loading, dialogue and synthetic fixture
preparation; do not claim the <=10-second cold release gate passes.

Full crew snapshots (needs/path/goal/RNG included), room power, drone phases, action
and speed match in all **45 nonempty phases**. Both renderers present Veld 130,
James 286 and Marsh 61 distinct frames, with zero missing private routes. No art
failures or engine errors; all six processes exit cleanly. Owner fingerprints
(2,936 non-log files) remain unchanged. Prior complete selected-bank pixel/metadata/
filter/timing consumer evidence remains applicable; no selected-art changes here.

Candidate texture memory 2,619.398 MiB in all pairs; reference same in pairs 1/2
and 2,619.556 MiB in pair 0. Four slots/26 live spills in each run. Pair 0 has six
extra reference route calls and three uploads despite matching phase state; do not
present exact draw-count equality. Source payload/unique frame counts stay unchanged.

Windows peak working-set candidate-minus-reference +91.086/−37.422/+9.164 MiB;
private-commit deltas +29.398/−85.777/−39.660 MiB. No consistent working-set reduction
established. Do not combine these counters with textures or infer Mac unified memory.

Phase mean frame times remain ~35–36 ms, no FPS improvement established. Candidate
worst phase p95 65.423/70.435/66.498 ms and p99 85.362/91.975/85.477 ms: frame gates
fail. This loader work does not resolve rendering/redraw or upload costs.

## Decision and next action
Retain the single-buffer implementation as a measured private candidate. Do not
enable normal gameplay yet. Next actual title/loading progress and save/Continue
coverage using this loader, including malformed/missing PNG diagnostics and warm
scene measurements. Worker alias decoding remains an independent hotspot; keep
scheduling bounded. Anonymous exit warning, larger spill/endurance checks, 12-room
memory budget, original bugs, packaged Windows and native Mac certification remain.
