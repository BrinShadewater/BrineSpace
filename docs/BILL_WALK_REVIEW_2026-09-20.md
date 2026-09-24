# Bill walking review



Updated: September 20, 2026 Â· Project: BrineSpace



## Objective and acceptance

Resolve the owner's report that Bill still walks oddly. Preserve identity, detailed

palette, world size, foot contact, equipment and unrelated animation states.



## Accepted decisions and constraints

No Higgsfield. This review changes no production pixels, timings or movement speed.

Earlier full-pack technical acceptance is not evidence of natural body motion.



## Current state

The active loader still selects major-bill-v3. The side-view leg repair is present.

Both east/west walks, bare and helmeted, reuse precisely the same upper 119 source

rows after accounting for the one-pixel bob in slots 1 and 4. Arms and shoulders

therefore have no independent movement. tools/repair_bill_walk.py explicitly

composites the same torso then pastes the same upper source strip in every frame.



Reconstructed pre-leg-repair poses with base_frames(repair_walk=False). These retain

some upper-body variation, but their old legs are not a complete alternating gait;

do not restore the entire original row. Contact sheets show the preserved/current

comparison. A study should recover upper-body motion without undoing the leg fix.



## Verification

Evidence: output/bill-body-motion-2026-09-20/.

- runtime-test.log: active complete-pack test, 11,773 checks, zero failures.

- native.log and native-selected/: 60 rendered frames, 240 side-view/equipment

  samples using the runtime player at 46 world units/second; zero parity failures.

- motion-audit.json: hashes of all 24 selected frames and exact upper-body equality.

- east-comparison.png and west-comparison.png: visually inspected source comparison.

- native-samples.jpg: sampled native poses inspected at two rendering scales.

- runtime-walk.gif: 2.4 seconds of captured motion. Created for review; static sampled

  inspection does not establish temporal smoothness or owner acceptance.



Side-view stride remains about 40.58 world units per cycle, approximately 0.882

seconds at normal NPC speed. Cadence alone cannot animate the rigid upper body.



## Upper-body motion study



Two built-in image-generation candidates are preserved with exact prompts, original

sheets and hashes in character/major-bill-walk-study-2026-09-20. No Higgsfield.

V1 is rejected: including the old source comparison confused the intended leg poses.

V2 used only the selected row and explicit near-wrist back/pass/forward phases.

It shows visible arm counter-swing, but changes face, shoulder insignia, suit and

some leg pixels; it does not satisfy exact preservation and is not installed.



V2 has a six-frame bare-east candidate manifest, one shared scale/pivot, preserved

alpha, and a 60-frame native comparison at actual NPC speed and two world scales.

Evidence is in generated-candidate/ beneath the existing output directory.

Native poses were inspected; temporal smoothness and planting are not yet accepted.

No west/helmet candidate exists. Production frames, manifests and timings remain

unchanged. The study proves a visible motion direction, not a finished repair.



## Next action

Build a bounded east/west upper-body candidate from preserved poses while retaining

the selected leg cycle. Keep a stable head anchor and fitted helmet. Inspect waist

joins, natural counter-swing, shoulder movement and looping at normal station scale.

If the old poses cannot provide a coherent cycle, create new referenced motion art

with the available image tool; no Higgsfield. Keep candidates separate until native

motion, contact and equipment checks pass. Do not broaden to unrelated actions.



## September 21: joint artwork also needs repair



Close-up inspection of both comparison sheets shows fragmented knee/shin contours

in selected articulated legs. Retain their alternating support phase, stride and

registration, but do not require damaged joint pixels to survive the repair.



Evidence: output/bill-body-motion-2026-09-20/leg-transparency-audit.json hashes

12 selected and 12 preserved bare frames. At alpha >=128 and four-way connectivity,

selected west frames 0/2/4 have 2/25/10 enclosed transparent pixels below row 119;

preserved west has none. East has zero enclosed holes in both sets despite visible

contour concerns. This metric excludes open notches and cannot certify anatomy.



This supersedes the upper-body-only next action above. The next candidate must

