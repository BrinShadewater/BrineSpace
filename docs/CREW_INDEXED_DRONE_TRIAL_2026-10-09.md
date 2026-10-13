# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: combine accepted crew storage with prior lossless drone prototype

## Objective and acceptance

Reduce current measured drone upload bursts without changing pixels, clocks, default quality or scene ownership. Preserve original PC/Mac release gates. No source admission from this diagnostic.

## Accepted decisions and constraints

Reuse the sixteen-source prototype from the physical October 7 compiled source, preserving its indexed PNGs, original dimensions, shader/material composition and ordinary fallback. Do not repeat rejected cropped-frame or larger-cache remedies. Accepted crew storage and current frozen Grid remain the base; only narrow drone integration is applied privately.

## Current state

Private overlay: `D:/bs-release-crew-cache-20261009/crew-indexed-drone-trial/`, 45 hashed members. Stage/pack/run/analyze tools under `output/renderdoc-tools-2026-10-08/` with `crew-indexed-drone-trial` in their filenames. No production script/art/delivery changes.

The first actual release attempt failed Grid parsing before gameplay. The owned failed process was stopped, evidence retained in `workloads/`, owner 2,938 unchanged. Corrected raw overlay removes duplicate global Grid class registration and holds prepared helper scripts; `workloads-v2/` completes successfully, session 57136 terminal exit 0.

## Verification

Actual `debug=false` 40-room idle 1×/2×/4×, 540 samples. Six captured state comparisons against both original controls match; no engine/missing-art errors; owner 2,938 unchanged. This is one candidate after earlier controls, not an interleaved matched acceptance comparison.

| Speed | Candidate mean | Candidate p95 | Texture endpoint reduction versus controls |
|---|---:|---:|---:|
| 1× | 25.640 ms | 27.822 ms | 351.364 MiB |
| 2× | 27.521 ms | 36.739 ms | 320.683 MiB |
| 4× | 28.396 ms | 39.161 ms | 59.006 MiB |

All mean/p95 values are lower than both earlier controls, but ordering/one candidate limit the claim. FPS gates still fail. Four >50 ms frames remain, worst 70.093 ms. Source audit corrects initial interpretation: `motion.gd:88` forwards indexed events to `Ordinary.record_frame_upload`. The frame collector therefore includes indexed work; its untagged selected paths do not prove a backend bypass. Lifetime counters have separate scopes.

## Next action

Backend diagnostic 85836 completes 540 frames and six exact state comparisons, owner unchanged. All phase snapshots show active factory, 16 sources, zero selected-source ordinary duplicates and zero cumulative fallback draws in sampled groups; indexed draw counts 2,127/3,308/4,109. The bypass hypothesis is rejected in this workload. Explicit tags show South collection uploads are indexed. North/East effects, North body and East collection remain ordinary. Timing means 26.605/28.651/30.568 ms are less favorable than the first candidate: no repeatable whole-frame gain established. Evidence: `backend-diagnostic/analysis.json` and raw tagged hitch events.

Next expanded measured hotspots and current private validation are recorded in [twenty-source trial](INDEXED_DRONE_HOTSPOTS_2026-10-09.md). Matched both-order action workloads, composed-motion/material/fallback and lifetime checks remain required before admission. Historic native prototype coverage does not certify this combined package.
