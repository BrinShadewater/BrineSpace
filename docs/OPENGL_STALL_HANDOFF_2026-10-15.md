# Project handoff

Updated: October 15, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: OpenGL stall trace and lookup reuse installed

## Objective and acceptance

Trace current OpenGL zoom and room-placement stalls, improve a demonstrated cost
without changing appearance, and benchmark the same frozen QA workload. Preserve
exact navigation/route behavior and visual output. Trace and measured source
change complete. Construction CPU improves; general FPS/pacing and atlas stalls
remain unresolved. [Full results](OPENGL_STALL_TRACE_2026-10-15.md).

## Accepted decisions and constraints

Production stays Compatibility/OpenGL. Frozen 40-room private LOD QA cohort is
separate from normal-source delivery and Mac validation. Native runs serial,
scratch APPDATA, copied owner layouts, before/after owner fingerprints and foreign
Godot guard. Existing pause authorization retained; do not stop foreign processes.
No public export, commit, art change, quality reduction or broad refactor.

## Current state

- Driver: `output/opengl-stalls-20261015/probe.py`; artifacts/runtime:
  `C:/bs-opengl-stalls-20261015/`. It reuses maintained isolated runner and frozen
  renderer-cohort sources, with a separate runtime copy and restored override.
- WPR CPU/GPU recording attempted with a unique instance after status confirmed
  no recorder. Non-admin token; rejected with policy `0xc5585011`. No ETL captured.
- `diagnose1`: release OpenGL, four 120-frame zoom/placement phases at 1×/4×,
  function-scope markers plus 1,056 query-only primary-thread CPU samples. No
  suspension. Primary-thread cumulative CPU/wall about 97–99% over phase windows;
  this is coarse accounting, not a ready/wait/GPU scheduling trace.
- Prior clean `pacing3` audit: all five normal zoom frames over 50 ms coincide
  with large sampled atlas uploads. Placement has no large upload; navigation
  and drawing dominate. All 56 large zoom uploads are initial cache-image events,
  not native-context fallback. Agent evidence in `agent-evidence/`.
- Navigation previously cleared/repopulated a lookup for ~14k retained nodes.
  Installed candidate preserves that prefix, erases entries for removed suffix
  nodes before graph removal, and retains immediate staged clear, disabled reset,
  graph/edge order and all existing fallback work.
- V1 Bill: `candidate-bill_npc.gd`, SHA256
  `3f5cfcbce23cb59278130dc804fa1e68d5956c35b9c20aed126167f6aaa11ccf`.
  V2 adds the original clear/repopulate fallback when the retained prefix is at
  most half the old graph. `candidate2-bill_npc.gd`, SHA256
  `43fcb3827a4751123e8ef1b20c684fb58c13c1e944541cd0ea9be464ee202086`.
  **Installed byte-for-byte in `scripts/bill_npc.gd`.** Existing UID preserved.
- Extended `tests/test_navigation_prefix.gd`; added trace/results/handoff docs and
  CURRENT_STATUS entry. Helpers remain under `output/`; no renderer/art/settings
  or playable-export changes. Both timing cohorts and raw evidence retained.

## Verification

`prefix-oracle1/2/3` pass. Final expanded V2 `prefix-oracle4`: 1,323 checks, zero
failures, 163,702 exact ordered graph records, 1,464 routes and 126,528 sorted targets.
Adds middle rotation/removal/reappend and negative-coordinate suffix cases;
retains disabled-state, locks, layout revision and staged/supersession coverage.
V2 covers exactly 0/¼/½/¾/all prefix fractions. Independent source review finds no
actionable correctness issue; reviewer did not run native jobs.
Normal-source validation: seven relevant regressions PASS in
`output/test-runs/20261015-132102-headless/`. Expanded maintained prefix test:
1,384 checks, 217,077 ordered records, 1,944 routes and 126,528 sorted targets,
zero failures. Includes Bill/Marsh, prefix fractions, middle removal/reappend,
negative suffix, disabled reset, locks, revisions, staged clear/supersession.

Final `ab2`: four serial release runs / 3,840 frames, both orders, no extra
function markers/thread sampler. All 16 state/camera/path pairs exact; guard
340 samples with no foreign Godot/duplicate game/error. Placement crew saves
3.448–4.213 ms. Normal placement frames 59.560/59.803→54.883/56.863 ms. Overall
mean 23.110→23.355 ms forward, 22.791→22.628 reverse; no general FPS gain.
Phase p95 improves 5/8 per order; zero candidate 60 FPS gates pass.

Native visual-reference1/visual-candidate2: 12 exact cross-process images and
12 exact within-process repeats, full checkpoint/camera/sidecar equal. Reference
fitted image matches prior reviewed visual-gl-j exactly. Placement plot reviewed.
All 20 completed owner guards preserve all 2,948 files. Source/test whitespace
checks pass; installed Bill matches measured candidate SHA above. Both UIDs
unchanged. No native job remains. No delivery/Mac acceptance inherited.

## Next action

This change is complete; do not rerun acceptance without a new change or concern.
Next application-side target: broad live-room/surface preparation and redraw on
structural frames. Separate atlas upload bursts need a new bounded hypothesis,
exact pixels and memory evidence; do not repeat rejected trials unchanged.
Kernel scheduling attribution still needs a capture-capable Windows session.
No claim of 60 FPS, atlas-stall resolution or actual current-source release
certification. Other sessions no longer need to remain paused for these runs.
