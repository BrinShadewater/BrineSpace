# Project handoff

Updated: October 8, 2026 · Project: BrineSpace · Task: renderer frame capture and draw-profiler attribution

## Objective and acceptance
Continue the full PC/Mac performance and readiness plan. Identify substantial renderer costs before optimizing. Native isolated diagnostics and captured replay do not certify a deliverable, target hardware, loading, endurance or Mac gameplay. No quality reduction, renderer upgrade or public upload.

## Current state
No normal runtime changes this milestone. Private draw-profiler on/off pair completed; a real OpenGL release frame was captured and inspected. Evidence lives in `output/all-crew-storage-2026-10-07/draw-profiler-overhead-2026-10-08/` and `output/renderdoc-tools-2026-10-08/`.

RenderDoc portable Windows64 v1.46 downloaded from the official builds-page link, `https://renderdoc.org/stable/1.46/RenderDoc_1.46_64.zip`. Archive SHA256 `9ca4d09ecaba2cc791168660d6fc2a7e3d70fe67146e87ec05c5f8dea70772f7`; renderdoccmd Authenticode valid, signer Baldur Scott Karlsson. Portable extraction only; no Vulkan-layer registration or global installation. Initial hidden qrenderdoc help/probe launches paused at first-run analytics and were stopped by their exact owned PIDs. Qt resolves its UI profile through Windows rather than our APPDATA override; the newly created tool UI.config was temporarily opted out for unattended scripts, then restored byte-for-byte. Godot's scratch APPDATA isolation and actual-userdir guard remained active.

## Verification
Draw-profiler pair: same actual debug=false 40-room/four-crew fixture, 256MiB drone budget, nine 180-frame idle/pan/zoom phases at 1/2/4x, viewport GPU timing off both lanes. All gameplay and prop counters equal; focus retained/cap0/VSync0. Turning the detailed draw profiler off lowered phase means by 0.167–0.878ms; ordinary gameplay already leaves it off. Off means31.36–41.19ms, p9534.19–56.78ms, max86.537ms. Both peak2348.739303MiB and three43-room restored states2006.029565MiB flat, exits234.533917MiB flat; no missing art. No meaningful FPS remedy or normal setting change established by this single pair.

Frame capture: isolated actual release EXE with identified existing combined four-crew/current Main/Grid/weak-badge overlays. Capture controller115920 game and117412 qrenderdoc completed/stopped; runner58842 terminal. File `station_frame253.rdc`, 678,992,621bytes, SHA256 `8da0aa3a339cf842cb37e9ee2a7f577110b2b60dfe49ac97dbe3a5b9a004a061`. Actual debug=false/OpenGL3.3/NVIDIA RTX4070Ti. Startup emits one cached-shader recompilation warning under injection; this run is not warning-free release acceptance. Thumbnail inspected: 40-room station at zoomed-out fixture view, normal UI, visible discovery reveal popup. Therefore it is an active early frame, not settled idle gameplay.

Replay opens successfully; exact captured draw count5096 (5098 actions). Intrusive per-action GPU queries sum to95.815ms and are NOT normal-frame GPU time or trustworthy additive workload attribution. Keep `replay-timing-intrusive.json` scoped accordingly. Full per-draw state seeking was deliberately stopped at2500 inspected draws because repeated replay was costly; its incomplete state was not accepted as a completed classification. Runner was subsequently hardened to reject nonzero controller exits.

Bounded classification completed: every32nd draw plus prior30 intrusive-duration-ranked draws,188 inspected total. Sample counts105 ordinary USE_ATTRIBUTES/DISABLE_LIGHTING canvas draws,71 ordinary DISABLE_LIGHTING canvas draws,6 USE_PRIMITIVE,6 custom unshaded draws. These counts describe a biased sample, not all5096.90 sampled draws bind the4×4 fallback texture;153 have one instance. Shader source and texture metadata retained in `replay-analysis.json` and concise `summary.json`. This supports tracing ordinary geometry and batching; it does not prove their total cost or that effects are free. Capture/replay adds overhead and no results count toward FPS acceptance.

Game adapter restored exactly. Owner fingerprint2936files before/after, zero changes. Tool UI config restored exactly. Replay controllers118760,115960,116752 and runner60479 terminal. Retained full release/PCK unmodified. About1.56GB disk free after capture; retain unique capture/art/archive inputs. No new fully audited Windows/Mac deliverable.

## Next action
Trace the large number of ordinary canvas/plain-geometry draws to room/layer commands. Prefer a cheap structured-command census or bounded sampled state inspection over thousands of independent replay seeks. Capture a settled frame after discovery reveals expire if needed, and explicitly label zoom/action/frame state. Test an identified batching/static-layer remedy with matched uncaptured workload plus exact visual checks; do not infer FPS savings from capture timings or reduce default quality. Full original nine bugs, target-PC/M1 checks, loading, two-hour soak, integration/export/audit/signing and delivery gates remain open.

Primary tool references: official `https://renderdoc.org/builds`; repository `https://github.com/baldurk/renderdoc`, qrenderdoc/Code/qrenderdoc.cpp for --python and first-run setup, docs/python_api/examples/exe_launching.py. Runtime v1.46 API docstrings retained in api-probe.json. Earlier attempted remote_capture.rst/main.cpp paths returned404 and were not treated as documentation.
