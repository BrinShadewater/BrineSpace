# Project handoff

Updated: October 1, 2026 · BrineSpace · BRINE reference-derived floating body

## Objective and acceptance
Owner requested continued work after warmer reference-sheet revision. Develop the floating model from that sheet with portrait likeness, matching current crew density/style and existing chamber size/motion.

## Accepted decisions and constraints
Warm v3 reference sheet supplies identity/design. Current Bill matte south idle supplies crew comparison, not old base sprite. Retain current 184.8-source-unit chamber body height, eight-second drift and glass/rim layers. No production selection change at this candidate milestone.

## Current state
source-v1.png is authored floating body with unwanted low-opacity halo. Imagegen cutout retry retained halo and changed likeness/proportions, so rejected-cutout-v2.png is retained but unused. build.py extracts first source near-opaque alpha >=240, retains RGB and uses premultiplied resize to 61x148 body.png. Threshold discards faint edge/hair as well as halo; review at source and native scale remains appropriate. body-review.png compares previous/new/current Bill at common 148px reference height. Exact prompts, IDs, hashes and extraction contract in manifest.json.

Preview scripts plus UID pairs, scratch-profile launcher, room-preview.png, 200 native captures, native-size float-preview.gif and eight-pose motion-review.png saved here. Existing preview inheritance and chamber source are reused; this is not production installation or fresh Continue evidence.

## Verification
Native chamber and sampled motion visually inspected: clean silhouette, warm skin, readable suit and frame containment; actual current Bill displayed below chamber. Eight-second loop, rigid face and endpoint velocity assertions passed for 200 samples. Both overall runs FAILED due unrelated ui_widgets.gd preload/compile errors through project dependencies. Removing broad NPC helper dependency still left errors via room shell dependency. Do not call this clean runtime verification. Failed first captures retained in captures-first-run and room-preview-first-run.png; full logs for both runs remain in output/brine-float-v12/session-9beac0a7d89940c696e31a87853525ce and session-c9e506d17970418aac3d803860f18f7e. Both scratch-profile guards passed: 2,931 non-log owner files unchanged.

## Next action
Review new model/float appearance. Diagnose project UI dependency separately before clean production-path proof. Promote only with appropriate body registration, native chamber/power/pause/restore validation and owner appearance acceptance. No owner layout, runtime selection, gameplay, commit or export changed.

## Later source installation — October 1, 2026
Owner requested continued work. This section supersedes the candidate-only and open compile-blocker status above; earlier failed evidence stays retained.

Current ui_widgets.gd compiles without changes; old dependency error no longer reproduces. Production brine_core_view.gd selects v12 body.png and uses its 61:148 aspect at the existing 184.8 source-unit height, centered at x626/top584.6. Existing float motion and body-only linear filtering retained. Relevant test now verifies 61x148 source and aspect preservation.

Actual main-scene chamber test PASS: four rotations, 16 entry/return routes, 3,565 movement samples, mesh containment/loop/face, native motion/pause/offline and three viewport sizes. Actual production renderer independently captured 200 frames at 25fps; production-float.gif saved. Native room captures and representative production frame inspected. Both runs have clean error logs and guards PASS: 2,931 owner non-log files unchanged per interval. Integration manifest gives exact log/capture paths. PNG files have Git LFS filter; scoped diff check passes.

New source installation is agent-verified, with owner appearance acceptance pending. Existing running processes may retain cached artwork. No export, commit, save migration or separate fresh title Continue proof. Next owner review of production-float.gif and current source game; any further change follows that feedback.

## Startup and fresh Continue closeout — October 1, 2026
Owner again requested continued work. Startup regression now PASS, including disk phase restoration, power/pause and cryopod sequence. One stale tests/test_brine_startup.gd assertion expected a blue live crew member; accepted September 30 recovery reaches natural colour before handoff, and cryo_release_effect.tint returns WHITE deliberately. Corrected that assertion only. First failed run/source snapshot retained. Startup review mirrors maintained fixture into a fresh evidence folder and confirms exact v12 body pixels.

Independent fresh-process check used a disposable producer checkpoint copied into a new scratch profile, then actual title Continue and loading-transmission Continue controls. Engine PASS:15checks/0failures, exact body pixels61x148, correct aspect/height, scratch autosave path and paused restored body clock. Wrapper invocation mistakenly expected16checks and rejected the completion string; its failure remains recorded, while independent report/clean stderr/exit0/profile guard confirm native pass. No rerun for that count mismatch. Restored station and startup native captures inspected.

Startup/Continue guards all PASS:2,931owner non-log files unchanged each interval. Exact sessions and output paths in manifest.json, including original failure and wrapper count mismatch. New helper .gd/.uid pairs preserved; fixture snapshot and exact prompt/source provenance retained. No export/commit or owner-save checkpoint used. Source-model work and requested follow-through complete; next owner appearance feedback. Earlier statement that fresh title Continue was not exercised is superseded for this disposable source-project checkpoint.
