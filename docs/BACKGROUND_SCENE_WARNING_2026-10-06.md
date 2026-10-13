# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: background scene-loading shutdown warning

## Objective and acceptance

Isolate the anonymous reference-count-zero warning without suppressing it, reducing quality or removing Studio. Preserve responsive loading and the full PC/Mac release plan. Normal memory-provider admission and release certification remain open.

## Accepted decisions and constraints

Private controls only. Keep current source and frozen provider intact. Loading-path evidence does not establish the exact C++ defect, and clean synchronous loading is not an accepted workaround if it blocks the interface.

## Current state

Controls and logs: `output/drone-main-lifecycle-2026-10-06/`. Added ordinary/indexed and Studio controls, synchronous loading controls, a bounded single-worker loader prototype, and scene-resource-only probes. No normal source, loader, renderer or art changed this turn.

## Verification

| Native control | Checks | Exit warning |
|---|---:|---|
| Ordinary drones, Studio, two Main cycles | 182 | Five zero-reference objects |
| Indexed drones, no Studio, two Main cycles | 192 | Four zero-reference objects |
| Synchronous scene load, indexed/no Studio, two cycles | 192 | None |
| Synchronous scene load, indexed/Studio, four cycles | 398 | None |
| WorkerThreadPool wrapping ResourceLoader.load, indexed/Studio, two cycles | 194 | Five zero-reference objects |

All behavioral/lifetime checks pass; successful native logs contain no engine errors. Counts are diagnostic observations, not equal-workload memory deltas. Procedural sites differ between fresh profiles; these are mode-isolation checks, not matched performance certification.

Synchronous cold scene-resource load blocks the main thread for 2,018,521 us; subsequent loads 2,379/1,981/2,187 us. Reject the cold blocking behavior for normal admission. Worker prototype takes 1,985,039 us with 120 main-loop frames observed; warm 16,811 us/two frames. It keeps the loop advancing but fails warning elimination; no normal admission or early-cancellation safety acceptance.

Further native reduction loads a PackedScene but never instantiates it. Private scene: threaded loader 24 zero-reference warnings, synchronous zero, direct worker 27. Unmodified normal `res://scenes/main.tscn`: threaded 29, synchronous zero. Thus the trigger is reproducible in background resource loading before station, crew, drone or Studio execution. New indexed rendering and Studio are not necessary conditions. This revises the earlier full-scene constructor hypothesis; do not keep diagnosing the warning solely as retained animation ownership.

All completed lanes verify scratch user data and fingerprint all 2,936 owner non-log files unchanged. Processes terminal. No export, commit or upload.

Primary research: [Godot issue #120661](https://github.com/godotengine/godot/issues/120661) reports matching zero-reference shutdown diagnostics with sub-threaded loading; [proposed fix #121025](https://github.com/godotengine/godot/pull/121025) identifies ignored LoadToken unreference results. Both remain open as inspected. BrineSpace calls the default false sub-thread option, so these reports support a hypothesis rather than prove the exact engine defect. [Background loading documentation](https://docs.godotengine.org/en/4.4/tutorials/io/background_loading.html) explains why synchronous loads can block the interface; our two-second measurement verifies that limitation here.

## Next action

Compare a physically frozen, actual debug=false compiled/PCK scene-loading case using the maintained release workflow, then reduce affected dependency loads if needed. Determine whether the release path shares the source-loading warning and whether a responsive workaround exists. Do not switch normal loading to the blocking or still-warning worker prototypes. Continue memory-provider composition/source integrity/admission and larger frame costs; original memory/loading, packaged bugs, endurance and Windows/Mac gates remain open.
