# Normal-clock checkpoint continuation

Updated September22,2026. Broad goal remains unfinished.

## Method and constraints
Extended the dealt-hand normal-clock opening in an isolated profile. At90seconds,
wrote the checkpoint, read it from disk, preserved checkpoint.loop in the evidence
folder, destroyed the live scene and used RunSave.pending through main startup.
Normal costs, failure rules, cycle timers and comms behavior remained enabled.
No source art, gameplay or owner data changed.

## Evidence
output/normal-expedition-restore-2026-09-22/review.gd and native.log: exit0, no
script errors. Restore opened paused; resources, full Bill snapshot (active weld),
placed-room data and cycle3 matched exactly. The120second wall window included
roughly20seconds loading and left only8seconds after Resume; that first pass alone
does not establish a post-restore cycle.

continue.gd reloads the preserved disk file and observes45seconds after Resume,
without new orders. Exit0; exact crew/resources on restore, survived, cycles3->5,
rooms4->5 as saved construction completes. Samples contain weld, idle and walk.
No injected blueprints/resources, no manual simulation stepping. End Expedition
was invoked afterward. continuation.json/log retain the measured sequence.

## Visual finding requiring diagnosis
Inspected restored-paused.png and continued-station.png. The camera is displaced
so most of the station is offscreen. State equality and resumed progress do not
close view restoration. Compare saved viewport/workspace values and settled UI
geometry before/after loading; isolate possible fixture window setup effects
before changing runtime camera behavior. Keep this checkpoint as reproduction.
The automated cursor's out-of-grid placement tooltip is a separate known capture
limitation. No full motion or ordinary human expedition acceptance is claimed.

## Next action
Diagnose the restored camera discrepancy using this disk checkpoint and native
before/after viewport telemetry. Preserve the verified state/continuation behavior.

Follow-up: camera discrepancy is reproduced and repaired; see
CONTINUE_CAMERA_FIX_2026-09-22.md. Ending the continuation deleted checkpoint.loop
because Continue adopted that copy's _path. The successful restore/progress evidence
above remains valid, but the old disk copy is no longer preserved. Use a disposable
working copy when loading a frozen evidence checkpoint.
