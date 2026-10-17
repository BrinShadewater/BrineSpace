# Project handoff

Updated: October 15, 2026 · Project: BrineSpace · Task: render submission batching

## Objective and acceptance

Continue toward 60 FPS with identical appearance. Attribute remaining submissions,
batch a measured group without reordering pixels, and compare actual release frames.

## Accepted decisions and constraints

Install ordered Windows synergy-circle packets. Keep the native platform fallback,
all clocks, geometry, colors, lines/arcs, crew, doors and warnings. Private room LOD
remains private. No Windows delivery update, Mac acceptance, commit or publication.

## Current state

- `scripts/grid_canvas.gd`: only two synergy regions changed. Eight consecutive
  edge/mote circle fans become one triangle submission. The earlier shared-door
  circle stays separate across its intervening arc/line boundary. Original
  `Transform2D * SYNERGY_UNIT_CIRCLE`, fan indices and blend order are retained.
  The lazy per-Grid index table is 1,536 integers / 6,144 bytes; geometry/colors are
  temporary per segment. `--reference-synergy-packets` preserves the original path.
- `tests/test_synergy_circle_packets.gd` and paired UID: native exact pixels,
  seven-call reduction per segment, shaders/tint/transforms/clocks/profiles,
  immediate toggles, platform fallback and owner teardown. Registered in
  `tests/index.json` render-perf, explicit native override because the capture-guard
  heuristic incorrectly classifies it headless. Test expectations respect platform
  support; this is not native Mac validation.
- `docs/CURRENT_STATUS.md`: milestone recorded.

Evidence: `C:/bs-render-submit-20261015/`; drivers:
`output/render-submit-20261015/`. Candidate PCK SHA256:
`96a44745a0e92ac16d1f19400fce639b7cb1c442ca1bae450e127cf8ef9eb97e`.
Reference PCK: `b6a8c044702dc41c700e03ddf39d905d86e3a7114abfb94fceff25f8015f56ea`.
Normal Grid file SHA256:
`b7f6cae2b50dc2ebd1aa9084a3284c6bc07b39884b6399a404ea0a4db5146c9d`.
`production-source.json` identifies the two measured helper blocks; the rest of
normal Grid, including the absence of private LOD, is preserved.

## Verification

Frozen paused native census: 2,352 calls, restored exactly after suppression.
Eight functioning synergy segments / 72 circles; hiding synergy removes 112 calls.
Conditional overlapping groups: floors 399, live surface 490, large rooms 320,
environment 443 (foundations 143, terrain 156), walls 200, doors 189, ordinary
contents 147, lighting 22. Suppression includes batch merges; these deltas are not
additive, and frozen timings are not running-game performance.

Correct regression red reports the missing packet flag. Private native green:
734 checks / 244 exact visible image pairs, each eligible segment seven calls
fewer; native fallback identical. Full actual-release station parity adds 12 exact
image comparisons at fitted / 0.25 / 0.5 zoom, both directions; frozen gameplay
states match. Representative station image reviewed.

Installed-source tests: `output/test-runs/20261015-085018-native/`. New packet test
734 checks / 244 pairs, original native-circle oracle 1,152 exact comparisons.
Both pass; no logged errors/warnings/leaks. Review found one test portability
issue, corrected before installed validation; no production correctness finding.

Actual debug=false release: 3,840 frames, idle/pan/zoom/lighting at 1x/4x in both
orders. All 16 gameplay/camera pairs match, loaded-source/PCK identities verify.
Process guard finds no foreign Godot worker or duplicate game.

| Order | Reference mean | Candidate mean | P95 improves | >50 ms frames |
|---|---:|---:|---:|---:|
| Reference first | 22.503 ms | 22.014 ms | 7/8 | 3 -> 2 |
| Candidate first | 24.197 ms | 22.040 ms | 6/8 | 5 -> 4 |

Calls drop about 56/frame (normal idle 2369 -> 2313, about 2.4%). First-order
effects CPU saves 88–128 us, delayed render CPU saves 0.089–0.231 ms. Normal idle
19.405 -> 19.038 ms; candidate repeat 19.032 ms (about 52.5 FPS). The reverse
reference also slows in unrelated live-room work and GPU time, so its 8.9% mean
difference is not an attributable gain. Do not claim that larger improvement.
All 16 candidate 60 FPS mean/p95 phase gates still fail. Texture peaks identical:
2784.653 MiB. Worst frames 72.291 -> 68.571 and 81.813 -> 65.640 ms; this scoped
trial does not establish a fix for structural-change hitches.

Fifteen guards preserve all 2,948 owner non-log files, including exploratory
failures. Excluded first census boot started before its pack finished; retry after
pack completion passes. First red test had a typed-WeakRef parse error; corrected
red establishes the intended missing-path failure. Neither is timing evidence.
Scoped whitespace checks pass. No task-owned QA process remains; owner editor
PID46624 stays open. Unrelated dirty work preserved.

## Next action

No checks remain for this bounded change. Larger submission groups are the live
room surface, floors and environment; a further batching proposal needs the exact
texture/material/order boundaries within those groups. Keep the measured modest
saving separate from full 60 FPS, endurance, structural pacing and PC/Mac release
acceptance, which remain open.
