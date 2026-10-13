# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: confirm zoom scheduling candidate and attribute remaining idle stall

## Objective and acceptance

Continue full PC/Mac performance/readiness work. Preserve selected art, animation, simulation, layouts, saves and default settings. No publication. Previous turn made progress through drawing/key attribution and a private scheduling candidate; this turn extends its actual visual and three-pair performance evidence.

## Accepted decisions and constraints

Keep the scheduling candidate private: tail-frame improvements are useful but aggregate performance remains mixed and all FPS gates fail. No normal runtime/art edits or new full export. Existing real-change scheduling and preparation-camera rules remain required. Do not infer GPU completion from API timings or sum nested profiling labels.

## Current state

Recovered109.886MiB by removing52 duplicate JSON/PNG scratch results from explicitly named completed profiles. PNG bytes match retained primary files; JSON parsed values match despite whitespace differences. Both original and retained SHA256 values, resolved short scratch paths and equivalence proof are in `output/renderdoc-tools-2026-10-08/duplicate-report-reclamation.json`. Primary evidence, logs, layouts, source, packs, archives and RenderDoc capture retained. First dry inventory used evidence-directory paths; corrected to the maintained profile-location mapping before deletion. No live QA/game processes during cleanup. Available space remains tight (~64MiB after new tests).

Private actual-release visual fixture: paused40room/fourcrew, real zoom-out, zoom-in plus door locking, and zoom plus lighting change. Waits for observable notification completion, starts above minimum zoom and requires actual scale movement. In both control/candidate, all3 settled images equal forced retained-layer/content redraw byte-for-byte; corresponding control/candidate SHA256s also match. Candidate45 sibling deferrals; control0. Control settles8/7/8frames and candidate9/9/9; all forced rebuilds3frames. This proves these settled cases, not active motion or all release visuals.

Failed fixture evidence retained: initial hashing API compile error corrected; subsequent first case was minimum-zoom-clamped and88/82pixels differed solely in21×22/21×21 discovery-notification Plus glyph. Native image inspection and source show the normal Plus scale tween. Stronger unobstructed/movement-required fixture passes. No game animation or Reduced Motion changes made to get a pass.

## Verification

Three matched actual `debug=false`40room/fourcrew nine-phase runs per lane; second pair order reversed. Same immutable candidate PCK hash. All27 phase comparisons have equal crew/drone/door/light/power-count/zoom states and prop counters. Candidate deferrals285/281/281 versus0 controls. All six peaks2348.739303MiB, exits228.259212MiB, uploads4297. Native scheduler12checks/0failures from prior turn remains scoped evidence.

Median of per-run statistics (not pooled percentiles): means improve7/9, p95 improves5/9. Zoom p95:1x53.903→52.199ms;2x51.948→53.575;4x60.287→59.656. Zoom p99:1x69.604→61.809;2x76.367→63.665;4x80.140→71.917ms. Means improve modestly1x/2x;4x42.046→42.395 worsens. This is a tail-frame scheduling benefit with mixed costs, not accepted general FPS gain or target-hardware certification. Drawing count is essentially unchanged.

Repeated control idle4x/frame146 stall106.275ms, compared with earlier specimen-control108.549ms at the same deterministic point. Latest control step4.872ms, before-render88.804ms, render signals12.325ms; matched candidate66.142ms, step3.689ms, before-render50.174ms. Repeated>100ms is an explicit release blocker in this fixture. Do not attribute its apparent improvement to the zoom patch merely from that pair.

Re-examining completed detailed probes identifies a stronger next lead at idle4x146: `env_pass_exterior_actors`38.316ms in drawing probe and34.617ms in key-cause probe, while total grid callbacks51.010/47.085ms. Typical exterior-actor stage is sub-millisecond. The stage contains harvest-site art, exterior drone/construction/dust rendering, optional admin lines and survey-probe art. These nested timings narrow the location, not the specific callee or cause. Earlier zero drone texture-upload events do not cover all preparation/decoding/other art calls.

All runners/engines terminal. Every new native/release owner fingerprint2936files unchanged, physical adapter restored byte-identically. Logs clean in accepted runs, focused workload samples, router released. Private sources/generators, identities, output and comparison: `output/renderdoc-tools-2026-10-08/{settle-budget-visual-trial,settle-budget-visual-corrected,settle-budget-visual-unobstructed,settle-budget-release-confirmation}`. Failed logs preserved in first two visual directories; accepted visual witness final screenshot retained. No ordinary executable export or normal runtime admission.

## Next action

Split exterior-actor profiling into harvest, construction, individual drone anchor/dust/sample/draw and survey stages, using bounded current-frame counters and explicit runtime caller/path proof. Reproduce idle4x146 and other spikes before choosing a decode/cache/draw remedy. Also keep total baseline canvas submission/preparation reduction active: the scheduling patch alone is insufficient. All original nine bug reports, full integration/loading/lifetime/endurance/target PC/M1/signing/notarization/delivery gates remain open.
