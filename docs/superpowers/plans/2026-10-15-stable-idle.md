# Stable-ID idle investigation implementation plan

> **For agentic workers:** Use superpowers:executing-plans to carry out the evidence and verification steps in this chat. Do not dispatch timing work in parallel.

**Goal:** Explain the observed 4× idle slowdown, preserve visuals and crew behavior, and benchmark average FPS and 4× placement hitches again.

**Architecture:** Reuse the immutable V3 stable-ID prototype and dense reference in a new isolated evidence directory. Attribute the existing trace before changing code; reproduce with controlled timing. Change only a proven cause, if one is established.

**Tech stack:** Godot 4.7.2 actual Windows release, Compatibility/OpenGL, Python analysis, existing optional GDExtension.

**Spec:** Owner request in this chat; `docs/STABLE_NAV_PERFORMANCE_2026-10-15.md` and its handoff define the accepted prototype and limitations.

## Global constraints

- Preserve original route choices, restrictions, clocks, rebuild scheduling and appearance.
- Keep prototype and normal runtime separate; no export, Mac package or integration is authorized by this investigation alone.
- Every Godot job uses scratch APPDATA and BRINESPACE_TEST_USER_DIR, with real-profile fingerprints before/after. Keep jobs serial and QA visible on the secondary display.
- Preserve immutable reference/V3 source and DLL hashes, independent actor graphs, canonical physical order and fallback modes.

## Review focus

- Whole-frame costs can overlap: treat CPU wall intervals, nested callbacks and GPU counters separately.
- Short samples can differ through render/atlas bursts: compare per-frame events and order effects, then replicate once for the unresolved idle concern.
- Sparse IDs use the dictionary reachability fallback: measure whether it is invoked before attributing slowdown to it.
- Simulation/camera differences invalidate comparisons: require exact state and camera/path pairs.
- Instrumentation changes timings: use diagnostic profiles for attribution and uninstrumented immutable packs for final FPS/hitch claims.

## Task 1: Attribute and reproduce

Files: `output/stable-idle-20261015/idle_work.py`, `prior_analysis.py`; evidence in `C:/bs-stable-idle-20261015/`.

- [x] Freeze prior reference and V3 sources/packs/native identity; record installed-source and owner-profile baselines.
- [x] Analyze existing idle traces by simulation, render boundaries, uploads, draw callbacks and frame index; preserve raw excerpts and aggregate results.
- [x] Run the same guarded four-process idle/placement comparison, checking eight exact state/camera/path pairs. Instrument only if attribution remains unresolved.

## Task 2: Test the cause

- [x] State a specific hypothesis supported by trace evidence. If the slowdown does not reproduce, retain that finding instead of inventing a navigation fix.
- [x] If a code defect is found, pin it with a focused failing regression/oracle, implement the smallest private change, and rerun the affected graph/route/fallback checks. Keep changed binaries/packs separately versioned.

Ruling: no runtime fix — no consistent idle penalty reproduced in two new series,
and the suspected dictionary detour branch has zero measured calls. Separate
diagnostic observers localize work without entering final FPS results. A second
identical benchmark was justified by unresolved variation, and every valid sample
is retained. Underlying OS/driver variance remains unknown; no hardware cause is
asserted. No red/green gameplay cycle is needed because no gameplay patch was made.
Independent final review found no blocker. Report distinguishes existing benchmark
observers from new diagnostic wrappers, phase-end state from per-frame camera
equality, and the observed 1× detour cost from its absence in sampled 4× idle.

## Task 3: Acceptance and handoff

Files: `docs/STABLE_IDLE_PERFORMANCE_2026-10-15.md`, `docs/STABLE_IDLE_HANDOFF_2026-10-15.md`, `docs/CURRENT_STATUS.md`.

- [x] Record FPS, 4× action frames and subsequent sixty-frame windows in both orders, including any regression and the 60 FPS gate.
- [x] Reuse proven visual/route evidence for byte-identical source; rerun affected oracles and image pairs if any runtime code changes. Do not count headless checks as visual acceptance.
- [x] Audit all owner, source and binary guards; preserve the prior profile-incident caveat. Update the concise handoff and current milestone.
