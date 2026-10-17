# Bill helmet-equipped east cargo

Staged equipped version of accepted bare east cargo:11 pickup/6 carry/6 unload
references, original timing/stride/profile. Generated shared-helmet fitting for
each head pose. Approved body/case artwork below neck is byte-identical to bare
exports. Body is never rescaled. Actual selected equipped idle head used at empty
endpoints; moving shoulders stay from the authored cargo frame.

Generated source helmet-pose-sheet.png:
exec-9aab1895-dc39-41ca-b575-8e66b8d021e1.png, original preserved under
C:/Users/Alex/.codex/generated_images/01a0ef89-cf35-77f0-9b57-2a08e6ea987f.
Input bare-pose-sheet.png is a23-frame atlas, source-cells.json records ordering.
Exact prompt in prompt.txt. Equipment authority is shared-helmet-standard-v1/
bill-east-reference.png and selected bill-equipped-east-selected-v1 idle.

Generated bodies grew; rejected for selection. Only equipment regions extracted
with a consistent shell/neck contour, excluding generated shoulder patches.
Warm head landmarks avoid registering crouch to its higher rear shoulder.
Frozen equipment scale and neutral/skin mapping calibrated once against selected
idle; no per-pose body resize or exposure adjustment. Registration records fitted
head boxes, offsets and protected body rows. Original case/limb detail retained.

144 checks pass: hashes, dimensions/alpha, original body pixels, timing/profile,
six distinct carry images and exact empty-handed joins. Close neck review and
82/54/27px dark/light views inspected. Browser compares complete bare/equipped
cargo chains, with11-pose manual stepping. Staged, not runtime-bound.

Build from repository root using build.py, build_review.py and verify.py here.
Other equipment views/carry turns and isolated native integration remain.
No Godot/save access, export or commit.


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
