# Continue camera focus repair

Updated September22,2026. Broad goal remains unfinished.

## Finding and installed change
The staged loader hides the game while restoring it. Hidden layout reports a
roughly2x2viewport when _finish_restore centers BRINE; scroll then remains near
the core's absolute position instead of subtracting half the visible viewport.
Continue is intentionally centered on BRINE, not an arbitrary saved pan.

scripts/run_save.gd now requests the existing deferred core-center helper after
revealing a successfully restored view. It retains the helper's camera revision
guard, preserves saved zoom, and leaves state loading/input protection unchanged.
No owner data, art or gameplay rules changed. Current packages predate this fix.

## Verification
Controlled native disk save/replacement-scene restore at zoom0.55 and1600x900:
before scroll(7454,7826), core ratio(.5125,.5125). Old restored scroll(8117,8117)
puts center at(.554356,.530871). Fixed scroll(7453,7825) centers within1.42viewport
pixels and stays stable across five observed frames. Fixed screenshot inspected.
Logs: camera-control.log and camera-fixed.log under
output/normal-expedition-restore-2026-09-22; camera-fixed.png is reviewed.

Maintained tests/test_staged_restore.gd now exercises a nondefault saved zoom and
asserts the Continue focus within2pixels after layout. Native exit0, zero failures;
existing staged/synchronous crew/resources/navigation, invalid-save rejection,
loading/input guards and partial-save prevention remain covered. Evidence:
staged-regression.log in the same folder. Paired UID retained.

## Diagnostic correction and workflow
The first camera.gd probe silently started a new loop after finding no checkpoint;
its camera-before.log/png are INVALID restore evidence. Continue adopts the loaded
file's _path. Ending the preceding continuation therefore removed the copied
checkpoint.loop as a live completed run. The previous successful restoration and
cycle progression records remain valid; the later claim that this copy remained
preserved was wrong. The controlled reproduction creates a new camera-checkpoint.loop
copy and does not conclude it. It is a camera fixture, not the old expedition.

Future checkpoint probes must fail on empty disk reads, restore from a disposable
working copy, and keep an untouched evidence copy. Do not infer successful Continue
from a plausible centered new-loop image or a zero process exit alone.

## Next action
Include camera focus and the Fit scheduling change in the next planned playable
export. Continue ordinary expedition/art review; native Apple Silicon acceptance
remains independent. No new export was made just for this fix.
