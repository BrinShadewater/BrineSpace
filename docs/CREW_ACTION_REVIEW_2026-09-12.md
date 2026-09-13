## Owner movement polish priority - September 12

The owner reports frozen torsos and unnatural foot motion. Walking now takes
priority over seated expansion. Twenty walk variants across Veld, Branforth and
Marsh are marked owner-rejected-gait-polish-pending; prior timing/source checks
remain evidence of those checks only, not visual acceptance. Eight previously
identity-corrected Veld walk variants are reopened for motion quality.

Source audit confirms the side-view rig pastes one torso crop with only a small
vertical bob over separately transformed limbs. Marsh axial views stretch leg
images for foreshortening. These methods do not establish weight transfer,
shoulder counterrotation or natural boots. Do not retain them merely to satisfy
old pixel-preservation checks when replacing the gait.

Two full-body Veld east raw sources and exact prompts are preserved under
character/veld-identity-correction-v1/sources/walk-east-fullbody-{01,02}.*.
Raw 01 repeats the same lead-leg half-cycle; 02 improves upper-body opposition
but still needs final recovery-phase correction. Neither is selected. Next:
complete a coherent alternating full-body loop, register against a fixed ruler
without removing body motion, fit the helmet and review real movement/contact.
Then apply the approach to remaining directions and characters. Bill unchanged.
North seated source is preserved but paused. Full animation/movement polish,
workflow improvements and bible updates remain the active objective.

Full-body gait study update: raw walk-east-fullbody-03 corrects the missing
sixth recovery pose. tools/prepare_veld_fullbody_walk.py registers six study
frames at a fixed 140/562 ruler and common raw ground line, with recorded pelvis
anchors instead of centering on swinging feet/hands. Source, exact edit prompt,
contact sheet, registration and stationary-loop.gif are preserved in the Veld
identity folder. Registered contact was inspected: upper-body poses now change
with the step, but support-leg/occlusion continuity, world-space planting and
travel cadence still need native motion review. No new gait is selected.
Next: trace the two feet across the loop and review translation at game scale;
correct any phase ambiguity before fitting equipment or replacing live frames.

Whole-body walk translation study now renders the actual CrewSpritePlayer at
fixed travel speed (0.1 cells/second), comparing 76 versus provisional 122 source
pixels per cycle. 180 native samples and traces are saved under
output/crew-replacement-2026-09-12/veld/fullbody-walk-study-{76,122}/, including
moving-study.gif and phase-contact.png. The corrected native phase contact was
inspected. The fixture explicitly disables project stretch; the first preview
was scaled incorrectly and was regenerated. Log: fullbody-walk-study.log.

Contact-band estimates in fullbody-walk-contact-estimate.json suggest the old
stride is too short for these wider poses. They are centroids of rolling boot
bands, not tracked fixed sole points, and cannot prove planted contact or correct
leg identity. The 122 setting is a review candidate only. Neither source art nor
stride is selected. Next: inspect the loop and alternating support-leg continuity,
resolve any residual phase errors, then calibrate foot contact and fit equipment.

Passing-pose correction audit: strip revision 04 and single-pose revision 01
still fail the intended support-leg relationship. A guide-only single-pose
revision 02 obtains the grounded-near/airborne-far leg arrangement, but changes
costume/proportions and retains wrong near-arm opposition. All are unselected;
exact prompts, raw sources and decision JSON are retained. The explanatory joint
guide is review/walk-east-fullbody-01/passing-pose-guide.png. The existing gait
study and cadence remain provisional; no live gait was changed.

The next correction should use the explicit joint guide for pose and a cropped
canonical costume/identity reference that cannot pull the generator back toward
the old contact pose. Verify leg depth order and opposing arm before registration;
do not treat an attractive full-body redraw as proof of a coherent gait.

Separated-reference passing study: walk-east-passing-single-03 uses the explicit
joint guide and a cropped canonical upper-body reference. It clarifies grounded
near-leg / airborne far-leg support. However, the registered mixed-source contact
shows a noticeably narrower body than the surrounding five frames, so it is a
pose reference only and not selected. Evidence: character/veld-identity-correction-v1/
review/walk-east-passing-study-01/{contact.png,loop.gif,registration.json}.
Raw source, exact prompt and decision are preserved. Next: use a coherent
whole-cycle pose guide and canonical identity crop to avoid mixing body rulers
from independent drawings; retain the owner-rejected live gait status.

Whole-cycle guide experiment: review/walk-cycle-guide-01/ now preserves six
joint poses with consistent leg lengths, alternating support and opposing arms.
Source walk-east-fullbody-05 uses this guide plus cropped canonical identity,
but the output still repeats the near-leg/near-arm relationship across halves.
It is rejected as a walk cycle; no live gait or stride changed. Raw source,
exact prompt and decision JSON are retained. Do not keep repeating equivalent
whole-strip generation requests. Next work must change the motion-source method
or constrain complementary half cycles independently, preserving body consistency.

Continuous motion-source experiment started: Higgsfield Seedance 2.5 is
available and authenticated. A single four-second 1080p right-facing in-place
Veld walk video is generating from preserved existing artwork. Source reference,
exact prompt and durable job ID are in the identity sources folder as
walk-video-reference-01.png and walk-video-01.{prompt.txt,job.json}. Latest remote
status is in_progress. Resume that exact job; do not create a duplicate.
No video output has been reviewed or selected yet. Next: inspect continuous
alternating limbs, identity, framing and foot shape, then extract a coherent
cycle only if suitable. This changes the motion-source method after repeated
static-strip failures; the live owner-rejected gait is unchanged.

Continuous video source completed and preserved as sources/walk-video-01.mp4
with provider job/prompt/reference records. Decoded output is 97 frames at 24 fps,
1248x1664 (actual metadata, not the requested resolution label). Added reusable
tools/review_crew_motion_video.py; it retains source geometry, writes paired raw
and magenta-keyed temporal samples and records every frame's bounds/time. Review
contact at character/veld-identity-correction-v1/review/walk-video-01/temporal-contact.png
was inspected: opposing arm/leg relationships and changing shoulder/torso poses
are present, unlike the rejected repeated-half-cycle strips. This is promising
source evidence, not selected animation or planted-foot acceptance. Next: find
stable repeatable contact-to-contact cycle, sample the required six slots, retain
body motion under one ruler, then review translated native playback and equipment.
Do not regenerate the completed job. Source metadata and exact prompt are saved.

Video cycle checkpoint: tools/prepare_veld_video_walk.py now extracts frames 29, 34, 38, 43, 48 and 52 from the preserved 24 fps source, with the next matching contact at frame 56. One fixed scale and translation preserve torso rise and shoulder rotation. The six-slot candidate is in character/veld-identity-correction-v1/review/walk-video-cycle-01/. The native walk fixture now accepts fullbody-study video-cycle; its 180 distance-driven captures at stride trials 76 and 122 completed without errors (output/crew-replacement-2026-09-12/veld/video-walk-study.log). Visual review shows alternating limbs and body response at station scale. Sole contact, loop cadence and fitted equipment remain under review; neither trial is a selected stride and no rejected walk row is closed.


Gait contact calibration: manual heel-to-sole landmarks for the video-derived east cycle support a provisional 102 dense-pixel stride. Boundary residual ranges are 1.0/2.73 pixels for its two support phases, versus 9.67/7.67 at the old 76 and 5.67/7.67 at trial 122. Evidence: review/walk-video-cycle-01/sole-contact-analysis.json and sole-landmark-review.png under character/veld-identity-correction-v1. Native playback captured 270 samples across all three strides without errors; output/crew-replacement-2026-09-12/veld/video-walk-study-102/moving-study.gif shows the calibrated trial. Manual contact readings have 1-2 pixel uncertainty and held poses still translate between boundaries. This is calibration evidence, not final walk acceptance; helmet fitting and loop review remain open.


Selected east gait milestone: Veld walk-east body and fitted helmet now use the continuous whole-body source, fixed registration, original six-slot timing and calibrated 102 dense-pixel stride. tools/veld_scanner_revision.py selects the new frames before the old identity-only branch; tools/rebuild_human_crew_art.py selects the new stride. Native selected playback compared 60 distance-driven samples against the extracted source, including fitted helmet: zero failures. Validator: zero errors, zero border touches, all 670 original source frames and 108 source manifests unchanged. Evidence: output/crew-replacement-2026-09-12/veld/video-walk-selected-native.log and video-walk-validation.log; selected-moving.gif in walk-native/east. Eighteen variants still use the owner-rejected gait; this new pair is whole-body-gait-selected-live-context-pending, not owner-accepted or broad motion completion. Normal station travel/transition review remains next.


Live east gait review: the updated playtest_dr_veld.gd walk-review mode captured 15 consecutive samples (1.4 seconds) for both bare and helmet variants in the native research lab, including the east-walk to north-kneel transition. Both fixtures passed, retaining requested equipment and the existing full work-chain checks. Room contact sheets show body articulation without visible clipping at this approach. Logs: video-walk-live-bare.log and video-walk-live-helmet.log under output/crew-replacement-2026-09-12/veld; live-core-review-east-walk and live-core-review-helmet-east-walk contain traces and live-walk.gif. Existing image-loading export warnings are separate from this native result. Ledger status is whole-body-gait-selected-live-walk-reviewed; idle starts/stops, other turns and owner acceptance remain open. The other 18 rejected walk variants still require replacement.


West gait source prepared: sources/walk-west-video-01.mp4 under character/veld-identity-correction-v1 preserves a completed 97-frame, 24 fps, 1248x1664 motion source using the independently authored west scanner standing pose as reference. Exact prompt, crop and durable generation record are alongside it. Temporal review shows alternating support and torso/shoulder response; candidate cycle 28-52 and six source slots 28/33/36/40/45/48 remain unselected pending shared-scale registration, contact calibration and fitted helmet. review/walk-west-video-phases-01/temporal-contact.png records the phase inspection. tools/review_crew_motion_video.py now supports explicit --start/--stop/--step intervals for repeatable boundary review; its eight-frame east boundary check and 16-frame west phase extraction completed successfully. No additional selected gait rows are closed.


Selected west gait milestone: Veld walk-west body and helmet now use independently generated whole-body motion (source frames 28/33/36/40/45/48), fixed registration and the original six durations. Calibrated stride is 108 dense pixels; manual heel residual ranges at slot boundaries are 2.6/3.6 pixels versus 10.67/10.67 with old stride 76, with 1-2 pixel reading uncertainty. Preparation tools now accept east/west; all 12 existing east frame hashes remained unchanged. Selected native test: 60 distance-driven samples, zero failures. Validator: zero errors or border touches, 670 original frames and 108 manifests unchanged. Both native lab runs passed with 34 continuous west-walk samples through north-kneel approach; bare and fitted-helmet room contact sheets reviewed. Evidence is in west-video-walk-*.log and live-core-review[-helmet]-east-walk-west under output/crew-replacement-2026-09-12/veld. Four side-walk variants are now whole-body-gait-selected-live-walk-reviewed; 16 rejected walk variants remain (Veld north/south, all Branforth and Marsh). Idle starts/stops, other transitions and owner acceptance remain open.


## Veld identity correction selected - September 12

Veld is a woman with medium-brown skin, a silver-streaked dark bun and no glasses,
including under her fitted helmet. Her original concept controls identity.
Selected corrections cover all four directions of idle, walk, scanner and
kneel/sample/stand, plus east helmet donning/removal: 29 body clips and 27
helmet variants, 348 frames. The ledger records 56 selected corrections;
278 other Veld variants remain under identity review. The full Veld, Branforth
and Marsh replacement goal remains open; these counts do not imply completion.

The two helmet transitions use six authored key poses, explicit holds and the
original twelve-slot timing for each action. Held helmets are empty, the worn
helmet is fitted, and endpoints exactly match corrected bare/equipped idle.
The taller frozen transition canvas preserves the overhead lift. Source 01,
rejected for a duplicated face inside the held helmet, remains beside corrected
source 02 and both exact prompts. A legacy endpoint overwrite was fixed so
selected poses cannot silently restore older identity art.

Native selected-source, timing and endpoint checks pass: 170 body / 164 equipped
states, zero failures. Preservation validation reports 670 original frames and
108 manifests unchanged, zero errors and no border touches. Evidence:
output/crew-replacement-2026-09-12/veld/helmet-transition-{selected,validation}.log;
helmet-transition-study-native/all-phases.png and selected native phase captures.
The all-phase contact and selected overhead pose were visually inspected.
Continuous locker pickup/placement and live transition occlusion remain open.

Earlier continuous laboratory work review covers north/east/south, bare and
helmet-equipped: each bounded run captures 63 frames over 6.2 simulation seconds
through kneel/sample/stand/walk, retaining equipment and fixed work position.
Evidence is in live-core-review{,-east,-south,-helmet,-helmet-east,-helmet-south}/
under the same output directory. West live work, broader activity joins and the
remaining life, water, death and other action families still require review.
Per-clip ledger rows retain prior evidence; missing evidence is not proof of a
required redraw. No export or whole-library visual acceptance is claimed.

