# Project handoff

Latest acceptance: context comparison completes all eight runs/12,960 samples.
All36 paired states match; zero errors and owner2,938 unchanged. Large means
29.2221->29.2402ms forward and29.2490->29.0337ms reverse remain mixed; worst
candidate frames125.197/126.156ms and all nine large phase gates still fail.
Preparation savings are demonstrated, sustained FPS acceptance is not. No normal
source admission. Earlier running entries below are historical progress evidence.

Updated: October 9, 2026 · Project: BrineSpace · Task: private local wall invalidation

## Objective and acceptance
Reduce construction/demolition redraw bursts while preserving selected rendering and simulation. Matched packaged workloads, relevant visual/behavior checks and full release gates govern acceptance.

## Accepted decisions and constraints
Private overlay only; normal source and delivery packages unchanged. Preserve shell/crown draw order, global display/layout/selection settings, neighboring structure/power and own door/ward state. All tests use verified scratch profiles; owner layouts copied read-only. Do not admit from synthetic checks or frozen screenshots alone.

## Current state
D:/bs-release-crew-cache-20261009/wall-key-trial/: key.gd projects wall dependencies to a3x3 neighborhood plus own port/ward entry and global flags; grid.gd changes only the frozen Grid slot-key assignment. overlay.pck mounts those exact two paths. identity.json and overlay-identity.json retain hashes. No helper UID/source installation yet.

## Verification
Synthetic22 checks: baseline fails exactly3 distant-state over-invalidation checks; local projection passes22, including neighboring state, doors/wards, power, global flags, corridor shade and snapshot immutability. Owner2,938 unchanged.

Initial actual debug=false surface parity fails a cull rebuild assertion and all15 direct-reference image pairs. Diagnostic probe proves live visible rooms12->2 but static rooms12->12, surface state equal and no floor rebuild needed. Original unchanged release baseline-q0 independently reproduces disappearing-station direct reference (max channel difference233); images reviewed. Thus the legacy direct fallback is an invalid reference for this current layered renderer, not proof against the candidate. Failed artifacts retained.

Corrected release-parity-forced compares current cached walls against freshly forced wall-slot repaint, preserves normal renderer, and freezes fixture time/input for identical snapshots. Rebuild assertion follows actual structural state changes. All15 RGBA pairs identical across4 rotations, close view, live rotation, power on/off, light fade, raised walls, placement/removal, culling, pan and zoom; no engine errors, constructor-source identity verified, owner2,938 unchanged. q0 image reviewed. This is static snapshot acceptance only. Shader TIME/time_scale behavior checked against official Godot documentation: https://docs.godotengine.org/en/4.5/tutorials/shaders/shader_reference/canvas_item_shader.html

GPU replay counter discovery also completes:14 counters supported; GPU Duration available, all3,812 draw actions align with structured commands and return timings. Temporary RenderDoc preferences restored; owner unchanged. render-capture-02/gpu-durations.json contains per-event/program/texture groups. Instrumented replay timings differ substantially from live viewport timings and must not be treated as game frame duration or proof of a causal bottleneck. Texture0 may not describe every custom shader input. No shader optimization admitted.

## Next action
Matched full wall comparison session15478 running in wall-key-trial/workloads: actual debug=false12/40 rooms,24 phases/all speeds,both orders, source identity guard and wall-slot counters. Poll existing handle; compare states, frame distributions, >50/>100ms stalls and rebuild deltas. Expand relevant dynamic/large-room boundary checks before any source admission. Resolve diagnostic fallback/reference issue separately; no current-source fix for it yet. Full release hardware, bugs, endurance and Mac certification remain open.

First matched12-room forward pair completes:24 phase-end states match; mean14.27498->14.26027ms (effectively unchanged).1x placement slot delta26->10, demolition24->8;2x/4x placement52->20, demolition24->8. Worst construction/demolition frames improve slightly in all six sampled phases, but no final FPS or stall acceptance. Evidence workloads/first-pair-inspection.json. Reverse12-room runs also complete; large workload comparison remains live in session15478.

Final matched wall session15478 exits0: eight runs/34,560 frames,96 paired states match, zero engine/safe-image failures, owner2,938 unchanged. Large forward mean28.8065->28.7642ms, reverse27.4862->27.6479ms; average performance mixed. Worst large frames160.751->143.055 and144.304->135.001ms. Large placement wall deltas82->6 (164->12 at faster speeds), demolition80->4; over90% fewer slot rebuilds, but all24 large phase gates still fail in both orders. analysis.json retains complete phase comparisons. No source admission yet; profile key-preparation overhead and remaining floor/exterior costs before accepting the tradeoff.

Preparation attribution: original lighting wall preparation~0.414/0.416/0.384ms per sampled frame; local-key v1~0.818/0.819/0.815ms. Repeated deep copies add measurable overhead. Context prototype key-context.gd/grid-context.gd copies neighborhoods once per pass, not globally/session-cached. Synthetic81 exact-key/copy-isolation checks pass;70 snapshots replace720 requests. Three paired CPU prep samples original1.845/1.873/1.873ms vs context0.706/0.723/0.680ms per pass. Not gameplay FPS evidence. Context overlay prepared; actual15-pair release parity session36142 running in release-parity-context. Normal source unchanged.

Context parity session36142 exits0:15 exact actual debug=false cached-vs-forced-wall image pairs, no errors, constructor verified, owner2,938 unchanged. Direct context-vs-v1 matched comparison session10531 now running in workloads-context:12/40 rooms, lighting/placement/demolition at all speeds, both orders,180 samples per phase (nine affected phases per run). Both lanes mount their own exact overlays; constructor guards distinguish context and v1. Full earlier24-phase release gates remain open. No source admission yet.

Context comparison preliminary: both12-room orders complete (18 states match), means16.0744->16.2804ms forward and15.6692->15.5341ms reverse, mixed. Lighting preparation consistently~0.45-0.47->0.24-0.27ms. First large forward pair also matches9 states; prep~0.77-0.80->0.36-0.39ms, means29.2221->29.2402ms effectively unchanged. Faster key preparation is demonstrated, sustained FPS remedy is not. Reverse large comparison still live in session10531. Evidence workloads-context/preliminary-prep.json. Next measured draw work remains full floor passes after local structural changes; current floor order is connectors, legacy rooms, layered floors split in original order. Any per-room floor experiment must preserve that layering and immediate interactive-room completeness, with next-frame/motion/lighting/neighbor checks. No floor prototype installed.
