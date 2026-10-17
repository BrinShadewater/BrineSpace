# Bill equipped south cargo

Staged12 pickup/6 carry/12 unload references. Uses the actual accepted equipped
south interact000 idle head/helmet, selected from bill-equipped-south-selected-v1.
Source resource crop108,68,148,112 excludes shoulder corners. Canonical source
in sources/canonical-head.png retains original RGB, scale and design. Every
pose translates this same resource to its authored head position; no new source
generation, face design, head rescaling or color grading. Axial head stays facing
its direction while the torso bends and the legs crouch beneath it.

Body/case below fitted neck is byte-identical to bare bill-cargo-south-coherent-v1.
Ground case, existing gait, timing520/840/520ms and stride/profile preserved.
Unload reverses fitted pickup with its own retained timing. Registration records
head offsets and protected body rows; source/body/exports hashed.

235 checks pass:canonical RGB identity, opaque carry-head RGB identity, original
body preservation, connected crown, metadata/timing/alpha/hash and exact reversed
joins. Contact and82/54/27px dark/light views inspected. Browser compares bare and
equipped complete cargo chains with12-pose manual pickup stepping.

Rebuild from repository root with build.py, build_review.py and verify.py here.
Owner visual review pending; staged/uninstalled. Carry turns and isolated native
integration remain. No Godot/save access, export or commit in this pass.


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
