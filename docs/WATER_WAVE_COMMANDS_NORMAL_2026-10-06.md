# Project handoff

Updated: October 6, 2026 · Project: BrineSpace · Task: normal wave-command admission

## Objective and acceptance

Continue the full performance and PC/Mac release plan. Preserve wave pixels, clocks, region sampling, materials, placement and fallback behavior. This admission reduces preparation overhead; overall release readiness remains unproven.

## Accepted decisions and constraints

Use the original RenderingServer rectangle and transform commands with local item/texture RIDs for ImageTexture waves. Keep the original Texture2D wrapper for other texture types, including AtlasTexture; keep missing-image polyline fallback. No new textures, shaders, nodes, permanent cache, segment reduction or quality change. Restore the draw transform after each wave. The earlier world-space triangle experiment remains rejected.

## Current state

- `scripts/grid_canvas.gd`: direct ImageTexture wave commands, unchanged original branches for other/missing textures; internal `--wrapped-wave-commands` comparison switch. Existing Grid UID retained.
- `tests/test_water_wave_commands.gd` and paired UID: native/render-perf registration in `tests/index.json`.
- Frozen original Grid, private candidate, actual-normal fixtures, logs and results: `output/water-wave-grid-2026-10-06/`.
- Earlier attribution and rejected prototype evidence remain in `docs/WATER_WAVE_SUBMISSIONS_2026-10-06.md`.

## Verification

Private actual-Grid comparison: 288 exact pairs across negative/positive cells, two fractional cell sizes/clocks, nearest/linear filtering, parent scale/reflection/modulation, flooding shader, lines/rects/all modes and selected/null/atlas textures. A marker drawn after the waves verifies transform restoration. Initial private duplicate global class declaration prevented inheritance; removed only from the private copy before successful checks. No production regression attributed to it.

Installed normal regression also passes 288 exact pairs, with zero engine errors. Explicit assertions prove reference wrapper/candidate direct switches differ and the selected source is an ImageTexture. Wave-only visibility assertion excludes the marker. Inspected first pair; independent alpha analysis counts 65 actual wave pixels (max alpha 6/255) in both images. A later run after adding the permanent visibility guard passes all 288 pairs again. No further native tests overlapped measured benchmarks.

Actual-normal matched mixed 40-room, 1080p benchmark: six 60-frame idle/pan phases at 1×/2×/4×, VSync disabled. Both branches use the same private crew/drone providers, so memory values are not normal-release certification. All recorded crew/drone/door/light/power/zoom states, texture counters and wave cell/segment counts match. Five later phase submission means improve by 0.256–0.265 ms/frame (~1.10–1.12→0.85–0.86 ms); path preparation remains ~0.4 ms. First-phase stage accumulation includes warmup and is excluded from per-phase attribution.

| Workload | Wrapper p95 ms | Installed direct p95 ms |
|---|---:|---:|
| Idle 1× | 41.096 | 43.894 |
| Pan 1× | 45.400 | 43.670 |
| Idle 2× | 40.849 | 42.043 |
| Pan 2× | 44.030 | 43.724 |
| Idle 4× | 46.405 | 46.865 |
| Pan 4× | 53.505 | 51.431 |

Whole-frame results remain mixed and above release targets. No universal FPS, GPU submission-count or memory improvement claimed. The larger frame costs and remaining stalls require further work.

All completed lanes verify scratch user data and fingerprint the real owner folder: 2,936 non-log files unchanged. Successful native logs checked separately from exit codes; all processes terminal. Scoped whitespace/index checks pass. No art edits, export, commit or upload.

## Next action

Move past the small wave-wrapper gain to larger steady room/actor/backend costs and private lossless crew/drone normal admission/lifecycle work. Preserve the full original memory/loading, packaged bug, endurance, Windows and actual Mac certification gates. This milestone does not close those requirements.