combine coherent knee/shin surfaces and arm counter-motion, preserving identity,

equipment fit and support timing. Use preserved anatomy as material reference and

selected support phases as motion guidance, with their roles explicitly separated.

No production pixels changed. Foot-plant mathematics alone does not approve art.



## September 21 generated joint-and-motion candidate



V3 from a single preserved east anatomy reference produces coherent leg surfaces

but repeats similar same-leg configurations in slots 0/3 and 2/5. It fails the

complete alternating support cycle and remains rejected, unextracted and unselected.

Original sheet, prompt, hash and review are preserved in the existing character

study directory as east-v3.*. No Higgsfield or production changes.



Next source experiment should establish two unmistakably opposite contact poses

before intermediates, checking near/far leg and arm identity explicitly. Repeating

whole-sheet requests with stronger wording has not reliably controlled gait phases.





Single opposite-contact experiment: near arm moved forward, but the pouch-bearing

near leg remained forward despite explicit limb identification. Rejected and

preserved as opposite-contact.png with exact prompt and hash in the study directory.

Stop further text-only phase retries. A controllable pose/occlusion source is needed

before another full animation generation. Production remains unchanged.





Pose-guided repair also rejected: used runtime east frame 003 as the explicit pose

and preserved frame 0 as material reference. Generated result changed leg landmarks

and retained the down arm. Exact prompt/source/hash saved as pose-guided.* in the

study directory. Stop further image-generation retries for this repair: sheet,

single-contact and dual-reference approaches have all failed phase control.

Next method to evaluate is deterministic layered reconstruction with explicit joint

and occlusion control, preserving original pixel identity. No production changes.





Rig-source audit: rebuilding from each preserved frame 0 with the existing

repair_bill_walk.build function exactly matches all 12 selected bare side-view

frames. Evidence: output/bill-body-motion-2026-09-20/rig-layer-audit.json records

layer extents, opaque areas and per-frame equality. The visible joint defects are

therefore present in the reconstruction output, not introduced by an import or

runtime selection mismatch. Layer bounds alone do not identify a sufficient fix.

An explicit user choice is pending for switching from image generation to local

script-assisted pixel-layer editing. Analysis only; no new raster output or live

frame changes. Next, if selected: adjust joint coverage in an isolated candidate,

then inspect source/normal-scale motion before any integration.





## Authorized local pixel-layer work â€” September 21



Owner explicitly authorized local pixel-layer repair and other needed animation

repairs. Earlier method-choice blockers are resolved. First bounded experiment:

tools/study_bill_joint_layers.py reuses preserved kneecap surfaces over the existing

cutout seams, retaining all original joint trajectories. Twelve isolated frames,

source hashes and before/after sheets are in output/bill-pixel-layer-2026-09-21.

West comparison inspected: patch overlap alone does not sufficiently repair the

fragmented leg surfaces. Not promoted. No selected frame/manifest or equipment

changed. Next experiment should use continuous limb surfaces with shared joint

boundaries rather than overlaying more cropped patches; arm counter-motion remains

required. Do not mistake this diagnostic study for the completed Bill fix.





Continuous-limb experiment: tools/study_bill_continuous_limbs.py uses four triangles

per leg with a shared knee edge, sampling preserved source pixels with nearest

sampling. Output is in output/bill-pixel-layer-2026-09-21/continuous, separate from

the patch study. Both directional sheets inspected. All 12 frames preserve rows

0â€“117 and 168 onward exactly against selected art; original joint trajectories

are retained. 631â€“1,115 pixels change per frame. These checks do not approve anatomy.

Uneven thigh width and poor hip transitions remain visible, so do not install.

Next refine source limb boundaries/hip coverage before arm counter-motion, helmet

integration and runtime motion review. Replacing cutout seams with a mesh alone

is insufficient; the mesh must follow actual authored limb surfaces.





Landmark review: source-joint-landmarks.png overlays the inherited skeleton on the

preserved source. Several knee anchors are displaced from visible kneecap centers.

The landmark-refined study adjusts those source knees and re-solves knees with the

