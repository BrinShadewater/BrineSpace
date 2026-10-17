# Veld North foot-contact repair

Updated: October 2, 2026 · Project: BrineSpace

## Objective and acceptance
Complete the full Veld animation library against original masters, then cross-library
polish. Current work: grounded North cargo gait during continuous travel, consistent
identity, physical proportions, camera and matte material in both gear variants.

## Accepted decisions and constraints
Original authored masters govern fidelity. Whole-source generated anatomy only;
one physical ruler, no limb strips/per-pose scaling/RGB recolouring/mirrored gear.
Moving bounding height may vary with pose; never normalize every boot to one floor.
Existing authorized reversible work; normal selectors and owner files preserved.

## Current state
Continuous movement review and source-contact diagnostic live at
../veld-carry-north-original-master-v1/motion-review-v1/. Foot contact FAILED despite
clock checks passing. New twelve-frame V1 and two-pose V2 raw sources/prompts,
inspect_source.py, registered diagnostic images and audits retained here.
V1 rejected: nearly fixed support contacts, body compressed. V2 diagnostic only:
LEFT support contact198→222, insufficient36target, body58 wide versus master63.
V3/V4 rejected: contact span13/19, colour too dark/too light, V4 too broad.
Direct continuous-motion trial in ../veld-carry-north-contact-video-v1 completed
but rejected after141-frame review: crossing/merging feet and colour flash81–82.
No accepted replacement/export/controller change. Full goal remains active.

## Verification
Prior native motion interval1093checks0/180presentations8.0s; two gear traces with
three actual distance-driven cycles each, prescribed speed/position.193inputs and
2931owner non-log files unchanged. Contact sole-bottom proxy finds12support runs,
max9.2world-unit drift (~13.1px at93display). Native APNG180decoded exact. All28
distinct source poses viewed on two47/93native boards. Not normal station gameplay.
New candidates inspected whole-source and registered beside original master.
Two frozen catalogues193/193 remain byte-identical. No candidate native acceptance.
Upper-body held reference61/hips42 is the proper landmark comparison; resting
silhouette63 includes arms/gloves. V2 neutral upper-leg median75–76 already close
to held77; speculative darkening in V3 was a regression. See record_refinement.py.

## Next action
Correct V2 whole-source width/proportions/swing anatomy while retaining support
travel; establish original-faithful fore/aft support endpoints and suitable stride,
then expand complete alternating cycle. Verify source contacts AND moving native
travel at real scale; sparse/discrete source holds still cause within-hold sliding.
Rebase North turns, remaining cardinal fidelity/actions, normal integration and
full-library polish remain. Do not substitute foot lift or timing tests for contact.
