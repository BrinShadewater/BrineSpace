# Bill bare west cargo candidate

## Master detail repair - 2026-09-30

Owner found cargo had lost master detail. Selected source edits now restore
quilted sleeve/leg panels, square shoulder badge, collar/cuff fasteners, chest
controls, belt hardware and boot segmentation from the left-facing figure in
crew-side-masters-v1/bill-side-master-01.png. Exact prompt is prompt-detail-v2.txt.
Sources pickup-detail-v2.png and carry-unload-detail-v2.png preserve the existing
pose sequence; originals below remain intact. Generated originals:
exec-50a23ae4-6029-4221-999c-6c1bca203f1f.png and
exec-a9d1fcb8-f826-410b-b66d-4e59b41b7da1.png.
Same fixed source calibration/matte treatment; shared grade helper unchanged.
review-before-detail-v2 preserves previous exports.158 packaging checks pass;
detail-comparison-v2 and82/54/27px dark/light views inspected. Pickup endpoint
148/146px; carry141..145px with natural stride. Owner review pending at ?v=detail-v2.

The initial candidate notes below describe the preserved original sources.

Independent west-facing sources; no mirrored east art. Pickup12 poses, carry6
poses, unload12 references reversing authored pickup with separate legacy timing.
Original520/840/520ms clip durations and stride/profile metadata retained.
Fixed source anatomy scales against selected west idle,256px/p128,224/standing148.
First/last empty-handed body is selected idle plus source case. Held-case pickup
and unload endpoints are identical. Current pack is staged, not runtime-bound.

Built-in image generation originals, preserved in sources and exact prompt files:

- pickup.png: exec-f0daf74f-9138-4e69-b1da-159754d7fea6.png
- carry-unload.png: exec-ff93a75f-90f3-4842-8986-a889d5aec2b7.png

Originals remain in C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f.
carry-unload top row is an authored reference/alternative set-down proposal;
selected unload reverses the smoother12-pose pickup. Source cells recorded as
unused separately; no duplicate source-pose count claims.

Shared matte_grade.py from east uses west head-mask orientation, selected west
idle tone calibration and local source seam detail. Settings, hashes and crops
saved in source-registration.json; grade-masks inspected. First source ground
case touches boot component; explicit inspected case crop prevents extraction
from silently discarding it.158 packaging checks pass, including prop presence,
dimension/alpha/hash, retained timing/profile and exact reversed action joins.
Contact and82/54/27px dark/light review inspected. Browser compares complete
retained/new cargo chains with manual pickup stepping. Owner visual review pending.

Rebuild from repository root: build.py, build_review.py and verify.py in this folder.
Other directions, matching equipment/carry turns and isolated native integration
remain. No Godot/save access or release/commit in this pass.


## Installed selection — September30,2026

Bill's actual grid loader now appends all four cargo profiles,paired helmet packs,
and the full carry-turn matrix. Native test_bill_cargo_selected passes1615 checks
covering selected pixels,registration,paired timing,all directed turn clocks,
gait restart,NPC cargo-state selection and explicit scratch user:// resolution.
Native offscreen selected half-turn contact view:output/bill-cargo-native-v1.
Owner acceptance and whole-station movement settling/turn/resume polish remain
separate. Earlier staged statements above describe the source milestone.

The selected locomotion stride fields now remain authoritative:Bill's partial
action/timing/fitting loads opt out of inherited legacy stride imports. Cargo
manifests/builders override only carry=.12. Generic player behavior defaults remain
unchanged for other actors.1600ms authored half clocks now reach the actual loader;
pickup/unload/carry simulation timing remains unchanged.
