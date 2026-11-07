# Project handoff

Updated: October 15, 2026 · Project: `C:/Users/Alex/Documents/Brine Space` · Task: stable-ID 4× idle investigation

## Objective and acceptance

Investigate the previous idle FPS regression without visual or crew-behavior
changes; benchmark average FPS and 4× placement hitches again. Investigation and
comparison complete. No reproducible navigation idle defect established; V3 stays
unchanged and private.

## Accepted decisions and constraints

Keep actual independent AStar2D graphs, stable cell blocks, ordered physical-route
oracles, actor restrictions and existing rebuild schedule. Do not optimize an
unused branch or claim an idle fix without evidence. No runtime integration,
export or platform package. Retain every guard-valid run, including the slower
following window. Normal game and owner saves remain unchanged this task.

## Current state

Evidence/frozen lanes: `C:/bs-stable-idle-20261015/`. Helpers:
`output/stable-idle-20261015/`; only diagnostic Bill overlays add timers/counters.
Production reference and V3 scripts/PCK/native are byte-identical to the prior
study. No new native binary or gameplay patch.

Added [results](STABLE_IDLE_PERFORMANCE_2026-10-15.md), this handoff and
`docs/superpowers/plans/2026-10-15-stable-idle.md`; updated `CURRENT_STATUS.md`.
Keep current chat/context. No commit or upload made.

## Verification

- 3,840 new production-lane frames / sixteen exact phase-end-state/camera-path pairs; all eight runs also match the preceding study's corresponding phase-end states/camera paths. Existing benchmark observers remain, with no new navigation wrappers. Per-frame actor state is not compared.
- Separate 1,920 diagnostic frames / eight exact pairs: every 4× idle phase has zero rebuilds or detours, two route calls totaling 90–124 µs, 240 topology checks (~0.304–0.326 ms/frame).
- Earlier 4× idle 46.52→44.63 FPS; new repeats 44.62→46.48 and 45.52→46.34. All three pooled 45.54→45.80. No consistent idle penalty or proof of a new gain.
- New pooled normal idle 52.86→52.72 FPS; 4× idle 45.07→46.41; 4× placement phase 43.21→42.81, p95 36.617→41.210 ms. 0/16 60 FPS gates.
- Four action frames all improve: 68.934/69.774/70.180/66.776→58.330/65.730/57.930/60.145 ms, mean 68.916→60.534. Three following-window means improve, but one is worse and no following-window p95 improves. Keep that limitation explicit.
- Drawing and render intervals dominate changing idle costs. Same callback count and diagnosed upload-byte total; OS/driver/power/scheduling cause remains unproven.
- At 1× idle, two detour-reach calls cost 11.150/11.198 ms dense versus 15.043/15.983 ms stable per phase. This real ~3.9–4.8 ms phase cost is separate from the sampled 4× idle finding; dictionary timers nest inside reach.
- Prior route/native/pixel checks reused for identical bytes, not freshly rerun; new timing image visually inspected. Normal source/UID/test hashes unchanged.
- All fifteen owner and twelve binary guards / three process guards pass. Final 2,948-file owner fingerprint equals initial/prior protected baseline. Only idle editor PID 46624 remains; earlier profile-incident caveat persists.
- Independent read-only review found no blocker; report clarifies observer scope, phase-end state equality and the separate 1× detour cost.

Audit and analysis JSONs are linked by the report. No long-session memory or Mac
packaging acceptance. No new code fix means no new red/green runtime test cycle.

## Next action

Investigate live drawing/render submission and recurring texture-upload bursts,
with reproducibility controls; the sparse detour fallback does not execute in
this idle fixture. Keep stable IDs for further placement work, but require broader
pacing and bounded-memory/platform acceptance before adoption. Preserve the
unknown cause of process-wide timing variance rather than naming an unmeasured
hardware cause.
