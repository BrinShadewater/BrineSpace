# Bill helmet-equipped west cargo

## Canonical head correction - 2026-09-30

Owner found animated face/helmet differed from idle. head-lock-v2 now selects
the exact accepted equipped-west interact000 head, not generated equipment.
sources/canonical-head.png extracts only helmet/neck and excludes idle shoulder
patch. Each frame starts from that same source; translation follows warm bare
head landmarks, crouch pitches0/5/10/15/20 degrees around the neck socket. Carry
uses unrotated canonical pixels. No head rescaling, recoloring or regenerated
face. Generated atlas retained as rejected design evidence, unused by builder.
Previous exports preserved under review-before-head-lock-v2.

235 checks pass including canonical source RGB and opaque carry head RGB matches,
body preservation, connectivity, timing/profile/hash and reversed unload joins.
Contact and82/54/27px views reviewed; preview at ?v=head-lock-v2.
Owner visual review pending; staged/uninstalled.

The initial candidate notes below describe the superseded generated-head pass.


Staged version of accepted master-detail west cargo:12 pickup/6 carry/12 unload
references with retained520/840/520ms timings and original stride/profile.
Generated pose-specific west helmet regions fitted over original cargo bodies.
Body/case pixels below fitted neck are byte-identical to approved bare exports.
Unloading reverses fitted pickup images, with its own original timing.

Source helmet-pose-sheet.png:exec-7722716b-beff-4451-8a2a-a1f21f6bd172.png.
Original preserved under C:/Users/Alex/.codex/generated_images/
01a0ef89-cf35-77f0-9b57-2a08e6ea987f. Exact prompt in prompt.txt.
Input atlas has18 unique pickup/carry figures, three occupied256px rows plus
empty fourth row. source-cells.json preserves ordering; no extra pose claims.
Authority: shared-helmet-standard-v1/bill-west-fitted-reference.png and accepted
equipped-west-selected-v1/interact-west first idle endpoint.

Generated body changes rejected. Only helmet/neck extracted, with a west-facing
contour excluding generated shoulder patches. Connected-component isolation
rejects boots spilling from previous generated rows. Warm head landmarks align
crouches independently of rear shoulder height. Equipment scale and shell/skin
grade frozen against selected idle; no pose-by-pose body resizing or exposure.
Actual accepted idle head at empty-handed endpoint. Registration records source
head bounds, offsets, grading and protected body rows.

221 checks pass: body preservation, timing/profile/hash/alpha, connected crown,
six distinct carry images, exact idle join and12 reversed unload references.
Contact and82/54/27px dark/light views inspected. Preview compares full approved
bare/equipped chains and offers12-pose manual pickup stepping.

Rebuild from repository root with build.py, build_review.py and verify.py here.
Staged/uninstalled; owner review pending. South/north equipment, carry turns and
isolated native integration remain. No Godot/save access, release or commit.


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