existing hip/ankle paths; all 24 leg poses remain reachable. Its provenance records

actual revised knees, source lengths and anchors (not the baseline trajectory).

West comparison inspected; contour defects persist, so this remains unselected.

Remaining source-layer ownership/occlusion needs explicit review before more mesh

refinement. Do not claim revised anchors alone establish anatomical correctness.





Isolated-source follow-up: near/far layers now partition every visible source pixel

below row 112 exactly once; their recombination is checked byte-for-byte before

warping. Wider cages no longer directly sample the other leg's source region.

Both sheets in output/bill-pixel-layer-2026-09-21/isolated-limbs were inspected.

All revised poses remain reachable, but visible ankle/cuff and pelvis joins remain

unsatisfactory. Not installed. The retained separate rigid boot treatment and

fixed torso overlap are still potential discontinuities; next review must examine

those joins rather than equating lossless layer extraction with good deformation.





Whole-limb alternative: tools/study_bill_whole_limbs.py preserves each isolated

leg and its boot as one rotated source layer, then aligns the sole vertically.

East comparison retains cleaner suit surfaces than the mesh studies. Upper-body

poses now reuse preserved slots [0,1,5,5,2,1], with the original head region retained.

This is a candidate, not acceptance: rigid knee shape, hip continuity, stance-foot

rotation/sliding, waist joins and smooth temporal transitions still need review.

The sole correction can shift the hip, so the older exact joint/foot-row checks

must not be claimed for this alternative. Both directions and a bare manifest are

in output/bill-pixel-layer-2026-09-21/whole-limbs. No helmet candidate or integration.

Next run the runtime player with this manifest at NPC speed and compare foot motion

before deciding whether the cleaner appearance compensates for rigidity. Preserve

existing production bindings until the full repair meets the gait requirement.





Whole-limb native evidence: native_review.gd in the candidate directory uses the

runtime player, 46 world units/second, 60 captured frames, east/west at normal and

2x scale (240 candidate samples). Completed with no missing frames/metadata or

engine errors. Native sampled poses inspected; native-walk.gif preserves 60 x 40ms

= 2.4 seconds. No claim of temporal acceptance from the sampled contact sheet.



contact-drift.json measures lowest opaque sole-row centroid plus expected world

travel during stance: east near/far 16.52/13.17 source pixels; west 13.67/18.93.

This centroid can move as the foot rolls, so it is NOT a tracked material-point

sliding measurement. Nevertheless, it exposes contact motion that the old ankle

anchor check did not describe. Review fixed foot landmarks/ground contact across

stance before promoting cleaner whole-leg art. Helmet, complete arm counter-motion,

waist continuity and native temporal acceptance remain open. Production unchanged.





Boot-orientation experiments: study_bill_smooth_limbs.py uses a thin-plate warp

with independent boot controls; east sheet shows stretched edges and is rejected.

study_bill_ankle_blend.py limits the rotation blend to a 16-source-pixel ankle band.

Its east sheet retains cleaner upper-leg surfaces but introduces unacceptable boot

shapes in some swing poses. Neither is installed or receives native acceptance.

Evidence directories: smooth-limbs and ankle-blend under the local pixel-layer study.

The original whole-limb variant remains the cleanest local surface comparison,

but its stance contact motion remains unaccepted. Next constrain the ankle warp's

local shape/orientation explicitly rather than broadening deformation or claiming

independent controls prove grounded feet. No runtime speed/timing changes.



### Integrated enclosed-alpha repair — September 21



Applied the bounded joint-pinhole correction to west poses 0, 2 and 4, bare and

helmet: 2/25/10 formerly transparent pixels per variant (74 total). Every prior

opaque pixel and alpha bounding box remains unchanged; no manifest, timing, pivot,

stride or silhouette change. The maintained repair builder now floods exterior

transparency, fills only enclosed lower-body gaps with nearest existing pixels,

and rejects unexpected totals above 32 pixels per frame. Original PNGs and hashes

are preserved in output/bill-pixel-layer-2026-09-21/alpha-repair/integration.json

