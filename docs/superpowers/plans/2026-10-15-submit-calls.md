# Submission and draw-call implementation plan

Goal: reduce actual render submission/draw calls while preserving exact pixels,
command/blend order and crew behavior; benchmark large-station FPS and 4× placement.
Use prior private water V2/stable-ID V3 cohort as frozen reference; no installed
runtime or gameplay changes by inference. All Godot jobs serial, scratch profile,
owner fingerprints before/after. Read-only review can proceed independently.

- [x] Freeze sources/packs/native/runtime/owner identities; attribute surviving draw calls.
- [x] Select waveform-only polygon batching; retain original surrounding primitives/order.
- [x] Correct focused oracle failure observed; native/script-fallback pixels and draw reduction pass.
- [x] Run reference→candidate→candidate→reference production timing lanes at 1×/4×.
- [x] Compare averages, p95, action/next/following-sixty pacing, exact state/camera paths.
- [x] Station/first-paint visuals, independent review, final audit/results/handoff/current status.

Evidence: `C:/bs-submit-calls-20261015/`; helpers `output/submit-calls-20261015/`.
Root-cause diagnostics are separate from acceptance timings. Preserve all valid
orders and regressions; no FPS claims from reduced API calls alone. Do not merge
across prop/actor depth boundaries or change sampling, precision or animation clocks.

Decision: keep waveform candidate private. About eight fewer steady calls (0.4%)
does not establish FPS/hitch improvement; 0/8 60 FPS gates. Deeper live-slot probe
finds no specimen effect to justify its proposed packet; not implemented. Larger
target is static prop/structural groups. See SUBMIT_CALLS_PERFORMANCE_2026-10-15.md.
