# Bill bare south cargo candidate

South-facing pickup12, carry6, unload12. Unload reverses selected pickup with
its own retained timing; clip totals520/840/520ms and stride/profile unchanged.
Staged for visual review, not runtime-bound.

Fixed source anatomy scales against selected south idle,256px/p128,224/standing148.
The ground-case endpoint uses the actual idle. Source lift cell11 overshoots
stature and is replaced by the separately authored neutral held-case cell0.
No per-pose height normalization. Horizontal head/body axis and vertical boot
plane registration keep the front-facing root stable.

Original generated sources and prompts preserved under sources:

- pickup.png: exec-831b7286-d96b-4a30-a028-8e2ff68a8050.png
- carry-unload.png: exec-816c4702-89e1-4414-aab1-a88608503b14.png
- carry-alternating-v2.png: exec-3a20a3d2-c968-4fdc-ae8e-c5cf025de461.png
- carry-alternating-v3.png: exec-c4b6fe16-f899-41db-8efd-9596ca27586b.png
- pickup-lift-v2.png: exec-cc6a5708-923b-4e73-b8cb-88a0cc98ab5f.png

Originals remain in C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f.
Selected lift-v2 smooths the crouch-to-rise sequence. Original carry and v2
favored one foot; v3 locally swaps the lower-leg arrangement in three generated
poses while preserving upper-body orientation, badges and case. It is an
independent south source, not a mirrored east/west character.

Shared east matte_grade.py calibrates to selected south idle, with axial head
mask coverage and local cloth detail recovery. Registration/settings/hashes and
diagnostic masks retained. Explicit case bounds preserve the ground prop where
it touches the boots.161 packaging checks include two-sided gait, standing
endpoint stature, prop presence, timing, profile, alpha, hashes and reverse joins.
Contact and82/54/27px dark/light views inspected. Browser compares complete
retained/new cargo chains and provides12-pose pickup stepping.

Rebuild from repository root: build.py, build_review.py, verify.py in this folder.
North cargo, equipment, carry turns and isolated native integration remain.
No Godot/save access, release export or commit in this pass.


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
