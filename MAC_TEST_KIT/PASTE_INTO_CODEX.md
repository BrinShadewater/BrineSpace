Continue BrineSpace from this Mac test kit. Read this folder's AGENTS.md,
Context/PROJECT_AND_GOALS.md, Context/BUILD_AND_SOURCE.md,
Context/OPTIMIZATION_MAP.md, Context/WINDOWS_EVIDENCE.md and
Context/NATIVE_MAC_TEST_PLAN.md before acting. Use Context/REFERENCES.md only as
needed. These files carry the project context and latest accepted Windows results.

The build to validate is brinespace-d3cfa1890bafefe7, exported with Godot 4.7.2,
with the immutable crew-frame Save fingerprint improvement and e54 router cleanup.
Verify the packaged identity/checksums first. Then validate launch/Gatekeeper,
ordinary New Game and Save/Quit/relaunch/Resume, visuals/crew/doors/lights/cards,
audio/input/Retina/display/focus, and average FPS plus zoom/placement/Save pacing
on this Mac. Use a disposable QA account or verified engine-level isolation;
never test against my real save folder. Keep the original app unchanged, results
outside it, and all timing runs serial/visible. Do not change graphics or crew
behavior to improve the numbers, or claim Windows/headless/static results as Mac acceptance.

If the optional source ZIP is present, it is the exact editable runtime selection,
not simply Git HEAD. Read its source provenance before importing it. Use it for
targeted source tests or a separately built fix if needed; preserve the frozen
export and report any version difference. The included benchmark is the corrected
40-room Windows fixture; port only the documented platform harness assumptions
before claiming an equivalent Mac run. Do not run it blindly on a single display.

Record hardware/OS/render backend, commands, isolation proof, exact fixture and
build identity, raw timings/outliers, screenshots/F8 reports and Save round-trip
outcomes using Context/TEST_RESULTS_TEMPLATE.md. Prioritize concrete Mac release
blockers, not speculative engine rewrites. Report findings and next steps clearly;
keep unknowns pending and save a local HANDOFF.md so Windows Codex can resume.