and its adjacent before images. Before/after joint surfaces visually inspected.

All 12 bare side-view frames exactly reproduce from the builder. Complete-pack

validation: 11,773 checks, zero failures. This is a local surface repair only;

natural arm motion, coherent open joint contours and full motion acceptance remain

unfinished. The whole-limb study is still unselected because boots tilt in contact.



### Isolated upper-body motion candidate — September 21



`tools/study_bill_upper_motion.py` stages 12 bare side-view frames using preserved

upper poses [0,1,5,5,2,1], aligned to the existing one-pixel bob and fixed head.

Pixels below the explicit waist cut are asserted identical to selected production

legs (including the integrated alpha repair). This separates arm-motion review

from the rejected whole-limb rotations. East/west sheets visually inspected;

shoulder/arm motion is visible, but hard waist joins and timing still need motion

acceptance and helmet coverage. Native comparison renders 60 frames/240 candidate

samples at NPC speed with zero loader/metadata failures; this is not a natural-gait

acceptance. Evidence and looping comparison:

output/bill-pixel-layer-2026-09-21/upper-motion/. Production motion unchanged.



Upper-motion equipped coverage: all 12 candidate side-view frames now have helmet

variants composed from the canonical HelmetRebaker overlay and existing registration.

The identical recipe first reproduced all 12 production helmet frames exactly.

Native equipment-manifest acceptance and 240 equipped playback samples pass.

Connectivity inspection finds one 8-connected opaque component in every bare

candidate, as in production; no detached waist islands. This is not a shading-seam

or temporal-motion acceptance. Native equipped frame 012 visually inspected.

Evidence: upper-motion/helmet-manifest.json, native-helmet/, native-helmet.log and

connectivity.json. Candidate remains staged; production remains pinhole repair only.



## Bill upper-body motion integrated — September 21, 2026



Integrated revision 2 of the preserved arm/shoulder sequence [0,1,2,5,2,1] into both

side views, bare and helmet (20 PNGs change; four contact frames already match).

Selected lower-body pixels, contact timing, stride, pivots and head registration

are preserved. Canonical rebuilding reproduces all 12 bare poses; the established

helmet recipe reproduces equipped baselines. Complete-pack validation passes

11,773 checks, and post-integration native equipped playback passes 240 samples.

This removes the frozen upper-body cycle; remaining leg contour and overall gait

quality work is still open, and owner motion acceptance is not claimed. Source

backups, hashes, phase comparisons and native captures are under

output/bill-pixel-layer-2026-09-21/upper-motion-r2. Earlier staged-only notes below

are historical. Existing Windows/Mac packages predate this change.




### Other active crew base walks audited

The September 21 audit covers 96 bare base-walk frames from active catalogs.
No canvas-edge contact; all non-Bill rows have six distinct registered upper
regions. Contact sheets inspected for Veld, Marsh and Branforth. Legitimate
between-leg background can register as enclosed alpha: no blanket fill applied.
Supplemental, equipped, action and drone clips and temporal quality are outside
this inventory. Evidence: output/crew-walk-audit-2026-09-21/report.json.

## Bill motion regression guard — September 21, 2026

Added tests/test_bill_walk_surface.py: selected side-view bare/helmet frames must
have at least three distinct bob-registered upper poses, retain the fixed head,
and reproduce exactly from the canonical body and helmet builders. Both tests
pass. An in-memory mutation restoring a frozen east torso is rejected, without
editing production files. This guards the specific stiffness regression missed by
file/manifest checks; it does not prove natural temporal motion. Runtime inspection
confirms ordinary ground walking selects the repaired base loops directly; no
walk-start/stop substitution occurs. Source-contract dependencies on the changed
side frames are limited to walk-east and walk-west.
Run: python -m unittest discover -s tests -p test_bill_walk_surface.py


## September 21 contour review: two rejected studies