Changed: tools/prepare_veld_helmet_transition_body.py, tools/veld_scanner_revision.py,
tools/rebuild_human_crew_art.py, tests/playtest_human_crew_candidate.gd, Veld selected
frames, source/review records and the animation ledger. The maintained character
workflow and installed mirror now require selected endpoint comparisons and
pivot-aware taller-canvas registration. Bill remains unchanged; Marsh helmet-free.

Native live locker follow-up: the focused Veld airlock test passes 224 travel
samples, equipment pickup/return, pause, power interruption and disk save/restore.
Captured phase traces compare the actual runtime texture bytes with the selected
source. Pickup at 0.321 seconds uses frame 2 with the helmet in her hands and
shelf hidden. This resolves the apparent empty-hand ambiguity in the small room
capture; no runtime animation mapping repair was needed. Evidence:
output/crew-replacement-2026-09-12/veld/helmet-locker-source-trace.log and
helmet-locker-source-trace-native/*-pose.json / *-actor.png / room captures.
These are discrete checkpoint captures; continuous locker motion remains open.

Continuous Veld locker review now captures both actions at 0.05-second steps:
44 pickup captures through 2.15 seconds and 46 removal captures through 2.25
seconds, including all twelve authored slots in each. Fixed-foot and equipment
completion checks pass, and runtime texture bytes match selected sources.
Native phase review found a remaining visual mismatch: the staged shelf helmet
is larger than the fitted held helmet, causing a size jump at pickup/return.
Keep live visual acceptance open until the shelf/held size relationship is fixed.
Evidence: output/crew-replacement-2026-09-12/veld/helmet-locker-continuous.log and
helmet-locker-continuous-native/{continuous-equip.json,continuous-remove.json,
handoff-phases.png,continuous-equip.gif,continuous-remove.gif}. That first run's
summary reused the broad test label; its actual scope is continuous locker motion,
travel and UI. The fixture now reports mode-specific coverage accurately.
Next: reconcile the staged shelf helmet with Veld's fitted held source while
preserving other actors and the shared interaction anchor.

Veld shelf scale correction: AirlockService now derives a 0.6 staged-helmet
scale from the active/reserved Veld locker request, retaining it while she stands
at the interaction point after return. Other servicing actors and Studio retain
the existing default. The shelf base and shared interaction point are unchanged;
no new save field or gameplay timing was introduced. The held shell is roughly
12 room units wide at Veld's existing body scale, matching the 12-by-15 shelf draw.
Changed: scripts/airlock_service.gd, scripts/grid_canvas.gd and
rooms/underwater/airlock-v1/airlock_view.gd.

The repeated native continuous Veld review passes 223 travel samples, both full
helmet actions, fixed-foot registration and UI. Native shelf-handoff-contact.png
was inspected: the previous conspicuous shelf/hand size jump is corrected.
Evidence: output/crew-replacement-2026-09-12/veld/helmet-locker-fitted-shelf.log and
helmet-locker-fitted-shelf-native/ captures. This establishes bounded q0 Veld
locker continuity, not every room rotation or broader animation acceptance.
Next: resume remaining Veld action-family identity corrections and the broader
Branforth/Marsh review/replacement queue. Counts remain 50 corrected Veld variants.

East seating identity study: generated canonical female Veld sit-down, seated
idle and rise sources, registered with one standing-derived anatomical ruler and
exact corrected standing endpoints. Eighteen bare study frames are prepared by
tools/prepare_veld_seated_identity.py under the identity folder's
review/seated-east-body-01/. Registered body contact was inspected. Source 01
had a baked checkerboard and is rejected for extraction; source 02 uses keyed
magenta. Both raws and exact prompts are retained. The source idle has two
authored settling poses with explicit holds, not six independent drawings.
Fitted equipment, furniture contact and native playback remain to be reviewed;
these frames are unselected and the 50-variant correction count is unchanged.

East seated fitted study now contains 18 bare and 18 helmet poses with bounded
collar edits and exact standing/seated/rise joins. Native study checks pass
original timing and all paired source slots; middle-descent native capture was
inspected. Evidence: output/crew-replacement-2026-09-12/veld/seated-identity-study.log
and seated-identity-study-native/page-00-frame-03.png. Added
prepare_veld_seated_helmet.py and seated-identity fixture modes. The fixture now
creates the final mode-specific output directory and checks every screenshot
write; an initial missing-directory run was corrected and rerun successfully.
The study remains unselected pending furniture contact and selected-pack checks.
Current correction count stays 50 variants.

East seated sequence selected: sit-down, seated idle and rise now use corrected
female Veld body art and pose-fitted helmets, adding six variants / 36 frames.
Totals are 29 body clips + 27 equipment variants = 56 corrected variants,
348 frames; 278 other Veld variants remain under identity review. All selected
pixels, original timing and corrected standing/seated joins pass the native
fixture; the selected endpoint phase was inspected. Preservation validation:
670 original frames / 108 manifests unchanged, zero errors or border touches.
Evidence: output/crew-replacement-2026-09-12/veld/seated-identity-{selected,validation}.log
and seated-identity-selected-native/page-00-frame-05.png. Explicit overrides
respect per-slot source offsets: only the embedded standing endpoints need the
smaller crop. Sources, prompts and registration remain preserved.

Current lounge and observation stations request north-facing seated actions;
this east selection does not claim live chair contact. Next: north-facing seated
and reading identity replacements, then continuous furniture review. The full
Veld/Branforth/Marsh goal remains active. Bill unchanged; Marsh helmet-free.

## Veld identity correction study - September 12 checkpoint

Corrected identity sources and reproducible fitting live in
character/veld-identity-correction-v1/ (see its README for files and evidence).
Agent reviewed bare/helmet faces and six paired native east sample phases:
silver-streaked bun, canonical female identity and no glasses. Final native
sample-identity-collar-native.log passes170body/164equipment with zero failures,
including original timing and unchanged pixels outside the head/collar region.
This is an unselected study; selected packs still require identity correction.
Next: correct connected idle/kneel/stand heads and joins before selecting the
sample correction. All334Veld ledger rows remain reopened. The full three-crew
animation goal is unfinished. No export.

## Veld identity correction - owner direction, September 12

Dr. Veld is a woman. Her canonical identity is the original concept at
character/dr-veld-v1/concept-01.png: silver-streaked dark bun, cobalt Science
markings and ivory chest panels. She does not wear glasses, including inside
the fitted helmet. Preserve her face through every direction and action.

Recent generated references drifted from this identity. Prior technical passes
and selected-source matching do not establish identity acceptance. Reopen Veld
body and equipment visual review; do not propagate the recent male-looking or
glasses-bearing source studies. South sample strip01 and fitted heads01 are
unselected and rejected as identity references. Retain their raw files/prompts
as provenance. East sample is installed but requires identity correction along
with affected existing clips. Use the original concept for identity and existing
frames only for motion/registration. Review bare and helmeted faces together.

# Crew action source review

Updated: September 12, 2026 · BrineSpace · Three-crew replacement

## Objective and acceptance

Complete Veld, Branforth and Marsh replacements at the accepted detailed identity,
including action interiors and joins. Manifest coverage is already complete;
remaining visual inconsistencies must be corrected and checked in motion.

## Accepted decisions and constraints

Preserve original sources, timing, registration, character identity and fitted
equipment. Bill is unchanged. Marsh remains without helmet equipment. Reversible
source revisions are authorized; no export is requested.

## Current state

Veld east sample inspection is selected for both body and fitted helmet. Four
authored vial-handling interiors retain the independent opening/closing poses
and original 160/140/180/140/160/180 ms timing. Native selected-source checks
pass for the 170 body / 164 equipped pack; validation reports zero errors,
670 original source frames and 108 manifests unchanged, and no border touches.
Agent reviewed the paired native phase contact and selected lowered-head pose.
Continuous live workplace motion/prop acceptance remains pending.

Implementation: tools/veld_scanner_revision.py explicitly overrides repair-east;
tools/prepare_veld_east_sample.py and tools/prepare_veld_sample_helmet.py rebuild
from preserved sources. tests/playtest_human_crew_candidate.gd checks sample
study/selection independently. Evidence: output/crew-replacement-2026-09-12/veld/
sample-selected-native.log and sample-selected-validation.log. Ledger refreshed.
Next: remaining eleven directional repair/sample clips and live transition review;
daily-life, death, water and other unresolved acceptance remain in scope.


Veld east sample fitted heads01 are authored and composited at34x34 on256px
frames. Helper tools/prepare_veld_sample_helmet.py asserts original pixels in
x>=144 and y>=155 remain unchanged, protecting vial/hand region and lower body.
Bare/equipped source contacts inspected; native timing, visor clearance and
selected-source verification remain pending. No repair override selected yet.


A complete808-clip acceptance inventory now lives in docs/crew-animation-ledger/.
It separates480body clips from328equipment variants and tracks selected hashes,
review status, evidence and next action. Water-related body category totals148;
this is audit scope, not a redraw count. Prior cargo/gait/rest acceptance still
needs row-level reconciliation. See ledger README for exact category counts and
limits. Current art task remains Veld east sample inspection equipment/native review.


Veld east sample strip01 now has four authored vial-handling interiors, registered
with a common99/434 kneeling ruler and original endpoints. Source contact reviewed
for visible hand/head changes. Helper: tools/prepare_veld_east_sample.py; review:
character/crew-action-detail-v2/review/veld-east-sample-01. Fitted equipment, native
transition review and selection remain pending. No repair runtime change yet.


Repair review is now active after the instrument batch. See CREW_REPAIR_ACTION_AUDIT_2026-09-12.md for refreshed selected-frame evidence and actor-specific requirements. Veld east sample inspection is the next authored sequence; no repair replacement selected yet.


All twelve directional instrument actions are selected: Veld scanner, Branforth diagnostic meter, Marsh controller. Branforth north integration completes this batch, with authored fitted helmet interiors for human directions and no Marsh equipment. Latest native selected-source/timing checks pass: 170 body / 164 equipment; validator preserves669original Branforth frames/108manifests,zero borders. Complete-pack refresh passes19,259checks. Evidence: output/crew-replacement-2026-09-12/branforth/meter-north-{selected-build,validator,selected-native}.log and instruments-complete-packs.log. Technical selection and sampled native clip review do not establish live workplace or full animation acceptance. Next: inspect remaining repair/life/water/death interiors and continuous live action transitions; preserve full three-character scope.


Branforth north fitted rear heads01 are composited at38x36, preserving body pixels below y60. Paired native timing/endpoints pass: 170 body / 164 equipment states with zero failures; twelve rendered slots reviewed. Helper: tools/prepare_branforth_north_helmet.py; evidence: output/crew-replacement-2026-09-12/branforth/meter-north-study-native.log and scanner-study-native-north/transition-contact.png. Explicit integration with(36,52) translation and selected-source verification remain next. This remains a study, not selected/runtime acceptance.


Branforth north meter strip01 is authored and registered with four rear action interiors, independent original endpoints and six140ms slots. Source contact reviewed: broad rear silhouette, hidden device, elbow motion and head dip. Helper: tools/prepare_branforth_north_meter.py; raw1983x793, standing ruler148/570, common sole679 and measured two-boot centers. Fitted rear helmet, paired native review and explicit selection remain pending. Existing body/equipment pivot(128,224) requires(36,52) study translation. Broader live/life/repair/water/death review remains unfinished.


Branforth west diagnostic-meter action is selected bare and equipped, including corrected amber-meter endpoints. Native selected-source/timing checks and revised endpoint/outside-edit preservation checks pass with zero failures. Validator:170body/164equipment states,669original frames/108manifests unchanged,zero borders. Evidence: output/crew-replacement-2026-09-12/branforth/meter-west-{selected-build,validator,selected-native}.log. Provenance includes endpoint edit raw plus independent original body/equipment endpoints. Next: north diagnostic action, then broader live/life/repair/water/death review; full three-crew goal remains unfinished.


Branforth west fitted helmet interiors are composited at38x38 with unchanged body pixels below y60. Corrected amber-meter endpoints are used in both variants. Native study passes170body/164equipment with zero failures; twelve rendered slots reviewed. Fixture now compares independent revised endpoints and verifies exact original pixels outside tool region(48,61,22,27), instead of requiring the old pale tool. Evidence: output/crew-replacement-2026-09-12/branforth/meter-west-study-native.log and scanner-study-native-west/transition-contact.png. Explicit integration and selected-source verification remain next.


Branforth west six-frame body study now consumes the corrected amber-meter opening/closing edits through prepare_branforth_meter_endpoints.py. New fitted west helmet head source/prompt01 is saved and visually inspected, including the downturned third pose; extraction/compositing is next. Source dimensions2172x724. Crop only shell/face/neck, exclude generated shoulders/hands, preserve body below collar, use corrected equipped endpoints. Native endpoint checks must compare revised references and separately verify unchanged pixels outside the tool region, not require the old pale tool. Selection remains pending.


Branforth west endpoint prop edits01 now replace the pale tool with an amber meter in both bare/equipped opening and closing poses. Helper tools/prepare_branforth_meter_endpoints.py registers the authored edit to region(48,61,70,88), with exact outside-region pixel preservation checks. Comparison reviewed; outputs in review/branforth-west-meter-endpoints-01. Not yet consumed by the six-frame study or runtime. Next: compose corrected endpoints into the study, fit interior helmets, and update native endpoint expectations to independent revised references while separately asserting preserved outside-region pixels.


Branforth west meter strip01 is authored and registered (four interiors plus independently preserved original endpoints; six140ms slots). Contact review exposed a prop discontinuity: original endpoints hold a pale tool while new interiors use the amber meter. Do not select yet or treat exact endpoint equality as sufficient acceptance. Resolve endpoint prop continuity before helmet authoring/native review. Helper: tools/prepare_branforth_west_meter.py; source/review uses branforth-west-meter and branforth-role-interact-west-strip-01. North and broader actions remain unfinished.


Branforth south diagnostic-meter action is selected bare and with authored fitted helmet heads. Rebuild, validator and native selected-source/timing checks pass:170body/164equipment states,669original frames/108manifests unchanged,zero border errors/failures. Evidence: output/crew-replacement-2026-09-12/branforth/meter-south-{selected-build,validator,selected-native}.log. Explicit override retains256px profile and(36,52) translation. Next: Branforth west/north diagnostic actions; broader live/life/repair/water/death review remains unfinished.


Branforth south meter fitted head study01 uses independently authored38x40 helmet heads, preserving body pixels below y60. Paired native timing/endpoints pass: 170 body / 164 equipment states with zero failures; twelve rendered slots reviewed. Helper: tools/prepare_branforth_south_helmet.py; evidence: output/crew-replacement-2026-09-12/branforth/meter-south-study-native.log and scanner-study-native-south/transition-contact.png. Explicit state integration with(36,52) translation and selected-source verification remain next; north/west and broader action review remain unfinished.


Branforth south diagnostic-meter strip01 is authored and registered: four interiors, independent original endpoints and six140ms slots. Compact amber device and broad bearded identity reviewed in the source contact sheet. Helper: tools/prepare_branforth_south_meter.py; source/reference set uses branforth-south-meter prefix. Existing pack has pivot(128,224); use(36,52) translation when integrating184px study. Fitted helmet, paired native review and selection remain pending; north/west and wider character action review remain in scope.


Veld scanner interaction replacements are selected in all four directions, bare and equipped. North selected-source/timing checks pass: 170 body / 164 equipment states with zero failures; validator preserves 670 original frames / 108 manifests and reports zero border errors. Complete-pack refresh passes19,259checks. Evidence: output/crew-replacement-2026-09-12/veld/scanner-north-{selected-build,validator,selected-native}.log and scanner-directions-complete-packs.log. The explicit north override uses its256px profile with(36,52) translation. This completes directional scanner source selection, not live workplace or full three-crew visual acceptance. Next: Branforth north/south/west diagnostic-meter actions; broader life/repair/water/death review remains.


Veld north scanner fitted rear heads01 are authored and registered at34x30, with original action body below y60 preserved exactly. Paired native study passed170body/164equipment with zero failures; all twelve rendered slots reviewed. Helper: tools/prepare_veld_north_helmet.py; evidence: output/crew-replacement-2026-09-12/veld/scanner-north-study-native.log and scanner-study-native-north/transition-contact.png. Integration and selected-source verification remain pending; use the existing256px profile and(36,52) study translation. Broader Branforth actions and live/life/repair/water/death acceptance remain unfinished.


Veld north scanner strip01 is authored and registered with four distinct rear action interiors, original opening/closing frames, and six140ms slots. Scanner remains occluded; elbow movement and head dip convey interaction. Axial support uses both-boot midpoint. Helper: tools/prepare_veld_north_scanner.py; source/review under character/crew-action-detail-v2. Loaded body/equipment profile confirms pivot(128,224). Fitted rear heads, paired native review and explicit selection remain pending; source contact reviewed only.


Veld west scanner is selected bare and equipped with independently authored fitted head poses. Native study timing/endpoints and twelve rendered-slot review passed; rebuilt selected-source comparisons also pass with zero failures. Validator preserves670 original frames/108 manifests,170body/164equipment states,zero borders. Evidence: output/crew-replacement-2026-09-12/veld/scanner-west-{study-native,selected-build,validator,selected-native}.log. Integration uses256px canvas/pivot(128,224) and explicit(36,52) translation from study. Veld north, remaining Branforth role directions and broad live/life/repair/water/death review remain unfinished.


Veld west fitted head study01 is authored and composited onto the original scanner bodies. Four36x33 head crops include the downward inclination; body pixels below y60 remain identical. Source contact review caught hair pixels behind the shell, corrected by extending the replacement boundary across the bun while retaining the collar. Helper: tools/prepare_veld_west_helmet.py; raw/prompt: veld-west-helmet-heads-01. Paired native study, integration with(36,52) packing translation, and selected-source verification remain pending.


Veld west scanner strip01 is authored and registered: four distinct interiors, independent original endpoints, six140ms slots. Original body/equipment references are saved as veld-west-scanner-{body,equipment}-{opening,closing,working}-01.png. Extractor: tools/prepare_veld_west_scanner.py; contact review: character/crew-action-detail-v2/review/veld-role-interact-west-strip-01/contact.png. Contract confirms256px/pivot(128,224), requiring(36,52) translation from the184px study. Source review completed; fitted side-head authoring, paired native study and selection remain pending. Wider three-crew scope remains unchanged.


Veld south scanner is selected bare and with authored fitted helmet heads. Initial selected-source check caught a pivot mismatch: south uses a 256px canvas/pivot(128,224), so the 184px study requires translation(36,52). Corrected rebuild and native selected comparisons now pass with zero failures. Validator preserves 670 original frames/108 manifests,170 body states/164 equipped,zero borders. Evidence: output/crew-replacement-2026-09-12/veld/scanner-south-registration-{build,validator,native}.log; retain initial failed scanner-south-selected-native.log. Next: Veld north/west and remaining Branforth role actions, plus broader live and action review.


Veld south scanner now has authored fitted helmet heads (34x38) composited onto unchanged action bodies, excluding generated shoulders. All pixels below y60 are checked unchanged. Paired native study passed 170 body/164 equipped coverage with zero failures; twelve rendered bare/equipped slots were inspected. Source: veld-south-helmet-heads-01.png; helper: tools/prepare_veld_south_helmet.py; evidence: output/crew-replacement-2026-09-12/veld/scanner-south-study-native.log and scanner-study-native-south/transition-contact.png. This is still an unselected study: explicit state integration and subsequent selected-source checks remain next.


Veld south equipped strip01 is rejected: the full-body helmet edit compressed body proportions and lost the first raised-hand gesture despite a compact shell. Raw, prompt and rejection record are preserved. Bare south strip remains unselected; next helmet authoring should isolate each head region and retain the corresponding body pixels before paired native review.


Veld south scanner strip01 has four new bare-headed tapping interiors, registered with separate original idle endpoints and original 140 ms slot timing. Source contact review confirms compact scanner and distinct gestures; fitted helmet authoring and paired native review are still pending, so this source is unselected. Sources/prompts and six registered frames are preserved under character/crew-action-detail-v2; extraction is tools/prepare_veld_south_scanner.py. Veld north/west, Branforth remaining role directions and broad life/repair/water/death review remain in scope.


Marsh controller interaction is now selected in all four directions: east strip02 and north/south/west strip01. North preserves rear occlusion and independent idle endpoints; native timing/source checks and six rendered-slot review passed. Validator: 140 states/676 references, no equipment, 211 original frames and one manifest unchanged, zero border errors. Complete-pack refresh: 19,259 checks, zero failures. Evidence: output/crew-replacement-2026-09-12/marsh/controller-north-*.log, controller-complete-packs.log and scanner-study-native-north/transition-contact.png. Changed: directional extraction profiles, explicit instrument override, native direction fixture and regenerated Marsh pack. This completes directional controller source selection, not full live workplace or three-crew visual acceptance. Next: remaining human directional role actions and broader life/repair/water/death motion review.


Marsh west controller strip01 is selected after native timing/endpoint checks, six rendered-slot review and selected-source comparisons (zero failures). Validator: 140 states/676 references, no equipment, 211 original frames and one manifest unchanged, no border errors. The shared south/west extraction retains separate measured standing rulers and sole anchors. Evidence: output/crew-replacement-2026-09-12/marsh/controller-west-*.log and scanner-study-native-west/transition-contact.png. North controller and wider crew action/live-workplace review remain unfinished.


Marsh south controller strip01 is now selected through the explicit interact-south override. Native study timing/endpoints passed and all six rendered slots were inspected; selected-pack native source comparisons then passed (140 body states, no equipment, zero failures). Validator preserves 211 original frames and one manifest, with zero border touches/errors. Evidence: output/crew-replacement-2026-09-12/marsh/controller-south-{study-native,selected-build,validator,selected-native}.log. Changed: south extraction helper, instrument override, directional native fixture and regenerated Marsh pack. North/west controller sequences, live workplace motion and the broader three-crew replacement remain unfinished.


Marsh south controller strip01 now has four separately authored interiors and independently preserved original opening/closing idle frames. Reproducible extraction: tools/prepare_marsh_south_controller.py; six unique frames at the original 150 ms per slot, 148 px standing ruler and pivot (92,172). Registered contact-sheet review shows improved proportions and texture over rejected matrix01. Native motion and selected-pack verification remain; this sequence is not selected. North/west sequences and the wider three-crew action replacement remain outstanding.


Marsh controller matrix01 was rejected after runtime-density comparison: enlarged head and simplified suit shading break continuity with the original idle. Twelve registered review frames and a reproducible comparison are in character/crew-action-detail-v2/review/marsh-controller-matrix-01. No runtime selection changed. Next: author one direction per strip using independent idle and directional pose references, preserve both original endpoints, then review native motion.


Marsh controller north/south/west representative poses are generated and
registered from their own directional identity references. North hides the
controller behind the torso; south exposes its casing and supported hands;
west is separately authored. prepare_marsh_controller_views.py records source
hash/crops and common 148/617 standing scale. Axial support uses the midpoint
between boot extrema: median sole pixels biased toward one boot in initial
review. Revised comparison is saved under review/marsh-controller-directions-01.
These remain unselected pose studies; full sequences and native review remain.

Marsh east controller interaction is now SELECTED from strip02. Native-scale
transition review found its action readable with acceptable continuity; original
style rejection for strip01 remains. The first native study exposed distinct
opening/closing idle frames: the closing original is now saved independently,
and extraction preserves both rather than forcing equality. Corrected study and
selected-source checks pass with zero failures. Validation preserves 211 original
frames/1 manifest, 140 states/676 references, no equipment or border errors.
The shared instrument override targets interact-east only; repair and welding
source aliases remain separate. Evidence: marsh/controller-study-native.log
(initial endpoint failure), controller-study-endpoints-native.log,
controller-selected-build.log and controller-selected-native.log under output.
Broader direction coverage and live-workplace review remain. No export.

Marsh controller sequence study01 is extracted from corrected strip source02,
with four work interiors and exact selected idle endpoints. Source01 is preserved
with a rejection record for oversized head/cartoon shading. Source02 reduces that
drift, but its material treatment is still smoother than the selected idle; keep
identity/style review open before selection. Shared extraction uses Marsh's own
148/544 standing ruler and measured support centers, without equipment output.
Contact/GIF/registration live under review/marsh-role-interact-east-strip-01.
Native playback and the remaining direction/action matrix are still outstanding.

Marsh general interaction now has a representative two-handed drone-controller
study, separate from the old shared work/repair gestures. Source/prompt and
selected east identity are saved under sources/marsh-role-interact-east-*.
The shared standing registration command now supports --actor marsh without
creating helmet equipment. Registered comparison preserves standing scale and
shows the compact controller at waist/chest level. This is an unselected pose;
full direction/action animation and native role playback remain. Preserve repair
and welding as separate state overrides when integrating it.

Branforth east diagnostic interaction is now SELECTED in both bare and fitted
equipment packs through the explicit actor/state override. Native selected-source,
timing and endpoint checks pass: 170 body/164 equipped states, zero failures.
Validation preserves 669 original frames/108 manifests, 1104 body/1056 equipment
references, and zero border errors. Logs are branforth/scanner-selected-build.log
and scanner-selected-native.log under output/crew-replacement-2026-09-12.
Fresh test_crew_complete_packs.gd passes 19,259 checks with zero failures;
complete-packs-role-update.log records this post-selection result. This verifies
pack contracts, not the remaining role/workplace, water/death or full visual scope.
Earlier Branforth study statuses below are superseded. No export was requested.

Branforth east diagnostic strip01 now has four new interiors between exact idle
endpoints, plus six individually fitted helmet poses. The common standing ruler
is 148/566, with measured sole centers; his shell remains 38x40. Shared extraction
and paired native-preview code now accept both humans without sharing their fit
dimensions. Native Branforth study passes all paired timed slots/endpoints:
170 body/164 equipped states, zero failures. The tapping sample was inspected.
Source/prompt, independent equipped endpoint, contacts and registration are saved
under the Branforth role-interact paths. Runtime integration/selected-source
checks remain; Veld's already selected scanner action is unchanged.

Branforth east role-work pass has a new representative diagnostic-meter pose,
saved with exact prompt and selected identity/tool references. Registered source
review preserves his stockier silhouette, beard, orange work panels and standing
height while making the compact amber engineering meter readable. The shared
standing registration helper now accepts --actor branforth; its prior Veld default
and sequence/equipment workflow are retained. Output registration/comparison is
under review/branforth-role-interact-east-01. The command passed. This is an
unselected pose study; full motion, fitted helmet and native checks remain.

Veld east scanner interaction is now SELECTED for bare and fitted equipment.
tools/veld_scanner_revision.py overrides only interact-east after source-path
resolution, preserving unrelated aliases. The equipped idle endpoint is now a
saved independent source, removing the runtime-pack dependency from extraction.
Native scanner-selected mode checks all twelve loaded source frames before any
preview substitution; timing and endpoint checks pass with zero failures.
Validation preserves 670 original frames/108 manifests, 170 body states/1104
references and 164 equipped states/1056 references, with no border errors.
Evidence: veld/scanner-selected-build.log and scanner-selected-native.log under
output/crew-replacement-2026-09-12. Earlier study notes below are superseded by
selection. Broader work actions, other actors and live-workplace review remain.

Veld scanner paired native preview passes: scanner-study mode in the existing
candidate fixture substitutes the six bare and six equipped study frames in
memory, samples every slot at the current interaction durations, and asserts
both selected idle endpoints. Result: 170 body/164 equipped states, zero failures.
The native tapping sample was visually inspected with fitted helmet and scanner
clearance. Evidence: output/crew-replacement-2026-09-12/veld/scanner-study-native.log
and scanner-study-native/page-00-frame-03.png. This is preview evidence, not runtime
selection. Next integrate both variants with explicit state overrides, preserve
independent source/endpoint provenance and run the selected-pack checks.

Veld scanner sequence01 now includes six fitted equipment frames. The existing
east shell is composed at 34x36 against each source crown; the tapping pose uses
a -6-degree tilt. Both equipped endpoints are copied exactly from the selected
interact-east idle. Source contact review shows close head fit and scanner/hand
clearance. Six profiles pass binary-alpha, clear-border and equal endpoint checks.
prepare_veld_scanner_pose.py records per-frame placements in helmet-registration.json
and exports helmet-contact.png beside the bare sequence. Still unselected until
native paired playback is checked; no body or equipment runtime pack changed.

Veld east scanner study now has a registered representative pose and six-frame
sequence (four fresh raise/use/lower interiors with exact selected idle endpoints).
tools/prepare_veld_scanner_pose.py uses one standing crown-to-sole ruler for the
strip and measured sole centers; registration records source hashes and anchors.
Source contact review shows compact scanner use at consistent body height. The
representative profile passes binary-alpha/no-border checks, and sequence idle
endpoints are byte-identical. Outputs: review/veld-role-interact-east-01 and
review/veld-role-interact-east-strip-01, including contact sheets and review GIF.
Still unselected: fitted helmet composition, native playback and final motion
review remain. The GIF uses a review timing default, not a changed runtime contract.

Next role-action pass is underway. tools/review_crew_role_actions.py exports all
24 selected interact/repair direction states across the three actors, with frame
hashes, timing and pivot-normalized contact sheets under review/role-action-inventory.
Veld review finds east interact uses empty-hand gestures while north/south/west
use a cyan-screen scanner. Primary-work attendance uses interact, so east scanner
work is the next concrete target. A representative east-facing scanner pose and
exact prompt are saved as sources/veld-role-interact-east-candidate-01, alongside
the two selected references. Raw review shows clear hand/device contact and the
east identity; density/registration, full motion and fitted equipment remain.
No Veld runtime source has changed yet. The inventory is coverage evidence only.

Reach sequence01 is now SELECTED for Marsh south torch-draw/weld/torch-stow.
The native transition fixture passed all 12 renderer-window samples; contact
sheet review confirms progression into/out of the pose. Active-loop native
coverage remains five distinct poses. Rebuild provenance includes pose04,
transition01, intermediate01 and loop01 sources; deterministic rebuilding also
regenerates the registered endpoint and transitions. tools/marsh_low_welding.py
selects the new branch via REACH_SELECTED. The selected native candidate check
passes all tool references/joins/window checks: 140 states, zero failures.
Source validation: 676 references, 211 original frames/1 manifest unchanged,
zero equipment, border touches or errors. Evidence: reach-selected-build.log,
reach-selected-native.log and reach-transitions-native.log under Marsh output.
Broader actor/state replacement and visual acceptance remain open. Bill and the
other Marsh directions are unchanged; no export. Earlier unselected notes below
are historical studies superseded by this selection.

Complete reach sequence01 is extracted: transition02 draw/reversed stow plus
four active work interiors between exact pose04 endpoints. One crown-to-boot
ruler (60/230), fixed support (260,430) and declared pivot register the strip.
Active tip gaps are 0.16-1.09 world units to the near leaf. Source joins pass.
tools/prepare_marsh_reach_loop.py exports 18 PNGs, contact sheet, review GIF and
registration under review/marsh-low-reach-sequence-01. The opt-in native
--reach-sequence fixture substitutes only the work array, restores it afterward,
and passes five distinct poses with zero paid-construction failures. Evidence:
reach-sequence-native.log and reach-sequence-native/contact-samples.png under
the Marsh output root. Three sampled renders show the torch on the painted leaf.
Full draw/stow renderer motion remains before runtime selection; do not treat
active-loop coverage as transition acceptance. Selected packs remain unchanged.

Transition study 02 replaces only draw4 with a new single-pose intermediate.
Contact-sheet review now shows progressive head lowering into pose04; the prior
head-height reversal is removed. Six reverse pairs and unchanged standing/work
endpoint pixels pass. Its source/prompt and revision02 outputs are preserved;
native transition-motion review is still pending. A four-pose active-work source
is now saved as sources/marsh-low-reach-loop-candidate-01.png with its exact
prompt. Raw review shows a stable deep lean and a short torch sweep. Next extract
that strip using measured supports/anatomical scale, inspect full draw/work/stow
motion and verify every active pose's native contact before selecting it.

Reach transition study 01 now supplies four generated intermediates between
the canonical standing identity and verified reach pose 04. Extraction lives in
tools/prepare_marsh_reach_transition.py with a common head-width scale and
measured support anchors. Six draw frames and exact reverse stow frames, contact
sheet, review GIF and registration are saved under review/marsh-low-reach-transition-01.
Six reverse pairs and both immutable endpoint pixel checks pass. Static review
finds a last-intermediate issue: draw4's upper body is lower than draw5, creating
an upward head change while reach extends. Correct that interior before selection.
The active welding loop remains unauthored for this reach revision. No runtime
pack changed; native contact acceptance remains limited to representative pose04.

Reach study 04 establishes representative native leaf contact. Its padded raw
source is 886x1774; generation shifted the boot line, so registration uses the
measured right sole y1295 at fixed width-derived scale (not whole-body scaling
to fit bounds). Registered tip y232.86 is 0.16 world units short of near-leaf
target y233.21. Native detail visibly places the tip on the painted leaf.
Run the existing preview flags plus --reach-study-04: it passed with zero
construction failures and five selected active poses after texture restoration.
Evidence: reach-study-04-native.log/.png and reach-study-04-native-detail.png
under the Marsh output root; source/prompt and review registration are versioned.
This is a usable representative pose, still unselected as a runtime animation.
Next author its draw/active-loop/stow interiors and joins, preserving the measured
support and compact torch, then verify the complete sequence in motion.

Coordinate-chain correction supersedes earlier gap figures and the claim that
study 02 has sufficient geometric reach. main.get_marsh_position subtracts
0.038 cells; grid_canvas adds 0.038 cells back. Net foot offset is zero, not
14.592 world units. Corrected tip-only leaf gaps are selected loop 22.85-24.01,
study 01 19.45, study 02 12.37 and study 03 10.39 world units. These agree with
the native observation that study 02 remains above the painted leaf. The required
registered tip y is 233.21, beyond the study's current 224-pixel canvas. Future
source reach needs padding and natural posture; do not move the entire actor or
lengthen the nozzle to hide the error. Both audit tools now use the full conversion
and all three study reports were regenerated. The native construction fixture
also asserts that the position adapter and renderer lift cancel. Runtime unchanged.
Native verification passed with zero construction failures and five selected
active poses; evidence: output/crew-replacement-2026-09-12/marsh/reach-coordinate-native.log.

Native study 02 preview is now captured and reviewed. The opt-in
`--marsh-reach-study` fixture substitutes the registered pose only in memory,
asserts the live renderer uses it, saves a screenshot, then restores selected
frames. Run with tests/test_crew_construction.gd -- --marsh --marsh-south
--marsh-motion --marsh-reach-study. Current run reports failures=0 and five
selected active poses after restoration. Evidence under the Marsh output root:
reach-study-02-native.log, reach-study-02-native.png and its detail crop.
Visually the tip reaches the inner threshold strip above the painted front leaf;
this is not full door-leaf contact acceptance despite the geometric edge result.
Resolve the rendered surface/offset difference before expanding or selecting the
sequence. Changed fixture retains its existing UID; runtime packs are unchanged.

Measurement correction supersedes the numeric study gaps below: the old color
centroid included copper handle pixels. The audit and pose registration now use
the lowest eight-connected hot-color component; cyan mask overlays were visually
checked for studies 02/03 and a synthetic handle-versus-tip regression passed.
Corrected leaf gaps: selected six-frame loop 8.26-9.42 world units; study 01
4.85; study 02 -2.22; study 03 -4.21 (negative means beyond the near leaf edge).
Study 02 therefore already has enough geometric reach and is the next candidate
for native contact review and transition authoring. Study 03, generated before
the mask error was identified, is preserved but unnecessary for further reach.
Both remain unselected. Updated tools: audit_marsh_tool_reach.py and
prepare_marsh_reach_pose.py; revision-specific tip-mask-review.png records the
selected pixels and gold target. Registration and selected-loop audit commands
passed. No runtime texture, gameplay behavior or native acceptance changed.

Single-pose reach study 02 is saved and visually reviewed at registered scale.
Its deeper forward lean reduces the leaf gap from study 01's 8.07 to 3.34 world
units. Tip centroid is y192.56 against target y200.13, leaving 7.57 source pixels.
The compact torch and fixed lower-body registration are retained. It remains an
unselected study until contact and transition motion are verified. Exact prompt
and raw source are siblings under sources/marsh-low-reach-pose-candidate-02;
review/marsh-low-reach-pose-02 contains comparison.png and registration.json.
Reproduce with python tools/prepare_marsh_reach_pose.py --revision 02. That command
passed; no runtime pack changed and no native acceptance is claimed. The helper
now accepts explicit revision selection so studies retain separate evidence.

Single-pose reach study 01 has now been inspected at registered scale. The head
and shoulders lean forward more convincingly, but its hot-tip centroid y181.83
remains 18.30 source pixels (8.07 world units) short of leaf target y200.13.
It remains unselected; do not expand it into a complete loop yet. Evidence is
`character/crew-action-detail-v2/review/marsh-low-reach-pose-01/registration.json`
and `comparison.png`. `tools/prepare_marsh_reach_pose.py` now exports the target
and remaining source-pixel reach, with review guides composited after sprites.
The registration command passed and the gold target pixel was verified on disk.
Next revise the representative pose to reach the leaf through body/arm posture,
then prove transitions and native contact. Selected runtime art is unchanged.

Door geometry audit refines the target: the closed south/front leaf begins at
local y187 and its floor track at y182, versus the cell-edge plane y192. Current
tip gaps are 8.26-11.08 to the nearest leaf surface and 3.26-6.08 to the track.
The earlier 13.26-16.08 figure remains correct only for the cell edge; do not use
it as painted-seal contact error. Export authoritative geometry without loading a
game via Godot --headless --path . --script tests/test_crew_construction.gd --
--export-door-targets, then run python tools/audit_marsh_tool_reach.py. Both ran
successfully; door-work-targets.json and south-reach-audit.json preserve results.
This pass changes the measurement pipeline, not selected art or gameplay. Next
target the leaf surface with natural forward reach and inspect full loop contact.

The reach audit is reproducible with tools/audit_marsh_tool_reach.py. Including
the renderer's 14.592-world-unit foot offset, current hot-tip centroids are
13.26-16.08 units short of the door-edge plane. This is geometry evidence, not
pixel-perfect painted-seal acceptance. Candidate low-south 02 is preserved with
its exact prompt and rejection JSON: it mainly lengthens the nozzle, retains the
old body lean and reframes the sheet. It is not selected. Revision 01 remains
active. Next revise forward torso/arm projection with natural anatomy, preserving
the compact tool and legal foot anchor; do not scale or shift the whole body.

South contact anchor audit is now measured: local work point (0,160), with nearby
centerline graph rows only at y144/y160. can_stand(0,176) is false. Thus preferring
y176 cannot move the worker without violating current room clearance. Source
orange-tip measurements put active reach only 1.32-4.15 world units beyond pivot
(x offsets -5.03 to +9.00), before the renderer's existing foot offset. Evidence:
construction-motion/side-2-anchor.json, south-tool-tip-audit.json and
south-anchor-audit.log under output/crew-replacement-2026-09-12/marsh. The audit
fixture passed paid south construction and all five active poses. Preserve this
legal work position; further correction belongs in a naturally forward-reaching
crouch and its registration, not a nearer-node preference or collision exemption.

Marsh south draw/weld/stow now uses a dedicated low crouched source (revision 01),
registered to fixed support baselines rather than the torch tip. The torch extends
below the boots, so the exporter adds one/two pixels of padding while preserving
the pivot and 148-pixel anatomical ruler. Source, exact joins, renderer-window and
native frame checks pass: low-welding-normalized-native.log. Complete-pack PASS:
20260912-140254-headless. Original 211 frames/1 manifest unchanged; zero source
errors/border touches. Selected raw art/prompt, registration and contacts are in
character/crew-action-detail-v2/{sources,review}/marsh-welding-low-south-*.

New tools/marsh_low_welding.py supplies only the three south overrides through
marsh_welding_revision.py; rebuild_marsh_art.py records its source provenance.
The native fixture compares padded profiles in pivot coordinates with explicit
RGBA-zero fill. Initial comparison failures came from transparent-white padding;
GPU and disk PNGs were identical. The charging error was also fixture setup:
recovered Marsh lacked origin and retained prior-case recharge state. Directional
cases now start with a valid core origin and fresh battery, preserving game rules.

The selected low pose passes paid south construction at the original work anchor
(low-welding-south-isolated-contact.log). A nearer-node preference trial passed all
four cases with every active pose observed, but did not visibly close the remaining
floor-to-seal gap; that placement change was removed. No production navigation or
collision change remains. Review: focused/south-low-tool and native
construction-motion/side-2-frame-22.png below the Marsh output root. Next measure
actual work point, eligible graph nodes and projected tool/seal anchors before
further contact changes. Broader role/rest/water/death action work remains open.

Marsh's complete tool sequence now has 12 selected states: draw/weld/stow in all
four views. Draw uses source slots [0,0,1,1,2,2], the active loop [2,2,3,3,4,2], and
stow reverses draw exactly. The torch stays visible during welding instead of
returning to empty-handed idle. Original six-frame 150ms timings remain unchanged.
Each group's tool-sequence.json records derivation; tool-sequence-contact.png
shows all joins. Older five-unique-pose weld checks below describe the prior loop.

Construction allows .52s for each tool handoff, shorter than Marsh's .9s clip.
grid_canvas.gd now normalizes elapsed draw/stow time to the selected clip duration
for Marsh construction only. Native checks cover all 72 selected tool frames,
reverse joins, tool-held loop, separation from repair and early/mid/final renderer
samples in the actual handoff windows. PASS: tool-sequence-window-native.log;
complete-pack PASS: 20260912-134906-headless. Source validation remains zero errors
with 211 frames/1 manifest preserved. Paid native construction recheck is recorded
in tool-sequence-construction-native.log. South projected contact remains unresolved.
Final paid construction recheck PASS: all four directions complete, all three
unique active tool poses observed per direction, zero failures. The early east
draw capture now reaches the visible torch-ready pose within the live window.

Marsh north/south welding revision 01 is selected alongside side revision 02.
The axial sheet keeps anatomical right-hand placement and rear tool occlusion.
The extractor now has explicit view groups/revisions; all 25 earlier side PNG
hashes stayed identical when adding the axial group. Sources, prompts and identity
references are preserved. Changed: marsh_welding_revision.py, rebuild_marsh_art.py,
playtest_human_crew_candidate.gd and selected Marsh exports.

All-direction native review passes 140 body states, zero equipment and zero
failures, including exact revised weld pixels and separation from repair. Source
validation preserves 211 original frames/1 manifest with zero errors/borders.
Complete-pack PASS: 20260912-134023-headless. Evidence: welding-all-native.log,
welding-all-native/ and focused/welding-axial-revised beneath the Marsh output root.

Native paid construction completed all four Marsh directions with zero failures.
Stage captures repeatedly landed on idle, so tests/test_crew_construction.gd now
offers --marsh-motion for consecutive simulation/render samples. Initial captures
show draw-to-weld transition as well as the new active poses; the final check
counts only selected weld pixels, separately from inherited torch-draw.
Final consecutive-frame fixture PASS: welding-construction-motion-final.log,
36 samples per direction, all five unique selected weld poses observed in each,
all four paid builds complete, zero failures. Capture files are in
output/crew-replacement-2026-09-12/marsh/construction-motion/.
Visual inspection of frame 18 in construction-motion for all four directions:
east/west read against their seals; south's torch reads above the low doorway,
so south projected work contact still needs correction despite passing placement.
Torch draw/stow transitions and full continuous visual acceptance also remain.

Marsh east/west welding now has dedicated torch/arm motion from source revision
02, with original six-frame timing and canonical idle joins. The two views use
their own identities. Revision 01 was rejected for an opaque painted checkerboard;
02 is a preserved background-only edit with removable magenta. Exact prompts,
identity references and raw sources live in character/crew-action-detail-v2/sources.
Extraction/contact evidence: review/marsh-welding-sides-02 in that asset family.

Native testing exposed frozen source aliases: repair/interact/eat and other states
reference old weld paths. The new source must be a separate state override, not a
mutation of that shared dictionary. tools/rebuild_marsh_art.py now isolates the
welding overrides; tools/marsh_welding_revision.py owns extraction/selection.
tests/playtest_human_crew_candidate.gd checks exact selected welding pixels and
distinction from repair, as well as existing complete coverage/timing checks.
The corrected native run passes with 140 body states, zero equipment and zero
failures (marsh/welding-isolated-native.log under the output review root). Original
211 frames/1 manifest remain unchanged; source validation has zero errors/borders.
Complete-pack PASS: 20260912-133635-headless. Exported filmstrips and sampled native
poses inspected; continuous motion, construction contact and north/south welding
remain unverified. Portable review: marsh/focused/welding-isolated/review.html.

Marsh now has all four revised carry directions selected. East/west use his own
loaded torso and corrected side-specific walking legs. North/south use each
direction's neutral loaded pickup endpoint, preserving grip and rear occlusion.
All retain four 180ms frames with clip-specific distance cadence. The axial donor
needs wider boot masks (x65..118) than the walking donor; the residual-pixel guard
caught this before selection. Image-space foreshortening is not proof of planting.

West walk/run corrections are also selected with independent measured landmarks
and 1.2 reach calibration. Both source rigs report zero stance drift/sole error.
Changed files: tools/marsh_west_geometry.py, tools/repair_crew_walk.py,
tools/repair_marsh_carry.py, selected Marsh pack and generated review recipes.

Verification: west walk/run/carry and north/south carry each pass 60 native
distance-driven source comparisons. Exported filmstrips and native axial sampled
stills at source/station scale inspected; this is not continuous visual acceptance.
Source validator reports 140 states/676 references, no equipment, no border/error
issues, and 211 original frames/1 manifest unchanged. Final complete-pack PASS:
output/test-runs/20260912-133025-headless. West-only prior PASS: 20260912-132747-headless.
Evidence: marsh/focused/corrected-west-motion and axial-cargo-corrected beneath
output/crew-replacement-2026-09-12; carry-native/north and south contain samples.

Next: inspect continuous cargo motion and pickup/unload joins, then revise Marsh
work/weld/repair and remaining rest/water/death interiors. Both humans' all-direction
cargo, seating and sleeping revisions are selected; broader role/dining/reading,
construction and water/death review remains. No export or full-goal completion.

## Earlier checkpoints (historical, superseded by current state)

Marsh east carry is selected with four alternating phases, original 180ms timings,
his own loaded torso/crate and corrected source legs. A clip-specific stride now
drives cadence. Native testing caught that CrewSpritePlayer previously required
a state-wide stride; it now honors a clip stride independently, preserving time
playback for unrevised Marsh carry directions. Carry and walk each pass 60 native
distance samples after this fix; exported carry filmstrip reviewed. Source
validation passes (211 frames/1 manifest unchanged, no equipment/border errors).
Complete-pack PASS: 20260912-132035-headless. Changed: repair_marsh_carry.py,
rebuild_marsh_art.py, shared exporter, crew_sprite_player.gd, gait native fixture
and Marsh selected pack. Remaining: other carry directions and broader work/rest/
water/death interiors. East carried animation is not evidence for those families.

Marsh corrected east walk/run geometry is now selected. Shared measured landmarks
live in tools/marsh_east_geometry.py; carry studies consume the same rig. A source
reach check initially found stance drift/sole errors, resolved by explicit 1.2
leg-length calibration. Both final rig checks report zero stance drift and sole
error; each native clip passes 60 distance-driven samples. Exported walk/run
filmstrips inspected. Source validator: 140 states/676 references, zero equipment,
211 original frames/1 manifest unchanged, no errors or border touches. Complete-pack
PASS: 20260912-131734-headless. Files: shared geometry, repair_crew_walk.py,
repair_marsh_carry.py and selected Marsh pack. Carry itself remains unselected
pending four-frame cadence integration/verification. Broader action review remains.

Corrected Marsh east walk/run/carry studies now use source-measured hips and limb
polygons. The carry upper body retains pelvis through y110, independent of the
walk torso cut at y103. corrected_rig() in repair_marsh_carry.py centralizes the
study geometry; corrected-walk.png and corrected-run.png were visually inspected
alongside carry contact. Run retains its own travel/lift/timing settings and uses
hip targets y110; recipe/joints preserved. These improve the previously distorted
thighs but remain unselected until the shared runtime rigs, carry stride and
native tests are updated. No runtime assets changed this pass.

Fresh Marsh donor audit contradicts earlier east-walk visual acceptance: the
current selected walk-east filmstrip contains distorted thighs/knees too. The
carry issue therefore is not only a torso composite seam. Measured donor grid
places hips around y104-109, versus the old rig's y116-117. The unselected carry
study now has corrected source limb polygons/hips and an explicit torsoCutY=103;
its legs read more coherently, but loaded waist registration still needs polish.
The shared build function accepts torsoCutY with existing default119 unchanged.
No runtime rebuild/selection occurred. Next finish the corrected east anatomy,
apply it consistently to walk/run/carry, then revalidate native stride/motion.
Evidence: focused/carry-donor-check/walk-east-filmstrip.png and local carry
donors.png, rig-grid.png, contact.png. Do not treat earlier gait checks as visual
proof against this newer directly observed defect.

Marsh action audit covers 20 cargo/weld/repair states in focused/action-audit.
Full east filmstrips show carry repeating the same leading leg; welding also
needs a stronger tool action. New repair_marsh_carry.py is an UNSELECTED four-phase
east study combining his own source walking legs with loaded torso/crate. Contact
reveals broken hip seams, so do not integrate. Next debug donor/hip registration,
retain original four-frame runtime timing, and validate distance cadence once
the anatomy is coherent. No selected Marsh assets changed in this pass.

Both humans now have all four sleeping directions revised and selected. South
uses each actor's own body source and generated fitted equipped source, including
upward face/helmet pitch. Bare scale/anchors drive both exports; shared bare head
anchors retain furniture alignment metadata. All 256 seating/rest joins pass.
Both native south playback checks report 170 body/164 equipped states and zero
failures; exported full filmstrips inspected. Both source validations pass with
original frames/manifests unchanged (Veld 670/108, Branforth 669/108). Complete-pack
PASS: output/test-runs/20260912-130852-headless. Changed: crew_sleeping_revision.py,
rebuild_human_crew_art.py, native fixture, equipped extraction helper, preserved
south sources/prompts and both selected packs. Live berths remain north-facing.
Next objective within this goal: remaining role, dining/reading, construction,
water/death and Marsh action interiors. Complete state inventory alone is not
evidence of visual acceptance for these outstanding families.

Veld south fitted equipped source 01 is preserved with exact prompt, based on her
bare south sheet and the common front helmet design. The generated helmet follows
the upward head tilt while preserving her visible face. New helper
tools/extract_south_sleep_equipment.py uses the bare source's row/column geometry,
scale and sole anchors; it rejects changed sheet dimensions. Bare/equipped contact
was inspected at extraction scale. No runtime selection yet: next integrate Veld
south with exact joins, then produce Branforth's own equipped south source and
validate both. This replaces upright-overlay fitting for the new axial rest study.

Both human south rest source-01 studies are preserved with their own canonical
front identities and exact prompts. Extracted contacts visually inspected: clear
foreshortening, visible soles and upturned faces distinguish supine rest from the
old smaller-standing silhouette. Both use --columns gutter with uniform scale.
They remain unselected pending fitted front equipment through head tilt, exact
transition joins and native review. No runtime changes in this source-study pass.
Files: sources/{actor}-sleeping-south-{identity,candidate}-01.png and candidate
prompts; review/{actor}-sleeping-south-01 extraction/contact/frames.

Both human west rest families are selected. Branforth west uses his own source 01
transition, endpoint breathing chest anchor x174, and a fitted 34x36 west helmet
with measured pose centers/angles. Exported complete transition filmstrip reviewed.
224 rest joins, native playback coverage/timing, source validation and complete-pack
test pass (20260912-125940-headless). Original Branforth 669 frames/108 manifests
remain unchanged; no border touches. Changed: source/identity/prompt, breathing
recipe and configuration, crew_sleeping_revision.py, selected Branforth pack.
Remaining human rest direction is south for both actors; broader role/water/Marsh
action review remains. Native clip review does not change north-facing live berths.

Veld west lie-down/sleep/get-up is now selected from her west-specific source 01
and endpoint breathing rig, with fitted 30x32 west shell and measured per-pose
centers/angles. Side fits are keyed by actor AND direction; shared head-anchor
export uses that same table. Exported full transition filmstrip inspected.
208 rest joins, native timing/coverage and source validation pass; 670 original
frames and 108 manifests remain unchanged. Complete-pack PASS:
output/test-runs/20260912-125650-headless. Files: crew_sleeping_revision.py,
rebuild_human_crew_art.py, playtest_human_crew_candidate.gd and selected Veld pack.
Remaining rest directions: Branforth west and both humans south. Broader role,
water and Marsh action review remains. Live berth activity continues to face north.

Veld west rest source 01 and exact prompt are preserved from her canonical west
identity. Transition contact inspected; her own final pose now drives a six-frame
breathing rig, with chest center x170 in its extracted canvas. The existing
repair_branforth_side_sleep.py now accepts actor/direction with explicit centers;
Branforth's six previously selected breathing PNGs reproduce unchanged. Veld
west exact donor/seam equality and nonzero chest motion pass. It remains unselected
pending west-specific helmet centers/angles, export and native validation. Files:
new source/identity/prompt, west review and local recipe, shared breathing tool.

Branforth east lie-down/sleep/get-up is selected with his own source-01 transition,
endpoint-derived breathing loop and fitted 34x36 helmet. Each pose uses his measured
head center/angle; Veld's geometry is not reused. Side head registration is shared
between bare/equipped variants. Exported filmstrip and native contact inspected.
All 192 rest joins pass, native playback reports 170 body/164 equipped states and
zero failures, source validation preserves 669 frames/108 manifests with zero
errors or border touches. Complete-pack test: 20260912-125234-headless PASS.
Files changed: crew_sleeping_revision.py, rebuild_human_crew_art.py and Branforth
selected pack; breathing recipe/source remain preserved. Both human east and
north sleeping families are revised. West/south sleep and remaining broader
action review are outstanding. Live berths still request north, so this is native
clip acceptance rather than a new live east-room claim.

### Previous milestones and studies

Branforth east now has a source-specific breathing study from candidate 01's own
final lie-down pose, via tools/repair_branforth_side_sleep.py. Six frames retain
the donor's anatomy; at most one dense pixel of localized chest lift keeps head,
boots and lower support edge fixed. Exact first/last donor equality and nonzero
interior motion are asserted; contact inspected. Outputs/recipe live under
review/branforth-sleeping-east-local-01. Still unselected pending fitted equipment
and native integration. Candidate 02 and exact prompt are preserved but unused:
the edit retained the wrong loop proportions and its gutter lies outside the
extractor's central search band. No extractor relaxation was needed for this repair.
Candidate 01's contact has been restored to uncalibrated extraction by the rig.

Branforth east sleeping candidate 01 is preserved with canonical identity and
exact prompt. Extraction uses gutter columns. Its loop row is anatomically
different from the transition endpoint: isotropic length calibration enlarges
head/torso too much. The current contact records that diagnostic calibration;
it is NOT selected. Revise the sleep row from its own final lie-down pose rather
than accepting equal length as sufficient. The runtime berth resolver currently
sets north facing for authored berths (crew_room_activity.gd); live east contact
would be an explicit fixture, not an observed autonomous activity.

Veld east rest revision 06 is now selected for lie-down, sleep and reverse get-up,
with fitted 30x32 side equipment and explicit per-pose rotation/center. Original
source aliases preserve canonical idle and exact rest joins. Side sleep exports
its bare head anchor for furniture alignment. The first validation caught a local
variable overwriting the profile pivot; corrected before final validation.
Final evidence: 176 rest joins, human source/profile validation and native timing
all pass; 670 original frames and 108 manifests remain unchanged. Complete-pack
test passed in output/test-runs/20260912-124630-headless. Native exported renders
were inspected. Live east berth contact is still unverified. Remaining work:
other human sleep directions and broader role/water/Marsh action review.
Changed implementation: crew_sleeping_revision.py, rebuild_human_crew_art.py,
review_veld_side_sleep_helmet.py and playtest_human_crew_candidate.gd, plus Veld pack.

### Earlier source studies (superseded by selection above)

Veld east revision 06 now has a reproducible fitted helmet study:
tools/review_veld_side_sleep_helmet.py writes twelve precomposed poses plus
registration.json and a bare/equipped contact under review/veld-sleeping-east-06-helmet.
The study uses a 30x32 shell with measured per-pose head centers and rotations,
including reclined and supine views; contact was visually inspected. It is still
unselected. Next compare equipped idle joins, refine any collar/face mismatch in
motion, wire the body/equipment revision and side head anchor, then run native checks.

Veld east candidate 06 is ready for fitted-equipment study, not runtime selection.
The targeted edit still shrank its loop row uniformly. Extraction now supports
explicit --match-sleep-scale for side sleeping sheets: one isotropic row factor
matches the final lie-down body's length and is recorded as sleepRowScale.
Use revision 06 with --columns gutter --match-sleep-scale. The resulting contact
was visually reviewed: slender identity and transition/loop body scale now agree.
All ten existing selected rest families retain identical PNG hashes. Next author
per-pose fitted side helmets and head registration, integrate, then verify joins
and native playback. Raw source and exact prompt remain preserved.

Candidate 05 uses only canonical Veld as its generation reference. Its slender
silhouette is closer, but sleep-row figures shrink relative to the lie-down end,
so it remains unselected. Raw art and exact prompt are preserved. Uneven spacing
is handled by opt-in --columns gutter in extract_crew_seating_study.py, requiring
exactly six isolated silhouettes per row and recording the mode in extraction.json.
The current candidate-05 contact uses that mode. All ten selected rest families
re-extract with zero changed PNG frames under the default mode. Next: correct
sleep-row scale against the transition before fitting side helmets; avoid another
whole-sheet redesign that discards the improved slender proportions.

Veld east candidate 04 is preserved with its exact prompt and extracted contact.
Magenta removal works. The generated row baseline crossed the geometric midpoint;
the extractor now finds an empty central gutter before splitting rows and records
rowSplit. Re-extraction of all ten selected rest families changed zero PNG frames.
Candidate 04 remains unselected: its body reads wider and softer than canonical
Veld, and fitted side helmet registration is still pending. Do not use its earlier
fragment-contaminated contact; the current contact was rebuilt with gutter detection.

Candidate 03 for Veld east sleeping is also rejected: its checkerboard is baked
into opaque pixels. Raw source and exact prompt are preserved; its initial review
exports are diagnostic only. The extractor now rejects fully opaque sources after
chroma removal before writing frames. All ten selected seating/sleeping sources
still extract successfully; candidate 03 triggers the expected rejection. No
runtime selection changed. Next source attempt should use flat magenta and retain
the canonical fine-detail identity and consistent standing-to-lying anatomy.

Veld east sleeping source study is preserved but NOT selected. Candidate 01 has
good detail but an overlong flat body; candidate 02 reduces length but softens and
enlarges the face/suit shapes, so it is not a visual improvement suitable for use.
Both raw sources, frozen target/identity and exact prompts are retained. Next:
correct length while retaining candidate 01's detailed identity, then author the
side-facing helmet tilt/registration and integrate coherent lie/sleep/get-up.
The study exposed near-transparent alpha speckles that polluted crop bounds and
sole anchors. The shared rest extractor now applies the export visibility threshold
before geometry measurements. Re-extracting all ten previously selected rest
families changed zero frame files. No selected runtime artwork changed this turn.
Updated source-density skill and mirror. This is source/pipeline progress, not
native acceptance of the new east sleep family.

Branforth north sleeping source 01 is selected with fitted equipment and his own
exported head anchor. Source/contact, selected body/helmet filmstrip and live q0
berth capture were inspected; his head rests on the pillow. Native activity,
alignment easing and timing/coverage checks pass. All 160 selected rest join
comparisons pass. Validator: zero errors/border touches, 669 original frames and
108 manifests unchanged. Complete-pack check:
`output/test-runs/20260912-122538-headless`.
Changed: Branforth north sleeping input/identity/source/prompt and review,
sleeping registry and rebuilt packs. Consolidated the bible's accumulated crew
action notes into current selected coverage, reusable rules and remaining work;
historical details remain here. Next: remaining sleep directions for both humans,
then role/water interiors and Marsh action review. Overall goal remains incomplete.

Veld north sleep head/pillow alignment is corrected. The rebuild exports a bare
prone-head offset in world units, shared by equipment variants. The runtime matches
that metadata to the authored berth pillow transformed through the prop pivot and
scale, easing the adjustment through lie-down/get-up. Frames without metadata keep
their prior placement. Live q0 berth capture was inspected: the head rests on the
pillow. Native checks confirm the target and zero/half/end transition correction.
All 144 rest joins pass; asset validator reports zero errors/border touches and
unchanged original sources. Complete-pack and all 72 room-activity cases passed
at `output/test-runs/20260912-122130-headless`.
Changed: human exporter, crew sprite metadata loader, room activity pillow targets,
crew-life head alignment, grid human render offsets and native berth assertions;
skill source and installed mirror updated. Evidence: sleep-head-native.log,
sleep-head-validation.log and seating-room/berth-q0-north.png under Veld output.
Next: Branforth north sleeping, then remaining sleep directions and role/water/Marsh
action review. This is one corrected live sleeping family, not overall completion.

Veld north sleeping source 01 is selected with fitted equipment: forward kneel,
supported lowering and leg extension replace the seated-looking transition into
prone sleep. Source/contact, body/helmet filmstrip and live berth capture were
inspected. Native timing/coverage and real berth approach/activity passed. All
144 full-channel seating/sleeping join checks pass; validator has zero errors or
border touches and unchanged 670 original frames/108 manifests. Complete-pack:
`output/test-runs/20260912-121708-headless`.
Changed: sleeping source/input/identity/prompt and review; extractor family option,
new `crew_sleeping_revision.py`, rebuild dispatch, sleeping native focus and berth
mode in the existing room fixture; join validator now includes sleeping families.
Remaining: live prone head sits below the pillow. Resolve source/furniture head
registration before calling this sleeping family complete or expanding it. The
capture is `veld/seating-room/berth-q0-north.png`, with a preserved before image.
Other sleeping directions/Branforth, role/water and Marsh action review remain.

Human seating milestone: Veld and Branforth now have all four sit-down, seated-idle
and reverse-rise directions selected with fitted equipment. Both west source 01
contacts and selected body/equipment filmstrips were inspected; native timing and
coverage passed for each actor. Full-channel join validation passes all 128 checks
across eight actor/direction families. Both asset validators report zero errors and
border touches, retaining original Veld 670/108 and Branforth 669/108 frame/manifest
counts unchanged. Complete-pack check: `output/test-runs/20260912-121238-headless`.
Changed: both west seating input/identity/source/prompt and review artifacts,
selection registry and rebuilt packs. Existing live lounge evidence covers north;
the remaining views are library/native sprite review. Next: sleeping transitions
and sleep loops, starting with the north-facing berth use; then remaining role,
water and Marsh action review. Seating completion does not close the overall goal.

Both humans' south seating source 01 revisions are now selected with fitted front
equipment. Seating selection covers east/north/south for each human; west remains.
Both raw-source contacts and selected body/equipment filmstrips were inspected.
Native timing/coverage passed for both actors. Full-channel seating join validator
passes 96 comparisons across six selected actor/direction families. Both asset
validators report zero errors/border touches and unchanged original sources
(Veld 670 frames/108 manifests; Branforth 669/108). Complete-pack check passed at
`output/test-runs/20260912-120838-headless`.
Changed: both south seating source/input/identity/prompt and review artifacts,
selection registry, rebuilt packs and native preview's shared four-direction
seating selector. Existing north lounge evidence is unchanged; south evidence is
sprite/timing review. Next: west seating for both, then sleeping and the remaining
role/water/Marsh action matrix. Original goal remains incomplete.

Branforth east seating source 01 is selected with fitted equipment, joining both
humans' east/north seating revisions. Source/contact and selected body/equipment
filmstrip were inspected; native timing/coverage passed with zero failures.
Validator: zero errors/border touches, 669 original frames/108 manifests unchanged.
Complete-pack check: `output/test-runs/20260912-120401-headless`.
New `tools/validate_crew_seating_joins.py` compares all RGBA channels in pivot
coordinates, clearing invisible RGB. All 64 standing/seated/reverse checks pass
across the four selected actor/direction families. This strengthens earlier manual
checks whose RGBA bounding-box comparison could overlook color-only differences.
Changed: Branforth east seating source/input/identity/prompt, review, selected
registry and rebuilt packs; shared validator and pipeline lesson with mirror.
Next: both humans' south/west seating, then sleeping and remaining role/water/Marsh
action review. Live lounge evidence remains north-specific.

Branforth north seating source 01 is selected with fitted equipment. This completes
both humans' currently used north-facing lounge seating revisions. Source/contact,
selected body/helmet filmstrip and live q0 lounge capture were inspected; Branforth
sits centered using the shared authored chair anchor. Native timing/coverage and
live activity checks passed with zero failures. Seated joins and reverse rise are
pixel-exact for body and helmet. Validator: zero errors/border touches, 669 original
frames/108 manifests unchanged. Complete-pack check passed at
`output/test-runs/20260912-120046-headless`.
Changed: Branforth north seating source/input/identity/prompt, extraction/review,
seating selection registry, rebuilt packs and actor-selectable native room fixture.
Use `tests/playtest_crew_seating_room.gd -- branforth` (or `veld`) on a real display.
Remaining seating: Veld south/west and Branforth east/south/west; then sleeping,
role/water families and Marsh action review. No full-matrix visual acceptance yet.

Veld north seating source 01 is selected alongside east, with fitted equipment.
The north source/contact was inspected and native timing/coverage passed. Validator
reports zero errors/border touches and unchanged 670 legacy frames/108 manifests;
complete-pack check passed at `output/test-runs/20260912-115545-headless`.
New `tests/playtest_crew_seating_room.gd` exercises the real lounge approach,
activity transition and selected grid renderer. Live lounge seating faces north,
not east; the fixture confirms this without forcing an alternate facing.
Before/after source captures exposed a pre-existing leftward chair-anchor offset.
`scripts/crew_room_activity.gd` now derives the left chair center from its authored
source registration (x=774.5, pivot=900, width=373) instead of a fixed 8-unit inset.
Aligned native capture was inspected: Veld is centered on the chair. Room activity
regression passed all 72 cases at `output/test-runs/20260912-115716-headless`.
Evidence: `veld/seating-room/` and seating-room-aligned.log under the replacement
output folder. Changed sources/prompts, seating registry, selected packs, native
fixture with UID, and shared room anchor. Next: remaining human seating directions,
Branforth north first for live use, then sleep/role/water and Marsh action review.
East remains library-verified; lounge contact evidence specifically covers north.

Veld east seating source 01 is selected for sit-down, seated idle and reverse rise,
including fitted equipment. The two-row source preserves detailed identity across
all interiors and uses one standing-reference scale. Native timing/coverage checks
passed with zero failures; source contact, full selected filmstrip and native poses
were inspected. Both body/equipment seated joins are exact and rise exactly reverses
sit-down. Validator: zero errors/border touches, 670 original frames/108 manifests
unchanged. Complete-pack check: `output/test-runs/20260912-115126-headless`.
Changed: preserved seating input/identity/source/prompt and review, new
`tools/extract_crew_seating_study.py` and `tools/crew_seating_revision.py`, human
rebuild dispatch, native seating focus and selected Veld packs. Furniture contact
still requires an in-room check; do that before expanding seating directions.
The existing preview_crew_life fixture explicitly loads old v1 packs, so its sheets
cannot establish acceptance of the selected revisions. Broader sleep, role, water
and Marsh action review remain open.

Both humans' four cargo directions are now selected with fitted equipment.
Branforth north source 01 preserves matched 146px standing endpoints; carry uses
the held endpoint with rear axial phase ordering and a 72px projected stride.
Source/contact and native rendered poses were inspected. Native timing/coverage
and 60 distance samples passed with zero failures; body and helmet unloading are
exact pixel reversals of pickup. Validator: zero errors/border touches, 669
original frames and 108 manifests unchanged. Complete-pack check passed at
`output/test-runs/20260912-114636-headless`.
Changed: Branforth north source/reference/prompt, extraction/carry review, selected
cargo registry and rebuilt body/equipment packs. Updated the shared pipeline
guidance for rear crate occlusion and endpoint reuse, including installed mirror.
Next: detailed human seated/rest interiors, then remaining role/water families
and Marsh action review. Native cargo evidence does not close those families.

### Earlier milestones (historical evidence)

Veld north cargo is selected, completing her four cargo directions with fitted
equipment. Rear source 01 measures 148/149px at its standing endpoints. The carry
cycle retains the pickup endpoint's upper body and crate, using the shared axial
rig with rear phase ordering and a 72px projected stride. The native cargo render
was inspected; full timing/coverage and 60 distance samples passed with zero
failures. Validator: zero errors/border touches, 670 original frames and 108
manifests unchanged. Complete-pack check passed at
`output/test-runs/20260912-114331-headless`.
Changed: north source/reference/prompt and review artifacts, cargo registry,
axial carry builder and native fixture direction support. Next: Branforth north
cargo, then role, seated/rest and water action review. No export.

Front-cargo milestone: Branforth south is now selected with his 40x44 front helmet,
matching 146px standing source endpoints, projected carry and reverse unloading.
Native review passed 60 vertical distance samples and full timing/coverage checks;
the focused render was inspected. Body and helmet unload pixels exactly reverse
pickup. Validator: zero errors/border touches, 669 legacy frames/108 manifests
unchanged. Complete-pack check: `output/test-runs/20260912-113622-headless`.
Both humans now have revised east/west/south cargo. Next is north cargo, then the
remaining role, seated/rest and water action review. Sources/prompts and portable
reviews are retained in crew-action-detail-v2; no export.

Veld south cargo is selected with front-facing fitted equipment and a 72px
projected carry stride. Native review passed 60 distance samples along the vertical
axis, full manifest timing/coverage checks and focused cargo render review.
Marsh's south walk/run masks also received six previously stationary boot-edge
pixels. Both changed clips passed 60 native comparisons each; updated renders were
inspected. A shared axial build guard now rejects leftover lower-body pixels.
Both validators report zero errors/border touches and unchanged legacy sources.
Complete-pack check passed at `output/test-runs/20260912-113234-headless`.
Remaining: Branforth south, both north cargo sets, and wider action-source review.

Veld front-cargo candidate: south pickup source 01 and exact prompt are preserved.
Extraction calibrates from the last standing pose and registers exposed outer boot
edges rather than the crate lip; standing crown/boot measurements are 150/148px.
`repair_front_cargo.py` reuses the pickup endpoint directly for a projected carry
cycle, retaining identical upper body/crate/grip. Expanded lower-leg masks remove
stationary sole remnants, and a build guard rejects uncovered lower-body pixels.
The revised contact sheet was inspected; projected sole error is zero. This is
image-space registration only. South equipment and native/runtime checks remain
pending; also audit earlier axial rigs for the same leftover-pixel hazard.

Side-cargo milestone: both humans' east/west pickup/carry/unload are now selected
with per-character, per-view fitted equipment. Branforth west has its own thicker
limb/boot masks and a 64px carry stride. Native review passed 60 distance samples
plus full manifest timing/coverage checks; pickup filmstrip and native cargo render
were inspected. Asset validator: zero errors/border touches, 669 original frames
and 108 manifests unchanged. Complete-pack check passed at
`output/test-runs/20260912-112510-headless`. New sources/prompts, extraction,
rig records and rendered evidence are retained in crew-action-detail-v2 and the
Branforth cargo-west output folder. The bible's accumulated cargo study notes
were consolidated into current direction; detailed history remains in this handoff.
Next: north/south cargo and the remaining seated/rest, role and water review.

Veld west pickup/carry/unload are now selected with west-facing fitted helmets.
The carry rig uses the donor's kneepad as its near-knee pivot and keeps hips at
the torso attachment. Its 64px cycle stride is installed through an explicit
actor/direction selection registry; caches also distinguish directions.
Native cargo review now checks 60 distance-selected samples against the rig stride,
in addition to manifest timing/coverage and focused render sheets. All checks pass;
pickup/equipment filmstrip and native cargo capture were inspected.
Veld validator reports zero errors/border touches and all original sources unchanged.
Complete-pack check: `output/test-runs/20260912-112034-headless`.
Next: Branforth west cargo, then north/south cargo and remaining action families.

Veld west follow-up remains a candidate: detailed pickup source 01, extracted
150/149px standing endpoints, and a dedicated west carry donor are preserved.
The shared extractor supports west boot anchoring without mirroring. The carry
tool supports west source masks; its current 64-source-pixel stride passes stance
checks after restoring hip attachment height. Review knee/hip seams more closely,
then fit equipment and bind the west cargo states. No west runtime selection yet.

Branforth east cargo is now selected alongside Veld. His dedicated single-pose
donor drives an actor-specific local carry rig, with original 140ms cadence and
76-source-pixel stride. Pickup reverses for unload and helmets use his 38x40 fit.
The shared cargo cache is keyed by actor. Veld's six selected carry frames remain
pixel-identical after generalizing the tools.

Branforth validator: zero errors/border touches, 669 original frames and 108
manifests unchanged. Native timing/coverage checks pass for 170 body/164 equipment
states; focused cargo sheets and the pickup filmstrip were inspected. Complete-pack
checks pass at `output/test-runs/20260912-111321-headless`. Changed tools are
repair_veld_carry.py, veld_cargo_revision.py and rebuild_human_crew_art.py, with
new Branforth frames and review evidence. Remaining west/north/south cargo and
other action-source inconsistencies still require correction; no export.

Branforth east pickup source 01 now has a reviewed six-pose extraction with matched
147px standing endpoints. A separate single carry-stride donor is preserved for
local rigging. Both source prompts are alongside the PNGs in crew-action-detail-v2.
No Branforth runtime promotion yet. `extract_veld_cargo_study.py` now accepts
`--actor veld|branforth` and derives the anatomical ruler from each frozen idle.
The unchanged Veld default reproduces all six selected pickup frames exactly.

Veld east pickup/carry/unload are now selected together. `veld_cargo_revision.py`
rebuilds the corrected pickup source and source-specific carry rig, reverses pickup
for unload, and fits helmets to each dense crown. Carry retains its original
140ms cadence and uses the rig's 76-source-pixel stride; it does not inherit the
walk rig's unequal timings. The source paths are resolved before legacy alias
packing, so the frozen pickup-to-unload mapping still reaches the new pixels.

Verification: Veld validator reports zero errors/border touches and 670 unchanged
original source frames/108 manifests. Native candidate checks pass for all 170
body/164 equipped states, with focused 12-sheet cargo rendering inspected.
Complete-pack checks pass at `output/test-runs/20260912-110633-headless`; fitted
locker join/reversal checks pass. No export. Continue remaining cargo directions,
Branforth cargo, seated/rest source inconsistencies and the wider action review.

`tools/review_crew_action_joins.py` compares selected frames in foot-pivot coordinates
and produces paired images plus a descriptive difference report. It does not turn
pixel differences into automatic art failures. Evidence is under each actor's
`output/crew-replacement-2026-09-12/<actor>/action-joins` folder.

`tools/review_human_crew_art.py` now supports `--review-name`, records selection.json,
reports unmatched state patterns, and labels filtered reviews accurately. Use
`repair-*` for role work: a `work-*` filter silently omitted those states before.
Marsh's preserved action filmstrips are in `focused/everyday-actions`.

## Verification

Join reports cover 56 human joins each and 28 Marsh joins. Forty joins per human
and 24 Marsh joins are pixel-identical. Marsh's four sleep/get-up differences
compare two authored prone poses; the inspected east pair retains its silhouette.
Marsh east pickup, sit, lie and get-up filmstrips were inspected.

Both human east paired sheets reveal a clear body/style change between detailed
standing idle and cargo-source standing poses. Interior seated/rest poses also
look softer. This is a visual defect despite complete source-density coverage.
No character art was changed in this milestone, so previous native pack checks
remain scoped to the previous revision. No new full native acceptance is claimed.

## Earlier source studies (historical)

Veld east source study is now preserved in `character/crew-action-detail-v2` with
two raw generated edits and exact prompts. Candidate 01's opaque checkerboard was
replaced with chroma in candidate 02. Deterministic extraction and the side-by-side
idle comparison show finer detail, but a uniform scale exposes final-pose height
drift (156px versus 145px). Neither source is selected. Correct that source drift
before carry/unload/equipment integration. Extraction recipe and evidence live in
`tools/extract_veld_cargo_study.py` and the revision's review folder.

Follow-up: candidate 03 corrects both standing endpoints to 145px at one scale;
all six extracted poses were inspected. The extractor now exposes explicit
`--revision 02|03`. Carry's original repeated-leading-leg defect was confirmed.
A local combination with detailed walk legs leaves a visible hip seam and is
rejected, with its exact crop/rig recipe preserved in the source revision README.
Runtime remains unchanged until the cargo sequence and equipment are coherent.

Carry follow-up: generated carry candidate 01 preserves the new identity but
repeats near-leg ordering. `tools/repair_veld_carry.py` uses its first frame and
source-specific limb masks to produce six alternating poses. The contact sheet
was inspected; both legs report zero stance drift/sole error. Portable paired
pickup/carry motion review is in `character/crew-action-detail-v2/review/veld-carry-east-local-02`.
This improves the failed mixed-source splice while retaining the donor's own hip
anatomy. No runtime promotion or native acceptance yet. Next: inspect the timed
join, compose fitted equipment, then bind pickup/carry/reverse unload together.

Correct the human cargo source sequences against their detailed idle identity,
starting with Veld east pickup/carry/unload. Preserve crate contact and inspect all
interior poses; replacing only the endpoints hides the mismatch. Then review the
other directions and human seated/rest sources. Continue Marsh role/carry/water
and the wider action matrix. Gait work is recorded in CREW_GAIT_REPAIR_2026-09-12.md.

## Axial video source review - September 12

Preserved south and north motion sources, each 97 frames at 24 fps and 1248x1664, with exact prompts, references and completed job provenance. South phase review suggests cycle 24-48 and slots 24/29/32/36/41/44; registration and fitted equipment remain pending. North motion alternates feet but generated bare hands, violating suit glove continuity; rejected for selection and retained as motion reference. Review contact sheets are in character/veld-identity-correction-v1/review/walk-{south,north}-video-phases-01. No selected rows closed. Front/rear stride remains the existing 0.12-cell baseline pending cadence and projected contact review.

## South selected gait and north glove correction - September 12

South body/helmet selected from frames 24/29/32/36/41/44 with fixed scale, original six durations and shared 0.12-cell stride. Selected native test: 60 samples, zero failures; validator: zero errors/border touches and original 670 frames/108 manifests unchanged. Both live lab runs passed with 53 captures through south-to-east walking; paired room contact sheets reviewed. An initial exact-boundary test mismatch was traced to Vector2 precision (phase 1.19999997317791 versus scalar expectation 1.2); the test now derives expected distance from the actual supplied position. Production playback was unchanged. Logs: south-video-walk-*.log in output/crew-replacement-2026-09-12/veld. North source 02 completed and preserved, 97 frames at 24 fps, with black suit gloves restored; extraction and equipment review pending. Fourteen rejected walk variants remain.

## North selected gait and Veld directional milestone - September 12

North body/helmet selected from corrected video 02, frames 26/31/34/38/43/46, fixed scale and shared 0.12-cell stride. Native selected-frame/cadence test: 60 samples, zero failures. Validator: zero errors/border touches, 670 original frames and 108 manifests unchanged. Bare live run retained two 2-frame direction adjustments then captured 61 frames into north kneel; passed. Helmet run timed out after partial captures; process termination verified before retry. Matching shared art harness automatic-processing/input isolation after startup produced a passing isolated helmet run with the same 2/2/61 episode pattern; room contacts reviewed. The timeout cause is not proven by retry success. Logs north-video-walk-*.log under output/crew-replacement-2026-09-12/veld preserve failed and passing evidence. All eight Veld walk variants are now whole-body-gait-selected-live-walk-reviewed; twelve rejected variants remain for Branforth and Marsh. Broader transitions and owner acceptance remain open.

## Branforth east motion candidate - September 12

Branforth east motion source is preserved and a six-pose whole-body candidate extracted in character/branforth-motion-polish-v1 (cycle 26-50). Standing-derived registration preserves his build; stride, fitted helmet and native selection checks remain pending. His older west meter reference lacks the canonical forehead goggles and needs identity correction before motion generation. No Branforth variant has been reclassified as selected. Source video: 97 frames, 24 fps, 1248x1664. Exact prompt, canonical reference audit, crop/hash and completed generation provenance are preserved. Extracted slots 26/31/34/38/43/46 at fixed scale 147/1216; all six frames passed clipping checks. tools/extract_crew_motion_cycle.py takes an explicit JSON recipe, validates source dimensions/fps, rejects clipped registration and preserves raw sampled frames and source/recipe hashes. Raw temporal and six-frame contact sheets reviewed; no native or owner acceptance claimed.

## Branforth east helmet and contact candidate - September 12

Branforth east candidate now includes an authored character-specific fitted helmet head and six registered equipment poses. Body pixels below the collar are unchanged. Manual heel readings propose a 106-dense-pixel stride, with approximately two pixels of reading uncertainty; native movement and selection checks remain next. The generic shell overlay has not been used for this candidate. Exact helmet prompt and raw source preserved in character/branforth-motion-polish-v1/sources. Paired contact and sole-landmark sheets inspected; 36-pixel-high helmet source registered with per-pose anchors and protected collar/body boundary. All six preservation assertions passed. No selected clip status changes or broad motion acceptance claimed.

## Branforth east selection - September 12

Branforth east body and fitted helmet are now selected at stride 106 dense pixels with original six-slot timing. Native selected-frame/cadence checks passed for 60 samples; validator found zero errors/border touches and preserved 669 original frames plus 108 source manifests. Source and station-scale screenshot reviewed. Live station travel and transitions remain pending; his older live fixture needs startup waiting and scripted-art isolation before use. The west reference still requires its recorded identity correction. Evidence: output/crew-replacement-2026-09-12/branforth/east-video-walk-selected-native.log and east-video-walk-validation.log. Per-clip ledger rows are whole-body-gait-selected-live-context-pending; ten rejected walk variants remain.

## Branforth east live review and west reference - September 12

Branforth east body and fitted helmet now have live travel review: both isolated maintenance-bay fixtures passed all original eight state-coverage requirements and captured 32 samples through east walk into north kneel. Expanded room crops retain the full head/helmet near the north boundary; both contact sheets reviewed. Broader starts/stops, turns and owner acceptance remain open. The new west-standing-identity-02.png restores his canonical goggles/moustache and corrects the near-side tool grouping; it is ready as a motion reference, not a selected animation. The fixture now waits for startup, registers living crew and clear spawn nodes, isolates manual simulation/input, advances a single visual/NPC clock, and retains short episodes. Initial room-bound crops clipped the head; expanded 611x611 crops passed visual review. Failed visual crop evidence is retained separately. Logs: east-video-walk-live-{bare,helmet}-padded.log under output/crew-replacement-2026-09-12/branforth. The west reference raw iterations and exact prompts are preserved. Ten rejected walk variants remain.

## Branforth west whole-body walk checkpoint

Replace the owner-rejected torso/leg cutout gait while preserving the mature stocky chief engineer, gray horseshoe moustache, forehead goggles, charcoal/ochre suit, full gloves and asymmetric tool belt. Bill remains outside this replacement; Marsh remains helmet-free.

East and west body/helmet walks are selected and have bounded native/live review. East uses source cycle 26–50 and stride 106 dense pixels. West uses cycle 34–68, slots 34/40/45/51/57/62 and stride 117. Both retain six-slot durations 170/130/150/170/130/150 ms, fixed anatomical scale and common foot registration. Exact prompts, references, completed videos and job records remain in sources/. Directional cycle recipes feed tools/extract_crew_motion_cycle.py; tools/prepare_branforth_video_helmet.py fits independently authored east/west heads. The shared replacement hook and rebuild set the selected frames and strides.

Checks: west selected native playback passed 60 samples; east passed 60 regression samples after the helper became directional. The asset validator reports zero errors and border touches, with 669 original frames and 108 source manifests unchanged. Ledger refresh showed changes only to the two west walk variants. Bare and helmet west maintenance-bay fixtures each passed all eight original state requirements and captured 47 samples through west walk into north kneel. East previously captured 32 samples. Expanded contact sheets retain full head/helmet near room walls. Manual west sole readings have approximately two pixels uncertainty; boundary residuals do not certify continuous foot locking.

Evidence: output/crew-replacement-2026-09-12/branforth/west-video-walk-validation.log, west-video-walk-selected-native.log, east-video-walk-direction-regression.log and west-video-walk-live-{bare,helmet}-padded.log. Source/candidate contacts are under character/branforth-motion-polish-v1/review/. Live media and traces are under live-walk-review[-helmet]-west-padded/ in the output directory.

Reference decisions: older west meter art drifted from canonical hair/goggles. west-standing-identity-01 restored identity but grouped the meter on the wrench side; 02 corrected that and supplied the selected west motion. Independently authored helmet heads preserve the matching face and compact shell.

Remaining: Branforth north/south body and helmet walks (four variants), Marsh four walks, broader starts/stops/turns, other animation/identity/seated polish and owner acceptance. Current gait checkpoint is 12 of 20 variants with bounded native/live review. The clip ledger governs current evidence status; a passing fixture does not accept every covered animation visually.

## Branforth four-direction whole-body walk milestone

Objective: replace rejected crew gait construction and continue broader animation, identity, workflow and bible polish. Bill remains outside this replacement; Veld is a woman without glasses; Marsh remains helmet-free.

All eight Branforth body/helmet walk variants are selected from preserved independent directional video sources. They retain six-slot timing (170/130/150/170/130/150 ms), fixed anatomical scale and common foot registration. Canonical mature stocky identity, gray moustache, forehead goggles, charcoal/ochre suit, full gloves and asymmetric tool belt remain the reference. Matching directional helmet heads are authored sources fitted to each moving pose, preserving body pixels below the collar.

| Direction | Source cycle | Selected indices | Stride | Live samples per variant |
|---|---|---|---|---|
| East | 26–50 | 26/31/34/38/43/46 | 106 dense pixels | 32 into north kneel |
| West | 34–68 | 34/40/45/51/57/62 | 117 dense pixels | 47 into north kneel |
| North | 26–52 | 26/31/35/39/44/48 | 0.128 cells | 58 continuous into west walk; three additional two-sample episodes |
| South | 26–50 | 26/31/34/38/43/46 | 0.128 cells | 11 into east kneel |

Checks: each direction passed 60 selected distance-driven native samples. Latest validator: zero errors/border touches, 669 original frames and 108 source manifests unchanged. Latest ledger refresh changed only the four north/south variants; the earlier west rebuild changed only its two variants. All eight bare/helmet live fixtures passed the original eight state-coverage requirements. Paired source, source-density/station-scale and live contact sheets reviewed. This is bounded gait evidence, not owner acceptance or visual acceptance of all actions covered by a fixture. North starts near the foreground room boundary; the full continuous trace retains that occlusion context.

Changed pipeline files: tools/extract_crew_motion_cycle.py, prepare_branforth_video_helmet.py, veld_scanner_revision.py, rebuild_human_crew_art.py, review_crew_live_walk.py; native fixtures tests/playtest_crew_walk.gd and playtest_branforth.gd. Four cycle recipes, exact source prompts/videos/job records, fitted heads and review media are preserved in character/branforth-motion-polish-v1. Current status, visual bible, clip ledger and the maintained/installed source-density skill reference are updated. Preview: review/all-direction-walks.gif is an in-place source preview; it does not show world contact.

Evidence: output/crew-replacement-2026-09-12/branforth/{north,south}-video-walk-selected-native.log, axial-video-walk-validation.log and {north,south}-video-walk-live-{bare,helmet}-padded.log. Earlier east/west logs remain in the same directory. Live raw frames, traces, GIFs and contact sheets are under live-walk-review[-helmet]-DIRECTION-padded/. The preview helper chooses the longest continuous episode and records its original indices without discarding the shorter episodes.

Limits: manual side-view sole readings have approximately two-pixel uncertainty; slot-boundary residuals do not establish continuous foot locking. Front/rear feet are foreshortened, so 0.128-cell cadence follows the mean of the calibrated side strides and was checked natively. Generated directions have different source periods; their indices must be chosen independently. Older west standing source 01 grouped tools incorrectly; corrected 02 supplies the selected west motion.

Next: Marsh's four walk directions, broader starts/stops/turns, transitions into older action art, other animation/identity/seated polish and owner acceptance. The current walk milestone is 16 of 20 variants with bounded native/live review. The overall goal remains open; the clip ledger governs per-variant evidence status.

## Branforth west anatomical-side and timing correction verified

Reference 03/video 02 replace the near-side wrench with the canonical anatomical-left meter. Cycle 26-44 selects 26/30/34/38/40/42 at stride 108 and durations 130/170/150/200/150/100 ms. Native 60-sample checks, 47-sample bare/equipped live runs, original-source validation and all 19,259 complete-pack checks pass. Float/int equality and export-format hash churn were diagnosed; consistent float export and east/north/south regression checks passed. The consolidated Branforth handoff records source versions, evidence and limitations.
