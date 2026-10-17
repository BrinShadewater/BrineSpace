# Project handoff

Updated: October 4, 2026 — Veld West authored carry cycle

## Objective and acceptance
Complete original-master-consistent cargo animation. Six-pose alternating carry candidate now staged for both gears, not owner accepted or installed. Visual consistency/contact gate remains incomplete; full Veld library unfinished.

## Accepted decisions and constraints
Five built-in imagegen complete-pose edits: opposite contact, near/far down and near/far passing. Previous near-contact v3 source reused as slot0. Explicit foreground/background knee/ankle instructions succeeded where earlier generic opposite-contact requests did not. All five new high-resolution sources, exact prompts and input hashes retained in their named folders. No new MiniMax job, billing for built-in edits unverified. Whole connected bodies, no isolated limb compositing, synthetic inbetween frames or per-pose grade/registration corrections.

## Changed files and current state
build_family.py produces12 PNGs, two manifests, paired APNGs, full chronology/head boards and three-scale software boards. Poses order: near contact/down/support-and-far-pass, far contact/down/support-and-near-pass. One fixed source scale0.10832719233603537 and offset73,73 for all1086x1448 sources. 256canvas, pivot128224, density148, dry, original840ms cycle and stride0.07351351351351351 unchanged. Original West helmet shell reused; body outside shell exact in all6 frames. Browser preview visible. No normal loader, controller, selected artwork or game timing changed. No live job.

## Verification
30 helmet-outside-body/APNG pixel-hold checks passed;21 outputs rebuild byte-exact. Native scoped player fixture504checks/0failures,12 three-scale presentations at47/93/148px. Exact source poses/pixels, metadata, moving-stride wrap, stationary hold, idle return, fresh-player restore, and103 ticks per gear over two moving cycles visit all6 slots.649 targeted inputs and2936 owner-profile nonlogfiles unchanged. Selected ending-West722 PNGs/38 manifests unchanged. All6 whole sources, bare/helmet chronology and software scales reviewed;4 representative native captures viewed. Test+UID in tests/test_veld_west_carry_poses_v4.gd; scratch-profile runner tools/run_veld_west_carry_poses_v4.py; output/veld-west-carry-poses-v4.

First native interval504checks/4failures preserved in output/pre-boundary-assertion: independent distance accumulation versus duration subtraction chose adjacent poses at exact0.7/1.4s boundaries. Diagnostic cadence showed source5 vs expected4 and source4 vs expected3, both gears. Final assertion permits adjacent slots ONLY within1e-6 of an exact hold boundary, retains exact comparison elsewhere and records all four boundary ties. Production player unchanged; no fixed wait or source-clock workaround.

## Limits and remaining work
Art gate remains incomplete despite technical pass. Head width27..29, axis128..132.5, top76..78; body H146..150 naturally changes with pose but does not prove proportion consistency. Boot opaque edge floor223..225 vs reference223, so no exact planted world-contact claim. Blue diagnostic medians progress56,84,128 to62,96,154; visible brighter badges on second half, not solved by clock checks. Small face/case/hardware changes remain. No continuously watched native animation, actual NPC route/furniture/root/contact, interruption or disk Continue acceptance. Wider contact/raised swing poses and loop/handoff smoothness need review. Original cargo head remains3px ahead of neutral master. West workshop arrival faces north; pickup currently idle during520ms wait and reversed pickup remains rushed audition.

## Next action
Reauthor material/detail consistency using the immutable high-resolution cargo master as PRIMARY identity authority and these correct full-body poses as separate geometry controls. Do not propagate brighter clothing from generated opposite pose into its children or apply per-frame exposure/anatomy masks. Establish supporting-foot geometry through the authored poses with one fixed ruler, then full loop and carry/unload/pickup/planted-turn handoffs. Preserve old840ms cadence/stride until visual/contact gates pass; then controller/lifecycle and fresh-process Continue checks before normal admission. No approval gate.
