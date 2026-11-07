# Project handoff

Updated: October 7, 2026 · Project: BrineSpace · Task: private crew provider packaged startup

## Objective and acceptance
Test actual debug=false packaged startup/memory/lifetime for the exact compressed
crew/worker/content-sharing candidate. Original full release scope remains open.

## Accepted decisions and constraints
Private candidate only; no normal provider admission or itch upload. Physically
frozen current selected art/runtime, default quality preserved. Test profiles
isolated and verified before BugReport writes; deliverable gets no overrides.

## Current state
Private package `output/crew-release-2026-10-07/release/BrineSpace.exe`.
Build brinespace-dbe44a995a5708be;
sourceSHA dbe44a995a5708be2ec8b8348d81834dc6725b76ce984c5ac11299241ffe6c23;
EXE109,283,328bytes/SHA7208c3a81fbb5e0af24ab319bd377bf2e72e9b5fdcc01d709bafe1550e067b76;
PCK3,623,023,191bytes/SHAe05e7c0c2d009f83ea1ad93c951eb660bfa19c723f74d01cef06120330b748c8.
Frozen root remains bs-crew-release-wj7kebwm. Current normal runtime/art untouched.
QA physical EXE/PCK copy under qa/, isolated startup results under startup/.

First export rejected: frozen provider insertion placed constants before class_name
GridCanvas; direct --check-only identifies Unexpected class_name at line6.
Corrected only declaration order in frozen Grid and freeze generator; direct compile
passes. Failed package/logs retained under failed-export-1 and failed-1-* logs.
Corrected source-location hashes updated. Successful export process terminal.

## Verification
Frozen release-manifest and assertion-safety checks pass. Maintained corrected
export clean. Outside-checkout PCK audit36,253 files,55remaps,zero missing/changed/
unexpected. Owner2,936 files unchanged through export,audit,three startup runs.
All processes terminal. QA identities/fixture hashes retained; no PCK mutation.

Three actual debug=false native1920x1080 initial-new-game runs, first isolated
profile then two learned-order launches. No synthetic40-room construction, title/
dialogue entry acceptance or active crew motion coverage in this fixture.
Request-to-ready including scene load:9,604.643/5,308.734/4,685.325ms.
Post-instantiation readiness8,302.658/3,964.794/3,385.497ms.
Scene load1,149.083/1,152.487/1,152.202ms. Reported ready textures1,082.994MiB;
after game exit80.055MiB in all three. Router released, no missing artwork,
errors/warnings/leaked-instance reports. All5,834 surviving compressed sources
prepared by5,834 jobs/peak8; learned12,645prefetch hits/0unused.
Presentation uploads0 at ready: crew still unreleased/inactive; this does NOT
certify live large-station memory/performance. Initial timing OS caches uncontrolled.

Critical timing scope: engine uptime at ready10,923.735/6,567.669/19,206.736ms.
Third run spends about14.521s before timed scene request, versus~1.26–1.32s in
the others. Do not hide this delay by reporting request-to-ready alone or certify
loading gates. Need instrument earliest autoload/native startup and repeat to
attribute bootstrap vs fixture/render waiting/OS scheduling. Progress draw gaps
not captured here; responsive-loading acceptance remains open.

Preset script_export_mode=0 in current Windows preset, confirmed text mode against
[Godot4.7.2 enum](https://raw.githubusercontent.com/godotengine/godot/4.7.2-stable/editor/export/editor_export_preset.h).
Do not call this compiled-script packaging or assume diagnostic parse costs vanish.
Binary-token export may be a later measured trial, not an accepted setting change.

Additional verified inactive duplicate cleanup: original qa/BrineSpace.pck removed
3,647,293,175bytes,exact retained release/BrineSpace.pck SHA
c9212f827665b7f230d4c939486f26e9c598832dbddaab6f593334a72e248e29.
QA logs/metadata/retained deliverable kept; pack-removal-for-crew-trial.json record.
Old qa and qa-cold-hints need restoring retained packs before reuse. Current new QA
complete; disk~2.55GB free after packaging/copy at observation, avoid unverified cleanup.

## Next action
Attribute pre-scene bootstrap delay with early autoload/parent timestamps before
claiming loading acceptance. Then actual release large-station active crew/drones/
production and motion/Studio/save/title/Continue lifetime; inspect captured art.
Preserve original FPS/memory/endurance/Mac gates; current provider still private.
