# Project handoff

Updated: October 15, 2026 | Project: C:/Users/Alex/Documents/Brine Space | Task: static prop / structural batching

## Objective and acceptance
Completed two structural packet trials with exact pixels/state. Roughly 40 fewer
steady calls (1.9%). Keep private: normal idle 55.25 to 53.81 FPS, 4x idle 48.97 to
49.50, 4x placement 46.23 to 46.59. Action 55.606 to 55.907 / 56.498 to 56.719 ms;
following windows mixed. Reverse normal-idle burst unresolved; 0/8 60 FPS gates.

## Accepted decisions and constraints
Reference is selected private water V2/stable-ID V3/LOD cohort; waveform trial
excluded. Ordinary/large-room inventory has no useful same-texture prop runs, so
no prop atlas/grouping implemented. Only merge existing same-order structural
geometry: north returns/corners; border prefix in room-shadow packet. Preserve
all math, UVs/colors, rectangles, doors, crew/actor boundaries and fallback flags.
Shadow cache remains 128 entries / 8 MiB, prefix adds 1,344 bytes per plan. All
runtime jobs serial/scratch-profiled. No normal source/UID/test modification,
new native build, export, Mac package, commit or upload.

## Current state
[Results](STATIC_BATCH_PERFORMANCE_2026-10-15.md). Evidence:
C:/bs-static-batch-20261015; helpers output/static-batch-20261015.
24 frozen scripts: prior 23 selected reference unchanged; painted_shell added
explicitly from unchanged current source. Candidate changes only painted_shell.gd
and room_lighting.gd overlays. Existing DLLs unchanged. Snapshots and reference23.pck
retain provenance. Immutable EXE/PCK hard links avoid another 3.48 GiB copy;
profiles/overlays/descriptors local and 20 GiB disk reserve preserved.
Changed docs: results, this handoff, CURRENT_STATUS top and static-batch plan.

## Verification
1,920 guarded release frames, eight exact phase-state/camera-path pairs. Correct
RED checks observed. North 768 + 192 special + 12 flag-off exact raster pairs;
shadow 128 exact (96 save-one, 32 existing oversampling fallbacks) plus 48 edge
cases. Total 1,148 focused pairs; 38 cache checks for fades, prefix/flag identity,
ownership, byte budget, edits/eviction/final-owner release. Seventeen station /
first-placement image pairs plus twelve repeats exact; representative image
inspected. Physical source hashes and process-lifetime counters confirm execution.
Review/audit pass. All 23 owner / ten stable / ten water guards clean; final 2,948
protected files equal initial/prior baseline. Only owner editor PID46624 remains.
Existing profile-incident caveat persists. No Mac/RSS/long-soak acceptance claim.

## Next action
Investigate reverse candidate normal-idle frames 71-80: broad CPU slowing, no
sampled uploads or structural repaint. All idle frames retain floor count 72 /
13 redraws; later floor trajectories identical across all four processes. Retained
commands still render, so downstream rendering remains possible; no cause proven.
Do not discard rows or rerun to select a gain. Before integration, resolve pacing
and separate structural changes from private navigation/water/LOD. Further prop
batching needs a deliberate texture/material or bounded atlas design with exact
sampling/depth/memory checks. Process-lifetime floor prefix counter does not reset
with shadow-cache clear; never report it as a per-scene counter.
