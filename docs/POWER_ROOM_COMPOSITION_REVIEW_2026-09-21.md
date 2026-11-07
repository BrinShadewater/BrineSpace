# Power room composition review

September 21, 2026. Broad objective remains active.

## Objective and constraints
Review remaining saved/default power-room furnishing without touching protected
owner rooms, source pixels or published packages. No Higgsfield.

## Current evidence
Saved Current Turbine, Biomass Digester and Heat Recovery: twelve native views,
1,920 walking samples, zero failures. Inspected q0 of each. Turbine and Heat Recovery
retain clear large functional machines; Biomass is mostly pump/hopper/sacks/controls,
with no obvious digestion vessel. Its wrapper deliberately removes the old machine
for the full-wall bank, while the current saved layout hides that bank as well.
No renderer bug is claimed from this authored arrangement.

Reviewed source shortlist fac-20, gs-117, mb2-276 and mb2-287, plus the old biomass
machine. The old machine is detailed but tall/front-elevation; it was not restored.
Staged fac-20 processing unit (185x94 source) at 1.25 display scale, with hopper and
feedstock sacks below and controls opposite. Loose pump/valve/barrel pieces are
hidden in the candidate. Source PNGs/registry unchanged; enlargement creates no
new detail. The source subject is a generic processing line, not verified scientific
digester engineering.

Candidate 1 at [-150,-180] blocked three approaches. Revision 2 at [-150,-144]
passes all four views / 640 walking samples. Native q1 inspected after correction;
remaining all-view and live-scale visual review still required. The first preview
also exposed misidentified support IDs: fac-118 is the blue barrel; mtp2-84 is the
control cabinet. Revision 2 hides the barrel and retains the cabinet at [72,72].
Source crops and registration must establish identity; filenames alone are weak.

## State and next action
Candidate only: output/power-layout-review-2026-09-21/biomass-candidate-r2.json.
Owner profile remains byte-identical to the snapshot; no production source, layout,
card or package changed. Review all native views and live presentation/feedback
before any guarded saved/default promotion. Preserve Turbine/Heat Recovery pending
further specific findings. Current verified builds remain e3d4c7647fe9e73f.

## Live review decision

The live fixture completed normally; no matching Godot process remains. Reviewed
its full station capture at slider 0.75 (actual grid zoom 0.64125), native room crop,
and r2 q0/q2/q3 alongside the previously reviewed q1. The synthetic funded fixture
proves framing only, not normal economy or autonomous work.

Revision 2 is rejected for installation despite its passing route checks. fac-20
reads as a tall front-elevation factory machine: the large upright casing, tank
and chimneys dominate while very little top surface is visible. This conflicts
with the current low/top-down equipment direction. Hopper and sacks remain an
isolated lower-left group, with controls isolated lower-right; filling the missing
anchor alone did not establish a convincing feedstock-to-processing work area.
Four quarter captures repeat the same machinery facing and are not evidence of
four authored equipment orientations.

Next: select a lower processing vessel or skid from actual source crops, then
compose feedstock handling adjacent to its inlet with accessible inward controls.
Do not add screen effects, promote layouts or bake a card for r2. Current production
layouts, art, registry and verified packages remain unchanged by this review.

## Lower-vessel study, revision 3

Reviewed a diagnostic source board of all 24 registry tank/vessel/processor/vat
entries at least 85 source pixels wide and aspect ratio >=1.15. Evidence:
output/power-layout-review-2026-09-21/wide-vessel-sources.png and matching JSON.
Most alternatives are tall factory lines, fuel tanks, laboratory specimens or
small accessories. mb2-286 has a substantially more visible top plane.

Staged mb2-286 at [-168,-138], scale0.65, hopper[-168,24], sacks[-72,48],
controls[48,-114] in all four Biomass candidate keys. Actual r3 native run passes
4 views /640 walking samples. q0 inspected: camera is improved, but bright lid,
water-drop emblem and lack of visible feed connection prevent production acceptance.
Remaining q views and live scale are not yet reviewed. Candidate stays output-only.
Next art work should address material/identity and inlet connection, or choose a
better source; do not promote merely because routes pass. No source pixels edited.

The first r3 command accidentally addressed the JSON envelope instead of layouts
and changed zero keys; its result was only a repeat of r2. Corrected the script
to address layouts, asserted exactly four keys, reran and replaced r3 evidence.

## Vessel art repair and revision4c

One built-in image_gen edit produced a matte olive vessel with an organic-material
emblem and attached covered feed hopper. No Higgsfield. Bought source atlas stays
unchanged. Raw1420x1108 RGBA has real0..255 alpha; alpha-bounds crop and nearest
thumbnail yielded246x193. Raw output, exact prompt, reference, source/output hashes
and processing details are preserved in output/power-layout-review-2026-09-21/
biomass-vessel-r4-provenance.json and its referenced files. This is newly generated
art derived from a reference, not an exact pixel-preserving local recolor.

A fixture-local library catalog injects the candidate, leaving production registry
and saved/default layouts untouched. Floor footprint [.04,.35,.92,.62] covers the
vessel body rather than using the thin baseline of the donor tank. First190-unit
placement failed6 door routes. Reducing width to160 at[-174,-156] passed all4 views
and640 samples; r4b all4 stills reviewed. r4c moves sacks to[-116,-20] and controls
to[30,-112], bringing supports closer. r4c also passes4 views/640 samples. Its live
fixture completed exit0; native crop and full75-slider view reviewed. Vessel reads
clearly without the previous glaring lid. Room remains sparse and operating
feedback is unfinished. r4c all4 stills, effect checks, source-edge/depth review,
guarded promotion and card baking remain. Do not claim owner visual acceptance.

## Installed follow-up

r4c is now installed; see BIOMASS_VESSEL_INTEGRATION_2026-09-21.md for final
files and checks. Correction: footprint metadata affects shadows, not collision.
All these navigation checks used the full prop rectangle without collision_boxes.
The later rear-over-top-plane depth probe is expectedly blocked; do not count its
log as a passing depth review. Other tested operating positions remain clear.
