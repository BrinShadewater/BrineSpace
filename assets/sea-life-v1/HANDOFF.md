# Project handoff

Updated: September 29, 2026 · Project: BrineSpace · Task: sea life batch 1 integration

## Objective and acceptance
Create the five sea-life species and install them before later lighting/card/effect
batches. Owner approved continuation from first-pass direction; final in-game motion
review remains a separate acceptance checkpoint.

## Accepted decisions and constraints
Current bible governs painted finish. Preserve placement, epochs, fade, culling,
quality counts, pause and whale periods; procedural art remains fallback. Both
additional concepts continue in existing drifter slots, without extra encounters.
Source provenance uses built-in imagegen; no additional generation this turn.

## Current state
12 runtime PNGs, seven retained sources, exact prompts, hashes, pivots and 26-light
registration. Small-creature loops use a single pose with periodic deformation and
attached glints. Tidewalker fin/sail roots match the painted silhouette. Runtime:
scripts/ocean_life.gd plus its new UID. Three new Godot fixtures and paired UIDs,
isolated Python runner, atlas HTML, 34 gameplay captures, nine assembly captures,
native summary and four GIF reviews. Release graph selects only 12 runtime PNGs.
No playable executable/PCK export. Shared generated manifests remain working changes.

## Verification
131 Python packaging checks; 79 Godot asset checks; effects quality and reliability
pass; native ocean-life gate passes. First native game review and camera correction
pass with 34 captures. Owner profile unchanged in these earlier isolated runs
(output/sea-life-20260929-175035, -175204, -175425).
Follow-up full-game overview run timed out at startup (-175709). Real profile changed
during this interval with a separate game session/F8 report. Lightweight native
assembly fixture passes, including exact paused-frame pixel equality (-180330);
that interval's live-profile difference was last_session.json only. All probes used
fresh scratch APPDATA/LOCALAPPDATA; late unchanged-profile acceptance is inconclusive.
No real data was restored or edited by this task. Complete native assembly, primary
gameplay views and sampled motion frames inspected. GL errors were absent from the
successful logs. Tidewalker has about 4.05 world units per active art pixel, documented
as the distant large-species density exception rather than artificial upscaling.

## Next action
Review integrated motion, then continue batch 2 lighting per Claude's staged handoff.
Keep Low/Reduced Motion gates and procedural fallbacks. Recheck native startup when
the test environment is stable; concurrent-session interference is a hypothesis.
Commit deferred at closeout because another process held .git/index.lock; lock untouched.
Commit only this pack, ocean-life script/UID, new fixtures/UIDs and runner; shared
status/generated files contain other sessions' changes and must not be committed whole.
