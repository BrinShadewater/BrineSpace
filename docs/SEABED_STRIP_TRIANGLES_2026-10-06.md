# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: performance / seabed animation submissions

## Objective and acceptance

Continue the full PC/Mac performance and release-readiness plan. Preserve selected pixels, motion, default quality, scene ownership and saves. This milestone reduces plant drawing overhead; it does not certify frame, memory, loading or packaged-release gates.

## Accepted decisions and constraints

Keep the original ordered strip vertices, UVs, triangle topology and float tint. Submit each plant's strips together through the existing RenderingServer triangle-array API. No texture conversion, shader replacement, geometry simplification, permanent cache or animation-clock change. Reduced-motion/Low paths and complete sway culling envelopes remain unchanged.

## Current state

- Normal `scripts/ambient_fronds.gd`: six original strip polygons become one ordered submission.
- Normal `assets/environment/upright-kelp-v1/upright_kelp_view.gd`: seventeen original strip polygons become one ordered submission. Existing module UIDs retained.
- Added `tests/test_seabed_strip_triangles.gd`, paired UID and native `render-perf` index entry. Its baseline draws the original immediate strip polygons.
- Private evidence and frozen pre-change implementations: `output/seabed-strip-triangles-2026-10-06/`. Initial attribution: `output/seabed-stage-profile-2026-10-06/`.

## Verification

Native diagnostic attributes most seabed preparation to sub-biome props (~0.75 ms) and upright kelp (~0.62 ms), excluding first-phase startup accumulation. Private checks: 288 exact, nonblank image pairs; another 48 with selected frond sources, mirrored parent and flooding shader. Original/candidate sample captures visually inspected.

Installed normal regression: 288 exact, nonblank pairs using all three selected kelp and three current frond sources; another 288 mirrored/flooded pairs. Both cover fractional sizes, nearest/linear filtering, clock samples across the eight-second join and reduced motion. Zero failures or engine errors; logs checked independently of exit codes.

The first timing pair overlapped a short native visual probe; retained as exploratory evidence only. A clean private repeat and subsequent actual-normal pair ran without competing native probes. Actual-normal mixed 40-room pair: 60 measured frames per phase, 1080p, VSync disabled, private crew/drone memory providers shared by both controls. All six recorded crew/drone/door/light/power/zoom states and texture counters match. Five later phase deltas show combined plant preparation lower by 0.616–0.640 ms/frame; first phase includes warmup and is not a per-phase attribution.

| Workload | Reference p95 ms | Normal change p95 ms |
|---|---:|---:|
| Idle 1× | 43.305 | 42.363 |
| Pan 1× | 48.122 | 43.894 |
| Idle 2× | 42.586 | 41.383 |
| Pan 2× | 46.660 | 43.486 |
| Idle 4× | 49.812 | 46.370 |
| Pan 4× | 52.401 | 55.756 |

Frame results remain mixed and fail the release target. Candidate 4× pan includes a 64.776 ms frame with ~15.6 ms grid preparation, plus other stalls associated with multi-megabyte uploads. Inspection does not prove the cause of all remaining stalls or explain the full p95 difference; do not claim a universal FPS gain. Pure plant preparation improves in every phase. No memory gain claimed.

Every completed native lane fingerprinted the real owner folder before/after: all 2,936 non-log files unchanged. Scratch user-directory checks pass; successful processes exited cleanly. Normal module whitespace check passes. No export, commit, upload or art changes.

## Next action

Profile water-wave preparation (currently ~1.5 ms/frame) before attempting batching or geometry reuse; require exact transformed-texture output checks. Continue the larger steady renderer/system costs and private six-source drone/crew admission/lifecycle work. Original packaged bug checks, normal memory/loading budgets, endurance, Windows and actual Mac certification remain open.
