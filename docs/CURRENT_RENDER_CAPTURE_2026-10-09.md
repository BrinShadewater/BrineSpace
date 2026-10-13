# Project handoff

Updated: October 9, 2026 · Project: BrineSpace · Task: current packaged render capture

## Objective and acceptance

Locate current 40-room rendering submission/geometry costs before choosing a
quality-preserving optimization. Capture/replay timings do not certify gameplay.

## Accepted decisions and constraints

Actual debug=false cab0dd6874401f88 package, physical isolated QA copy; original
delivery untouched. Normal node-processing simulation driver retained; no old
process_frame signal stepping. Detailed draw/viewport timing disabled in capture.
Known idle editor left untouched. Original release gates remain open.

## Current state

Capture session98748 exits0, replay22025 exits0. Evidence at
D:/bs-release-crew-cache-20261009/render-capture-02/:
completed.json, capture-config.json, batching-analysis.json, current-frame.png,
fragment-*.glsl and station_frame321.rdc. Capture638,759,373 bytes,
SHA2563787256572e4957a5b6dd65083b14f2fc0537d7adfa850f16236e82ef1dcfdb9.
Driver helpers capture-current-cache-rendering.py/replay-current-cache-rendering.py.

## Verification

Native completion confirms debug=false/40 rooms. Owner2,938 unchanged; temporary
tool preferences restored. Shader-cache recompilation warning retained; no engine
error appears in native log. Captured image reviewed: station/cards/compact four
needs bars/inspector/environment present. A synergy notification is visible;
this is a single-frame capture, not unobstructed room or animation acceptance.

Full structured commands:3,812 draws,6,664 texture binds,8,106 VAO binds and3,812
program-use calls.3,258 draws have one instance (~85.5%). Plain canvas programs
1004/33270 account990/2,571 draws; dominant fragment variant has USE_ATTRIBUTES
and DISABLE_LIGHTING. Counts establish submission complexity, not GPU durations
or a proven causal bottleneck. All draw commands counted; shader inspection is
every128th draw plus first per program (command/draw counts match).
Dominant attribute program uses white texture1355 times and texture34749
209 times; texture/layer identification is the next investigation.

First attempt53252 stopped after controller remained before script launch;
tool settings had analytics prompt allowed and Python debugger enabled. Local
qrenderdoc.cpp puts Analytics::Prompt before Python script execution. Retry
temporarily disables analytics/debug/update prompts and succeeds. First-attempt
owner/config checks pass. Artifact move initially failed on an open handle and
left both render-capture and render-capture-attempt-01; retain both, no deletes.
Immediate mkdir retry failed safely; later attempt uses a distinct -02 directory.

## Next action

Identify dominant texture/primitive groups and their screen/layer locations,
cross-check source draw paths, then trial compatible geometry batching or targeted
invalidation with matched frame/state and native pixel checks. Do not infer the
most expensive shader from draw counts alone, change default effects, or begin a
broad renderer/monolith refactor. Full standard benchmarks/native Mac/bug closure/
endurance/signing certification remain open.
