# Paid expedition resume observation

Updated September 22, 2026. Broad objective remains active.

## Objective and constraints
Observe live autonomous movement and work across a disk checkpoint after recent
repairs. Paid construction, normal resource failures, isolated profile. Blueprint
selection and setup are controlled; no owner-room or gameplay-rule changes.

## Current state and verification
Evidence: output/expedition-resume-2026-09-22/.
Native 120-second observation after paid setup passed, exit 0, no logged errors.
Bill chose his own goals; normal process/cycle timers ran. Dialogue was minimized
through its normal method; the camera followed Bill. The station survived cycles
4 through 9 with free_build=false and failures_disabled=false.

At the midpoint, a real disk save/restore preserved position, state, resources
and cycle exactly and landed paused as designed. The normal pause toggle resumed
play. After 65 seconds, samples cover cycles 7, 8 and 9 and 351 distinct positions,
so completion is not inferred merely from progress before the restore.
This checkpoint happened during idle, not during a work or locker action.

1113 samples /1110 crops: all four walk directions, hunger/curiosity/maintenance
goals and a naturally selected south kneel (9), repair (20), stand (9) sequence.
One paused sample; three offscreen crops omitted with capture indices absent.
The work contact sheet and 54-frame excerpt use actual capture IDs and sampled
time differences. Native approach/work/rise/departure reviewed; no missing limb
or obvious endpoint jump established. Power/lighting changes during departure
remain visible in the clip. This is not owner smoothness approval, a human
expedition, FPS evidence or broad save-state coverage.

## Packaging correction
The current dependency scan unexpectedly selected Branforth's new raw generation
and authoring registration through a dynamic revision-directory reference.
tools/build_release_manifest.py now excludes only that specific study directory
from broad discovery, retaining explicit/formatted file references and other
source directories. New focused regression plus seven existing tests pass.
Before/after real collection removes exactly two files /1734776 bytes, adds none,
and retains all 48 installed Bill/Branforth locker frames. No source is deleted.
No export was performed; exact PCK and actual-release verification remain future
release gates. Updated docs/RELEASE_WORKFLOW.md records this narrow exclusion.

## Next action
Continue ordinary station/room interaction review and owner motion feedback.
Review the observed work point's intended service context before deciding whether
any facing/contact adjustment is warranted. Refresh packages at a release milestone;
native Apple Silicon testing remains independent and pending.
