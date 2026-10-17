# Bill complete dry carry-turn candidate matrix

Twelve directed transitions each for bare and helmet Bill: eight quarter turns
and four opposite half turns. This completes candidate dry carrying-turn coverage,
not Bill's full animation set, installation or visual acceptance.

Quarter sources are the four authored planted bare turn packs and fitted helmet
variants. New front helmet quarters reuse atlas rows0/1 with actual body-angle
selection. Fixed graphite/silver, skin and blue-glass transforms remain separate.
Exact approved equipped neutral cargo frames anchor every cardinal direction.
Body/case/boots below fitted neck are preserved; no per-pose size normalization.

Half turns follow the existing clockwise routes:east→south→west,south→west→north,
west→north→east,north→east→south. Duplicate identical midpoint frames merge into
one with their durations added. Eleven half frames retain both800ms quarter
clocks,total1600ms. This differs from the older runtime680ms half clock; runtime
timing and movement settle/resume require explicit integration/native review.

Run build.py,verify.py,build_review.py locally. 343 structural/source-copy/profile/
timing/midpoint checks pass. Original quarter frames referenced rather than newly
authored;88 half-frame references are exact copies. Four quarter/body poses may
reuse a source head angle; source provenance records those selections honestly.

index.html compares synchronized bare/helmet views for all24 states at148/82/54/
27px. quarter-matrix.png and gameplay-matrix.png show all quarter source joins.
New front packs each have57 protected-body/endpoint/reverse checks. No owner or
native acceptance,installation,Godot save access,commit or export in this milestone.

Next:review whole family,install cargo without replacing neutral turn endpoints
with walking framezero,validate scratch-profile native timing and joins. Remaining
Bill water/everyday/death/other retained states and full-set consistency/polish
remain tracked in ../bill-animation-coverage-2026-09-30/coverage.md.


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