Re-inspected the selected side-leg poses after upper-body integration. A staged
higher-clearance swing (sole targets 160/165 instead of 166/169) exposes existing
cutout knee seams more strongly. A separate source-pixel kneepad overlay, using the
original stride and source knee patches of radius 8/7, makes passing poses bulky.
Neither is integrated. Selected bare/helmet files and canonical builder unchanged.

Evidence: output/bill-pixel-layer-2026-09-21/contour-review/review.json and its three
contact sheets. This was visual pose review only; no native gait acceptance claimed.
Next repair must address individual knee silhouettes/overlap before changing swing
height. Do not repeat these generic clearance/patch recipes as finished animation.

## Targeted east passing-knee contour installed

A source-space edit replaces the generic studies: east phase 2's knee silhouette
has two outward teeth trimmed and a one-pixel notch bridged, retaining the dark
outline. Exactly 15 pixels change in each matching bare/helmet frame. Other phases,
upper body, timing, foot contact and registration remain unchanged. The canonical
`repair_bill_walk.py` builder applies this explicit phase-local correction and rejects
unexpected source edges rather than silently filtering new artwork.

Enlarged before/after pose comparison inspected. Focused surface tests pass (2),
including exact builder reproduction of all 24 selected side frames; complete pack
passes 11,773 checks. This is contour cleanup, not completed natural-gait acceptance.
Evidence/backups: output/bill-pixel-layer-2026-09-21/contour-review/
(targeted-integration.json, east2-targeted-pixels.json, east2-targeted-comparison.png,
pack-check.log). No new generation or Higgsfield use.

## September 21: standalone preview parity repair

The production builder already restored upper motion, but repair_bill_walk.py main
still exported frozen torsos and static helmet upper bodies. Updated that entry
point to use restore_upper_motion and the canonical registered helmet overlay.
Head-only identity metrics now describe what is preserved. All 24 review PNGs
exactly match selected production pixels; three focused surface tests pass,
including a new command-level regression. Evidence: output/bill-review-command-2026-09-21.
Production sprites were unchanged. Natural gait and knee review remain open.
Maintained and installed source-density guidance updated with this verified lesson.

## September 21: passing-pose rise study, not installed

Current knee-angle inspection shows supporting legs remain substantially bent in
passing poses. A staged three-source-pixel additional body/hip rise on phases 1/4
keeps existing sole targets, durations and stride. Both directions and registered
helmet variants were composed from existing pixels. Native distance-driven playback
captured 60 comparison images (four rows per image). This is capture evidence, not
a natural-motion test or proof of improvement. Inspected source and native poses
are slightly more upright, but knee/shin overlap remains lumpy; no production
change was made. Next work should repair the individual overlapping joint surfaces
before accepting a gait-height change. Recipe, current/revised sheet and native
captures: output/bill-knee-review-2026-09-21/. The first diagnostic crop sheet was
corrected to an integer 3x aspect-preserving enlargement before review.

## September 21: source joint ownership diagnosis

Measured 289 east and 211 west near-leg source pixels shared by thigh and shin.
This confirms overlap, not that overlap alone causes the bad-looking gait. Three
staged source-layer approaches were reviewed: clipping the thigh at the knee
exposes a harsh seam; an individually selected separate kneepad changes relatively
few pixels and leaves the bulky pose appearance; reversing thigh/shin order moves
shading seams without resolving anatomy. None is installed. Production gait,
frames and canonical builder remain unchanged. Avoid another broad overlap-mask
or layer-order substitution; the next useful repair is pose-specific contour and
shading work with registered feet. Evidence and verdicts are in
output/bill-joint-ownership-2026-09-21/review.json.

## September 21: west contact ankle spur repaired

Installed a guarded 30-pixel contour edit in each bare/helmet west phase-0 frame.
The bright cutout spur above the boot is removed, preserving the toe, sole and
registered contact. Canonical builder and native runtime agree: three focused
tests, 11,773 complete-pack checks and 240 native comparisons pass. Enlarged and
native contact views inspected. Broader knee/gait quality remains open. See
BILL_POSE_CLEANUP_HANDOFF_2026-09-21.md and output/bill-pose-cleanup-2026-09-21.
