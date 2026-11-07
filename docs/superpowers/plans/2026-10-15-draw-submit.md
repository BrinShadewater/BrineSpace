# Drawing and render submission implementation plan

> **For agentic workers:** Use superpowers:executing-plans in this chat; keep all Godot and timing jobs serial. Use one final read-only review.

**Goal:** Reduce measured drawing/submission costs without appearance or crew-behavior changes, then benchmark FPS and 4× placement hitches.

**Architecture:** Freeze the preceding stable-ID V3 cohort as the reference so only the new rendering change differs. Profile existing CPU draw scopes before choosing a bounded optimization; retain original drawing as an oracle and compare exact pixels and simulation state.

**Tech stack:** Godot 4.7.2 actual Windows release, Compatibility/OpenGL, GDScript, maintained isolated Python benchmark runner; unchanged optional stable-ID native binary.

**Spec:** Current owner request; `docs/STABLE_IDLE_PERFORMANCE_2026-10-15.md` defines the cohort, prior evidence and limitations.

## Global constraints

- Preserve draw order, geometry, colors, animation clocks, crew/door/warning liveness and route behavior.
- No monolith split, renderer/quality switch, art change, gameplay change or unrelated cleanup.
- Scratch APPDATA and BRINESPACE_TEST_USER_DIR for every Godot job, owner fingerprints before/after; visible silent secondary-display QA, no overlapping timing jobs.
- Freeze reference/native/source identity. Diagnostic wrappers remain separate from final timing lanes; keep every guard-valid run.

## Review focus

- Shared room views can be reconfigured between child draws; retained data must capture all consumed state.
- Layout edits, replacement, power, flooding, doors, actor entry and zoom can invalidate caches; preserve explicit invalidation or avoid cross-frame state.
- Retained nodes alter compositing if regrouped; preserve command/child order and compare native pixels.
- CPU wall callbacks, GPU queries and upload timings overlap; do not add nested costs or claim unsupported causes.
- Faster action frames can hide worse following windows; report subsequent sixty-frame pacing and all valid orders.

## Task 1: Find and reproduce the cost

Files: `output/draw-submit-20261015/draw_work.py`, `profile.py`; evidence `C:/bs-draw-submit-20261015/`.

- [x] Freeze V3 source/pack/native and normal-source/owner baselines.
- [x] Run bounded release diagnostics and aggregate room/content/environment costs.
- [x] Select root cause/minimal change and record contract. Static harvest retention declined (~0.11 ms); select ~1.3 ms water geometry, preserving submission/topology and all dynamic inputs.

## Task 2: Implement and verify

- [x] Add focused regression/oracles; observe failure before implementation.
- [x] Implement private native packets V1 and ordered command preparation V2. Preserve geometry/order/dynamic inputs; no cross-frame native geometry.
- [x] Run correctness/native pixels, first placement and invalidation cases; inspect representative image. Coverage limited to normal finite generated paths.

## Task 3: Benchmark and handoff

- [x] Run guarded reference→candidate→candidate→reference at 1×/4×; exact state/camera paths.
- [x] Analyze FPS, p95, action, next/following sixty frames; preserve regressions/60 FPS gate.
- [x] Final source/binary/owner audit and independent read-only review; document results/handoff/current status.

## Decision

V2 remains private: modest water CPU/FPS gain, mixed action frames, normal p95
regression, 0/8 60 FPS gates. GPU draws essentially unchanged; this is not a
submission-count improvement. Normal runtime untouched. Correctness/visual/owner
guards pass in stated domain. Mac/build/package, longer pacing and native-memory
acceptance remain open. See `docs/DRAW_SUBMIT_PERFORMANCE_2026-10-15.md`.
