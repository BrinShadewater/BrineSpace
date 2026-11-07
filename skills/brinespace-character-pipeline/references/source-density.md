# Source density, local repair, and complete replacement



For multi-character migrations, `tools/inventory_crew_art.py` freezes actual native

loader pixels and metadata; `tools/map_crew_art_sources.py` matches preserved source

pixels and retains identical alternatives. Never overwrite a migration baseline

after switching bindings. Loaded equipment need not mean playable coverage: Marsh

retains legacy helmet rows despite his android no-helmet contract.



If content matching fails, reproduce source-to-target pivot offsets and canvas

composition before declaring source art missing. Ten Branforth north-swim endpoints

match only after clipping into the runtime's 128px join canvas. Record that baseline

defect and expand the rebuilt profile while preserving world registration; do not

preserve lost edges as a requirement of a complete replacement.



Reproducible project example: `tools/rebuild_bill_art.py`,

`tools/validate_bill_art.py`, and `docs/BILL_FULL_REPLACEMENT_2026-09-12.md`.

`tests/test_bill_complete_pack.gd` verifies the active consumer; native review is

separate. Isolate fixture settings before instantiating the game, explicitly select

windowed capture dimensions, and sample changed poses from authored durations.

Idle breathing may intentionally repeat adjacent frames; an arbitrary delay is

not evidence that animation is broken.



When existing sprites look coarse beside room art, compare source pixels per world

unit before changing the drawing style. `standingHeight` is the anatomical source

calibration, not the canvas height or an instruction to resize every pose. A 148px

standing figure at 65.28 world units supplies twice the source detail of a 74px one

at the same world size. A hard-coded denominator controls rendering scale; it does

not by itself downsample images.



Re-extract from the preserved higher-resolution sources. Enlarging final frames

adds no detail. First reproduce the shipped baseline from the source/crop/scale

rules, then increase density while preserving identity, the existing palette,

timing, pose order, and anatomical anchors. Scale padding, pivots, equipment fits,

crop offsets, and world-area cleanup thresholds together. Keep prone/crouching

height relative to standing rather than independently normalizing each pose.



Separate density, motion, and stylistic changes. The owner rejected reducing Bill's

colour/shading detail as muddy. Do not treat palette reduction as a generic cure for

coarse sprites. A same-world-size reference beside actual room art, plus native

close/normal/fit captures, distinguishes real source detail from magnification.



## Inventory the effective consumer



For a full replacement, enumerate the actual runtime states, including overrides,

reverse clips, joined endpoints and composed half-turns. Directory counts and the

base manifest alone omit substantial coverage. Preserve timing, per-frame facing,

water kind/pose, depth offsets, and equipment availability, not just images.

Bill's September 12 inventory contains 175 bare states and 168 equipped states;

these are revision-specific evidence, not hard-coded targets for future characters.



A useful migration contract maps every effective runtime frame to a preserved

source frame and any pivot-padding offset. Match pixels with transparent RGB

normalized. Keep the source hashes and reproduce individual registered crops before

rebaking. Do not treat an old low-density endpoint as a new dense source.



## Equipment and validation



Complete low-density provenance reconstruction can require multiple original

palette stages: Marsh's v2 output was quantized again by v5. Reproduce that legacy

sequence to verify source selection; dense output can then retain the final

accepted palette without resampling already-quantized shipped frames. The example

is `tools/rebuild_marsh_art.py`, with all 211 source frames reproduced exactly.



Pair fitted worn helmets with a review of held/donning/removal source art. A smaller

overlay on idle/walk does not repair a large helmet already painted into those

transition frames. Check the whole authored clip (Veld's locker clips have 12

slots), hand contact and both endpoints before claiming fitting is complete.



Initialize fixture layout inputs before building navigation or capturing actor

snapshots. The first native render may otherwise load layouts and increment the

geometry revision, legitimately canceling an in-progress action. Probe the old

and current topology signatures before altering animation or navigation code.



The owner flagged oversized helmets during the Veld/Branforth replacement review.

Sharing a helmet design does not mean copying its old top-left or animation fit.

Prefer character-specific precomposed clips from preserved body motion with a

helmet fitted to each dense head/pose; review tilt, crown, neck and foreground

hands. Dry clips can use a restricted crown region for per-frame anchoring, but

raised tools must not move that anchor. Tread and swim need separate fittings.

`tools/rebuild_human_crew_art.py` records these operations. Generate new worn-gear

source art when the composition cannot reproduce the pose naturally, especially

donning/removal. Marsh's android states do not require helmets.



Re-extract helmets from their authored cutouts, then fit against the rebuilt body.

Never enlarge a flattened equipped frame and call it new detail. Preserve visor

openings, scalp occlusion, direction/tilt and foreground hands. Rebuild clearance

from the final composed pixels in world coordinates.



Godot headless `ImageTexture.get_image()` can expose shared image data during local

composition, unlike native readback. Clone the image before mutation, and use native

rendered evidence for migration baselines. A headless-only dump can accidentally

show helmet pixels in a nominally bare frame; investigate that before editing art.



Keep old revisions intact and replace bindings only after complete coverage is

verified. User authorization to replace the full library covers the integration;

do not create repetitive approval gates. Validation must prove actual selection,

playback, equipment alignment, clearance, pause/save behavior and native room use.

Source/native checks do not establish an exported release or universal gait quality.

If the owner also requested animation repair, complete coverage at higher density

is an intermediate milestone. Carry identified motion defects forward in the same

goal rather than redefining that request as a resolution-only replacement.



Reusable examples: `tools/bill_art_inventory.py`, `tools/rebuild_bill_art.py`, and

`docs/BILL_DENSITY_REBAKE_2026-09-12.md`. Local pixel reuse can stabilize an idle or

head, but repeated same-leading-leg source poses do not become a complete stride

through reordering. Record unresolved motion limitations honestly.



For owner-authorized local pose repair, a bounded articulated-pixel study can reuse

authored limb regions without recolouring or mirroring the character. Preserve a

hash of the source and explicit masks/joints. Protect accepted identity pixels,

retain bone lengths, verify ground contact, and inspect joint seams in motion.

Never label source-region rotation as a newly drawn source or as added resolution.



Derive stance displacement from cumulative authored frame durations. Equal phase

indices can have unequal durations. Compare the planted foot in world coordinates

against the engine's distance-driven stride: a believable in-place loop can still

slide when attached to the actor. Record any proposed stride override separately

from simulation movement speed, and validate both facing directions independently.



Bill's integrated example uses full clip keys (`walk-east`, `walk-west`) as stride

overrides with the state-wide `walk` fallback retained for other directions. Both

the generic player and legacy human clock must honor the same resolution order.

Verify an intermediate distance fraction that distinguishes the override from the

fallback, plus pause and native frame parity. Reconstruct pre-repair source pixels

independently; never feed installed repaired frames back into the source rig.



The first local walk passed contact math but looked like a short shuffle in native

review. Increasing the source stance travel from 32 to 46 pixels per half-cycle

and adding a one-pixel body rise improved the step. Mathematical planting evidence

does not replace visual assessment of stride reach, joint seams and body motion.



## Fitted human helmet revisions



Share the helmet design while fitting its shell, visor and neck seal to each

character and pose. Precompose finished character-specific clips from accepted

body motion where possible. Generate corrected source poses where hands, head

tilt or silhouette cannot be preserved by composition. Keep the anatomical head

size fixed; shrinking the face to fit a helmet is not a fitting correction.



Review held, lifted, donned and removed helmet poses together with worn idle,

walk and swim. A smaller worn overlay does not fix a large helmet painted into

pickup/donning frames. Preserve these edits as new source revisions with prompt,

references, hashes and extraction recipes. Keep candidates out of runtime until

their sequence endpoints and station-scale motion have been inspected. Marsh's

android identity does not require oxygen gear simply because legacy files exist.



Register edited locker sources using the original body scale and the sole anchor,

not total bounds that include an overhead helmet. Preserve exact selected idle

frames at the sequence endpoints, translating pivots rather than rescaling bodies.

Check joins in world foot coordinates and removal against reversed equip frames.

Review the interior poses as well: perfect endpoints alone can hide a late snap.



For native room evidence after save/resize, flush deferred station centering before

focusing the room under review. Inspect the saved pixels: a successful capture call

can still contain the wrong room or only UI. Keep animation/state checks distinct

from unrelated authored-room containment and scrollable-sidebar failures.



Review every pose of a loop as a filmstrip before accepting animation coverage.

Six distinct images can still repeat the same leading leg. Track near/far limb

ownership through lighting, overlap and costume details; explicitly compare

opposite contact phases. Inventory run/walk pixel aliases separately from timing.



Generated walk instructions and even a constrained seam-cleanup request can replace

the intended leg ordering. Inspect the returned poses before extraction or binding;

retain rejected sources with the actual rejection reason. A local source-pixel rig

can prove alternation and stance travel, but numeric planting alone does not clear

joint seams. Keep the original donor reconstruction independent of installed art.



When selecting a rigged clip, install its measured per-direction stride alongside

the art and verify the renderer's distance-selected frames against an independent

rebuild. A later generated seam edit invalidates the rig's pixel-contact evidence:

label retained measurements as guide checks until the edited pixels are measured.

Freeze any review strip used as a generation reference before subsequent iteration.

Preserve source-pixel texture when a smoother edit simplifies accepted materials.



Keep authored rigs separate from the explicit selected-clip registry. Direction-

specific donor masks and limb lengths must be checked independently; never mirror

the opposite costume view. If a stance target exceeds the preserved bone lengths,

correct the attachment/stride geometry instead of stretching the leg. Native gait

checks should obtain cadence from the independent rig record, not assume every

character shares the first character's timing.



Source matching can canonicalize identical run and walk pixels to walk paths.

When replacing such a clip, override the destination animation state explicitly;

do not rewrite the frozen source contract or assume a new run array reaches the

renderer. Validate against an independent state-specific donor reconstruction.

Keep human locker endpoint replacement guarded by human identity: legacy android

body aliases do not authorize helmet equipment or human-only pack lookups.



Generated review pages must not infer native validation from the selection flag.

Link or record actual checks separately. A repaired side cycle does not establish

front/back gait quality: inspect original limb ordering before choosing those rigs.



For axial views, keep costume sides and view-specific donors intact when varying

projected leg lengths. Label projected sole registration separately from world

contact checks; side-view ankle drift equations cannot certify front/back planting.

Native direction reviews must advance the actor along the actual movement axis,

and preview pages must use the same travel direction rather than a universal side scroll.



Audit action joins in common foot-pivot coordinates and inspect paired images.

Large pixel differences can reflect an authored breathing pose, while an obvious

body/style change demands source correction across the clip. Exact endpoints can

hide inconsistent interiors. Record focused review selections and unmatched globs;

keep named review folders so later filters do not overwrite earlier evidence.



Verify generated transparency from image mode/alpha, not a visible checkerboard.

Preserve opaque failures and background-correction edits separately. Calibrate a

multi-pose source from one standing anatomy ruler, register by boots excluding

grounded cargo, and compare both standing endpoints before promotion: a consistent

floor line can conceal body growth across the sequence.



When combining cargo upper bodies with an accepted walk, inspect the anatomical

hip attachment and occlusion before reuse. A matching canvas and sole pivot do

not establish a matching pelvis. Preserve a failed splice recipe and correct the

source instead of promoting a visible seam merely because the gait already passed.



A cargo rig must use the destination carry cadence when measuring stance travel;

reusing a walk helper does not authorize changing action timing. Bind pickup,

carry, reverse unload and equipment coherently, including legacy source aliases.

Fit helmets from the revised per-pose head anchors rather than old action offsets.



For an intentionally local gait rig, request one clearly separated contact-pose

donor instead of repeatedly asking generation to track limb ownership across a

whole strip. Derive anatomical scale from that actor's reference, not another

crew member's height. Preserve generated source and rigged sequence as separate

artifacts so their evidence and limitations remain distinguishable.



When generalizing a character rebuild, key caches by actor and keep donor masks,

anatomical rulers and helmet dimensions character-specific. Verify the already

selected actor stays pixel-identical while introducing the next one.



For opposite cargo directions, choose the boot-anchor region opposite the crate;

do not mirror the artwork or reuse an east-only crop window. Keep target hips

attached to the torso when resolving reach limits. Reduce stride where appropriate

and carry the revised stride into playback; zero ankle drift can coexist with a

visible gap caused by lowering the hip attachment.



Place source knee pivots on the actual joint/plate, not an estimated midpoint of

the lower silhouette. When the repaired stride changes, verify distance-selected

runtime frames from the independent recipe, not just elapsed-time playback.

Keep selection and caches keyed by both actor and direction.



Front cargo can hide boot centers behind a crate. Calibrate from an unobstructed

standing pose and register exposed outer soles, keeping prop depth separate from

anatomical height. Projected leg masks must cover entire boots; otherwise leftover

pixels remain frozen at the original floor while the cropped legs move. Check

the lower-body residual mask before accepting an axial rig.



Apply a newly discovered extraction invariant to earlier uses of the same helper.

The cargo residual check found six stationary boot-edge pixels in Marsh's selected

south gait; expanding the masks and verifying the two affected native clips fixed

the issue without rerunning unrelated art generation.



For rear cargo, author the crate in front of the character in world space: the

back must occlude its center. A front-facing crate painted across the back is not

a valid rear view. Preserve the held pickup endpoint as the axial carry donor

when its grip and silhouette are sound; use rear phase ordering, not a mirrored

front cycle. Keep projected sole checks distinct from native distance playback.



Review seating as a transition plus idle family at one anatomical scale. Keep

furniture out of character source sheets, retain the established seat/depth

contract, and verify actual seat contact in-room after inspecting sprite joins.

Before reusing an older preview fixture, inspect its loading path: a fixture

explicitly loading v1 artwork cannot validate a selected v2 source revision.



Confirm which facing the live activity chooses before treating a directional

sprite review as furniture acceptance. Compare old/new sources at the same live

anchor to distinguish source registration from furniture placement. Derive chair

centers using the prop renderer's source registration and scale, not a fixed inset

that only appears plausible at one furniture size.



For exact RGBA join checks, compare all array channels after clearing invisible

RGB. Do not rely on an RGBA difference image's default bounding box: alpha-only

bounds can hide changed colors when both frames share the same alpha. Normalize

different canvas profiles into pivot coordinates before comparing endpoints.

`tools/validate_crew_seating_joins.py` applies this to every selected seating family.



For lying poses, verify both mattress containment and head/pillow registration.

A foot-based anchor may keep the body inside the berth while leaving the head

below its pillow after foreshortening changes. A passing room activity test proves

the approach and state transition, not that the resting contact is visually right.



Export a selected prone head offset in world units from the bare source and share

it across equipment variants. Match that anchor to a pillow target transformed

through the furniture's authored pivot/scale. Ease the correction in lie-down and

out during get-up; never shift only the sleep loop and introduce an endpoint jump.

Keep this opt-in through metadata so unrelated characters retain their placement.



Transparent generated art may carry almost-invisible alpha speckles far from the

body. Apply the export visibility threshold before measuring bounds and anchors,

not only after resizing. Verify earlier selected extractions remain unchanged when

introducing that preprocessing. For side-on lying poses, compare straight body

length against standing height at the same scale; fixed foot registration can

conceal an overlong body. A correction that restores length but loses facial/suit

identity is still a rejected candidate.



Reject fully opaque sprite sources after chroma removal before measuring or exporting frames. A painted checkerboard is image content, not alpha; do not accept its resulting contact sheet as a sprite extraction. Verify the guard against existing selected sources as well as the rejected candidate.



For generated multirow sheets, choose an empty row gutter near the intended split rather than cutting blindly at the image midpoint. Record the chosen split and compare existing selected PNG hashes after changing extraction. A few boot pixels across the midpoint can contaminate the next row and distort anatomical scale.



Uneven sprite columns can use opt-in silhouette gutters when each row has exactly six isolated horizontal alpha spans. Keep equal columns as the existing default; record extraction mode. Compare transition endpoints against loop anatomy: successful extraction does not establish consistent body scale.



If a generated loop row is uniformly smaller than its matching transition endpoint, an explicit isotropic row calibration can preserve anatomy without further regeneration. Record the factor, keep the default unchanged, and visually compare head, torso and limb proportions; equal body length alone is not acceptance. Never use this to hide nonuniform anatomical distortion.



Side-rest helmet studies must register to measured head centers and head angles per pose, not the topmost body pixel (which may be a knee). Preserve a reproducible bare/equipped contact and machine-readable registration before integration. Check collar overlap and canonical equipped idle joins in motion.



Keep head-anchor coordinate variables separate from the export profile pivot. Body and equipment must retain identical profile geometry; validate after the rebuild process is terminal. Veld east rest integration exposed and fixed accidental pivot reassignment before selection checks passed.



Reject row calibration when length matches but head/torso thickness grows relative to the transition endpoint. Branforth east sleeping study 01 demonstrates nonuniform anatomy mismatch; it needs source revision, not selection with a scale factor. Inspect actual activity facing before describing a direction as live-room tested.



When repeated generated rest loops change anatomy, use the character's own accepted transition endpoint as a deterministic breathing donor. Restrict deformation to the chest, pin skull/feet/support edge, assert exact loop seam and nonzero interior motion, and inspect before fitted-equipment integration. Preserve rejected generations without selecting them.



Share the side-rest composition function but keep per-character shell sizes and head-center/angle tables. Verify exact idle/rest aliases and reverse transitions after exporting both variants. Branforth east uses his own anatomy and a 34x36 fit; Veld uses 30x32. Do not infer live furniture coverage from native clip acceptance.



Reusable breathing deformation should take explicit actor/direction anatomy anchors and each direction's own transition donor. Verify existing selected PNG hashes when adding a new rig configuration. Veld west uses chest x170; Branforth east uses x105, neither body is mirrored or borrowed.



Key fitted side-rest geometry by (actor, direction), including equipment view and head anchor. An actor-only table becomes unsafe as soon as the opposite direction is added. Preserve each source direction's own asymmetrical suit details and validate complete equipment profile parity.



Record breathing chest anchors alongside side-specific helmet geometry; Branforth west uses his own endpoint with chest x174 and a 34x36 west shell. Preserve raw generation and exact prompt even when the generated loop row is replaced by an endpoint-derived rig.



For south-facing supine animation, inspect the actual old pose rather than preserving a misleading standing silhouette. Establish a fixed elevated foot-end camera, visible boot soles, foreshortened torso and face tilted upward. Do not apply side-view standing-height versus flat-length comparison to a foreshortened axial view.



For axial reclining helmets, a character-specific equipped source can preserve upward face tilt better than an upright overlay. Extract it using the bare source geometry and scale, never equipped crown-to-sole height. Require identical sheet dimensions or explicit registration, and compare bare/equipped contacts before runtime selection.



Generated equipped rest frames must retain bare profile geometry and head-to-furniture metadata. Preserve exact canonical idle/rest source aliases through the manifest so opposite transition endpoints and reverse get-up remain identical. Validate the final exported profile, not only the equipped source sheet.



A carry study can retain its own loaded torso while reusing the same character's articulated gait source, but inspect the hip seam before integration. A rectangular torso split can leave duplicate thigh pixels or disconnected joints even when the cycle alternates correctly. Keep original runtime frame count and establish distance cadence separately.



When a composite fails, inspect the selected base gait itself against an unmodified source donor with coordinates. Prior native timing passes do not prove anatomy. Marsh east audit located hips about y104-109 while the old rig used y116-117; correct source landmarks and torso cut together before borrowing legs into cargo.



Measure loaded pelvis retention separately from gait torso segmentation: Marsh east carry retains through y110 while the corrected walking source uses y103. Reusing a cut line blindly can remove the pelvis. Review corrected source geometry in walk, run and loaded variants before changing the shared runtime rig.



After correcting source joint landmarks, verify reach against world-space stance targets. Short source segments can trigger solver clamping and lift planted feet. Record any length calibration explicitly and review resulting anatomy as well as zero-drift metrics; Marsh east uses 1.2 with corrected landmarks and retains its native stride settings.



A clip-specific stride must activate distance playback even without a state-wide default. Do not add a generic carry stride just to activate one revised direction, because it changes unrevised directions too. Verify selected source pixels over travel samples, not only manifest stride values.



For axial carry, prefer the same direction's neutral loaded pickup endpoint when

it has sound grip and anatomy. A walking donor's leg boxes are not transferable:

Marsh pickup boots extend outside his walk masks. Retain the residual-pixel guard

and measure the loaded donor independently before selecting the four-phase cycle.

Keep rear prop occlusion and original runtime durations. Sampled native stills and

distance equality do not substitute for continuous motion and transition review.



Before replacing a source clip, enumerate every frozen runtime state that points

to its source paths. Marsh repair/eat/interact and other actions alias old weld

frames. Store a new welding sequence in a separate runtime override dictionary;

mutating the shared source map silently changes those unrelated actions. Native

checks should compare the selected sequence with its independent reference and

verify a representative aliased action remains distinct. Preserve the initial

failing run as evidence rather than weakening that check.



Specify tool handedness anatomically for front/back sources: a right-hand tool

appears screen-left from the front and screen-right from behind. Back view must

occlude hands and tool correctly. Keep view groups and source revisions explicit

in the extractor, and compare existing output hashes when adding a new group.

Stage-only construction captures can repeatedly land on idle endpoints; an opt-in

native sequence should advance simulation in small steps and prove that the live

renderer actually traverses the active poses before judging contact.

Separate draw/stow transition samples from the active work loop when counting

distinct poses. Compare active renderer pixels with the selected clip, rather

than accepting any changing texture. Inspect low foreground doorway contact

independently from side/tall-wall contact; foot clearance cannot certify tool reach.



Audit the controller's action window against the authored nonlooping clip duration.

Marsh's .9s tool transitions were truncated by construction's .52s window. Normalize

render elapsed time to play the full clip while retaining gameplay duration and

the source timing contract. Verify early/middle/final renderer samples, exact

draw-to-work and reverse-stow joins, and that the active loop never drops the tool.

Use samples inside frame intervals for pointer/index assertions; floating-point

boundaries may select adjacent frames with identical pixels.



For low tool work, register a fixed boot/knee support line independently of the

torch tip, which may extend below it. Preserve that extension with canvas padding

instead of lifting the body or clipping the tool. Normalize differing profiles

around their declared pivots for join checks, filling the comparison canvas with

explicit RGBA zero: transparent white leaves invisible RGB differences when

transparent padding sizes differ. Confirm actual GPU and disk pixels before

diagnosing such a comparison failure as damaged art.



Directional construction fixtures must give recovered Marsh a real charging

origin and reset his battery/return state between independent room cases, just as

they reset the room resources. Preserve production battery and collision rules.

A floor-level pose can require a nearer legal work node; keep actor/direction

scope explicit and retain all route, furniture and closed-door checks.



Measure actual chosen work coordinates and nearby graph nodes before adjusting

approach preferences. Marsh's core south case chooses (0,160); (0,176) is blocked

and absent from the graph, so a closer preference cannot fix its contact gap.

Measure the source tool-tip offset separately from the renderer's foot offset.

Keep those coordinate spaces explicit when requesting a new reach pose.



Distinguish cell edge, door leaf and floor-track surfaces before converting a gap

into an art request. Export the actual closed-door parts from the renderer helper.

In Marsh's south case those y targets are 192, 187 and 182 respectively; the cell

edge overstates the gap to the leaf by five world units. Keep geometric target

evidence separate from visible material contact and occlusion acceptance.



For a reach revision, report the target in registered source pixels as well as

world units. A visibly improved lean may still fail contact: Marsh single-pose

study 01 is 18.30 source pixels short despite its clearer downward gaze. Keep

that study unselected until representative reach works, then expand the sequence.

Draw review guides after all sprite composites and verify exported guide pixels;

the overlay is review evidence, never part of the runtime texture.



Keep each representative pose revision's registration and exact prompt separately.

Measure progress against the same fixed support and target: Marsh reach study 02

reduces the gap to 3.34 world units without selecting it prematurely. Convert the

remaining gap back to source pixels for the next edit; a smaller gap still does

not prove surface contact or a usable transition sequence.



Correction to the preceding Marsh study measurements: color thresholds also

matched the copper torch grip, biasing centroids toward the hand. Select the

distal connected hot-color patch and export a visible mask before using a gap to

request more art. The corrected study 02 tip already passes the near leaf by

2.22 world units. Review the mask itself, not only the resulting number; retain

an independent handle-versus-tip regression. Do not generate further reach from

the earlier mixed-pixel centroid.



Preview representative studies through a fixture-local texture substitution,

copying renderer metadata and declaring the actual pivot/standing height. Restore

the original frame array afterward and retain the normal motion assertions.

Marsh study 02 passes native texture selection yet touches the threshold strip

above the painted leaf, so geometric-edge reach alone must not select the pack.



Trace the full position adapter before counting a renderer offset. Marsh's

main.get_marsh_position subtracts 0.038 cells and grid_canvas adds it back:

net offset is zero. Earlier reports incorrectly added 14.592 world units and

understated the gap. Study 02's actual leaf gap is 12.37. Assert this cancellation

in the native fixture, and size review canvases to include the corrected target.



When generation adds bottom padding, inspect support placement again even if the

prompt requested fixed feet. Study 04 shifted its boot sole; re-registering the

measured sole at fixed scale yielded a 0.16-world-unit leaf gap and visible native

leaf contact. Record that anchor correction explicitly. Use the verified pose as

the endpoint for sequence authoring, not a repeated still advertised as animation.



For generated intermediates, retain exact independently verified endpoints and

review the interior-to-endpoint posture progression. Reach transition 01 passes

reverse/pixel endpoint checks but its penultimate head is lower than the final

pose, exposing a visual reversal those checks cannot catch. Keep it unselected

until the interior is corrected; exact joins are necessary, not sufficient.



Repair a failed intermediate using both neighbouring poses as references and

explicit intermediate head/hand landmarks. Transition02 fixes its posture reversal

without regenerating sound earlier frames or either endpoint. Keep the replacement

slot and its source hash in the extraction record; review full motion afterward.



Register a generated work strip to the verified endpoint's crown-to-boot ruler,

with one common scale and fixed support across poses. Reach sequence01 uses

60/230 and confirms five distinct native work poses after a fixture-local array

substitution. Restore the selected array afterward; native work-loop evidence

does not cover draw/stow motion merely because the source endpoints match.



At selection, rebuild every derived dependency from its saved raw source, record

all source hashes, and rerun selected-pack reference/transition-window checks.

Marsh south reach selection preserves original aliases and timing while replacing

only three explicit tool states. Keep fixture substitutions separate from the

selected-pack check so a preview cannot accidentally certify an unchanged pack.



Before a new role-action pass, inventory selected manifests and render every

direction at declared pivots. Check prop semantics across views: Veld's east

interact gestures while other directions show a scanner. Use the target view for

identity/scale and other views only for prop design; never mirror identity to

patch a missing action. Frame uniqueness counts alone do not establish role use.



A standing scanner strip without overhead or ground-extending props can use a

common crown-to-sole ruler; retain measured foot centers separately. Veld east

scanner01 keeps exact idle endpoints while changing only four work interiors.

Record review GIF timing separately from the immutable runtime timing contract.



For modest head changes, compose the fitted shell per frame and record its angle,

not only its crown position. Veld scanner study uses a small tapping tilt while

retaining exact selected equipped idle endpoints. Review shell/hand clearance in

the paired contact sheet before native playback; do not infer fit from body checks.



For a paired action preview, sample each bare/equipped slot using the loaded

runtime duration table and compare both endpoints to the selected originals.

Veld scanner-study performs these checks before integration. Keep preview

substitution evidence distinct from subsequent selected-pack source verification.



Before selecting an action, preserve accepted equipped endpoints as independent

source artifacts rather than reading the pack being rebuilt. Veld scanner uses

an explicit paired state override after source-path resolution so shared aliases

remain unchanged. Native selection checks compare loaded frames before replacing

any preview rows; a successful substituted preview alone cannot prove selection.



Reuse standing registration mechanics across actors while retaining separate

identity/prop references and source records. Branforth's diagnostic meter uses an

amber protected display and physical controls; Veld's scanner remains cyan.

Shared extraction does not imply shared body proportions or helmet dimensions.



Keep actor-specific standing rulers and shell sizes when sharing action tools.

The diagnostic/scanner helper uses Branforth's 148/566 ruler and38x40 shell versus

Veld's 148/547 and34x36. Run the paired native fixture with the actual actor id

so coverage, timing and idle endpoints come from that actor's loaded contract.



Use an explicit selected-actor set for a shared action override and keep per-actor

source provenance. After selecting both human instrument actions, refresh the

complete-pack contract check once; keep that evidence distinct from remaining

live workplace and full visual acceptance.



When a nonhuman actor shares an extraction helper, retain its equipment policy:

Marsh can use standing instrument registration without invoking human helmet

composition. Separate controller interaction from repair/welding aliases through

explicit runtime state overrides rather than mutating the common source frames.



Check style drift after expanding a representative pose: Marsh controller strip01

enlarged the head and smoothed material detail. Preserve rejected source/prompt

with a reason, and compare a corrected strip directly beside immutable idle

endpoints at runtime density before treating a height match as identity approval.



Do not assume two idle endpoints are identical. Marsh interact-east's closing

frame differs subtly from its opening frame; native endpoint comparison caught

the accidental replacement. Preserve both independent endpoint sources and compare

each to its corresponding original slot. Keep the initial failed check as evidence.



For axial standing registration, a median of opaque sole pixels may favour one

boot's larger painted area. Compare body centre to the reference; use the midpoint

between both boot support extrema when appropriate. Marsh controller axial studies

needed this correction. Side poses can retain their measured single-foot anchor.



A multi-direction animation matrix can preserve layout while drifting identity.

Marsh controller matrix01 passed the requested 3x4 arrangement but enlarged the

head and simplified suit shading. Register beside independent idle references

before selection; split subsequent authoring by direction when this drift recurs.

Keep rejected raw sources, prompts and reproducible comparison evidence.



For a standing sequence with a downward head tilt, use the upright frame ruler

for all interiors instead of independently normalizing their heights. Marsh

south controller strip01 has one lower crown but a common sole; per-frame

height fitting would erase the intended head motion and inflate that pose.



Share controller extraction mechanics while keeping measured view profiles.

Marsh west uses its own standing ruler and per-frame sole positions; south uses

a different ruler and two-boot midpoint. Preserve the authored direction and

verify the selected runtime pixels separately from the substituted study.



A rear-facing controller action should communicate through elbow and head motion

while the torso occludes the device. Marsh north retains that occlusion instead

of inventing a display on his back. Review the rear clip at native scale and

keep directional source selection distinct from live workplace acceptance.



Full-body helmet generation can alter body proportions and erase hand gestures

even when the shell fits. Veld south equipped strip01 failed this paired-pose

check. Prefer head-region edits with the original body retained, then compare

below-collar pixels and each helmet angle before native equipped review.



For authored fitted-head replacements, crop away generated shoulders and retain

the corresponding action body. Assert unchanged pixels below the collar; Veld

south uses y60 and four independent head crops, including a downturned pose.

Review both bare and equipped slots together at native scale before selection.



Check each directional source contract before packing registered action studies.

Veld south interact uses canvas256/pivot(128,224), unlike east184/(92,172).

Translate the study by(36,52) rather than assuming every direction shares a

profile. Native selected-pixel comparisons caught this even though coverage and

source preservation passed; keep that distinction in acceptance evidence.



Side head replacements must include tied hair behind the skull, not only the

face bounds. Veld west initially left bun pixels floating behind his helmet.

Review the full silhouette and extend the removal region only above the collar,

preserving shoulder and backpack pixels below the head boundary.



Preserved endpoint pixels can still conceal an action-design discontinuity.

Branforth west original endpoints hold a pale tool, while authored interiors

use an amber meter. Inspect prop continuity explicitly; resolve the mismatch

before equipment/native acceptance rather than relying on endpoint equality.



When deliberately revising an endpoint prop, test two separate invariants:

exact pixels against the independent revised endpoint and exact original pixels

outside the bounded edit region. Branforth west uses both in native study and

selected checks, retaining protection without locking in the obsolete tool.



For full-library replacement, maintain a per-clip evidence ledger covering body

and equipment separately. Fingerprint selected pixels, timing and pivots; flag

changes without silently retaining acceptance. Missing reconciled evidence is

not a confirmed redraw requirement. Do not report percentages from file coverage.



Kneeling action studies must retain the original crouched ruler, rather than

being stretched to standing height. Veld east sample uses a common 99-pixel

kneeling height and grounded support. When returning a 256-pixel study to its

184-pixel frozen source profile, translate pivot128,224 to92,172 and assert all

opaque bounds survive the crop. Protect the vial/hand region during helmet

compositing and verify selected pixels against the independent study.



Identity corrections must use each corresponding bare/equipped body as the

compositing base. Veld sample endpoint checks exposed40changed collar pixels

when a bare base replaced an equipped frame. Preserve outside-head pixels,

use one shared head scale, and register at the collar rather than bounding-box

centre. Correct connected transition heads before selecting revised endpoints.

A generated turnaround can validate faces while still having inconsistent body

equipment; do not treat identity-reference approval as animation-body approval.



Fit identity heads across a connected standing/kneeling/action sequence before

selection. A head that appears fitted within a crouched clip can grow relative

to the standing head. Use a shared source ruler, exact corrected endpoint copies,

and paired native scale review. Track adjacent uncorrected actions explicitly;

selected checks for one chain do not close identity review for the whole actor.



When selection supersedes a study, migrate older review modes to the current

explicit source and pivot. Otherwise old review commands compare against rejected

identity. Keep preparation metadata neutral and selection/evidence in the ledger.

Consolidate current handoff sections while preserving concurrent project edits.



For a gait identity correction, retain the independent original rig as the

stride/timing authority and compare lower-body pixels exactly. Compare full

corrected body AND fitted equipment at each distance-driven sample. Confirm

state coverage before assuming a character has another actor's run states.



For directional identity heads, sample once from the raw source using recorded

registration transforms, rather than reducing a reduced reference again. Review

collar joins close up; bounding-box alignment can leave a floating helmet. In

distance tests, calculate expected travel from the supplied Vector2 positions:

an unrounded scalar can choose the other frame at an exact phase boundary.

Probe sample, expected/actual frame and playback snapshot before changing runtime.



An identity head correction cannot certify the rest of an action body. Compare

corrected idle against every interior for torso width, leg length and prop

retrieval/stow progression. Veld scanner head-only study retained a visible body

change and collar artifacts; keep it unselected and reauthor the full body using

corrected idle anatomy. Exact endpoint copies do not by themselves make a smooth

transition. Preserve rejected approaches as provenance, not accepted references.



For a full-body action replacement after identity correction, calibrate the

standing ruler against the selected idle silhouette, retain distinct retrieval

and stow poses, and copy corrected idle endpoints independently. Fit the helmet

to those authored bodies and assert hand/device pixels remain unchanged below

the collar. Check the frozen source profile before applying any translation:

new Veld south scanner art already uses256/pivot128,224 and needs no extra shift.



When fitting heads from different source sheets, compare final opaque helmet

height and collar contact against the corrected idle, not the numerical resize

factor alone. West scanner needed a different source factor from south because

its head occupancy differed. After reduction, register the actual opaque bottom

to the collar; raw-coordinate rounding left a visible rear neck gap. Inspect

close-up seams and preserve body pixels below the collar. For rear-view actions,

keep the scanner naturally occluded in front and author elbow/head motion; do

not twist the actor or place the instrument on the back to make it visible.



For a connected sample-inspection chain, preserve held vial/glove pixels in

front of the helmet collar when they overlap its fitted head region. A simple

head rectangle can otherwise erase the interaction. Fit the settled kneel once

and copy it to sample endpoints and the start of stand; retain the original

per-slot timings even when stand reverses the authored kneeling poses.



When a generated figure crosses its nominal cell boundary but remains separated

from its neighbours, extract at verified transparent column gaps. Require the

expected number of separated silhouettes and record exact crop bounds. Fixed

equal-cell slicing would cut the west kneeling source and include a sliver of

the next pose. Keep one anatomical scale and register the planted foot after

extraction; do not normalize each pose to equal bounding-box dimensions.



Side-view helmet masks need a narrower collar region than the head region. A

full-width rectangle cut away the west kneeling shoulder, leaving an apparent

floating head. Inspect collar/shoulder seams at enlarged nearest-neighbour scale

then verify all native phases. Estimate head centre from the upper crown only

when a raised vial reaches face height, so the prop does not shift the helmet.



In a rear-view one-knee transition, the raised rear boot sole can extend lower

in image space than the planted foot. Use the planted-foot region for floor

registration, not the whole silhouette bottom. Keep the same contact rule in

the connected sample action so changing boot perspective does not move the body.



For autonomous native crew review, wait for startup_complete and explicitly

record recovered/present crew before placing them on verified clear navigation

nodes. Legacy pre-cryo fixtures can otherwise omit the actor. Advance NPC and

visual time together; remove animation-only time jumps before capturing a

continuous work sequence. Record state, facing, foot position and simulation

time per capture, and assert that kneel, action and stand all occur with fixed

work-position registration. Report observed directions/equipment separately.



For helmet donning sources, inspect held and overhead shells for duplicated

faces even when the prompt explicitly says empty. Preserve the actor's attached

head while correcting only empty helmet interiors. Keep rejected and corrected

raws with exact prompts, and review the held-to-worn size relationship at the

same registered body scale. A reversed donning study is not automatic removal

acceptance; verify hand release, placement and its distinct original timing.



Explicit transition sequences must retain their own corrected endpoints. A later

legacy endpoint repair can silently restore old identity art even when the source

study passes. Compare every selected slot against pivot-normalized study pixels,

including both ends, and compare those ends with the currently selected idle.

Helmet overhead poses use the frozen taller transition canvas; translate by the

actual pivot difference instead of copying the ordinary standing-frame crop.



When a live handoff looks ambiguous at room scale, capture the actual runtime

texture and its frame index, action elapsed time, shelf visibility and foot

position beside the room image. Compare its bytes with selected art before

changing the renderer. Tiny props and temporary cryo tint can obscure detail;

discrete checkpoints still do not establish continuous motion quality.



Prop handoffs need a shared visible size across shelf, hands and worn states.

Inspect consecutive native phases with the staged prop included: correct event

timing and matching actor frames can still hide a shelf-to-hand scale jump.

Keep behavioral checks separate from this visual continuity requirement.



Fit staged props using the actor asset ruler and preserve the shelf base when

changing scale. Derive servicing presentation from existing live request/action

state, retaining the returned pose until the actor leaves; avoid a new save field

for a purely visual fit. Reset reusable room-view properties on every draw.



A displayed checkerboard is not evidence of alpha: inspect the actual image mode

and alpha extrema before registration. Reject a baked RGB checkerboard; retain

the raw and exact corrective background prompt. Keyed magenta is acceptable when

the resulting figure isolation and enclosed limb gaps are visually verified.



Native review modes must create their final output directory after mode selection

and assert every screenshot write. A zero-failure animation check without saved

captures does not establish visual evidence. Inspect an actual emitted image.



Source offsets can vary per slot within one clip: standing endpoints may use a

smaller embedded source while seated interiors occupy the full canvas. Normalize

each override against its frozen per-frame sourceOffset before rebaking; do not

apply one crop blindly to the whole sequence. Compare normalized selected pixels

with the study at both endpoints to detect double-applied translations.



Owner gait rejection overrides prior pose/timing acceptance. A pasted static

torso over transformed legs is not coordinated locomotion; axial leg stretching

can distort boots. Review a whole-body cycle with opposing arms/legs, pelvis

weight transfer and shoulder response. Check that half cycles actually exchange

support legs: generated six-pose strips can repeat the same lead leg. Do not

normalize away authored vertical body motion or preserve faulty old gait pixels

just to satisfy a historical identity-only preservation check.



Register whole-body gait sources against one anatomical ruler and common ground

line, with recorded pelvis anchors. Silhouette centers drift when arms or feet

swing; per-frame bounding-box normalization erases weight-transfer motion. A

stationary loop is only a first review: trace each leg identity/occlusion through

both half cycles, then evaluate planted-foot contact against actual translation.



When replacing a gait source, recalibrate distance per cycle from the new poses;

old stride values belong to old foot travel. Compare candidate strides at equal

world movement speed. A contact-band centroid is not a fixed sole landmark

because heel-to-toe roll changes the visible footprint; label such estimates

provisional. Native scale studies must explicitly disable project viewport

stretch before claiming source-density or game-scale visual review.



Repeated pose correction failure needs a changed reference strategy, not stronger

wording alone. Whole-character style refs can dominate a joint guide and restore

the unwanted pose; guide-only generations may obey legs but drift in costume.

Separate cropped identity/costume guidance from an explicit pose diagram and

verify support leg, overlap and opposite arm independently before selection.



A correct isolated pose may still be unusable in a loop if torso/leg width and

proportions differ. Review the inserted frame beside the entire sequence at the

same anatomical scale; do not stretch it to hide inconsistent anatomy. Prefer

a coherent whole-cycle pose guide over repeatedly mixing standalone drawings.



Stop equivalent whole-strip retries after repeated lead-leg/arm recurrence, even

when an explicit whole-cycle guide was supplied. Record the failed experiment

and change the motion-source method or separately constrain complementary half

cycles. Do not count new raw files as completed motion replacement.



For continuous-video gait sources, preserve the actual video, exact prompt,

reference and durable job ID. Verify actual fps/frame count/dimensions rather

than provider resolution labels. Inspect temporal samples without per-frame

alignment first, then choose a repeatable contact-to-contact cycle. Generated

motion is source material, not proof of a seamless loop or planted world contact.



When calibrating a new gait, track the same heel-to-sole landmark through each support phase and compare world-position residuals for candidate strides. Record manual reading uncertainty. Low residuals at sprite boundaries do not prove continuous foot locking: held frames still translate between boundaries, so inspect the native moving loop.



Use explicit source-frame intervals for video phase and loop-boundary review (review_crew_motion_video.py --start/--stop/--step). Keep source indices visible in the contact sheet and registration; evenly spaced overview thumbnails alone can skip the support change.



Front/rear foot travel is foreshortened. Do not derive a world-space stride directly from its short vertical sole displacement; compare cadence across turns with the side views and inspect projected support motion separately. Keep current status and bible checkpoints concise; retain detailed experiments in the dated review report.



Audit gloves as part of directional costume continuity. A rear reference with hands hidden beside the body can generate bare hands even when the suit is otherwise preserved. State full-finger suit gloves explicitly in motion prompts; keep a failed source as motion evidence rather than selecting it for a superficially smooth gait.



For native distance-driven frame checks, derive the oracle distance from the actual supplied Vector2 coordinates. An unrounded scalar can straddle a frame boundary relative to engine-precision coordinates; inspect phase and position before changing playback or relaxing pixel checks.



In autonomous directional capture, preserve brief path-facing adjustments as separate episodes and keep observing for a reviewable continuous segment. Do not force actor movement merely to satisfy the capture. A manually advanced art fixture should apply the shared input/automatic-processing isolation after startup; retain timeout evidence and do not infer its cause from a successful retry alone.



For additional crew video cycles, use tools/extract_crew_motion_cycle.py with an explicit reviewed JSON recipe. Record source indices, fps/dimensions, one scale/translation, selected durations and pivot. The extractor rejects clipped poses and retains source/recipe hashes; this validates registration mechanics, not motion quality.



A crew foot inside a room does not imply its head stays inside that room crop. For native travel review near walls, include standing-height margin around the room or use a full-viewport capture; inspect the actual head/helmet bounds before accepting the media. Preserve original state-coverage assertions when adding a new motion-capture mode.



Determine the cycle interval independently for each generated direction. Equal fps,

duration and prompts do not imply equal gait periods: Branforth's east source used

24 frames per cycle while the west source used approximately 34. Preserve the

source cycle and selected phase indices separately from game playback durations;

copying another direction's indices can cut the return step and create a bad seam.



For native traces with multiple walk episodes, use tools/review_crew_live_walk.py

to build preview media from the longest continuous episode. Preserve the complete

trace and all short adjustment episodes, and label the chosen source indices.

Do not concatenate unrelated episodes into a supposed smooth walk. The preview

includes the exit and repeats for convenience; it is not a seamless gait loop.



Audit asymmetric equipment against anatomical sides across the complete turnaround,

not merely against the previous same-direction image. In a right-facing east view

the visible side is the character's right; in a left-facing west view it is the

character's left. Anatomical right appears viewer-left from the front and viewer-right

from the rear. Branforth's wrench belongs on his right and meter on his left: a

west reference that keeps the near-side wrench is wrong even if its prior same-view

review passed. Write this mapping explicitly in reference decisions and prompts.



Recalibrate held-pose durations when a replacement has unequal support-phase

travel; preserving old timing can retain sliding despite better poses. Keep the

selected recipe authoritative for exported durations and record an explicit

expected revision in independent checks without rewriting the frozen original

contract. Godot JSON numbers are floats; strict Array equality against integer

literals can fail for identical values. Print actual values/types before changing

playback or weakening checks.

Keep exported timing numeric representation consistent with preserved manifests

as well: integer-versus-float JSON text can churn evidence hashes even when

playback is identical. Reconcile that churn with regression evidence before

restoring review status; do not silently label all changed rows accepted.



Use tools/record_crew_motion_job.py with a saved provider listing to preserve the

unique exact-prompt job, prompt/reference hashes and resume handle. It never submits

jobs and refuses ambiguous matches or changed preserved input hashes. Use a review

revision suffix when recapturing changed sources so earlier evidence is retained.



### Derived NPC walk fixtures



Check the actual NPC update pause guard before adapting a live fixture. Marsh requires an unpaused game, with automatic processing and the tick timer stopped while the fixture advances its explicit clock. Preserve battery drain and helmet rejection; a walk review must not silently disable character-specific behavior. Record the observed walk exit and retain raw captures alongside the selected preview.



### Directional gait milestone



Close a directional walk pass separately from the complete animation library. Review source phases and real travel through an observed exit; room occlusion at the exit does not accept the destination action or furniture contact. A uniform-duration four-direction preview is valid only when all included recipes actually share those durations. After selection, reconcile the asset README and current handoff instead of accumulating contradictory pending/job statements. Keep the clip ledger authoritative for selected hashes and preserve broader idle, turn, run, carry and action work.



### Selected-state continuity



Use tools/review_crew_motion_continuity.py to compare idle, walk, action, run and carry poses at one standing density and common pivot before replacing adjacent states. Preserve source hashes in the report. Differences in pose height may be intentional; changes in identity, suit design and rendering density require visual assessment. Missing optional states in a catalog are not runtime defects until their consumers are checked. A good isolated walk can still expose old idle/action identity discontinuities.



For stop/start review, capture a complete idle cycle on both sides of a real move/arrive sequence, preserve battery/gear behavior, and isolate the immediately adjacent frames at each state change. Label controlled-route evidence separately from autonomous routing. Passing planted-foot checks can coexist with an abrupt first gait pose; retain that transition defect explicitly instead of equating test success with visual completion.



The maintained live-walk review helper now writes state-transition pages with exact before/after sample pairs. Inspect those as well as the first/middle/last overview: short state-change artifacts can disappear from overview sampling. Transition source extraction does not establish endpoint compatibility or a physical travel profile.



When calibrating an authored walk start, inspect the support foot before assuming uniform speed. Weight shift may require near-zero initial travel. A travel profile fitted to manual heel readings is not independent validation: report measurement uncertainty, review intermediate frames, and verify physical movement plus rendered motion in runtime. Avoid solving entry snaps with a render-only clip that slides a planted foot.



For movement transitions, consume leftover update time after the transition boundary and evaluate pose and travel at the same elapsed time. Verify integrated travel under small and boundary-crossing update partitions, plus zero delta, reversal and blocked-step cancellation; a single fixed-delta visual fixture can hide lost time or a one-update pose lag.



An authored stop needs both a matching final idle and a compatible entering support leg. Test multiple remaining-route lengths/gait phases, not only one convenient arrival. Deceleration should consume remaining route distance before arrival; final settling must not overshoot the target or delay unrelated arrival actions.



Keep stop trials opt-in while testing different route lengths. When an approach move can collide or complete a path, recheck the path before reading its target to start deceleration. Exact destination arrival and a good idle endpoint do not prove every entering gait phase or arrival action.



Transition pose overrides must yield to death and new action/stage states, including when the render query occurs before another movement tick. Test this explicitly; successful travel/collision probes do not catch a stale animation masking an arrival action. Preserve a failing-before log and the scoped passing rerun when the review exposes this defect.



Test arrival timers as well as destination coordinates under variable update intervals. If a deceleration reaches its endpoint partway through an update, account for the remaining time in the arrival state; otherwise longer updates silently extend its duration even though position tests pass. Keep this distinct from the pose-settling duration.



For saved movement transitions, validate relationships as well as field types: pose and travel clocks must agree, the stop target must match the remaining path or settled foot, and start/stop cannot both be active. Reject incompatible facing, medium and action states. Retain compatibility with snapshots that predate optional transition metadata, and pair rejection probes with a valid encoded actor round trip in the native scene. Actor round trips do not establish full save-game acceptance.



When promoting a motion trial, move the behavior into the production actor path and make the fixture exercise that path. Package new states in an explicit supplemental contract with fixed timing, pivot and selected pixel hashes; retain the frozen original contract. Verify ordinary goal selection as well as manually assigned paths: job selectors can set walk state before the first movement tick and bypass an idle-to-walk hook. Preserve existing actor-specific battery, equipment and checkpoint behavior.



Include destinations inside an authored start when checking transition time. A short route can finish before the start clip ends; invert the calibrated distance curve to obtain the actual arrival time and consume the remaining update in the arrival state. Matching the endpoint alone can hide update-size-dependent idle delays. This timing repair does not establish that the truncated start is visually suitable as a short repositioning step.



After an actor snapshot round trip, exercise the actual disk write/read and staged Continue path while the transition is active. Reacquire the controller after station restoration because Continue replaces it; compare physical position, action clock, arrival timer and selected texture bytes, then check pause/resume. Distinguish headless texture equality from native overlay/scene visual review. Restore the initial fixture checkpoint before continuing unrelated checks within the same regression.



When a video ignores a canonical facing, inspect the opening frame before tuning extraction. A generic image reference may be interpreted as identity guidance rather than an exact starting pose. Inspect the current model schema and CLI media bindings; where supported, try a dedicated start-image input and record that binding in the durable job. Preserve the rejected source and reason. A start-image binding is a constraint to verify, not proof of correct facing or motion.



For GIF previews of 30/60fps captures, round cumulative timestamps to the format's 10-ms timing grid. Rounding each frame independently can speed up the preview. Verify the encoded GIF duration against trace duration and report the timing quantum; preserve native raw frames for finer inspection. Keep simulation/capture cadence explicit and preserve idle duration when changing the number of samples per second.



For a source that translates through the frame, record root displacement explicitly instead of normalizing each pose bounding box. Subtract that track during extraction, preserve local torso weight transfer, and verify inverse translation reconstructs the original registered pixels exactly. Report landmark uncertainty and natural travel distance; reconstruction checks only prove registration reversibility, not planted-foot quality or suitability at arbitrary route lengths.



A short-step settling pose may legitimately remain active after path completion, but only at its recorded destination. Cancel its override immediately if the route changes or disappears before arrival, even before another movement tick. Check cancellation through the render query as well as through move; otherwise a stale pose can survive while gameplay has already switched routes.



Exercise specialized movement through the full actor update as well as direct move probes. A parent route-selection hook can arm an ordinary transition after a specialized move has already started, producing overlapping clocks hidden by render precedence. Snapshot validation can expose that overlap; guard the initiating hook and keep a regression that calls it while the specialized transition is active.



Preserve a native before-change capture under an explicit baseline directory before rerunning a fixture whose output name is deterministic. Keep its log and reviewed boundaries linked in the handoff; otherwise the after-change run can silently erase the evidence needed to judge improvement.



Use an explicit, uncertainty-labelled supporting-foot travel study before extending a locomotion controller to another direction. A fixed-grid contact preview can test pose-to-pose translation without changing runtime assets; hash the input frames and recipe. Record preview timing separately when it differs from extraction timing, and do not equate discrete contact alignment with continuous native foot locking.



If a transition source has correct intermediate motion but never reaches the required end stance, preserve the rejection and use an explicit end-image binding when the model supports it. Record both endpoint hashes and bindings. Matching endpoints can still conceal shuffling or foot sliding; review the full support sequence and derive runtime travel from the resulting source rather than the prompt.



When production timing differs from an extraction study, preserve both duration lists in rebuild provenance and hash the selection manifest as well as the source video and recipe. A rebuild summary must count every emitted supplemental pack; verify selected PNG/manifest bytes remain unchanged for provenance-only repairs.



## Side-view body motion follow-up — September 20, 2026



Bill's selected leg repair preserves one upper-body pose across all six slots with

only a one-source-pixel bob. This passes registration, planting and coverage checks

but leaves shoulders and arms rigid. The owner's renewed walk complaint supersedes

any implication that September 12's technical acceptance settled natural gait.

When repairing identity drift, protect the face/head region without automatically

freezing the entire torso and arms. Review body counter-motion alongside planted

feet. Recover preserved upper-body motion separately from the rejected original

leg cycle; verify waist seams and equipped head alignment. See the current

BILL_WALK_REVIEW_2026-09-20 handoff for baseline evidence and remaining work.



For a localized motion-generation study, supply only the selected runtime row as

pose reference; mixing an old rejected leg cycle into a comparison-sheet reference

can make generation follow that cycle instead. Describe near/far arm phase explicitly.

A prompt to preserve legs or face is not evidence they stayed unchanged. Compare

actual pixels and shapes before integration. Register extracted frames with one

shared scale/pivot; do not independently normalize every pose. Preserve faint alpha

for inspection and distinguish a generated candidate from an accepted replacement.





Articulated cutout limbs need separate joint-surface acceptance: correct bone

lengths and planted-foot timing can still leave broken contours or alpha gaps.

Compare silhouettes and interior joints against preserved anatomy. Enclosed-hole

counts are diagnostic only; open notches and shading seams can fail with zero holes.

Preserve motion constraints without freezing flawed reconstructed pixels into later

repairs. See Bill's September 21 joint review for measured evidence and limits.





When a generated cycle repeats the same limb phase, test one explicitly opposite

contact pose before commissioning another sheet. Identify the near leg through

persistent equipment/occlusion, not just the requested label. If that single pose

also preserves the wrong overlap, stop wording-only retries and obtain a controlled

pose source. A changed arm does not prove the leg phase changed. Preserve failures

and prompts; never install them because the joints look cleaner.



For an upper-body motion repair with fixed head registration, reuse the canonical

helmet overlay recipe and first prove it reproduces selected equipment pixels.

Then compose it over candidate bodies and test through load_equipment_manifest;

matching filenames alone does not establish phase/pivot compatibility. Isolate

unchanged leg pixels with assertions so arm review cannot silently change contact

motion. Pixel connectivity detects detached fragments, not natural joint shading.


Do not generalize Bill's repaired joint pinholes into an automatic full-cast fill.
When legs overlap at both ends, legitimate between-leg background becomes an
"enclosed hole" to a flood-fill detector. Review the anatomy and source before
classifying it. Likewise, distinct upper-body hashes rule out exact duplicates but
do not prove visible arm swing or natural motion. Resolve base and supplemental
runtime clips separately when describing audit coverage.

Bill's selected side repair has a focused regression guard:
`python -m unittest discover -s tests -p test_bill_walk_surface.py` checks bob-
registered upper variation, fixed-head registration and exact canonical body/helmet
reproduction. It was verified against an injected frozen-torso mutation. Keep this
separate from the complete-pack manifest check and visual gait acceptance.

Review commands must reproduce the selected runtime repair, including restored
upper-body phases and canonical helmet overlays. The standalone Bill walk command
is covered by test_bill_walk_surface.py: all 24 exported side-view body/helmet
frames must match production. A correct production builder does not prove an older
preview entry point is current. Keep head-preservation metrics separate from arm
motion; freezing the whole upper body is not an identity-preservation success.

Bill dry cargo uses separate carry clips through human_water_player; base walk
repairs do not cover those clips. Compare selected manifests and route selection
before claiming locomotion coverage. Align cross-clip sheets by declared pivot
and standingHeight, not canvas edges: carry and base walk have different canvases.

Cast review boards must load crew catalogs through the selected REVISION_ROOTS,
not retired direct manifest paths. Use texture pivot/standingHeight and preserve
aspect ratio across different canvases. Missing action coverage should be labeled,
not disguised by idle fallback; loop review clips deliberately. Keep capture and
coverage checks separate from visual acceptance. test_sprite_polish.gd now accepts
--states=walk,carry and --output=res://... for a bounded current-cast review.

A generated local pose repair is not a drop-in frame even when the composition
looks aligned. Inspect alpha bounds at multiple thresholds: faint stray alpha can
inflate bounds. Preserve the raw source, record resampling/palette/repair-band
operations, and restore protected original regions exactly. Review neighboring
poses before installing a single cleaner knee; the resulting shape discontinuity
can worsen the clip even when the isolated still improves. See the September21
passing-pose candidate for an uninstalled example, not an accepted recipe.


For raised-foot poses, a horizontal repair band does not prove boots are preserved.
Use the articulated source foot masks, restore protected pixels from the current
frame, and report that exact scope. The September21 adjacent-pose study caught
19/5/74 boot-region pixels in phases1/2/3 that the band-only check missed.


Pixel preservation must include protected transparency when silhouette is invariant.
Keeping only original opaque foot pixels still allows new opaque pixels nearby.
The east-loop candidate therefore has a separate foot-bounds-v2 study restoring
the entire source foot rectangles. This is conservative around ankle overlap;
review that boundary visually rather than calling any protected-region assertion
whole-animation acceptance.

Track distinguishing knee details on the same near/far limb through crossings. Independently repaired poses can attach a pad to whichever knee is forward. Conversely, extracting visible patches from a composited pose does not provide the hidden fabric needed for articulation: prove complete joint coverage before expanding the loop. Bill September21 coherent-knee study is rejected evidence of this failure, not a production recipe.

For complete replacement limb sources, record explicit source hip/knee/ankle landmarks and component masks. Fit each bone to the existing trajectory; do not substitute sprite bounding-box alignment for articulation. Keep raw source, normalized candidate and native player evidence separate. Original boot rectangles can protect contact pixels while the intervening joint shading still needs visual review.


## Bill West shared-standing anatomical calibration - October 2, 2026

Source character/bill-water-exit-west-master-v8 replaces Knee tuck only;14other
complete gear poses exact,16decoded APNG frames/holds exact500ms finite.30frozen
inputs current;2publishers parse; raw alpha and PNG/APNG LFS filters checked.
Original-first trial exec-83ba4497-5319-4ae8-9862-c03ed4b5ae96 still oversized
233x257 head proxy, retained/rejected. Original-only two-figure generation
exec-31b84f04-299f-40e3-a854-9ceda91a3250 includes standing ruler:958opaque pixels,
one148/958 whole-source scale for both figures,137x150 knee vs140x143neutral head.
Neutral faces East contrary to requested West: height calibration ONLY, not West
idle acceptance or a mirrored source. Cropped original West-only reference prepared
for NEXT generation; do not claim it was used for this past knee request.

Raw/head/whole/master-neighbor boards reviewed; normal/quarter source playback
terminal Standing8/8 restores Play; paused knee5/8 screenshot retained. Body/collar
much closer original anatomical proportions. Mixed sequence visibly jumps between
new knee and larger older bodies/arms. Do NOT enlarge the corrected knee to match
older oversized art. Same1536x1024canvas and borrowed148/956standing denominator
never established generated anatomical scale; fixed21x23bare/40x40helmet protects
identity only, not torso/limb/neck scale. Rebuild surrounding whole sources with an
independent same-sheet standing ruler, then review both joins, matte finish and
actual station motion/contact. No per-pose body/limb fitting or mirrored equipment.

V8 remains mixed_scale_comparison_unselected. NativeV7 3905checks covers sourceV6
only, not V7push/V8knee; prior source/root/clock proofs retain original scope.
Current native material/head-overlay placement, continuous palm/knee/toe contacts,
natural hazards/checkpoint/visible Continue and normal admission remain pending.
North/South master repairs and full-library consistency/polish still required.
Full Bill objective active/incomplete. Handoff:character/bill-water-exit-west-master-v8/HANDOFF.md.


## Bill West calibrated palm-to-knee source join - October 2, 2026

character/bill-water-exit-west-master-v9 updates Palm push index3 only fromV8;
14other complete gear poses exact, including corrected Knee tuck. Original West-only
crop sole reference for builtin exec-2d5a29f3-d81c-41f2-bb75-97b5a26e73a8; neutral
now correctly LEFT-facing. Shared sheet neutral opaque height956 gives148/956 for
both whole figures. Head proxy135x139 action vs139x141neutral: much closer original
adult proportions; this bounded proxy is not full bone-length/camera acceptance.
Whole crown-X134/lowestpaint224 translation, no body/limb/posed-height fitting.
Registered crown134147, bare21x23 at128146, helmet40x40 at119133 native1/rotation0.
Nonempty exact opaque donor checks31bare/247helmet, protected outside/foreground/
below-head checks pass, one connected bare silhouette and no alpha clipping.
32current frozen inputs,16APNG phases/holds exact500ms finite; publisher AST and
both generation original/copy/reference/prompt hashes pass; raster LFS confirmed.

Raw/neck/master-neighbor/full chronology boards seen. Corrected palm and knee are
closer in body scale and quiet matte finish; remaining lower-hands/low-elbow and
half-kneel/rise look oversized, final selected standing darker. Normal/quarter
source playback reachesStanding8/8 and restoresPlay; pausedPalm4/8 browser screenshot.
Not continuous contact, complete cross-family/master acceptance or native admission.
NativeV7 tests sourceV6 only; no V9 native interval or normal selection change.

A background-removal second trial exec-d583d482-7f40-4fbb-99a9-f33395a92546 retained
unused: visible raw-viewer brown/grey halo was RGB under alpha0, not an opaque
background. Inspect alpha and composited sprite before requesting extraction; do
not change valid anatomy/material to fix invisible RGB. Second trial changes suit
shading unnecessarily. Preserve generated alpha, both originals and exact recipes.
On Windows distinguish saved CRLF file-byte SHA from submitted LF prompt-text SHA;
record both instead of reporting mismatched hashes as exact provenance.

Next independently calibrate old low-elbow/lowering and later half-kneel/rise whole
sources against original West-only master and shared standing ruler; then compare
both joins and current-bank head-readability overlay/contact/hazards/restore/Continue.
North/South master repair, full-set consistency/polish and normal integration remain.
Full Bill goal active/incomplete. Handoff:character/bill-water-exit-west-master-v9/HANDOFF.md.


## Bill West calibrated hand-lowering and elbow support - October 2, 2026

Source V10 replaces Low elbow index2 fromV9; V11 replaces Lower hands index1 fromV10.
Both builtin original West-only reference requests, retained exact prompts and raw
originals. Jobs exec-8fa7170b-c191-4452-9088-c9711cf1a43d (support) and
exec-0fcbeac2-42b5-4600-bffd-2c8403f87ad4 (lowering). Same-sheet LEFT-facing standing
rulers947 and908opaque pixels establish one148/947 or148/908 whole-source scale
for each respective sheet; no per-pose body/limb fitting or mirrored equipment.
Support head proxy145x155 vs neutral140x141; lowering130x138 vs136x138neutral.
These bounded hair/face proxies indicate much closer master-sized heads but do not
certify full skeleton, elbow angle, perspective or material invariants.

V10crown134164,bare128165,helmet119152,hip184195;V11crown126166,bare120165,
helmet111152,hip165198. Crown-X/lowest painted support224 translation only;
equipment markers/lowestpaint do not prove continuous palm/knee/toe contact.
Shared21x23bare/40x40helmet native1/rotation0 donors and protected outside/head/
foreground checks pass; nonempty opaque checks32bare/247helmet V10,34/247 V11.
One connected significant bare silhouette/no alpha clip. Each32inputs current,
14other gear poses exact,16APNG phases/holds exact500ms finite; two publisher ASTs,
source original/copy/ref/saved-file/submitted-text hashes and raster LFS verified.
V11 preserves both prior calibrated palm/knee plus new support exactly.

Both raws, neck/master-neighbor/full chronology boards seen. Four interior poses
now closer in anatomical scale and quiet matte finish. Old swimming endpoint,
half-kneel/rise are larger, selected final standing darker; these joins remain open.
Low-elbow bend and weight-bearing hand tracking still visually provisional.
V10 normal source playback reachesStanding8/8/restoresPlay, support3/8 paused.
V11normal/quarter reachesStanding8/8/restoresPlay, lowering2/8 screenshot retained.
Source cadence samples and exact exports do not establish full native contact,
head-readability overlay registration, natural hazards/checkpoint/Continue or normal
admission. NativeV7 3905checks still sourceV6 only; neither new bank selected normally.

Lesson: measure neutral height on EACH generated sheet (947 and908 here), not its
fixed1536x1024 canvas or a borrowed denominator. Scale neutral and action together,
retain natural lower posed height and independent head/limb/shoulder review. Comparing
both neighbors exposes the remaining oversized endpoints; repair them against the
original rather than expanding calibrated sources. Keep metadata provenance dynamic
from the actual measured neutral height. Whole-library objective active/incomplete.
Next calibrated half-kneel/rise and swimming family/endpoints, then current native
contact/overlay/lifecycle/save/Continue checks; North/South and full-set polish remain.
Handoff:character/bill-water-exit-west-master-v11/HANDOFF.md.


## Bill West calibrated rise and current idle endpoint - October 2, 2026

Source character/bill-water-exit-west-master-v12 replaces Half kneel/Rise indices5/6
fromV11 using ONE builtin original West-only request exec-3cb7f4cc-e497-447d-965f-ec3aec43be35.
Three complete LEFT-facing figures: standing ruler + both actions; original raw,
exact prompt/ref/source hashes retained. Neutral949opaque pixels -> one148/949
whole-source scale across allthree figures; no per-pose/body/limb fitting or mirrors.
Bounded heads neutral139x143,half138x151,rise140x150; much closer original head/body
scale, not full anatomical/angle/contact acceptance. Whole crown-X/lowestpaint224
translation: half150112,bare144113,helmet135100,hip161170;rise15788,bare15188,
helmet14275,hip163149. Shared21x23bare/40x40helmet native1/rotation0; exact protected
body/foreground/below-head, nonempty opaque donor31bare/247helmet half and34/247rise,
one significant connected bare silhouette/no alpha clip pass.

Endpoint audit found legacy bare standing image NOT current configured idle:
ordered _load_major_bill_animations and crew_sprite_player source resolution read;
actual crew-runtime-matte-v1/bill manifest idle-west selects
frames/idle-west-breathing-v1/000.png, not similarly named frames/idle-west/000.png.
Old endpoint proxy27x20 differs from legacy named idle21x22; do not generalize that
bounded diagnostic to all normal heads. V12 bare final now exact CURRENT manifest
frame0 padded[68,52] from184/p92/172/H148 into352/p160224.5426visible pixels changed;
no resize/mirror/recolour. Helmet old endpoint already exact current configured
bill-shared-helmet-runtime-v2 idle-west0 and retained. Two manifests/current frame0s
and loader scripts included in38bounded build inputs. This is current configured
source/metadata parity, NOT new native loaded/moving gait acceptance.

11other complete gear poses exact fromV11,16APNG phases/holds exact500ms finite.
38inputs current/stable; both publisher ASTs, generation original/copy/ref/prompt
file-byte/submitted-text SHA and PNG/APNG/screenshot LFS checked. Raw, paired neck,
master-neighbor and whole chronology boards seen. Normal/quarter source playback
reachesStanding8/8/restoresPlay, Half6/8 paused screenshot retained. Six interior
poses now closer original anatomical scale; older swimmer still larger and current
configured idle visibly darker. Continuous support-foot/hand/knee tracking, whole
master grade/perspective/body proportions and native overlay/hazards/checkpoint/
visible Continue remain open. No normal catalog/controller changes; nativeV7 3905
checks covers sourceV6 only. Current new bank unselected, full Bill goal incomplete.

Lessons: use a shared standing ruler for coupled articulated actions; inspect
both joins instead of only a corrected pose. A preserved old endpoint is not a
current runtime join. Resolve the actual state's frameFiles through ordered loader
bindings and profile, including breathing/state overrides; test positive-alpha
source pixels and pivot padding, preserve transparent RGB semantics. Keep static
source parity separate from actual loaded/native gait and restore evidence.
Next calibrate West swimmer family/endpoints and reconcile original master vs idle
matte grade without losing quilting/skin detail; then current-bank physical contact,
head-overlay and native lifecycle/save/Continue review. North/South and full-library
polish/integration still required. Handoff:character/bill-water-exit-west-master-v12/HANDOFF.md.


## Bill West standing-calibrated swimming Extend and exit join - October 2, 2026

Source character/bill-swim-west-calibrated-v1 corrects Extend only using builtin
imagegen exec-3082dc8a-18f6-41e7-86a5-f2d5581e64b3, original West crop sole authority.
Standing ruler 933 opaque pixels gives one148/933 scale to both complete figures;
head proxies neutral137x140/action134x140. Whole equipment-hip registration192237
preserved; not ground-contact proof. Six older stroke phases and12gear poses exact.
30current frozen inputs,14decoded APNG poses/holds exact960ms infinite; metadata
arrays and stride retained. Original/copy/ref/saved/submitted prompt hashes pass,
three publishers parse, raster LFS confirmed. Extend/neck/master/paired boards seen.
Normal/quarter playback samples Extend and Sweep; full loop wrap not independently
certified. Corrected Extend visibly smaller than older six phases; mixed comparison
unselected. Shared heads protect identity, not full underlying anatomy/articulation.

Source character/bill-water-exit-west-master-v13 copies both corrected Extend
endpoints exactly;14other gear poses fromV12 exact,16APNG phases/holds500ms finite.
31current frozen inputs after rebuilding against scoped Swim review. Full current
exit chronology seen; normal/quarter source playback endsStanding8/8/restoresPlay.
Swimming1/8 screenshot retained. Other three comparison boards copiedV12 unchanged,
not evidence of new swimming join. Current configured standing endpoint remains
visibly darker; actual contact/root, original material/perspective and shoulders
remain provisional. No normal selection/controller changes, no new native test.
NativeV7 coverage remains sourceV6 only, not either current candidate.

Lesson: calibrate the entire swim family, preserve coupled exact transition endpoints,
water/facing arrays and clocks. Equipment-hip registration preserves source continuity
but proves no flotation/contact. Do not enlarge corrected poses to older oversize art.
Next original-master/shared-standing Sweep then Pull/Gather/Recover/Reach/Glide;
update entry bridge (still older swimmer), grade without losing quilt/skin detail,
then current native overlay/contact/natural hazards/checkpoint/visibleContinue.
North/South and full-library consistency/polish/integration remain. Full Bill goal
active/incomplete. Handoffs in both new candidate folders.


## Bill West shared-standing arm sweep - October 2, 2026

Source character/bill-swim-west-calibrated-v2 replaces Sweep index1 only fromV1.
Builtin exec-08345d9f-1d78-4317-b1a4-b5b3c223375c original West-only crop sole
reference. Raw preserved immediately with exact LF prompt/job/ref/source hashes.
Both LEFT-facing complete figures share standing951opaque-pixel ruler, one148/951
whole-source scale. Neutral head142x144/action145x156 proxy: closer original adult
build, not full skeleton/camera approval. Whole hip-equipment192237 translation,
not physical water support; crown152201,bare146202,helmet137189. Shared21x23/40x40
heads native1/rotation0, nonempty opaque33bare/247helmet checks exact, protected
outside/foreground/below-head regions, one significant bare silhouette/no alpha
clipping pass. Corrected Extend exact; five older phases also retained:12other
complete gear poses exact.14decoded APNG phases/holds960ms infinite; water/facing/
depth array lengths and stride retained.30current frozen inputs, two publishers
parse, original/copy/ref/saved/submitted prompt hashes and raster LFS checked.

Raw, paired neck, original/neutral/prior/Extend/Sweep/Pull comparison and full paired
chronology seen. PausedSweep2/7 browser screenshot; normalPull3/7, quarterGather4/7
andReach6/7 sampled. Full loop wrap not independently certified. Extend/Sweep now
closer in body scale and quiet matte finish; five larger/brighter old poses remain.
Full skeleton/shoulders/head attachment/grade/articulation/flotation not accepted.
New bank unselected; no normal/controller changes and no new native test coverage.
Water exitV13 still shares exact unchanged Extend endpoint; entry still older source.
NativeV7 test scope remains sourceV6, not this new family.

Lesson: measure each sheet's standing ruler independently and compare both neighbors
at fixed native equipment scale. Similar head proxies are diagnostic, not proof of
whole limb/torso/camera consistency. Keep muted hardware AND quilt texture while
repairing articulated whole poses; do not enlarge corrected sources to oversized
neighbors or resize limbs separately. Next Pull/Gather/Recover/Reach/Glide, update
entry endpoint, then grade/current native contact/overlay/hazards/restore/Continue.
North/South and full-library cross-family polish/integration remain. Bill objective
active/incomplete. Handoff:character/bill-swim-west-calibrated-v2/HANDOFF.md.


## Bill West shared-standing arm pull - October 2, 2026

Source character/bill-swim-west-calibrated-v3 replaces Pull index2 only fromV2.
Builtin exec-ee96903d-57f5-492b-99d3-6289625e190c used sole original West crop.
Raw retained immediately, exact LF prompt/job/ref/source SHA. Both LEFT-facing
figures share standing936opaque-pixel ruler, one148/936 whole-source scale.
Neutral head136x137/action143x159 proxy: no complete skeleton/camera acceptance.
Whole hip-equipment192237 translation retained, crown149195,bare143197,helmet134184.
Two small cyan indicators10/11source pixels remain independently located in bounded
hip ROI; equipment proxy is not anatomical contact. Shared21x23/40x40heads native1/
rotation0; nonempty opaque32bare/245helmet exact (some foreground overlaps helmet),
protected outside/foreground/below-head, one connected bare silhouette/no clip pass.

Corrected Extend/Sweep and four older phases exact:12other complete gear poses.
14decoded APNGframes/holds960ms infinite; facing/water/depth arrays and stride kept.
30current frozen inputs, two publishers parse, original/copy/ref/saved/submitted
prompt hashes pass; raster LFS confirmed. Raw/neck/master-neighbor/full paired
chronology seen. PausedPull3/7 screenshot; normalRecover5/7 and quarterExtend1/7
playback samples. Full loop/cadence wrap not independently certified. First three
poses closer in body scale and matte finish; four older phases larger/brighter.
Underlying neck/shoulders/skeleton/perspective/grade/articulation/flotation pending.
No normal selection/controller changes or new native acceptance. ExitV13 keeps
exact unchanged Extend, entry still older swimmer. Historical nativeV7 scope stays
sourceV6 only. Full Bill objective active/incomplete.

Lesson: a cropped/occluded hip indicator can still supply a bounded equipment
registration proxy; preserve its actual source count/center, never substitute a
floor/support claim. Keep both neighbor joins and actual source metadata in review.
Copied preview prose can silently retain old phase counts; verify rendered status
and update publisher wording before handoff. Next Gather then Recover/Reach/Glide,
entry coupling, matte idle join, then current native contact/overlay/hazards/
checkpoint/visibleContinue. North/South and full-library consistency/polish and
normal integration remain. Handoff:character/bill-swim-west-calibrated-v3/HANDOFF.md.


## Bill West gathered-hands independent scale check - October 2, 2026

Source character/bill-swim-west-calibrated-v4 replaces Gather index3 only fromV3.
Two builtin original-West-only trials retained with raw/prompt/ref/job SHA. First
exec-100fc923-3ed4-465a-817e-c829870628e5 is1774x887, standing839, neutral128x128
vs action143x156 head proxy; retained unselected because swimmer enlarged relative
to ruler. Second exec-29a562b7-8dc5-47a3-9d00-bf33bfb3f420 is1536x1024, standing938,
neutral145x142 vs action143x144. Shared one148/938 whole-figure scale; no limb/body
fitting. Both LEFT-facing, muted quilt and dull hardware. Full skeleton/camera and
head attachment still provisional. Whole hip192237 translation; crown147200,
bare141200,helmet132187; shared21x23/40x40 native1/rotation0, exact nonempty opaque
32bare/247helmet and protected outside/foreground/below checks, connected bare/no
alpha clip pass. Extend/Sweep/Pull and three old phases exact:12other gear poses.
14decoded APNGframes/holds960ms infinite; arrays/stride retained.30current inputs,
two publishers parse, BOTH original/copy/reference/prompt hash sets and LFS pass.

Both raw sources, neck/master-neighbor/full paired boards seen. PausedGather4/7
screenshot; normal/quarterReach6/7 samples. Full cycle/wrap not independently
certified. First four poses closer scale/matte; three older phases larger/brighter.
Unselected comparison, no current native test or normal/controller changes. ExitV13
shares unchanged Extend; entry still older. NativeV7 covers sourceV6 only. Full
master/shoulders/grade/articulation/flotation, current contact/overlay/hazards/
checkpoint/visibleContinue and normal admission remain. Full Bill goal incomplete.

Lesson: shared sheet alone does not ensure shared physical scale. Check ruler and
action independently before canonical head fitting; V1 mismatched skull ratios
would otherwise be hidden. Preserve rejected whole source, correct generation,
never separately shrink the posed torso/head to force parity. Canvas dimensions
also vary; derive density from measured neutral, not assumed tool size. Next
Recover/Reach/Glide, entry coupling and idle grade, then current native review.
North/South and whole-library polish/integration remain.
Handoff:character/bill-swim-west-calibrated-v4/HANDOFF.md.


## Bill West swimming recovery scale and body-angle review - October 2, 2026

Source character/bill-swim-west-calibrated-v5 replaces Recover index4 only fromV4.
Builtin exec-06edec0a-b78b-48a5-92a8-84d2677068c3, original West crop sole reference;
raw/prompt/job/ref SHA retained. Standing952opaque pixels -> one148/952 whole-source
scale. Neutral138x138/action137x137 head proxy, both LEFT-facing. Whole hip192237
translation, crown157200,bare151198,helmet142185. Native21x23/40x40donors, exact
opaque39bare/247helmet; protected outside/foreground/below, connected bare/no clip.
12other complete gear poses exact fromV4:four calibrated/two older phases retained.
14decoded APNGframes/holds960ms infinite; water/facing/depth arrays and stride kept.
30current inputs, two publishers parse, original/copy/ref/prompt hashes and LFS pass.

Raw/neck/master-neighbor/full paired boards seen. PausedRecover5/7 screenshot;
normal/quarterReach6/7 samples, full loop/wrap not independently certified. First
five phases closer physical scale/subdued finish. Recovery body angle steeper than
Gather, forward arm path/kick/shoulder attachment still provisional; do not confuse
skull-size parity with full articulation/camera acceptance. Reach/Glide remain
larger/brighter. No normal selection/controller changes or current native test.
ExitV13 shares unchanged Extend; entry older; historical nativeV7 sourceV6 only.

Lesson: compare body orientation and shoulder/hand trajectory separately from
shared-standing scale. Preserve actual whole-pose angle while diagnosing joins;
no limb fitting or unreviewed rotation to conceal discontinuity. Next Reach/Glide,
then complete-loop original/neighbor grade/proportion/cadence review and entry
coupling. Current native overlay/contact/hazards/checkpoint/visibleContinue,
North/South and whole-library polish/integration remain. Full Bill goal incomplete.
Handoff:character/bill-swim-west-calibrated-v5/HANDOFF.md.


## Bill West seven-pose standing-calibrated swim bank - October 2, 2026

Source character/bill-swim-west-calibrated-v6 replaces Reach/Glide indices5/6;
10other complete gear poses exact fromV5, all seven now standing-calibrated.
Two builtin original-West-only jobs exec-6470e532-158b-425f-a478-9f193912d4c1 and
exec-a80452f2-68ce-4e19-9dc8-b6d107581224. Both raw/prompt/ref/job SHA retained.
Reach standing949 ->148/949, neutral132x136/action133x141 head proxy; Glide standing
893 ->148/893, neutral131x136/action131x125. Separate rulers/whole scales recorded
PER JOB, no shared-last-job density assumption or separate limb fitting. Hip192237
translation for both. Reach crown148202,bare142201,helmet133188; Glide crown148207,
bare142205,helmet133192. Native21x23/40x40heads, opaque35/36bare and247helmet exact;
protected body/foreground/below checks, connected bare/no alpha clipping pass.
34current frozen inputs, two publishers parse, both original/copy/ref/prompt SHA
sets and LFS pass.14APNGframes/holds960ms infinite; arrays and stride preserved.

Both raws, paired Reach/Glide neck, original/neutral/prior/Recover/Reach/Glide and
full paired boards seen. Actual browser UI observes Glide7/7 -> Extend1/7 at BOTH
normal/quarter speeds, remains playing; pausedGlide screenshot. This proves source
wrap occurrence, not smoothness/native clocks. First complete independently
standing-calibrated stroke bank remains unselected. Steeper Recover body angle,
shoulder/hand path, kick cadence, bone/torso/camera and full grade still provisional.
No old oversized stroke phase retained; entry bridge STILL older swimmer, exitV13
shares exact unchanged Extend. No normal/controller changes or new native test.
Historical nativeV7 sourceV6 exit only, not this new swimmer.

Lesson: batch distinct whole poses with separate standing rulers, preserve measured
per-job scale/provenance. Review full cycle including final-to-first at actual
playback speed; distinguish observed UI wrap, exact APNG clock and physical motion
acceptance. Source completion starts consistency/polish, does not imply full-set
acceptance. Next whole-loop body-angle/articulation/grade comparison and entry
coupling, then current native contact/overlay/hazards/checkpoint/visibleContinue.
North/South and full-library consistency/polish/integration remain. Bill goal active.
Handoff:character/bill-swim-west-calibrated-v6/HANDOFF.md.


## Bill West current idle and calibrated swim entry endpoints - October 2, 2026

Source character/bill-land-water-west-v13 updates entry indices0/6 fromV12,
10other complete interior gear poses exact. Initial exact current manifest-selected
bare idle-west-breathing-v1/000 and shared-helmet idle-west/000, whole padding68/52
from184x184/p92/172 to352x320/p160224/H148; also exact exit-masterV13 final. Last
exact calibrated-swimV6 Extend0, also exact exit-masterV13 initial.4coupled endpoint
images exact across both gear modes. No body resize/recolor/mirror. Actual current
idle manifests/frame0s frozen, not inferred from similarly named legacy sources.
29current input hashes/publisher AST/pivot/height/loopfalse pass;14decoded APNG
frames/holds exact500ms finite. Raster LFS confirmed. Full paired entry and old/new
endpoint boards seen. Normal/quarter source playback reachesSwimming7/7/restores
Play entry, terminal screenshot retained.

CONSISTENCY_AUDIT.md records remaining visible issues: Ready head/body larger and
brighter than configured idle; Levelling/Near-prone broader/brighter than corrected
swimmer. Current idle darker than original-calibrated action family; preserve quilt
and skin detail during grade. Swim Recover body angle, shoulder/hand trajectory and
kick/wrap smoothness still provisional. Endpoint coupling fixes state context but
makes no interior anatomy/material/contact acceptance claim. Both native/control
and normal admission remain unchanged. Historical nativeV7 sourceV6 only; no new
native interval covers current swim/entry/exit banks.

Lesson: synchronize BOTH contexts using actual selected frameFiles, not a preserved
legacy idle or old swim endpoint. Same metadata is insufficient: assert exact source
pixels/pivot padding and paired entry/exit endpoint identity. Exact endpoints expose
interior defects; never use that narrow pass as full physical transition acceptance.
Next whole Ready repair with original West-only master/shared standing ruler, then
remaining entry interiors and full-family grade/articulation polish; current native
overlay/contact/hazards/checkpoint/visibleContinue. North/South and full-library
consistency/polish/integration remain. Full Bill goal active/incomplete.
Handoff:character/bill-land-water-west-v13/HANDOFF.md.


## Bill West shared-standing Ready and Crouch entry repair - October 2, 2026

Source character/bill-land-water-west-v14 replaces Ready/Crouch indices1/2 only
fromV13. One builtin original-West-only three-figure request
exec-132583dc-abbc-4659-94c3-a9029d074569; raw/prompt/job/ref SHA retained. All LEFT-
facing share standing964opaque-pixel ruler, one148/964 whole scale; neutral138x145,
Ready138x142,Crouch139x148head proxies. No limb/body fitting. Whole lowest painted
sole-band midpoint160/support224 translation. Bottom12source-row sole boundsReady
682969853981,Crouch12159701380982 are registration proxies, NOT physical continuous
foot contacts. CrownReady15079/Crouch13791, bare14478/13191, helmet13565/12278.
Native21x23/40x40donors, nonempty opaque33bare/247helmet each exact; protected
outside/foreground/below regions, connected bare/no alpha clipping pass.

10other complete gear poses exact, including current idle and calibrated swimmer.
Four coupled entry/exit endpoint images exact.28current frozen inputs/two publisher
ASTs/raw/ref/prompt SHA/LFS pass.14decoded APNGframes/holds500ms finite. Raw/neck/
original-neutral-idle-Ready-Crouch-Push comparison and paired chronology seen;
normal/quarterSwimming7/7 terminal restoresPlay entry, pausedReady2/7 screenshot.
Ready/Crouch closer master-sized quilt detail and subdued finish; current idle
darker and three airborne old interiors larger/brighter. Full skeleton/shoulder/
perspective/grade/contact/cadence/native acceptance remains pending. No normal/
controller changes or new native coverage; historicalV7 sourceV6 scope unchanged.

Lesson: coupled entry articulation benefits from one independent standing ruler,
while each whole figure gets its own painted support registration. Do not flatten
posed height or confuse low sole pixels with actual foot contacts. Keep neighbor
joins, ground approach and current idle grade separate from donor identity checks.
Next original-master/shared-standing Push off, Levelling and Near prone, then whole
water-family grade/articulation/current native overlay/contact/hazards/checkpoint/
visibleContinue. North/South and full-library polish/integration remain. Bill goal
active/incomplete. Handoff:character/bill-land-water-west-v14/HANDOFF.md.


## Bill West complete calibrated entry and raised-arm head masking - October 2, 2026

character/bill-land-water-west-v15 replaces Push off, Levelling and Near prone;
8 other complete gear poses exact from V14. All five entry interiors now use
original-West-only generated whole figures with measured standing rulers. Push
943 ->148/943; shared Levelling/Near947 ->148/947. Two built-in jobs
exec-955259cc-a6b6-4b63-8690-0f51866ba6d8 and
exec-a594e7aa-a800-4cf0-a156-41776f5c3b79; raw originals, exact LF prompts,
reference/job/source hashes retained. Measured action ROIs follow actual paint,
not intended prompt slots: upper figure extends to658, lower begins688.

Initial head erasure detached the raised far hand. Retained failed diagnostic;
corrected bounded grey foreground restoration on both sides of the head and
helmet left overlap. Do not resize limbs/equipment or relax connectedness checks.
Current protected body/foreground/below-head and connected/no-clip checks pass;
opaque donor pixel checks bare32/37/37, helmet228/226/221. Hip proxies176172,
176204,189224; lowest painted pixels241/243/232 are not physical support acceptance.

32 current frozen inputs, 2 publisher ASTs, both original/copy/ref/prompt SHA sets,
5 raster LFS paths and 4 paired entry/exit endpoints pass. Build14 decoded APNG
frames/holds500ms finite. Normal/quarter UI reachesSwimming7/7 and restoresPlay
entry; pausedPush4/7 browser screenshot. Raw/neck/full paired boards previously
seen; original-master board and current paired browser reviewed this interval.
Idle remains darker; shoulders, body angles, hand/kick path, camera/material and
root/contact remain provisional. No normal selection/controller changes or new
native coverage. Historical nativeV7 covers older source banks only.

Next whole water-family entryV15/swim-calibratedV6/exit-masterV13 consistency,
then current native overlay/contact/hazards/checkpoint/visibleContinue and normal
admission. North/South and full-library consistency/polish remain. Full Bill goal
active/incomplete. Handoff:character/bill-land-water-west-v15/HANDOFF.md.


## Bill West joined water-family consistency audit - October 2, 2026

October 2, 2026. Source-only, unselected. EntryV15, swimV6 and exitV13 use the same352x320 canvas,p160224,H148. Review sequence29slots/2920ms includes two swim cycles; these are timing slots, not29unique drawings.44source drawings,6manifests and originalWestcrop frozen (51inputs).

1. Current configured idle/standing is visibly darker than original-master-calibrated actions; whole-grey medians52.33bare/54.33helmet versus roughly68..75.5 actions. Metrics include hardware and differing poses: diagnostic only, not a grading formula.

2. Exit Swimming to Lower hands shifts crown from152205 to126166 (26left,39up source pixels). Lower hands hold40ms after60ms swim context. Full current source root/contact review needed before accepting physical transition.

3. Near prone to Extend changes equipment hip from189224 to192237; 3right/13down source pixels. Source gear marker registration is not world root.

4. Swim Pull/Recover body-angle and hand/kick construction change; common head identity and standing denominator do not establish articulation continuity.

5. Entry/swim/exit contexts match exactly in both gear modes, but same ending pixels do not guarantee matching neighboring frames or arbitrary active-stroke-to-exit joins.

Repair order: evaluate native root/head-overlay and support trajectory for current family; correct exit launch and entry settle at whole-source/root contract, then source-grade current idle against master and all normal idle joins, then stroke body-angle/hand/kick polish. No global brightness multiplier or separate body/limb shrinking. Current fixture evidence covers older banks only. North/South master repair and full-library consistency remain.

Evidence:character/bill-west-water-family-audit-v1/review.json and HANDOFF.md.
Normal and quarter UI reachStanding29/29 and restorePlay; one quarter wait timed
out during advancingGather18/29, subsequent terminal observation completed.
Current swim/exit/master boards and browser seen. Five LFS rasters and publisher
AST pass. Lessons: diagnose context joins, arbitrary active-stroke joins, physical
roots, material and articulation separately. Whole-grey diagnostic includes
hardware; it must not become a global brightness correction. No normal runtime
changes. Full Bill goal active.


## Bill West current water-family native baseline - October 2, 2026

character/bill-land-water-material-west-v8 now uses entry-westV15,
swim-west-calibratedV6 and exit-west-masterV13 in an isolated native fixture.
3905checks/0failures,126.55s,0engineerrors;545 bounded input hashes stable DURING
interval and current after.2931owner non-log files unchanged under scratchAPPDATA.
444originalPNG captures/232records;32selected advancing presentation crops reviewed
in four paired entry/exit boards. Five review raster LFS paths and six native UID
pairs pass. Synthetic guard checks pass but guard images not re-reviewed this turn.
No source/normal selection edits. Support hold remains fixture-only, actual needs,
oxygen/medium/safety/navigation and finite bridge clock continue.

Current bridges start1.116667 and6.916667, complete1.616667 and7.416667 on exact
incoming gait contexts. Current full-pose route240worldunits,y8368;22clear route
candidates. Active exit outgoing source is calibratedSweep1, NOT staticExtend0.
Dry outgoing/incoming source is actual256square walk gait, NOT configured idle.
Exact static context joins therefore cannot certify actual active-phase joins.
Root holds technically pass while anatomy/support contact and cadence remain
provisional. Historical head overlay positions retained for baseline; comparison
with current bare donor rectangles finds up to14.228worldunit displacement.
Rectangle center is a reproducible proxy, not accepted face/helmet center.

Rejected setup interval: first new launcher still invoked historicalV7 test,
capturePassedfalse,return0,owner2931files unchanged. Historical output captures
refreshed by that old test; do not relabel them currentV8. Corrected launcher and
UID generator explicitly targetV8; current interval above passed. Preserve failure
evidence; a native exit0 is insufficient without exact selected script/artifact.
First entry-board crop clipped right edge; corrected to its actual screen region
and both new boards re-reviewed. Review crop quality is separate from source clip.

Next current source-bound readability centers, identical-lighting baseline/fitted
comparison, actual gait/context and physical support repairs. Then full material,
stroke angle/hand/kick cadence, natural hazards/checkpoint/visibleContinue and
normal admission. North/South master repair and all-family polish remain. Full
Bill goal active/incomplete. Handoff:character/bill-land-water-material-west-v8/HANDOFF.md.


## Bill West source-bound bridge head readability - October 2, 2026

New fixture character/bill-land-water-material-west-v9 derives currentV8grid;
per-instance texture-to-center map links36gear/pose donor centers from current
source review hashes. Bare21x23/helmet40x40 rectangle centers; no shared texture
mutation, source pixels, body tint, timing or physical root changes. Current
11entry/exit interiors and7swim poses mapped pergear; dynamic gait endpoints
retain explicit historical fallback. Normal catalogue/controller unchanged.

4011checks/0failures,117.14s,0engineerrors;560bounded inputs stable DURING interval
and current after.2931owner non-log files unchanged scratchAPPDATA.106new per-tick
source/gear center checks.190progressing presentations match V8 exact sourceRGBA,
physical root/clock/water/medium/state/direction/path/material.22selected fitted
versus baseline native pairs reviewed in all fourboards; five raster LFS paths
and newUID pairs pass. Heads follow current artwork more closely, but unchanged
13x12world ellipse still reaches collar/shoulder pixels. No full motion/contact,
natural hazards/checkpoint/Continue or normal admission established. Guards tested
but guard images not newly reviewed. All native jobs terminal.

Lesson: source-bound center is separate from effect footprint and normal-renderer
path. Inherited flood_readability_v2 uses fixedWest(-22,-6) for ordinary swimming,
outside corrected bridge material path. Donor rectangle center is a calibration
proxy; do not claim exact face anatomy or full gear mask. Next fit source-bound
coverage and ordinary-swim center under same lighting while preserving tint,
weights/shadow/wake logic; independently fit actual dynamic gait endpoints.
Then active-phase joins/physical support, master-match idle and wholewater grade,
stroke articulation/cadence, lifecycle/checkpoint/visibleContinue/normal admission.
North/South master repair and full-library consistency/polish remain. Full Bill
goal active/incomplete. Handoff:character/bill-land-water-material-west-v9/HANDOFF.md.


## Bill West fitted head footprint and ordinary-swim renderer - October 2, 2026

Fixture character/bill-land-water-material-west-v10 derives V9grid, retains
current entryV15/swimV6/exitV13 artwork and source-center maps. Per-instance head
sizes21x23bare/40x40helmet yield worldellipse radii4.631x5.072bare/8.822helmet,
replacing old13x12. Ordinary-swim renderer now uses current selected source center
and size while preserving body tint/weights/shadow and wake formulas; wake/bubble
origin follows head. Dynamic walking context endpoints remain historical fallback.
No shared texture mutation, source pixels, clock, physical root or normal selection
change. Rectangle-based effect footprint is a proxy, not exact opaque head mask.

4207checks/0failures,122.94s,0engineerrors;562bounded inputs stable DURING interval
and current after;2931owner non-log files unchanged scratchAPPDATA.500originalPNG
captures.190advancing presentations exact source/root/clock/water/medium/state/
direction/path/material versusV9 baseline.22selected bridge pairs and14same-clock
ordinary-swim pairs reviewed in six boards, all seven poses/both gears. Ordinary
pairs at water.8/onephysicalroot use explicit fixture source override; establish
static renderer differences, not natural full stroke dispatch or smoothness.
Seven review raster LFS paths and new native UID pairs pass. No natural hazards,
checkpoint/visibleContinue/full contact/cadence/normal admission established.

Lesson: fit effect center AND coverage at physical source scale, and exercise both
transition and ordinary renderer branches. Preserve material policy while moving
pose-bound light/wake origins. Compare exact source/root/clock/water fields so a
lighting correction cannot hide anatomy or registration changes. Review crops use
actual observed screen regions; ordinary swim differs from entry route region.
Next actual256square walking gait endpoints/master-grade/anatomy/source-density
joins, then whole active-phase transition/support contact, idle/master and fullwater
grade, stroke hand/kick/body-angle cadence. Natural lifecycle/checkpoint/Continue
and normal admission, North/South and all-family consistency/polish remain. Full
Bill goal active/incomplete. Handoff:character/bill-land-water-material-west-v10/HANDOFF.md.


## Bill West actual walking-water master/context audit - October 2, 2026

character/bill-west-active-gait-water-audit-v1 resolves actual selected West walk
materialV1 through ordered loader sources and exact capturedV10RGBA. All96gait
files checked for unique context matches;117current frozen hashes,8context images
exact. Entrytick67bothgears frame28. Exitlast443/completion444bare34,helmet0;
nexttick445bare35,helmet0. Same total clip length does not imply equal current
phase across equipment branches. V10native evidence remains dated4207check scope;
no new native test in this audit. Current normal/water selection unchanged.

Walking256square/p128224/H148 translates32x0 into352x320/p160224 without resizing.
Both original-master/actualwalk/Ready/Crouch/Rise/Extend boards and browser reviewed;
three review rasters LFS pass. Actual walking textile/hair darker/warmer than the
original master and calibrated water actions. Crown/jaw/neck/collar source designs
also differ. Selected bare26x27rectangle comes from later-authored seated/run head;
water21x23from later swim component. Box sizes alone do NOT establish proportion
mismatch or justify separate shrinking. Canonical subset checks are insufficient
for original master identity, and material names do not certify current grade.

Next whole walking source material/identity repair against originalWestmaster,
representative whole poses then all48phases/both gears preserving2second gait and
.1796875cell stride. Do not substitute a handful of repeated timing slots or a
whole-sprite brightness multiplier. Compare actual28/34/35bare and28/0helmet
contexts with current water sources before endpoint fit/normal selection. Then
activephase transitions/physical support/cadence, idle/master/fullwater grade,
natural hazards/checkpoint/visibleContinue/normal admission, North/South and
full-library consistency/polish. Full Bill goal active/incomplete. Handoff:
character/bill-west-active-gait-water-audit-v1/HANDOFF.md; AUTHORING_BRIEF.md.


## Bill West whole walking representative source correction - October 2, 2026

character/bill-walk-west-master-repair-v1 begins whole-source walking correction.
Builtin exec-2b6ea67c-a466-4d00-9f19-e5ff29d4fb30 terminal; raw original retained,
copy/exactLFprompt/job/source/reference hashes saved. OriginalWestcrop is sole
identity/material/camera authority, selectedbare28motion context only. Twofigures
standing/walking share independent standing938opaque-pixel ruler ->one148/938.
Neutral head proxy142x161,walking145x152; head proxy alone is not anatomy proof.
Alpha max254; remove only detached nonzero alpha94neutral/312walk via largest
connected component. Preserve raw and bodycolour; no separate limb/head fitting.

One unselected whole bare candidate256square,p128224,H148 plusneutral ruler;
painted sole-band targetold121222,newwholetranslation-61/68. Paintedsole proxy
not physical root/contact acceptance. Raw and master/browser review show grey
quilt,warmhair anddull hardware closer than selecteddark/purplewalk; newarm/foot
geometry androot-relativeupperbody differ from motionreference. Do not admit it
because material improved. No canonical head orhelmet fitted, no runtimeclock/
manifest/normal/controller changes. Candidate coverage1bare,47bare/48helmet still
unrepaired. Full48phase selectedwalking remains;98normal frame/manifest SHA exact.
Original/copy/ref/prompt SHA,publisher AST,5rasterLFS paths pass. No newnative check.

Lesson: original-master material improvement and standing-scale parity are separate
from exact whole-pose motion retention. Transparent previews can contain detached
low-alpha paint; retain raw and record component cleanup. Apply one whole-source
scale, then diagnose painted support/root-relativehip/head trajectory instead of
resizing parts or flattening posed height. Next geometry-preserving whole28repair,
representative34/35/0contexts andfull48phases/both gears withneighborreview. Do not
alias a few poses to claim full48frame gait. Activewaterjoins/contact, idle/master
andfullwatergrade, naturalhazards/checkpoint/visibleContinue/normaladmission,
North/South andall-family consistency/polish remain. FullBillgoal active/incomplete.
Handoff:character/bill-walk-west-master-repair-v1/HANDOFF.md.


## Bill West pose-preserving walking material studies - October 3, 2026

Two builtin image edits retain actual selected West walking028/034 as exact4x
nearest edit targets; original West master remains sole identity/material/camera
reference. Raw originals, workspace copies, exact LF prompts, ordered reference
SHA and terminal job/provenance retained. Authorings exec-bc6e7c41-ee87-40ec-9a32-
0f876d08e898 and exec-919ba8d5-e8e7-4db7-9e74-20579152d6a5.
Output1254square rather than requested1024: comparisons uniformly resample the
WHOLE canvas to256 with zero translation; no bbox fitting, per-part edits or
posed-height normalization. This retains inherited pose geometry; it is not an
independent new standing-density calibration. Alpha180 largest-component
outline diagnostics:028 overlap94.88%, oldbounds[78,78,168,223],new[78,77,168,223];
034 overlap92.93%, old[100,76,150,224],new[100,75,150,224]. Boot bounds028 exact;
034 bootregion one pixel wider. Head/face/collar minor differences remain.
Master, both source comparison boards, six selected neighbor contexts and browser
seen: grey quilt, warm brown hair and dull hardware closer. Two authored studies,
not a complete gait; remaining46bare/48helmet phases. Installing isolated brightened
frames would create colour seams against the old bank.98 selected frame/manifest
SHA unchanged; provenance/publisher AST and10raster LFS paths pass. No native test,
normal admission, runtime or controller change. Next exact35/0 context edits and
full48/both-gear continuity; then dynamic water joins/contact/lifecycle/persistence
and full-library master/camera/build/grade polish. Full goal active/incomplete.
Handoff:character/bill-walk-west-master-repair-v2/HANDOFF.md.


## Bill West walking adjacent and loop-boundary source evidence - October 3, 2026

Four additional builtin whole-frame edits000/001/035/047 retain exact4x nearest
selected targets and original West master authority. Original generated images,
workspace raw copies, exact prompts, reference hashes and terminal provenance
retained. Sources remain1254square; compare by one256/1254 WHOLE canvas scale,
zero translation, no pose/bbox/part fitting. Total six bare source studies, not a
complete gait:42bare/48helmet phases remain. Six-pose board and both new whole
master comparisons seen; body grey quilt/hair/material closer, minor local
anatomy/outline shifts remain. New035 silhouette93.75%,00094.70%,00193.69%,04792.78%.
Loop47→0→1 reveals crownY old[79,80,79],edit[79,81,78], i.e. olddelta[1,-1]
versusedit[2,-3]. High silhouette overlap did not prevent extra head bob: correct
whole authored crown/face/neck trajectory before admission; do not translate the
head separately or infer temporal acceptance from single-frame bounds.
Adjacent34→35 crown old76→76 vsedit75→76 also remains. Browser bounded preview
plays actual42/42/41ms wrap and41/42ms pair, each at normal andquarter speed,
reaches3/3or2/2thenstops/Play afterfinalhold. Screenshots retained. This proves
bounded source presentation, not full48gait, native actor/root/contact or normal
selection. Rebuild locally via build_context_review.py andbuild_context_page.py;
raw source alpha retained. Provenance/publisher syntax/29rasterLFS pass;
98selected gait hashes unchanged. No Godot/native test, profile interaction or
runtime/controller edit. Next correct source head trajectory at000/001, preserve
six own poses, then all48/bothgear continuity and dynamic water joins/lifecycle/
persistence/normal admission, North/South andfull-library polish. Goal active.
Handoff:character/bill-walk-west-master-repair-v2/HANDOFF.md.


## Bill West head correction rejection and eight-pose gait bank - October 3, 2026

Whole-image head fixes V3/V4 are rejected: desired crown47/0/1=[79,80,79],
V3=[79,80,73],V4=[79,77,81]; V3 also enlarges001/changes boots. LocalizedV5
imagegen edits use fixedsource crop[520,320,740,540],220square→1024edit target,
1254generated crop→220return to SAME rectangle, no headbbox/part fit. All1524116
full-source pixels outside crop and normalizedrows114..255 are exactV2. However
V5 crown[79,79,81] still fails and neck/head geometry remains unaccepted: REJECTED.
Each retains raw original/workspace copy, exact prompt, references/SHA, completed
job, publisher, source boards, rejection/validation andhandoff; no runtimeadmission.
All110bounded inputs unchanged forV3/4/5;6/6/12rasterLFS paths pass respectively.
Lesson: numeric tiny-edit instructions and silhouette overlap do not guarantee
head trajectory; even protected-body region edits need eye/jaw/neck/collar review.
Do not promote a source simply because the rest of its body stayed exact.
Continue filling the complete gait with rough edges tracked, while keeping head
motion a mandatory pre-install gate. V2adds own002/003 edits exec-1be295af-7f7c-
4275-9fc5-6f769cc990fd and exec-eacec9cd-0e90-449e-b564-4009ebccd9d1 against original
West master and exact4x selected targets. Whole1254→256canvas,zero translation.
Silhouette overlap93.42/94.04%; bootregion002left1pixel/003right1pixel differs.
Master/two pose boards/eight-pose overview seen; mattegrey/warmhair/detail closer,
head/collar/outline differences remain. Total8own bare studies,40bare/48helmet
phases remain; failed revisions do not add unique coverage. New1→2→3 bounded
browser segment uses originalholds and reaches3/3thenStopped/Play atnormal and
quarter speed; screenshot retained. No full48loop/native/root/contact acceptance.
98normal gait files unchanged; 40V2rasterLFS paths/publisher AST/provenance pass.
ExplicitUTF8 reads restored preview labels; always preserve UTF8 when loading
written templates, prompts and handoffs on Windows. No Godot/profile interaction.
Next author004..007 andfull48/bothgear, then head/face/neck continuity, activewater
joins/contact/lifecycle/persistence/normaladmission, North/South andfull-library
master/camera/build/grade polish. Goal active/incomplete.
Handoff:character/bill-walk-west-master-repair-v2/HANDOFF.md.


## Bill West twelve-pose material bank review - October 3, 2026

V2 now has 12 distinct bare source studies (000..007,028,034,035,047),
with36 bare/48 helmet phases remaining. New004..007 retained completed builtin
imagegen raw originals, exact prompts, original West master and exact4x pose
references/SHA. Whole1254 to256 uniform canvas normalization, zero translation;
no per-part fitting. Four master/pose boards and12-pose bank board inspected:
grey matte quilting, warm brown hair and muted hardware closer to master.
This is material progress, not full camera/anatomy/motion acceptance. Frame007
crown sits2pixels above selected pose; minor glove/boot outline changes remain.
Tiny head edits in V3/V4/V5 remain rejected and unselected.

New bank.html/build_bank_review.py discovers verified completed own pose studies,
checks raw/prompt/reference provenance and98 selected gait hashes, and uses actual
manifest holds. Browser3to4to5to6to7 at normal/quarter speed reaches5/5 then
Stopped/Play after final hold; screenshot retained. This bounded preview does not
prove a complete loop, root/contact or in-game handoffs. Publisher syntax and
all V2 raster LFS attributes pass; bank-validation.json records exact scope.
No Godot/profile interaction or normal runtime selection change.

Lesson: compare material bank at shared canvas scale and neighboring source holds;
count distinct poses separately from rejected revisions. Better grade and high
outline overlap cannot certify face/neck trajectory or temporal consistency.
Next008..011 and full48/bothgear, source head/neck continuity, active water joins,
contact/lifecycle/persistence/normal admission, North/South andfull-library polish.
Full Bill goal remains active/incomplete.
Evidence:character/bill-walk-west-master-repair-v2/bank-assessment.json,
bank-validation.json,bank.html,HANDOFF.md.


## Bill West sixteen-pose passing-step bank - October 3, 2026

Added own008..011 material studies via builtin imagegen, original West master
plus each exact4x selected pose. Four jobs in completed exec2666; saved raw
original/copy hashes, exact UTF8 prompts, ordered references and completed
provenance. Whole1254square to256square normalization, zero translation, source
alpha retained, no part or posed-height fit. Total16distinct bare studies;
32bare/48helmet phases remain. No normal selection or controller changes.

Raw results, four master/pose boards and16-pose bank overview inspected. Mattegrey
quilting, warm brown hair and ivory/red hardware closer to original. Crown008/
010/011 one pixel higher;009 bootbottom one pixel lower and011 one higher.
Face/collar/contour variation remains; high silhouette overlap93.32..94.55%
is diagnostic only, not motion/anatomical acceptance. Frame007 and wrap-head
issues remain tracked; rejectedV3/V4/V5 head fixes remain unselected.
Browser7to8to9to10to11 uses originalholds41/42/42/41/42ms; normal andquarter
runs reach11,5/5,Stopped/Play after final hold. Screenshot retained. Bounded
preview proves presentation only, not full-loop smoothness or world contact.
98selected gait hashes/provenance checked by publisher;3publisher AST checks and
all V2rasterLFS attributes pass. No Godot/profile interaction. bank-validation.json
records scope. Next012..015/full48/bothgear, head/neck continuity and activewater
joins/contact/lifecycle/persistence/normaladmission, North/South/full-librarypolish.
Continue shared-canvas neighbor comparisons through passing poses; independently
successful material edits can still vary eyes, jaw, collar and sole contour.
Full Bill goal remains active/incomplete.
Evidence:character/bill-walk-west-master-repair-v2/bank.html,bank-assessment.json,
bank-validation.json,HANDOFF.md; source prompts and provenance alongside.


## Bill West twenty-pose source bank - October 3, 2026

Added own012..015 via builtin imagegen exec2676, completed4jobs and persisted
raw originals/workspace copies/exact prompts/reference SHA/provenance immediately.
Original West master + exact4x selected targets; whole1254 to256 normalization,
zero translation, no part/posed-height fit. Four master boards and20-pose bank
inspected: grey matte quilting and brown hair closer;012 head crown1px high,
013 boot footprint expands,014/015 bootright1px wider. Eyes/jaw/collar variation
remains.20distinct bare studies;28bare/48helmet still required. No admission.

Bank preview now spans0..15 consecutively with originalholds,total667ms; normal
andquarter playback reach15,16/16,Stopped/Play. Source preview/screenshot only,
not full48loop/native/world contact acceptance.98selected hashes/provenance,
3publisher syntax checks and92rasterLFS paths pass; bank-validation.json records
scope. No Godot/profile interaction. Previous head/collar motion gates remain.
Lesson: broaden contiguous preview as bank grows; separately track grade/detail
improvement and face/neck/sole drift through crossing poses. Next016..019/full48
bothgear, head/neck repair, activewater joins/contact/lifecycle/persistence/normal
admission, North/South/full-library master/perspective/proportion/grade polish.
Full Bill goal active/incomplete. Evidence:character/bill-walk-west-master-repair-v2/
HANDOFF.md,bank.html,bank-validation.json; sources/prompts retained alongside.


## Bill West first-half source bank - October 3, 2026

Added eight own016..023 builtin imagegen studies: exec2687/2695 completed4jobs
each; raw results copied immediately with exact UTF8 prompts/reference SHA and
completed provenance. Original West master + own exact4x selected target;
whole1254 to256 uniform normalization, zero translation, sourcealpha retained.
Eight master/pose boards and shared-scale012..023 bank crop inspected. Mattegrey
quilting/warmhair closer; face/neck/collar/hardware changes remain unaccepted.
017/021..023 crown1px high;headleft1..2px/bootwidth1..2px drift;019/021 bootbottom
1px high. These are explicit rough source candidates, not anatomical acceptance.

Total28distinct bare studies:0..23,28,34,35,47;20bare/48helmet phases remaining.
Preview now has first20 and firsthalf0..23 at actual selected holds833/1000ms;
both reach lastslot thenStopped/Play at normal/quarter speed. Screenshot saved.
This is bounded source presentation, not full48loop/root/contact/native acceptance.
98selected gait hashes plus raw/prompt/reference provenance pass publisher;
3publisher AST checks and126rasterLFS paths pass. No Godot/profile or normal
selection change. Index/assessment/validation/publishers/HANDOFF updated.

Lesson: shorten long sequence labels without changing phase mapping/holds, and
broaden contiguous comparisons as sources accumulate; temporal head/detail
coherence must remain a separate gate from grade/silhouette similarity.
Next024..027,skip already-authored028,then029..033/036..046/full48bothgear;
head/neck continuity,activewater joins/contact/lifecycle/persistence/normaladmission,
North/South/full-library master/camera/build/grade polish. Full goal active.
Evidence:character/bill-walk-west-master-repair-v2/bank.html,bank-validation.json,
bank-assessment.json,HANDOFF.md; sources/prompts and provenance retained alongside.


## Bill West complete bare source bank - October 3, 2026

Objective remains the full Bill animation set matching original masters, style,
camera, build/height/proportions and matte grade, followed by cross-family polish
and normal gameplay integration. Complete bare source coverage is not completion.

Since the recorded 28-pose milestone, added 20 distinct builtin imagegen studies:
024..027,029..033,036..046. This continuation authored 12 of them:033,036..046;
handles2722/2726/2732 terminal and all results copied immediately. Eight preceding
024..032 jobs had already finished on2706. Exact prompts/reference/raw SHA retained.
Original West master plus each own 4x selected pose; whole1254-square to256-square
uniform normalization, zero translation, alpha retained, no separate part fitting.

Bank now covers all48 bare phases0..47, including existing028/034/035/047.
48 helmet phases still required. New master/pose boards and complete two-part
head/shoulder contact sheet reviewed. Grey matte quilting/warm hair closer; eye,
face, collar and hardware variation remain. Window diagnostics report maximum
absolute deltas head2px, glove3px, boots2px; these are not anatomical acceptance.
030 far glove remains3px inward;033/037/040/046 crowns1px high,038/0391px low;
036 boot width2px and several closing-pose sole bottoms1px high. Keep these gates.

Updated bank publisher/HTML/index/assessment/validation, added build_loop_audit.py,
full-loop-continuity-diagnostics.json, head review panels and full48 screenshot.
98 selected gait hashes and exact source/prompt/reference provenance passed bank
publisher.3 publisher syntax checks and212 raster LFS paths passed. Normal and
quarter bounded0..47 playback reach47,48/48,Stopped/Play using original2000ms.
Earlier33-frame quarter endpoint reconciled. Source presentation is not continuous
native motion, physical root/contact, controller handoff or owner acceptance.
No Godot/profile interaction, normal selection changes, commit or export.

Lesson: complete phase coverage makes temporal identity variation easier to see;
inspect face/collar and near/far gloves across the entire gait alongside outline
metrics. A good per-frame grade/overlap cannot certify coherent joints or motion.
Do not independently normalize exposure, posed height or individual body parts.
Next: head/neck/glove/sole continuity repair and full48 helmet master pass; active
water joins/contact/lifecycle/persistence/normal admission, North/South and full
library camera/build/grade polish remain. Full goal active/incomplete.
Evidence:character/bill-walk-west-master-repair-v2/bank.html,bank-validation.json,
full-loop-continuity-diagnostics.json,HANDOFF.md; exact sources/prompts alongside.


## Bill West helmet representative master pass - October 3, 2026

New unselected character/bill-walk-west-helmet-master-repair-v1 contains four
contrasting helmet phases000/012/024/036, not a loop. Six builtin imagegen results
completed on2747/2752/2756, raw copies/exact prompts/reference SHA retained. Each
own selected pose was enlarged4x. Original West master controls suit material;
canonical40x40 helmet enlarged8x controls design; same-phase bare study supports
material only. Whole1254 to256 uniform normalization, zero translation, no part
or posed-height fitting. Bare source bank remains48;44helmet phases unauthored.
All four revised phases remain rough/unselected, with continuity still required.

Rejected024v1: boots left2/right4/bottom5px change, outline overlap83.15 percent.
Rejected024v2: geometry closer but heavy black contours/darker material.024v3 uses
original master + same-phase bare material study + sole selected helmet target;
boot bottom now matches, width1px each side; overlap92.77 percent. Grade closer.
Other flags:000helmet crown2px low/sole1px low;012glove/boot width;036crown1px high,
boot right3px wider/bottom1px low. Helmet window1144..1408RGBA pixels changed across
latest candidates: exact helmet preservation is NOT established. Face/collar,
shoulder/glove and master lighting/proportions remain visual/motion gates.

Master/selected/edited/bare boards, rejected revisions and static browser reviewed.
Publisher checks all six source/prompt/reference hashes and98frozen selected gait
files.1new publisher syntax check and28raster LFS paths pass; bare publisher also
updated to reference distinct helmet source coverage and parsed successfully.
No Godot/profile, normal runtime selection, commit or export. Static nonconsecutive
inspection cannot prove gait timing, seam, actual contact or native acceptance.

Lesson: extra material/gear references can accompany pose drift despite clear
prompt roles. Compare all toes/sole, near/far gloves, helmet and collar before
expanding. Reducing to master/material/sole pose improved024 geometry and finish,
but does not prove general success. Keep rejected revisions and do not count
retries as distinct phases. Separate authored coverage from approved continuity.
Next adjacent helmet phases/loop boundary, then full48; repair bare and helmet
head/neck/glove/sole continuity, actual water joins/contact/lifecycle/persistence/
normal admission, North/South and full-library master/camera/build/grade polish.
Full Bill goal remains active/incomplete. Evidence: own index.html,bank-assessment,
bank-validation,HANDOFF; sources/prompts and rejected boards retained alongside.


## Bill West opening helmet continuity review - October 3, 2026

Helmet source bank now has12 distinct phases:000..007,012,024,036,047;
36remain unauthored. Eight new builtin edits001..007/047 completed on2764,
all saved immediately with exact prompt/reference/raw provenance. Total14results
includes two rejected024revisions; retries are not additional motion phases.
Original master + corresponding bare material + sole selected helmet pose used.
Whole1254-to256 uniform normalization/zero translation retained; no part fitting.

All eight new master/pose boards, complete12-pose overview and fixed-canvas
47/0..7 helmet/collar strip inspected. First8 and47/0/1 bounded browser sequences
reach final7|8/8 and1|3/3 Stopped at normal/quarter speed, with original333ms/125ms
holds. Screenshot opening-browser-review.png retained. This is source preview,
not full48loop, continuous native motion, physical contact or owner acceptance.
Matte quilting is closer; helmet/face/visor/collar trajectory remains provisional.
000crown2px low creates a join correction target.004glove left2px wider and boot
left2/right1/bottom2px changes;007boots2px wider each side/bottom1px low;
047crown1px low/sole1px low. Window diagnostics are not anatomical proof.

14original/copy/prompt/reference hashes,98frozen selected gait files,2publisher
syntax checks and71PNG LFS paths pass. Bare companion metadata reconciled to
12helmet/36remaining; bare48unchanged. New continuity publisher/page/assessment,
overview/headstrip, updated validation and handoff retained. No Godot/profile,
normal runtime selection, commit or export. Full Bill objective remains active.

Lesson: adjacent phase and last-to-first review exposes helmet dips and changing
boot volume hidden by isolated boards. Retain exact gait holds and fixed crops;
do not repair by independent posed-height/exposure/head or limb normalization.
Next correct000join/004boot and glove volume, add008..011, then remaining helmet
phases. Both gears' identity/neck/sole continuity, active water joins/native contact,
lifecycle/persistence/admission, North/South/full-library master polish remain.
Evidence:character/bill-walk-west-helmet-master-repair-v1/continuity.html,
bank-validation.json,opening-helmet-head-review.png,HANDOFF.md; exact prompts
in sources/walk-NNN-prompt-v1.txt, ordered refs in generation-provenance records.


## Bill West helmet loop crown correction - October 3, 2026

Frame000v2 builtin whole material edit completed2779; original/raw copy, exact
prompt and ordered master/bare-material/sole selected-pose SHA retained. Crown
now matches selected75px instead of v1two-pixel dip. Glove window bounds match;
helmet left1px wider, boots left1px inward/right1px wider/bottom1px lower remain.
Overlap92.01percent and1242changed helmet-window pixels do not certify identity.
Master/pose and47/0..7fixed helmet strip reviewed; grade closer, face/visor/collar
and sole continuity remain provisional. Previous000v1review archived, superseded
metadata retained. Twelve distinct source phases unchanged;36helmet phases remain.

15raw/original/prompt/reference records and98selected gait hashes passed publisher;
2syntax and74PNG LFS checks passed. Continuity preview rebuilt. Prior browser
normal/quarter evidence predates this revision; no revised cadence/native/contact
claim. No Godot/profile or normal selection change. Goal active/incomplete.
Lesson: fewer explicitly assigned references and a precise crown constraint improved
registration but still changed boots. Whole material editing needs full silhouette
and neighbouring identity review, even when targeted height improves. Next004boot
/glove correction and008..011, complete helmet48, both-gear continuity and water
/native/lifecycle/persistence/admission/full-library master polish.
Evidence:own review-000.json,master-pose-review-000.png,continuity.html,HANDOFF;
exact prompt sources/walk-000-prompt-v2.txt, generation-provenance-000-v2.json.


## Bill West helmet passing-phase review - October 3, 2026

Four builtin edits008..011 completed2787 and saved immediately with exact
prompts/orderedrefs/raw SHA.008/009 retained as rough unselected candidates;
helmet-window bounds match selected.008glove/boot left1px wider;009glove1px
each side and boots1px each side/bottom1px lower.010rejected:pose/body drift,
boots7px lower/glove right4px wider/79.12percent overlap.011rejected:canvas
1230x1278instead of square and visible whole pose drift. Raw originals retained.
Do not stretch nonsquare output to force compatibility. Publisher initially
failed its square assertion; fixed to verify provenance first then exclude
explicitly rejected outputs, preserving the geometry requirement for candidates.

Bank14usable rough phases,16distinct attempted phases,19results/4rejections;
34phases still need usable candidates, including010/011retries. Source boards008
..010,011raw and7..11comparison inspected; matte/detail closer but temporal
face/collar/glove/sole continuity remains unaccepted. Added finite7..9/first10
preview windows using selected holds. No browser/native playback claimed for
these added windows. All19provenance records/98selected gait hashes passed
publisher,2syntax/93PNG LFS checks passed. Bare48unchanged; companion metadata
reconciled. No Godot/profile/normal selection/commit/export. Goal active.

Lesson: identical edit prompts may change gait geometry or canvas shape at
passing-foot poses. Inspect outputs before normalization, retain rejected
evidence, and separate attempted coverage from usable source candidates.
Next reauthor010/011 from sole own pose, repair004and sole drift, remaining
helmet phases, both-gear continuity/water joins/native lifecycle/persistence/
admission and full-library master polish. Evidence:own bank-validation.json,
passing-source-review.png,continuity.html,HANDOFF; prompts sources/walk-008
..011-prompt-v1.txt and generation-provenance records.


## Bill West passing-foot geometry retries - October 3, 2026

010/011v2 builtin whole material retries completed2796, immediately saved with
exact prompts/orderedrefs/raw SHA. Original helmet pose is PRIMARY, original
master supports interior material only; no failed output or bare pose reference.
Both1254square.010outline overlap96.94percent/01196.21percent; both helmet-window
bounds match selected.010glove matches, boots1px narrower each side/bottom1px
higher;011glove right1px wider, soles1px higher. Earlier010v1boots7px lower and
011v1nonsquare remain rejected;010rejected review archived before rebuilding.
Both new poses retained rough/unselected, darker suit finish than008/009/012
still requires coherent material pass. Fixed8..12body/helmet board inspected.

Bank16distinct rough candidates/32remaining,21results/4rejections. First12finite
browser normal+quarter playback reach11|12/12|Stopped using original500ms holds;
source screenshot retained.21original/copy/exactprompt/refs plus98frozen selected
hashes pass publisher;2syntax/101PNG LFS paths passed. All48bare candidates
unchanged; companion metadata updated16/32. No Godot/profile/runtime selection,
commit/export or complete-loop/native/contact acceptance. Full objective active.

Lesson: giving original pose primary-reference position and removing competing
material-pose reference improved crossing-foot geometry. It also retained darker
cloth, so geometric success does not establish temporal grade. Compare adjoining
whole poses before accepting, retain one ruler/canvas, never fit individual parts.
Next coherent010/011material finish while protecting improved pose,013onward,
004/sole/identity repairs, fullhelmet48/bothgear continuity and active water
joins/native contact/lifecycle/persistence/admission/full-library master polish.
Evidence:own passing-retry-review.png,first12-browser-review.png,bank-validation,
continuity.html,HANDOFF; exact sources/walk-010/011-prompt-v2.txt and provenance.


## Bill West passing-frame material refinement - October 3, 2026

Two builtin material-only edits010/011v3 completed2806 and saved immediately,
exact prompts/orderedrefs/raw SHA retained. Primary own v2target + same-phase
bare material + original master; no failed output reference. Both1254square.
011v3 cloth closer to008/009/012, helmet window bounds matchselected; glove
right1px wider, boot right1px wider/sole1px higher; overlap95.22percent. Retained
rough/unselected, temporal face/collar/sole acceptance remains open.010v3 rejected
whole pose drift:helmet crown7px low/boot bottom3px low,77.46percent overlap.
Archived rejection and restored010v2geometry candidate; its darker finish remains.

Master/pose boards and8..12previous/retained body comparison reviewed. Candidate
bank still16/48,32remaining;23results/5rejections, not extra phase coverage.
23original/copy/prompt/reference records and98frozen selected gait hashes passed
publisher;2syntax/110PNG LFS paths passed. Rebuilt source preview; previous
first12browser evidence predates011v3, no revised playback/native/contact claim.
No Godot/profile/normal selection/commit/export; full objective active/incomplete.

Lesson: re-editing a geometrically improved source for fabric colour can still
move its head and feet. Validate whole geometry again, retain successful earlier
pose, count material refinement separately from phase coverage. A colour match
must not displace good stance. Next expand013onward while keeping010material
gap/004glove-boot/sole/identity defects explicit, completehelmet48, bothgear
continuity and active water/native lifecycle/persistence/admission/library polish.
Evidence:own passing-grade-review.png,review-010/011.json,bank-validation,HANDOFF;
exact prompts sources/walk-010/011-prompt-v3.txt and provenance records.


## Bill West helmet stride expansion13to16 - October 3, 2026

Four builtin whole material edits013..016 completed2812, saved immediately with
exact prompts/orderedrefs/raw SHA. Own original helmet pose PRIMARY, matching
bare material ONLY, original master finish; all1254square uniformly256/1254
to256canvas,zero translation/no partfit. Allfour helmet-window bounds and sole
bottom heights match selected.013overlap94.57percent/glove1px wider each side/
boots left1right2px wider;01495.30/glove exact/boots1px each side;01594.92/glove
left1/boots right1;01695.84/glove right1px inward/boots right1. Window diagnostics
are not anatomical acceptance. Matte finish closer, face/collar/visor/hardware
variation remains. Master/pose boards and12..16fixed body/head comparison seen.

Bank20rough distinct candidates0..16/024/036/047,28remaining;27results/5rejections.
Added reproducible build_segment_review.py and stride-12-16-review.png. First16
browser normal/quarter reach15|16/16|Stopped at original667ms. Screenshot retained;
source presentation only, not full48/native contact/controller or owner acceptance.
27provenance records/98selected hashes,3publisher syntax/132PNG LFS checks pass.
Bare48unchanged; companion metadata20/28. No Godot/profile/normal selection/
commit/export. Whole full-set objective remains active/incomplete.

Lesson: primary original pose plus separately assigned same-phase material/master
references can retain helmet/sole heights through crossing and early outward
stride while small glove/boot widths still vary. Check fixed neighbouring crops
and original holds, not just overlap or single-frame exposure. Next017onward,
remaining010grade/004bootglove/headnecksole fixes; fullhelmet48,bothgear water
joins/native contact/lifecycle/persistence/admission and full-library master polish.
Evidence:own continuity.html,stride-12-16-review.png,first16-browser-review.png,
bank-validation,HANDOFF; exact sources/walk-013..016-prompt-v1.txt/provenance.


## Bill West helmet outward stride17to20 - October 3, 2026

Four builtin whole material edits017..020 completed2819, saved immediately with
exact prompt/orderedrefs/raw SHA. Own helmet pose primary, matching bare material
only, original master finish; all1254square uniformly256/1254to256,zero translation.
Allfour sole heights match selected;017/018helmet window bounds match;019crown1px
low/left1px inward,020crown1px low.017/019boots right2px wider,018left/right1px,
020right1px.017/019glove window matches,018/020left1px wider. Overlap94.51..95.29
percent is diagnostic only. All master/pose boards plus16..20fixed fullbody/head
board reviewed; matte/detail closer, face/collar/helmet/sole-width stillprovisional.

Bank24rough distinct candidates0..20/024/036/047,24remaining;31results/5rejections.
Extended preview with16..20and first20windows at original holds, missing phases
excluded. First20normal+quarter reach19|20/20|Stopped at833ms; screenshot retained.
New020 staticboard inspected, not included in first20playback. Source presentation
is not full48/native contact/controller/owner acceptance.31provenance records/
98selected hashes,3syntax/154PNG LFS checks pass. Bare48unchanged,companion24/24.
No Godot/profile/normal selection/commit/export. Fullobjective active/incomplete.

Lesson: preserve sole height separately from boot width and helmet trajectory;
matching one bound cannot prove coherent volume or face/neck identity. Continued
whole pose + material references retained gait but1px crown/1..2px toe variation
remains. Next021..023then025onward, remaining010grade/004bootglove/headnecksole
corrections; fullhelmet48,bothgear waterjoins/native contact/lifecycle/persistence/
admission and full-library master polish. Evidence:own continuity.html,
stride-16-20-review.png,first20-browser-review.png,bank-validation,HANDOFF; exact
sources/walk-017..020-prompt-v1.txt and generation-provenance records.


## Bill West helmet first-half completion21to23 - October 3, 2026

Three builtin whole material edits021..023 completed2831; immediately saved raw
copies with exact prompts/ordered reference SHA. Own selected helmet target primary,
same-phase bare material only, original West master finish. All1254square uniformly
normalized256/1254,zero translation/no part fitting. All three helmet/glove window
bounds match selected; boots right1px wider,021/022sole1px higher,023sole matches.
Outline overlap94.02..94.95percent is diagnostic only. Master/pose boards and fixed
20..24body/helmet board inspected: matte quilting closer; face/collar/hardware
identity and toe/sole continuity remain provisional.

Bank27rough distinct phases000..024/036/047;21remain.34results/5rejections. First24
finite normal/quarter browser playback reaches23|24/24|Stopped at original1000ms;
screenshot retained. This is source playback, not full48/native/contact acceptance.
34provenance records/98frozen selected hashes passed publisher;3syntax/171PNG LFS
paths pass. Bare48unchanged,companion metadata27/21. No Godot/profile/normal
selection/commit/export. Full Bill objective remains active/incomplete.

Lesson: matching head/glove bounds while restoring suit detail still leaves sole
height and boot width variation. Compare neighbouring whole poses and fixed crops,
retain original holds and independent identity/contact gates; do not infer anatomy
from overlap/window equality or normalize individual parts. Next025onward, existing
010grade/004bootglove/face-neck-sole corrections; fullhelmet48,bothgear waterjoins,
native contact/lifecycle/persistence/admission and full-library master polish.
Evidence:own stride-20-24-review.png,first24-browser-review.png,continuity.html,
bank-validation,HANDOFF; exact sources/walk-021..023-prompt-v1.txt and provenance.


## Bill West helmet returning stride25to28 - October 3, 2026

Four builtin whole material edits025..028 completed2840, immediately saved with
exact prompts/ordered refs/raw SHA. Original helmet pose primary, same-phase bare
material only, original master finish. All1254square uniformly256/1254, zero
translation/no part fit. All helmet-window bounds match selected.025glove left1px
wider/boots1px each side wider/sole1px higher;026glove/bootwidth matches but sole1px
lower;027glove/sole matches,bootright1px wider;028gloveleft1px wider/boots match.
Outline overlap94.73..95.50percent is diagnostic only. Four master/pose boards and
24..28fixed fullbody/head board reviewed: matte quilting closer, face/collar and
hardware trajectory remain provisional.

Bank31rough distinct phases000..028/036/047;17remain.38results/5rejections. First29
normal/quarter finite browser playback reaches28|29/29|Stopped at original1208ms,
screenshot retained. Returning24..28source window also published; no separate
playback claim for it. No full48/native/contact acceptance.38provenance records/
98frozen selected hashes passed;3syntax/193PNG LFS paths pass. Bare48unchanged,
companion metadata31/17. No Godot/profile/normal selection/commit/export. Goal active.

Lesson: reference studies may have legacy recorded filenames; resolve explicit
phase-to-study paths from authoritative assessment, never infer absent assets from
a naming pattern. Initial028preparation failed on assumed indexed bare filename;
resolved recorded canvas-normalized-study.png and updated helmet review publisher
to use the bare bank mapping. Artwork unchanged. Matching helmet bounds still
leaves glove/sole drift: whole neighbouring geometry and identity review required.
Next029onward,004bootglove/010grade/face-neck-sole repairs,completehelmet48,bothgear
waterjoins/native contact/lifecycle/persistence/admission and full-library polish.
Evidence:own continuity.html,stride-24-28-review.png,first29-browser-review.png,
bank-validation,HANDOFF; exact sources/walk-025..028-prompt-v1.txt/provenance.


## Bill West helmet closing stride29to32 - October 3, 2026

Four builtin whole material edits029..032 completed2847, immediately saved with
exact prompt/ordered refs/raw SHA. Sole selected helmet pose primary, same-phase
bare material only, original West master finish. All1254square uniformly256/1254,
zero translation/no part fitting. All helmet-window bounds match selected.029
gloveleft1px wider/bootright1;030gloveleft/right1px left and bootleft/right1px right;
031gloveleft1/bootright1/sole1px lower;032gloveright1px inward/bootright1/sole1px lower.
Outline overlap93.99..95.65percent diagnostic only. Four master/pose boards and
28..32fixed fullbody/head board reviewed: matte quilting closer, face/collar and
hardware continuity remain provisional.

Bank35rough distinct phases000..032/036/047;13remain.42results/5rejections. First33
normal/quarter finite browser playback reaches32|33/33|Stopped at original1375ms;
screenshot retained.28..32source window published, no separate playback claim.
42provenance records/98frozen selected hashes passed publisher;3syntax/215PNG LFS
paths pass. Bare48unchanged,companion35/13. No full48/native/contact/identity
acceptance, Godot/profile interaction,normal selection,commit/export. Goal active.

Lesson: advancing helmet bounds can match while glove position and sole geometry
still drift at narrowing stride. Preserve original articulated whole poses and
holds, inspect adjoining fixed body/head crops, retain identity/contact gates
independently of overlap or window equality. Next033..035then037onward;004bootglove/
010grade/face-neck-sole repairs,completehelmet48,bothgear waterjoins/native contact/
lifecycle/persistence/admission and full-library master polish remain. Evidence:
own stride-28-32-review.png,first33-browser-review.png,continuity.html,validation,
HANDOFF; exact sources/walk-029..032-prompt-v1.txt and provenance.


## Bill West helmet opposite stride33to39 - October 3, 2026

Six builtin whole material edits033..035/037..039 completed2853, immediately saved
with exact prompts/ordered refs/raw SHA. Selected helmet pose primary, matching
bare material only, original master finish. All1254square uniformly256/1254, zero
translation/no part fit.033sole1px high/gloveleft1;034helmetleft1/glove1each/bootright1;
035gloveleft1/bootright1;037helmetleft1in/glove1each/bootright1;038crown1low/glove
right1/bootright1;039gloveleft1/bootright2/sole1high. Other sole/crown bounds match.
Overlap94.22..96.08percent diagnostic only. Six master/pose boards and fixed32..39
body/helmet comparison with existing036 reviewed. Matte closer; face/collar and
hardware trajectory provisional. Older036finish/head variation remains explicit.

Bank41rough distinct phases000..039/047;seven remaining040..046.48results include
five rejected revisions. First40normal/quarter finite browser reaches39|40/40|Stopped
at original1667ms; screenshot retained.32..39source window published without separate
playback claim.48provenance records/98selected hashes,3syntax/247PNG LFS checks
pass. Bare48unchanged,companion41/7. No full48/native/contact/identity acceptance,
Godot/profile,normal selection,commit/export. Full objective active/incomplete.

Lesson: same-camera near-overlapping legs can retain heel/crown heights while
changing glove width, toe volume and collar hardware. Compare articulated whole
figures across the passing phase and earlier retained candidates, preserve one
canvas/ruler and original holds; bounds/overlap alone do not prove identity or
contact. Next040..046, then complete48bothgear continuity and targeted004/010/036
material-head-sole corrections; waterjoins/native contact/lifecycle/persistence/
admission and full-library master polish remain. Evidence:own continuity.html,
stride-32-39-review.png,first40-browser-review.png,validation,HANDOFF; exact
sources/walk-033..035/037..039-prompt-v1.txt and provenance records.


## Bill West helmet full source coverage - October 3, 2026

Seven builtin image edits040..046 completed on exec2863, all immediately copied with exact prompts, ordered reference hashes and original/copy provenance. Both West walk source banks now have48 distinct candidates. Helmet total55 generated results, five rejected results; retries are not phases. All55 provenance receipts and98selected gait hashes passed;3publisher syntax checks and286PNG LFS paths passed.

Seven new master/pose boards and stride40..47 actually inspected. Whole square1254-to256 normalization preserves original canvas without part fitting. New helmet crown/window matches except043left1px wide; sole matches except0461px high. Small glove/boot width differences remain. Fixed helmet/collar boards cover all48 and were inspected:010darker finish and036head/finish step remain apparent, with face/collar/hardware identity variations elsewhere. Window bounds are diagnostics, not anatomy acceptance.

Full48 finite browser source preview retains original2000ms holds. Normal and quarter runs observed Playing and endpoint47|48/48Stopped; screenshot retained. This does not certify continuous native contact, controller behavior or owner acceptance. No Godot/profile, normal admission, commit or export. Existing selected gait remains unchanged.

Lesson: full source coverage enables a whole-loop comparison but does not establish consistent identity. Review the complete head/collar trajectory and grade together before correcting isolated phases; preserve natural bob and fixed ground registration. Next targeted010/036and remaining head/collar/glove/sole polish in both gears, then actual water joins/contact/controller/Continue and North/South/full-library consistency. Full Bill goal remains active.


## Bill West helmet neighbor-aware polish - October 3, 2026

Builtin edits010v4/036v2 completed on exec2875, raw originals/copies, exact prompts and all ordered references retained. Original selected pose is primary; labelled same-phase bare/adjacent helmet board supplies material only; directional master controls finish. Before-state boards/diagnostics archived. Both edits retained as preferred rough source candidates:010darker cloth step reduced,036head/finish step reduced.010helmet/glove/boot window bounds all match original;036helmet matches, glove right1px wide, boots left1/right2wide with unchanged sole. IoU0.945665/0.960010. Bounds do not certify face/neck/joint identity.

Both master boards,08..12/34..38segments and regenerated all48helmet/collar boards actually inspected. Full48 finite normal/quarter playback reaches47|48/48Stopped, original2000ms.57provenance receipts/98selected hashes verified by publisher;3syntax checks and297PNG LFS paths pass. Both source banks48, five rejected results. No Godot/profile, normal admission, commit or export. Full goal remains active.

Lesson: correcting an edited dark frame can inherit its pose drift; returning to its exact original selected target with adjacent MATERIAL-only context gave closer finish and registration here. This is a two-frame result, not proof of universal pose protection. Full identity/helmet/collar/glove/sole polish and actual water joins/contact/controller/Continue remain next, then North/South and cross-family full-library acceptance. Evidence:neighbor-polish-assessment.json,neighbor-polish-browser-review.png and saved prompts010v4/036v2.


## Bill West walk/water shared neutral refinement - October 3, 2026

New character/bill-west-active-gait-water-audit-v2 compares complete walk candidates at exact previously capturedV10contexts: outgoing28both gears, resumed34/35bare and0helmet. Whole dry256canvas translated32,0onto352x320water canvas, pivot160224,148ruler. Four before/after join boards actually inspected. Entry0andexit7are byte-identical old standing images pergear; both were darker than revised walk and neighboring Ready/Rise. No new native observation.

Three builtin endpoint edits retained with exact prompts/reference/original/copy hashes. Barev1preferred, helmetv1REJECTED whole-figure position drift (IoU.353;head window empty), helmetv2preferred using exact-position bare material reference and original helmet pose authority. Uniform1254to352square then remove only32pxbottompadding to restore352x320, zero translation/no partfit. BareIoU.958599head/glovebounds exact/bootright1wide/sole224same;helmetv2IoU.946436head/glovebounds exact/bootleft1right1wide/sole225vs224. Matte/hair closer, face/collar/helmetidentity and boots still provisional. Both masterboards and regenerated four candidatejoins viewed.

Four staged complete entry/exit banks preserve original500ms/nonloop metadata,26interior frames exact and30decodedAPNGframes exact,36frozen inputs. All3generation receipts,20baselinejoin inputs,98selected gait hashes,3syntax checks and56PNG LFS paths pass. Browsercomparison/screenshotseen; finiteAPNGmetadata verification is not continuous motion/contact proof. No Godot/profile, normal selection, commit or export. Full Bill goal active.

Lesson: sourcecoverage alone misses shared legacy neutral endpoints. Audit actual gait handoffs and bothgear sources; exact shared hashes permit one revised source pergear serving entry andexit. Empty diagnosticwindows should record failed registration rather than crashing or fitting the figure to hide movement. Multiple pose/materialrefs can induce repositioning; same-position material context improved this retry, not a universal guarantee. Next exact candidate source loading and dynamicwalk/waterjoins, contact/roots/cadence/controller/hazards/checkpoint/Continue; full-libraryidentity/polish and North/South remain.


## Bill West revised gait native water joins - October 3, 2026

New fixture-onlyV11 loads complete48phase bareV2/helmetV1candidate banks at original256canvas/p128224/H148/2000ms/.1796875cell stride, plus staged7entry/8exit sources from gait-water-auditV2. Tests verify every loaded gait/source pixel and pivot, preserving original controller clocks/route. Native4793checks,0failures,116.76s,exit0,no script/artwork errors;728bounded inputs stable and2931owner non-log files unchanged under scratchAPPDATA. Six new script UID pairs/two Python syntax/four review raster LFS checks pass.

190advancing presentations preserve exact prior physical root/clock/water/medium/state/direction/path/material fields. Eight captures match revised walk phases exactly:67bothgear28;443/444bare34,helmet0;445bare35,helmet0. Actual finite bridges complete on exact incoming gait frames. Four native room/source boards inspected. Matte suit closer to water interiors, but Ready/Rise versus gait head/jaw/collar and helmet design/attachment differences remain visible. Existing underwater body tint/head ellipse proxy retained; no anatomy/contact/smoothness visual acceptance. Prescribed hydrology/route, support intercept and synthetic guards/controlled swim probes do not prove natural jobs/hazards/Continue.

Important correction: runtime bridge REPLACES preview neutral endpoints with actual outgoing/incoming gait sources. Earlier shared-neutral source repairs improve authored source previews but do not themselves render at native boundaries. Test both complete revised gait banks, rather than crediting neutral-only changes with a runtime fix. Initial runner mistakenly invoked oldV10test; its4207checkrun is rejected asV11evidence and archived, exact underscore test path/UID corrected before trueV11run. No normal admission, commit or export. Full Bill goal active/incomplete.

Next whole-source head/collar/helmet continuity at actual outgoing28/Ready and Rise6/resumed34/0, source-bound dynamic head readability/contact/root/cadence review, natural hazards/checkpoint/visibleContinue and full-library/North/South consistency. Native screenshots remain under output/bill-land-water-material-west-v11; own review.json/index.html/HANDOFF.md retain scope.


## Bill West water joint source repairs - October 3, 2026

New character/bill-west-water-joint-continuity-v1 contains five completed builtin imagegen edits with exact prompt/reference/source/original/copy SHA receipts. Three provisional whole-source candidates: bare Ready1, bare Rise6 and helmet Rise6. The Rise helmet collar is visibly more connected; face/jaw and matte detailing improve modestly. Actual adjacent candidate gait references28bothgears,34bare/0helmet and original West master reviewed. Uniform1254-square to352-square then remove documented32px bottom pad; no part fitting/translation/height normalization.

Helmet Readyv1 andv2 REJECTED: whole-figure drift, soles20/16px low, crowns6/10px low and below-collarIoU.587/.607. V2 same-pose bare material reference did not prevent movement. Original helmet Ready retained byte-exact in staged entry. Bare Readysole2px low; bare/helmet Risesole1px low with1-2px edge changes; these are measured provisional contact risks, not acceptance. Whole figures and fixed head/collar boards inspected; collar improvement does not certify helmet identity or anatomy. Four complete uncropped sequence boards viewed after correcting a too-small diagnostic crop that clipped prone legs. Preserve full canvas for body/contact review.

Four staged paired7entry/8exit banks retain500ms/nonloop/H148/p160224;27prior frames exact,30decoded finiteAPNGframes exact,37frozen source inputs. Five receipts/two rejections/98selected gait hashes/two Python syntax/64PNG LFS checks pass. No native run this milestone, no owner profile touched, no normal admission/commit/export. Review index and source-selection/validation.json record limits.

Lesson: connected collar edits can still resize/reposition an entire helmet figure even with explicit invariants and same-pose material references. Reject physical drift rather than recentering or stretching it away. Material-only reference wording is not proof of pose preservation. Verify full-source contacts and actual adjacent gait separately; runtime neutral endpoints are dynamically replaced. Next solve helmet Ready with a focused single-target edit, evaluate remaining head proportion/contact differences, then native actual-gait joins/readability/cadence and natural gameplay/checkpoint/Continue. North/South and full-library consistency remain; full Bill goal active.


## Bill West focused collar and native water repairs - October 3, 2026

Focused single-target builtin helmet Readyv3 repairs the collar without the large whole-figure movement of rejectedv1/v2. Crown and right bound exact; below-collarIoU.91348 versus.587/.607. Sole remains2px lower by alpha127; opaque224 threshold shows1px change. Four whole-source candidates now provisional: Ready1/Rise6,bothgears. Six exact generation receipts, two rejected, preserved original/copy/prompt/reference hashes. Uniform1254-to352square/crop bottom32 only, no part/height fitting. Native boot diagnostic shows Ready edge bands and Rise1px opaque-sole change; no floor-contact approval.

New fixture-only character/bill-land-water-material-west-v12 loads the four staged joint source banks plus both complete48phase revised walks. Six paired new scripts/test/UID helper and maintained own runner. Exact hyphen AND underscore paths checked before run. Native4793checks0failures116.67s/exit0/no errors;783bounded inputs stable,2931real owner non-log files unchanged using scratchAPPDATA.190control/root/clock/water/path/material presentations exact versusV11;8actual gait phase matches remain28both outgoing,34/35bare and0helmet incoming. Both finite bridges eachgear complete on exact incoming phases.

All four native room/source boards actually inspected. Collar attachment improves; visible head/helmet proportions and vertical registration still change at gait/Ready/Rise handoffs. V10interior head ellipse proxies and historical dynamic-gait fallback remain unchanged, not anatomy proofs. Do not assume revised gait is a canonical identity reference merely because it loads correctly. Next cross-reference original West master and canonical helmet on the common148ruler to establish which source drifts before another head edit; preserve natural posing/foreshortening and body contact.

Complete staged sequences retain500ms/nonloop/H148/p160224,26prior frames exact/30decoded sourceAPNGframes exact/38frozen inputs. New synchronized before/after finite previews reconstruct190native capture ticks with380frozen native PNG inputs. Each normal and quarter-speed APNG decodes exactly:380frames total; entry capture window750ms and exit833ms include pre/post gait, not changed bridge duration. Native browser helmet entry replay observed60to104 at both speeds; screenshot saved. This is reconstructed captured playback, not full continuous live-game visual acceptance. No natural jobs/hydrology/hazards/checkpoint/visibleContinue or normal admission,commit/export.

Six Python syntax checks,six new UID pairs,79source/review raster LFS checks and98selected gait hashes pass. Exact source validation/selection/prompts updated after capture;783hash stability describes native run interval, not later documentation/review metadata. Both own handoffs/indexes retain current scope and next actions. Local loopback preview server restarted after connection-refused; browser now viewed and marked deliverable.

Lesson: a minimal one-target collar edit preserved placement much better in this case; this is observed evidence, not a universal guarantee. Check crown, shoulder and sole independently; alpha thresholds can distinguish soft-edge expansion but cannot certify physical contact. Keep complete source canvases in motion/contact boards, and compare raw sources plus actual station captures at unchanged root/clock. Full Bill goal active: canonical head/helmet consistency,source-bound readability/contact/cadence, natural runtime/Continue and North/South/full-library polish remain.


## Bill West physical master registration and head-neighbor review - October 3, 2026

New character/bill-west-master-head-audit-v1 establishes original West master crown20/forefoot sole976 at existing density148/956, sole mapped to common224. Earlier image-bottom reference placement put the actual sole7.453125px high because the master has empty space below its boots. This corrects review registration only; no runtime art or density changed. Source landmark uncertainty2px is diagnostic, not anatomical segmentation. Sixteen authoritative source/manifest/canonical-helmet inputs frozen unchanged. Established helmet idle/crop is authority; a revised walking candidate is not automatically canonical.

New character/bill-west-master-head-repair-v1 keeps eight builtin generation receipts, exact prompts, source/reference/original/copy hashes. Two multi-reference v1 results rejected for severe whole-body movement (bare clipped at original canvas, body IoU.438; helmet IoU.495). Minimal single-target retries give provisional bare028v2 and helmetReadyv2; four neighbor single-target edits027/029/034/035 completed and all individually reviewed. Five bare corrections reduce head silhouettes, crown1-3px lower; body-below115 IoU.9775-.9817. HelmetReady crown moves65to72, nearer established idle, body IoU.9804. Small1px boot/hand edge changes remain; no opaque pixels outside original canvases. Uniform raw1254-to352 then reverse documented padding only; no head/body pose fitting. These preserve pose substantially better but face/shoulder detail remains softer than original master, and helmet identity/contact still provisional.

Full48phase bare source comparison now includes these five corrections and43 untouched frames, preserving2s normal/8s quarter-speed timing. All96 decoded APNG frames exact;54 source inputs frozen; neighbor boards show remaining head-size joins at untouched boundaries. Browser normal and slow replays observed advancing to47/47, screenshot saved. This is partial source-bank diagnostic, not continuous live-game acceptance. No isolated subset installed. Eight receipts/two rejected,16 audit inputs,98 selected gait inputs,4 Python syntax and43 PNG LFS checks pass. No native run/owner profile access this milestone; prior V12 native results do not validate these new heads.

Lesson: align reference physical landmarks, not transparent/image bounds; retain original density and reviewed landmark uncertainty. Master likeness and silhouette preservation do not prove detail or cadence. Minimal one-target edits helped these repairs, not a universal rule. Check full-source canvas/sole, each adjacent head, original master and full-bank playback. Never promote a few repaired phases into a completed walking-family claim. Next resolve softness/material identity and remaining43 bare heads, canonical helmet family/Ready-Crouch attachment; bind new source head centers before native joins. Natural runtime/hazards/save-Continue, North/South/full-library consistency and normal admission remain. Full Bill goal active.



## Bill West restrained detail pass and complete head survey - October 3, 2026

Six more builtin source edits completed with immediate raw copies and exact receipts. Detail028v3 used corrected raw sprite plus original master as construction-only support; REJECTED despite better insignia/face: whole figure moved/enlarged,3558 opaque pixels outside original256canvas,body IoU.34891,boots clipped. Rejection raw/candidate/review preserved. Single-target restrained detail028v4 and neighbors027/029/034/035v2 preserve pose much better: body-below115 IoU.95489-.96717, no opaque canvas overflow, crown0-1px higher/right/sole0-1px changed. No per-part fitting/recentering or masked repair. Exact source baseline is frozen proportion candidate, explicitly named in review.json; original walking baseline remains in full-motion review.

Five preferred detail studies improve face, quilting and badge definition modestly at source scale; not complete master fidelity. All five individual whole-figure/master boards and original/proportion/detail family board inspected. Full48 original head/collar survey inspected: head/face shapes, face brightness and badge clarity still vary; fixed crop is diagnostic, not anatomy segmentation. No isolated partial walk installed. Full48 before/partial-after APNGs rebuilt with five detail corrections and43 untouched frames, unchanged2s/8s finite timing;96 decoded frames exact. Updated browser normal and slow starts/endpoints observed; this does not prove continuously watched native cadence.

Fourteen total exact generation receipts/three rejected,16 master inputs/54 motion inputs/48 survey inputs/15 detail inputs/98 selected gait hashes unchanged,6 Python syntax and62 raster LFS checks pass. Original six proportion-review artifacts retained separately. Own source review index/prompt-set and validation rebuilt. No native run or owner profile access this milestone; V12 tests cannot certify new detail sources. Full goal active: finish consistent head/face/material construction throughout walking family, canonical helmet and water source joins/head centers, native/natural runtime/hazards/checkpoint/titleContinue, North/South and full-library consistency/polish.

Lesson: a high-detail support master can override explicit pose/canvas constraints even in a detail-only edit. Reject physically displaced results rather than fitting them back. A minimal single-target clarification can improve linework while still moving edges or interpreting badges differently; inspect original, proportion revision and detail revision together, plus every neighboring seam. Stronger outline is not proof of canonical identity or matte grade. Keep technical checks, source review, runtime acceptance and full-library completion separate.



## Bill West walking border head corrections - October 3, 2026

Four new builtin single-target whole-source edits026/030/033/036v1 combine restrained compact-head and existing-detail instructions. Exact source/target/prompt/original/copied-result receipts saved immediately. All four before/after/master boards actually inspected: crown1-2px lower, body-below115IoU.94985-.96369, sole0-1px lower;036leftbound2px wider. No opaque pixels outside original256canvas. Uniform1254-to352 then remove original32px canvas translation only; no head/body fitting. Proportions improve modestly but face softness/brightness and badge clarity still vary, particularly026. These are provisional source studies, not complete master fidelity.

Nine corrected phases now26-30 and33-36;39 other phases remain unchanged. Expanded13pose neighbor board includes25/31/32/37 untreated boundaries; all48 original/partial head surveys inspected. Complete48frame before/partial-after APNGs rebuilt at unchanged2s normal/8s slow;96decoded frames exact. Build_review discovers actual completed receipt keys; motion labels/counts now derive from source selection. Validator rejects preferred sources with canvas overflow. No isolated partial bank installed, no native run or owner-profile access. PriorV12 native result does not validate new heads.

Eighteen completed exact receipts/three historical rejections;16master inputs,58motion inputs,57survey inputs,15 prior detail-board inputs and98selected gait hashes unchanged. Six Python syntax and79raster LFS checks pass. Own prompt set/review index/validation and handoffs updated; guidance mirrored. Full Bill goal remains active: finish whole walking identity/material family, canonical helmet and water joins/head centers, native/natural jobs/hazards/checkpoint/titleContinue, North/South and full-library polish.

Lesson: combined compact-head/detail instructions preserved these poses, but did not recover consistent detail or grade. Never turn improved body/head bounds into an identity approval. Cross-reference complete sequence and original master; newly shifted boundaries remain pending until the whole family is coherent.



## Bill West shared-sheet source trials and geometry rejection - October 3, 2026

New bill-west-head-sheet-trial-v1 makes ONE builtin whole-sheet edit for25/31/32/37 in fixed2x2cells. Raw1254square uniformly maps to704square; explicit352cells then original[32,0,288,256] extraction. Four complete/master head boards viewed; bodyIoU.91685-.95188, soles0-1px lower, no opaque canvas overflow. Four provisional sources bound byte-exact into head-repair review via immutable shared generation receipt, fixed raw normalization/cell coordinates. No per-body/pose fitting. Head/brightness/detail still provisional.

Expanded four independent sheets00-03/04-07/08-11/12-15: all5new builtin shared results copied immediately with exact prompts/reference/source/original/raw-copy receipts. All20whole sources and master head windows inspected. Three whole groups REJECTED:00-03bodyIoU.844-.899 and up to5px leftbound shift;04-07IoU.474-.528, soles29-32px lower,22/25opaque pixels lost for4/5;08-11IoU.668-.690 and soles13-15px lower. Do not scale/translate these bodies back into apparent agreement. Only12-15 preferred provisionally:bodyIoU.94203-.96505,crowns2-5px lower, soles0-2px lower. Face/master likeness and boot contact still pending. Rejected raw/candidates/boards/receipts retained, never selected.

Full48source comparison now includes17provisional corrections12-15 and25-37,31unchanged phases. Full48partial head survey and13pose neighbor board inspected; palette/detail/head differences remain.96decoded sourceAPNGframes exact at unchanged2s/8s.26pose receipt files represent20distinct generation units in head bank;8derived cells from2shared generations are not8provider calls. Three failed shared generations remain separately in expansion bank; total authoring units across these source banks23,not26or31. Prompt report deduplicates shared IDs and derives actual phase labels.

Validation:head bank16master/66motion/65survey/15prior detail/98selected gait hashes stable,6Python syntax/95PNG LFS. Shared source validator5generation calls/20explicit cells/8exact bound candidate pixel comparisons,4Python syntax/45PNG LFS. No native run or owner profile access; priorV12 applies only to prior sources. No normal admission/commit/export or full visual acceptance.

Lesson: one successful fixed-sheet trial does not prove other poses preserve scale. Every cell needs silhouette/sole/canvas checks and whole-source review before binding. Wider strides and mid-step groups here drifted severely while some near-planted sources preserved geometry; this correlation is diagnostic, not a universal pose rule. Keep one common sheet scale, explicit extraction, and reject anatomical displacement instead of fitting it away. Count provider generations separately from derived source cells. Next repair failed00-11 with tightly focused single-target head edits, complete31remaining phases/material/face construction, then source-bound head centers/native joins, canonical helmets/water, natural gameplay/checkpoint/titleContinue and North/South/full-library polish. Full Bill goal active.



## Bill West focused early-stride head repairs - October 3, 2026

Four builtin single-target edits000-003 return to exact original walking sources, replacing the rejected shared-sheet approach for these poses. Exact prompts, source/target/master-diagnostic hashes, original results and immediate project copies retained. Whole before/candidate/master boards actually inspected. Body-below115 IoU.97938-.98067, no opaque canvas overflow, crowns0-3px lower, soles0-1px lower, right bound0-1px narrower. Head silhouettes modestly more compact; face softness and suit/badge detail remain below master fidelity. No pose fitting, recentering or body stretching.

Full48 comparison now21provisional bare head corrections,27unchanged. Added early-neighbor-head-review.png covering47/0/1/2/3/4/5; actually inspected alongside full48partial head survey. Untouched seam47/0 and boundary3/4 remain visibly inconsistent; this is not loop acceptance. Source APNGs rebuilt with original2s normal/8s slow,96decoded frames exact.24distinct generation units/30pose receipt files,8derived shared poses,3individual rejected receipts; separate three rejected expansion calls retained.16master/70motion/69survey/15detail/98selected gait hashes stable;6Python syntax/113PNG LFS checks pass. No new browser or native motion observation, normal admission, commit/export or owner-profile access. Existing browser record predates these four sources; priorV12 native checks do not validate them.

Lesson: single-target retries preserve these wider strides substantially better than the shared sheet, but compact heads remain softer and shift the visible mismatch to untreated neighbors. Review the actual47-to0 seam and both corrected/untouched boundaries, not just consecutive corrected poses. Geometry checks cannot certify master detail or palette. Continue remaining27phases (next004-011), face/badge/matte refinement, canonical helmet/water joins and source-bound head centers, native/natural jobs/hazards/checkpoint/titleContinue and North/South/full-library polish. Full goal active/incomplete.


## Bill West single-target stride expansion and head-attachment rejection - October 3, 2026

Eight builtin single-target head edits004-011 completed with exact original sources, target/prompt hashes, original/raw-copy results and receipts. Seven provisional004/006-011 preserve body-below115IoU.96804-.98453, crowns0-3px lower, soles0-1px lower, right bound0-1px narrower, zero opaque canvas overflow. All eight whole before/candidate/master boards actually inspected.005v1REJECTED: crown10px lower and visibly displaced/compressed head/collar despite unchangedsole225 and bodyIoU.94046. Original005 stays in full sequence; rejected review/candidate archived. Compact heads remain softer than original master; badge shape/detail and face brightness vary, particularly009. This is not master-fidelity acceptance.

Full48 source comparison now28provisional bare phases000-004/006-015/025-037,20unchanged (005/016-024/038-047). Expanded early neighbor board47/000-016 and full48partial survey actually inspected.47-to0 seam,005gap and015/016 boundary remain pending.96decoded APNGframes exact at original2s/8s; no continuous browser/native observation this milestone.32distinct generation units/38pose receipts (8derived shared cells),4individual rejections;3additional failed shared calls remain separately.16master/77motion/76survey/15detail/98selected gait hashes stable;8Python syntax/147PNG LFS pass. No normal admission/commit/export/profile access; existing browser record andV12 native evidence predate these sources.

New prepare_single_head.py reads actual bank-assessment study paths, including028specialname, creates documented352square/+32x target and4xNEAREST enlargement. save_single_head.py verifies prepared original/source/reference/prompt hashes before immediate copy and receipt binding, refuses overwrites. These are deterministic source/provenance helpers, not anatomy fitting. build_motion_review.py expands seam/early coverage.

Lesson: even a near-matching lower-body silhouette and exact sole cannot prove head registration; isolated head/collar displacement can lower apparent stature while bodyIoU remains high. Review actual attachment/crown and neighboring gait, retain original if rejected, and record face/badge/grade softness separately. Next original005 retry with explicit head/collar anchors, then016-024/038-047 and full-family detail/material coherence. Canonical helmet/water head centers, native/natural gameplay/hazards/checkpoint/titleContinue and North/South/full-library polish remain. Full objective active/incomplete.


## Bill West anchored head retry and middle stride - October 3, 2026

Five builtin edits:005v2 from original with explicit eye/nose/chin/neck and unchanged collar anchors;016-019v1 original single targets. All five whole/master boards,14-20neighbor board and full48partial head survey actually inspected.005v2 improves rejected10px-low crown: original78 to77, bodyIoU.98111,sole225 to224.016-019IoU.97835-.98465,crowns2-3px lower,soles0-1px lower,right0-1px wider. Zero opaque original-canvas overflow. No part/pose fitting. Faces still soft and019darker;badge/suit detail/master identity/attachment/grade not fully accepted.

Full48comparison now33provisional bare phases000-019/025-037;15unchanged020-024/038-047. Mid-neighbor-head-review.png added;19/20,37/38,47/0 joins remain pending.37distinct generation units/43pose receipts,8derivedshared cells,4individual rejects plus3separate rejectedshared calls.96decoded APNGframes exact2s/8s;16master/82motion/81survey/15detail/98selected gait hashes stable;8Python syntax/165PNG LFS pass. save_single_head.py now supports versioned non-overwriting receipts. No new browser/native/profile activity; oldbrowser/V12evidence predates new sources. No normal admission/commit/export.

Lesson: explicit feature/neck coordinate anchors plus smaller outline correction helped this005retry preserve attachment; one result is not a universal guarantee, and geometry preservation leaves detail/palette differences. Retain rejection and compare original/master/neighbors. Next020-024/038-047, whole-family detail/matte consistency, canonical helmet/water source centers, native/natural gameplay/hazards/checkpoint/titleContinue and North/South/full-library polish. Full objective active/incomplete.


## Bill West full walking head-study coverage and family review - October 3, 2026

Ten builtin single-target original edits038-047 completed, immediate copies/exact receipts retained. All ten whole before/candidate/master boards, closing36-47/0/1neighbor board and full48head survey actually inspected. NewbodyIoU.97397-.98302,crowns0-4px lower,left/right bounds exact,soles0-1px lower,0opaque canvas overflow. No per-part/body fitting. All48barewalking poses now have PROVISIONAL head corrections, not full visual acceptance.52distinct generation units/58pose receipts,8derivedshared cells,4individual rejected receipts plus3separate failedshared calls. Normal selected gait unchanged.

Added build_family_review.py/family-review.json/walk-water-master-family-review.png: original sole-registered master, seven corrected walking samples0/12/24/28/34/37/47 and prior barewaterReady/Rise. Ten whole sources and fixedhead/collar crops actually inspected. Compact proportion studies are softer than master and vary infacebrightness/collar/badge construction;37/38head shape changes remain noticeable. Water sources retain stronger detail in some areas. Coverage does not prove likeness/detail/grade/cadence/contact. Next review complete48normal/slowmotion and source-scale detail/face/colour coherence, including shared12-15/25/31/32/37 versus single-target frames and water joins. Do not average colours or fit anatomy to hide design drift.

Full48APNGlabels now state complete provisional coverage; finite2snormal/8sslow unchanged,96decoded frames exact.16master/97motion/96survey/15detail/11family/98selected gait hashes stable;9Python syntax/227PNG LFS pass. Index shows family board only if itsselection hash matches currentreview. Rebuild order after a source revision: build_review,build_family_review,build_motion_review,build_head_survey,validate_review. No new browser/native/profile activity; olderbrowser/V12evidence does not cover these sources. No normal admission/commit/export.

Lesson: completing a proportion pass exposes residual differences among authoring methods and adjacent action families. Compare full sources at physical density plus fixed detail windows; exact registration/coverage cannot certify design/material fidelity. Keep originalmaster and establishedhelmet authority. Canonicalhelmet/water sourcebound centers, native/naturaljobs/hazards/checkpoint/titleContinue and North/South/full-library consistency/polish remain. Full objective active/incomplete.


## Bill West shared-source replacement and master-detail limits — October 3, 2026

Seven built-in single-target edits from original walking poses012-015/025/031/032, using the smaller outline adjustment with explicit original eye/nose/chin/neck anchors. Exact targets, prompts, raw copies and receipts retained; former shared-v1 candidates/reviews archived separately. All seven whole before/candidate/master boards, shared-to-single comparison and full48 head survey inspected. Body-below115 IoU .97670-.98735; all soles224 unchanged; crowns0-1px lower; horizontal edges at most1px changed; zero opaque canvas overflow. Preferred whole48 walking studies now contain zero shared-sheet poses; eight historical derived receipts remain as evidence. No per-part fitting or body rescaling. All sources still provisional.

The comparisons show a tradeoff: these single-target revisions preserve original placement better than the earlier shared poses, but faces, quilting, collar and insignia stay softer than the master. A common authoring method does not establish common identity, detail or palette. Preserve older sources for direct comparison; inspect neighbors and master independently, and do not label a uniform method as finished consistency. Next prioritize face shading (including darker026) and source-scale suit/badge definition across the full sequence and water family.

Review/family/motion/head survey rebuilt. New shared-to-single-review.json freezes36 original/prior/current/receipt/master inputs; validator checks them, and index displays its board only while those inputs match.61distinct generation units/67pose receipts,5individual rejected receipts, plus3separate shared rejections.16master/97motion/96survey/15detail/11family/36method/98selected gait inputs stable;9Python syntax/263PNG LFS checks pass;96decoded APNGframes exact2s/8s. No new browser/native/profile run; prior browser evidence predates these seven revisions. No normal installation, commit or export. Canonical helmet/water joins, natural runtime/hazards/checkpoint/titleContinue and North/South/full-library polish remain; full objective active.


## Bill West face-only shading and cropped-master detail trials — October 3, 2026

Four built-in edits saved with exact targets/prompts/raw copies/receipts:026v2 face shading from frozen proportion-v1, then026v3 suit detail from frozen face-v2;030/033v2 suit detail from frozen proportion-v1. The three detail trials use the original master crop[65,120,335,540] solely for material construction. Original master source/hash, crop and saved support are recorded and pixel-verified; no anatomy fitting, masked recoloring or body rescaling. Original high-resolution source confirms the pale circle within the square shoulder plate.

026face v2 preserves all whole bounds, body IoU .98100, modestly clearer warm midtones. Three detail trials preserve body placement substantially better than earlier whole-master reference failures: body IoU .95226-.97023, zero canvas overflow, crowns1px higher;026/030soles1px lower,033sole unchanged225; side edges0-1px changes. Whole before/candidate/master boards, neighboring head board and staged original/proportion/face/detail/master/water comparison actually inspected. Collar/markings/outlines are clearer in places, while faces, quilting and material fidelity remain softer than master and phase-to-phase differences persist. No claim that a face-only or suit-only prompt left every other pixel unchanged. No native contact/cadence or normal acceptance.

Lesson: cropped construction support can constrain a reference's role more narrowly than a whole standing figure; these three observed results avoid the earlier gross pose displacement, but still change edges and facial rendering despite invariants. A cropped reference is not a universal guarantee. Preserve the full target, exact source crop and all intermediate baselines; inspect neighboring sources/master/water and whole feet before deciding whether extra detail helps the family.

Added reproducible build_cropped_detail_review.py (14frozen inputs) and build_shared_replacement_review.py (36inputs/current preferred revision discovery). Validator checks comparison hashes, original support SHA and exact crop pixels; index guards material/method boards against stale inputs. Full48 APNGs remain2s/8s,96decoded frames exact.65distinct generation units/71pose receipts,5individual rejections plus3separate failed shared calls.16master/97motion/96survey/15prior-detail/11family/36method/14material/98selected gait inputs stable;11Python syntax/277PNG LFS checks pass. All48 preferred walking studies remain unselected individual edits. No new browser/native/profile run; previous browser record predates these revisions. No commit/export.

Next expand restrained detail only where neighbor comparisons justify it, and continue full-sequence face/material identity, especially darker019/039 and remaining soft phases. Rebuild order:review, family, shared replacement comparison, cropped detail comparison, motion, head survey, validation. Canonical helmet/water source centers, native natural jobs/hazards/checkpoint/titleContinue and North/South/full-library polish remain. Full objective active/incomplete.


## Bill West cropped-detail gait rejection - October 3, 2026

Cropped-master detail support still changed023's lower-body silhouette (IoU .89883), moved the lowest boot edge2px down and widened both bounds1px despite zero canvas overflow and an unchanged-pose prompt. Reject023v2 and retain registeredv1; keep raw/receipt/review evidence. Other024/032/035detail sources remain provisional, not proof of unchanged contact. Compare whole pose, feet, neighbors and master independently of detail gains. Before rebuilding an earlier comparison that references a replaced candidate, freeze its actual source bytes and bindings; a copied report alone still points at mutable files.


## Bill West restrained sleeve/collar retry - October 3, 2026

023v3 restarts from frozen registeredv1, narrowing the cropped-master edit to existing sleeve/collar interior seams and rivets, explicitly preserving all legs/shoes and the outer silhouette. Whole before/candidate/master and neighbors reviewed. Unlike rejected broad-detailv2 (IoU .89883,boot+2px), this retry retains all whole bounds[103,80,206,224] and bodyIoU .98358,zerooverflow. Detail change is modest; one successful geometry result does not establish universal invariance, master fidelity, palette or contact/cadence acceptance. Preserve both exact prompts, baselines, raw results and rejection. Coverage now rebuilds from preferred receipts and validates against current review; method counts remain separate from quality acceptance.


## Bill West face-definition limits — October 3, 2026

Cropped original-master face support did not reliably restore angular identity: 000v2 remained soft and changed body edges; 046v2 enlarged/displaced the whole figure, leaving 3237 opaque pixels outside the original canvas. Both rejected. Single-target 046v3 and equal-canvas, fixed-physical-density face-reference 046v4 avoided gross enlargement but still failed the master-definition comparison; both rejected. Preserve registered v1 sources and exact raw outputs/prompts/receipts, rather than fitting failures back into place or selecting geometry-compatible softness. Equal-canvas padding is a reference-only construction, reconstructed from the original crop and documented uniform resampling; it is not anatomy repair or proof of likeness. Narrow sleeve/collar edits 001/045v2 remain provisional: lower-body IoU .93485/.98624 shows that even the same restricted prompt is not universally invariant. Whole pose, master, neighboring frames and motion must be reviewed separately.


## Bill West whole-figure rendering pilot — October 3, 2026

After cropped-face, single-target and equal-canvas face trials failed to recover master definition, 046v5 tested the complete original master rendering authority at common physical scale. Some illustrated texture returned, but candidate bounds changed from [106,78,199,224] to [102,77,204,235], body IoU .68906. Boots moved11px lower and figure widened despite the exact-pose prompt; zero overflow did not mean valid registration. Reject and preserve raw result, whole/master board and metrics. Do not force it into place or propagate the method. Original master texture still differs visibly from the walking family. This observed failure supports checking whole-pose geometry and identity independently, not a universal claim that whole-master references always fail.


## Bill current-family evidence and reference authority — October 3, 2026

Current loader/catalog audit resolves212bare/194helmet states, then compares80representative poses in eight same-physical-scale boards. State coverage and manifest age are not art acceptance. East/West show larger face/rendering and cloth variation across idle/movement/actions/cargo/welding; North/South also retain material/detail differences. Fixed standing head windows can miss lowered/swimming heads: inspect whole figures rather than treating a blank crop as missing art. North v5 master-standing is a prepared authored stance/matte reference; source-selection says not pixel-identical original. Correct its label and trace untouched authority before claiming original-master fidelity. Bare references do not certify helmet design; all40equipped samples here are precomposed. Record actual references and registrations instead of inheriting an older board's master label. Static snapshots do not certify full cadence,contact or runtime reachability. Evidence:character/bill-full-family-consistency-2026-10-03-v1/review.json.


## Bill East original-master interaction family — October 3, 2026

An isolated master-identity/material edit of extended-arm003 clarified face and quilt/badge details but created a brightness pulse against unchanged neighbors. Expanded into a complete six-slot provisional family using five independent built-in edits and an exact derived005endpoint: selected000/005source and target pixels and prompts are identical, so reuse000output with an explicit hashed derivation receipt instead of counting a sixth generation. Neighbor wording preserves each actual arm gesture; the extended-arm pilot wording is not blindly applied to resting endpoints. Original East reference is an unpainted crop[300,0,640,1024] from crew-side-masters-v1/bill-side-master-01.png, uniform148/956*4resampling and documented canvas padding, reconstructed pixel-exact. It improved definition in this observed family but is not a universal pose-lock technique. Source body IoU .96475-.98056,crown/sole/side edges0-1px changes,zerooverflow; do not call these unchanged anatomy. Full family is more coherent but remains brighter than current selected idle/gait. Preserve original-master authority and review joins at gameplay scale before admission rather than silently treating either grade as accepted. Pixel/timing/endpoint checks do not certify contact or continuously watched cadence.


## Bill East interaction native density and inherited loader closure — October 3, 2026

Actual Grid Bill loader plus independent fixture-only staged interaction player:
53 checks, zero failures, six exact source-pose captures at H148/82/54/27.
Timing, six source textures, stateful cursors/restores, finite endpoint and return
to selected idle verified. 3303 bounded inputs and all 2931 owner non-log files
unchanged under scratch APPDATA. New Godot tools retain paired UID files.
All three native pages and corrected current-context board visually inspected:
master definition remains clearer at small sizes, but bright face/ivory hardware
still creates an idle/action material seam. Candidate stays provisional/unselected.
Pivot guides are not world floor/contact, continuous cadence or normal-job proof.

A literal manifest audit missed inherited load_candidates: 26 traced manifest
loads add four carry-start states per gear AND overwrite existing carry sources.
Actual native inventory is 216 bare/198 helmet, versus literal 212/194. Preserve
older audit evidence; bind corrected selected sources to the full inherited load
order. Counts/keys do not prove all selected texture pixels or natural reachability.
The old lifeRows summary is still literal-only, not updated closure authority.
First fixture count failure retained; no runtime change to satisfy wrong assumptions.
Review and provenance: character/bill-east-interact-master-consistency-v1/native/.
Next restrained master/idle material pilot, complete-family joins, actual contact,
natural behavior and checkpoint/titleContinue, then whole-library polish.


## Bill East grade pilot: master authority versus legacy seam — October 3, 2026

One built-in whole-figure extended-arm grade edit binds exact previous candidate,
original East master and current idle, raw output copied with prompt/input hashes.
Common352 target nearest4x; whole raw1254 uniformly resampled then184 returncrop,
no source recolor/splice/anatomical fit. Bounds[136,76,224,225] to[136,76,225,225],
body IoU .97479, zero opaque overflow. Raw and four-column density/head board
actually inspected. Cheek/hair/hardware subdued, but face duller than master.
Do not expand/admit this pilot. Earlier warm detailed six-pose study remains
provisional; current idle itself needs coherent master-consistency repair.

Lesson: continuity to an older selected asset is a supporting constraint, not a
replacement for original-master authority. Reducing a seam by dulling improved
identity can move away from the requested full-set result. Preserve rejected
whole-pose studies and compare master, ownidle and action together at physical
scale; geometry checks cannot establish correct color or facial character.
Evidence:character/bill-east-interact-master-consistency-v1/grade-pilot-v1/.
No native run for this new pilot, no normal selection, commit or export.


## Bill East idle master-consistency key poses — October 3, 2026

New character/bill-east-idle-master-consistency-v1 preserves a frozen72-slot/
37uniqueRGBA/3000ms breathing baseline. Two independent built-in complete-pose
edits target18and36 with original East master identity/material authority and
provisional interaction0 endpoint as consistency reference. Exact unchanged
source0 equals interaction0, allowing one explicitly derived seed, not a third
new generation. Raw originals/copies, exact prompt/reference hashes retained.
Whole352canvas/nearest4x targets; whole raw1254uniform resampling and184returncrop.
No source recolor, anatomy fit, part splice or selected-runtime changes.

Both raws, complete eight-panel selected/new/master/action board and five-column
H148/82/54/27 density board inspected. Warmer angular face, quilt, muted red and
circle badge closer to master; midpoint/peak materially coherent with action.
New18/36bodyIoU .97840/.98321,sidebound-1px,zerooverflow. Derivedseed0 has crown
and sole1px different from18/36. Original0-to18/36mask changes36/69pixels;
new187/159: sparse pose resemblance does not prove subtle breathing amplitude,
registration or cadence. Retain3/37unique poses provisional/unselected; no partial
mixed-style runtime loop or static endpoint substituted for original breathing.
277current idle/inherited closure inputs unchanged;2exact targets reconstructed,
2raw/copy hash equalities,4Python AST/12PNG LFS pass. No new native/profile run.

Lesson: exact duplicate source groups permit explicit derived slots; similar
breathing poses do not. Separate source coverage, identity, phase deformation and
floor registration. A shared reference can improve detail while independently
redrawn phases introduce larger temporal variation. Preserve the full cycle and
inspect adjacent poses, constant soles and material joins before selection.
Next temporal registration/refinement plus34missing unique phases, complete
72slot loop/interaction join, then native actor/contact/cadence/runtime acceptance.
Full Bill objective active/incomplete. Handoff in this new bank.


## Bill East idle seven-pose expansion and endpoint registration — October 3, 2026

Five new independent whole-pose edits0/1/9/27/35 extend18/36 to7of37unique
breathing poses. A peak-rendering reference plus original master and exact target
replaces the earlier derived endpoint; previous3pose evidence archived intact in
key-pose-evidence-v1. New start and all seven candidates match original crown/sole
bounds, resolving prior seed1pxverticaldifference without local anatomy fitting.
Sidebound0or-1px;bodyIoU.97779-.98790,zerooverflow. Warm angular face/quilt/hardware
more coherent across phase and interaction study. All raws/both full comparison
pages inspected;0/18/36/master/action H148/82/54/27 board reviewed.277normal idle/
inherited closure inputs stable;7exact targets and raw-copy equalities,6Python AST/
34PNG LFS pass. No native/profile run or selection change. Full72slot/3000msloop
still absent;30unique phases remain. Neighbor0/1and35/36pixel diagnostics retained,
not a continuous cadence certificate.

Lesson: retain prior derived provenance when independently reauthoring an endpoint;
current coverage must count actual generation receipts, not the historical seed.
Match unchanged contact to original targets, compare adjacent phases as well as
extremes. Crown/sole equality does not establish anatomical phase amplitude or
worldcontact. Do not silently reduce37unique phases to a few held poses. Full
Bill scope remains active; next missing phases/full loop/interaction join, native
actor contact/cadence and full-library cross-family polish.

Temporal follow-up: Adjacent selected0/1and35/36alpha masks identical; new65/52mask changes and premultipliedRGBmean.91/.75 versus.00008/.00098. Independent redrawing introduces variation much larger than breathing; no temporal acceptance. Investigate phase-preserving consistency against existing breathing contract before blindly authoring30remaining. Full72slot/37phase/3000ms target remains intact.


## Bill East complete master breathing replay — October 3, 2026

New character/bill-east-idle-master-motion-v1 replaces independent phase redraw
noise with the existing accepted chest-only animation recipe from one original-
master-guided whole-pose source0. Before reuse, recipe reconstructs ALL72selected
East RGBA frames exactly. Full72slots/37distinct phase groups/3000msdurations retained;
1.25pxchest expansion/.65pxrise, headrows0:53andfeet121:183exact at every phase.
This is motion authoring from generated artwork, not local identity painting,
recolouring, anatomical fitting, static holds or a reduced phase count. Seven
independent prior art studies retained as source/material diagnostics; thirty
additional independent redraws are not needed to replay the proven full motion.

First build failed exact phase0RGBA: premultiplied roundtrip cleared invisible RGB
in transparent chest pixels. Failed builder/72frames archived; zero-displacement
phase now uses source unchanged. Full144decoded normal/slow APNG frames exact.
Source donor0exact and all37originalduplicate groups preserved.

Actual normal Grid/Billplayer, fixture-only full idle override:448checks/0failures,
engine0/13.17s,all72source/cursor/snapshot checks, two wraps,nine density captures.
3688bounded inputs and all2931owner non-log files unchanged under scratch APPDATA.
Nine actual captures/five pages and selected/new phase board inspected. Improved
warm face/matte quilt remains coherent at H148/82/54/27. Source-player proof does
not certify main/world floorcontact, natural behavior, continuously watched
cadence,actionjoins/fullSave/TitleContinue or normal admission. Candidate unselected.
New tools keep paired .gd.uid;3Python AST/162PNG LFS checked including failed evidence.

Lesson: before reauthoring dozens of near-identical phases, inspect the accepted
motion recipe. Replay the entire proven chest envelope from improved generated
source, pin identity/support contacts, verify original replay pixel-exactly and
bind motion derivation separately from new art generation. Preserve all frames
and exact durations. Identity motion must preserve hidden RGBA as well as visible
appearance. Next idle/interact/sourcecontact joins and actual-world cadence; then
other cardinal/gear/water/life families and whole-library master polish.
Full Bill objective remains active/incomplete.


## Bill East actual-room idle / interaction source join — October 3, 2026

Separate V2/V3 actual main/Bill/default cold_store reviews establish retained bare source admission, prescribed paused phases and fixed-root sole depth. V1 called actor.update directly while expecting pause; main owns that guard, so the actor moved (746checks/240failures). Preserve failed fixture/evidence; corrected V2 invokes actual main process guard,896checks0. Do not repair runtime artwork to satisfy a probe that bypasses its controller contract.

Actual dry bare drawing caches human_animations/human_animation_timing rows at load; subsequent player.load_manifest alone leaves those tables selected. Bind staged rows explicitly in the fixture and observe actual retained actor submission before screenshots. Player-only evidence is not proof of normal room admission.

V2 confirms old interaction0/3/5 soles one source pixel low. New bill-east-idle-interact-joined-v1 uses whole new idle0 at endpoints0/5 (normal selected endpoints also alias idle0), and lossless whole184canvas y-1 at3. No opaque pixels discarded, surviving RGBA exact;1/2/4 whole byte copies. Preserve760ms action/full72slot3000ms idle. No scaling/recolour/head splice/anatomy fitting or normal selection change.

V3 strictYsole:902checks0,150samples(72idle/6interact/72return),36native/source captures,zero depth findings;4404before/after inputs and2931owner non-log files unchanged,scratchAPPDATA,engine0/48.83s. Entire source board/all3fixed station crop pages inspected. Warm face/matte detail remains visible at station scale. Compare source contact at bottom opaque pixel boundary(bottom+1), actual65.28/H scale and384*.038 root lift; horizontal sole centroid is diagnostic, not planted-foot anatomy acceptance. As-run contactAccepted means Ysole only; detailed verification excludes full2Dfoot, autonomous dispatch, continuous cadence, fullSave/TitleContinue and normal admission. Native input report preserved before later review metadata.

Next continuous idle/action/return review, cross-family head/material/shoulder joins, other East states and full cardinal/gear/water/life polish. Full Bill goal active/incomplete; provisional/unselected. Handoff:character/bill-east-idle-interact-joined-v1/HANDOFF.md.


## Bill East temporal inspection and rejected first-reach revisions — October 3, 2026

Joined motion.html now plays full72idle/6interaction/72return sources at original6760ms and offers normal/quarter speed, per-pose seeking, same ground line and three display scales(source2x/H82/H54). timeline.json rebuilt byte-exact from manifest, all78source hashes unchanged. Actual browser normal and quarter runs reach150/150sampled slots and final6760ms; sampled idle0/reach1/2/3 screenshots inspected. This proves preview advancement and those visible poses, not continuous visual acceptance of every frame, native autonomous cadence or normal admission. browser-motion-review.json preserves scoped evidence.

Source endpoint head RGBA exactly matches idle across entry/exit, soles172throughout. Interior first-reach head/collar differs visibly from idle in sampled view; unregistered head pixel deltas include legitimate pose movement and must not become a style score. Preserve geometry/motion diagnostics separately from identity/material judgement.

Two built-in whole-pose slot1 master+idle consistency revisions retained as rejected pilots. V1 common352bounds[135,75,207,242] versus exact target[136,75,200,224]:height+18px,173opaque pixels outside compatibility crop. V2 uses all1254square references/explicit531pixel height and sole798ruler, still[137,76,207,237]:height+12px,sole+13px,8opaque outside. Both improve illustration detail but change build/contact; raw and complete comparison boards inspected. Same-sized references and numeric prompt rulers alone did not enforce geometry in these observed cases. Do not crop boots, force anatomy into place, propagate method or run native acceptance on rejected poses.

Exact raw copies, six reference hashes, two actual generation receipts/prompt hashes retained,16new PNG LFS attributes/Python syntax pass. No normal runtime/source replacement. Next try detailed fresh idle0 whole figure as edit target with first-reach pose guide; preserve existing face/build/feet while authoring connected arm/shoulder motion through built-in editing. Evaluate one full pose before expanding interior1/2/3/4. Other East families, West provisional bank, cardinal/gear/water/life and full-set master polish remain open. Goal active/incomplete; no live generation handles.


## Bill East detailed-donor reach and stature limitation — October 3, 2026

New bill-east-reach-adjacent-motion-v1 retains all six 760ms slots and exact
idle endpoints. Detailed idle edit target produced a closer warm face, collar
and matte suit. Independent expanded poses from the same donor changed occupied
height to205/191/223 and overflowed; rejected before admission, preserved without
anatomy fitting. Small adjacent whole-pose edits yielded four usable source poses;
supporting superseded recovery remains traceable. All whole figures and three
actual native comparison pages reviewed.

Actual main paused furnished-room V4:904checks0,150prescribed samples,36capture
pairs,engine0/53.84s.4567tested inputs and2931owner non-log files unchanged under
scratch APPDATA. Strict Ysole depth passes. Current crowns24,24,23,22,21,24 and
heights148,148,149,150,151,148 reveal late-pose head/stature rise. Lossless whole
Y-1 registration preserves pixels/contact but can increase crown drift: fixed
profile height and floor checks do not establish anatomical stature consistency.
Candidate provisional/unselected; natural dispatch/full cadence/gear/whole-run
Continue and normal admission remain unverified. New-bank browser review pending.

Lesson: a successful detailed-donor pilot does not establish family consistency.
Compare both contact and stature before expansion/admission. Try small direct edits
from the successful donor to reduce accumulated redraw drift; retain rejected
results and complete provenance chains. Source head-window differences include
movement and are not a style score. Verify PNG RGBA/hash before treating a black
transparent preview as corruption. Use explicit UTF-8 for generated tool reads;
display-only board-label correction retained original pages and exact body pixels.

Full Bill goal active/incomplete. Next late-reach stature/arm arc, full playback,
other East/West/cardinal/gear/water/life families and complete master polish.
Handoff:character/bill-east-reach-adjacent-motion-v1/HANDOFF.md.


Bill East direct recovery follow-up (October 3): built-in edit from successful
first-reach raw001, exec-6a2d312f-0298-47dd-b737-de1423a9a7bf, preserves sole224
without registration and reduces recovery stature excess from3packed pixels to1.
Common bounds138,75,203,224 versus donor138,76,199,224; zeroopaque overflow,
lower-body IoU.960468. Entire raw and four-column whole/master/head board reviewed.
Forward low forearm/material improved, but collar/hair still redraw slightly and
complete sequence/cadence remains untested. Keep provisional source study outside
current six-slot manifest; earlier904native check does not cover this new source.
Three receipt/reference/prompt checks and Python syntax pass;3PNG LFS attributes
checked. No normal selection change. Full goal active; fix extension stature,
then assemble and review complete candidate sequence before runtime validation.
Evidence:character/bill-east-reach-adjacent-motion-v1/recovery-direct-004-v3/review.json.


## Bill East full reach stature refinement — October 3, 2026

New bill-east-reach-adjacent-motion-v2 retains exact idle endpoints, slots1/2,
six original760ms durations and full150slot/6760ms idle/action/return timeline.
Direct recovery from first reach and relaxed-shoulder extension reduce source
heights148/148/149/150/151/148 to148/148/149/149/149/148. Whole extension drawing
translated downward during generation; lossless whole y-6 registers source sole172,
all surviving RGBA/alpha counts exact, no anatomy fitting/scaling/head splice.
Aligned lower-body IoU.970777. Source raw/complete master comparisons and full
six-pose before/current board inspected. Face/shoulder and extended/recovery arc
still need polish; one-pixel stature variation remains.

Earlier small arm-extension edit exec-a28535b2-df60-46b2-84dc-124a445e8bc4 enlarged
occupied height58px, sole57px lower,1850opaque crop overflow: rejected/preserved.
Successful shoulder-relaxation source exec-603489c2-4190-4302-baa1-95dd9d2f0118
has occupied height149, source wholebounds138,81,229,230 before registration.
Both actual raws viewed. Small-edit wording alone does not protect geometry;
measure whole figures and reject real anatomy growth. Whole-canvas translation
may be registered losslessly only with no discarded alpha and continued source
proportion/master review; it does not repair anatomy or establish visual acceptance.

Nine source inputs,78timeline hashes,three receipt/reference/prompt chains stable;
four Python syntax/15PNG LFS pass.12decoded APNGframes exact760/3040ms. Current
bank has no native validation; earlier904checks cover prior v1 only. Normal
selection unchanged. Browser normal advancement complete150/150; quarter/sample
review recorded separately. Full Bill goal active/incomplete: actual room/current
cadence, other East/West/cardinal/gear/water/life and full-set master polish remain.
Handoff:character/bill-east-reach-adjacent-motion-v2/HANDOFF.md.


## Bill East current reach actual-room and cross-family milestone — October 3, 2026

V5 actual main/Bill/furnished Cold Store bare-room fixture loads current
bill-east-reach-adjacent-motion-v2, binds real retained source tables and checks
all six occupied heights against inspected148/148/149/149/149/148.910checks0,
150prescribed paused source samples,36native/source capture pairs,zero Ysole
findings;engine0/51.07s.4542tested input hashes and2931owner non-log hashes
unchanged,scratchAPPDATA. All4542as-tested inputs and nine source-lineage hashes
rechecked before later review metadata. Native as-tested family report retained.
All three full fixed native crop pages inspected; improved matte detail/warm
face and reduced stature drift persist at station scale. One-pixel stature and
small face/collar variation, abrupt reach return remain open. This is prescribed
bare source/depth evidence, not continuous cadence,2Dplanted feet,natural chooser,
gear/water,fullSave/TitleContinue or normal admission.

Eight representative original-master/staged-idle/reach and selected idle/walk/
run/carry/weld sources compared at common declaredH148/p160224. All figures and
head diagnostics reviewed; whole figures authoritative. Literal plus inherited
closure bindings and current loader block unchanged. Carry uses current East
gait-v3, correcting historical literal cargo context. Selected faces darker and
walking/running fabric smoother/less detailed than master; broad family matching
still open. Never propagate improved single family as full library acceptance.

Five Python syntax checks,two paired native UID files,76new native/cross PNG LFS
attributes verified. Normal source/loader unchanged. Next current reach arc/face
polish plus full East walking master pilot; West48phase/cardinal/gear/water/life/
hazard/fullset consistency remain. Full goal active/incomplete; previous turn
classified progress (complete revised reach bank/source and browser evidence).
Handoff:character/bill-east-reach-adjacent-motion-v2/HANDOFF.md.


Bill East walk master pilot (October3): one full stride24 of48, built-in
exec-73ef655c-2404-4bca-905d-d17ea95e929f. Exact raw/prompt/three refs saved.
Master/detailed support refs use same physicalH148/p128224 fourfold profile as
whole target while preserving high source density. Archive first whole-square
density mismatch and second low-res packed/upscaled preparation before generation.
Use1408common (4x352), crop736 (4x184), translate144,208 onto1024; no bbox fitting.
Matching canvas sizes alone does not match physical scale. Packing to low-res then
upscaling discards reference detail; perform fixed profile operations directly at
high density for generation refs and reduce once for actual compatibility output.

Whole raw/master/donor and neighbor23/24/25 boards inspected. Warm face/quilt/
worn hardware closer, but bounds85,78,181,224 versus85,81,180,223: crown-3,
sole+1,height+4,IoU.930729. Single revised pose would create a head/material seam
against unchanged neighbors. Keep provisional geometry/temporal issue, no normal
manifest/admission/native run. Do not falsely count this as full48source coverage.
Provenance/neighbor hashes stable;6Python syntax/11PNG LFS checks pass.
Next restrained full-pose stature/contact correction and representative other
stride phases before full48 expansion. All other Bill family/polish scope remains
active; no live generation handles. Handoff:character/bill-east-walk-master-pilot-v1/HANDOFF.md.


## Bill East four representative master walking poses — October3,2026

New built-in whole-pose0/12/36 and24v2 head/neck settling repair extend source
study to4of48preferred walking poses; five generation units including superseded
original24. Four new raws and all full target/new/master boards inspected.
keypose-review-v1 compares all four originals/candidates/master, source/head and
H148/82/54/27density; all boards inspected. Full loop not reduced to four holds,
no partial manifest or normal admission.44source slots remain unpreferred.

Phase24v2 reduces prior height+4 to exact selected142pixels. Its whole canvas
is losslessly registeredy-1, survivingRGBA and alpha counts exact/no discarded
alpha. Other three whole uniform256packed sources unchanged. Preferred occupied
heights145/147/142/147 versus selected144/146/142/146, deltas1/1/0/1; Ysole deltas
zeroall4. Bounds delta0(-1,-1,+1,0),12(0,-1,+1,0),24(-1,0,+2,0),36(-4,-1,+1,0).
Matte quilt/worn hardware/warm angular faces closer, face/collar/boot shape still
variable. Phase36 extra4pxleft extent remains anatomy/motion review concern.

Fixed foot crop reviewed. Lowest-row Xcentroid deltas.75/1/-1/7.818px are raster
diagnostics, not physical support positions. Phase36 bottom4rows span120..151
selected versus122..151new, despite large lowest-row centroid difference. Changed
sole shape/rasterization can alter this statistic; neither centroid difference
nor matching Ysole alone proves/slips2Dplanted anatomy. Preserve full foot review.
Declared standingH148 does not require constant occupied gait height: keep
authored phase-dependent body articulation rather than fitting everypose to148.

Four receipt/reference/prompt chains and49selected manifest/frame hashes stable;
sixPython syntax/39PNG LFS checked including preparation/old source evidence.
No native run/browser/full48cadence or normal loader change this pass. Prior910
nativechecks cover idle/reach only. Next inspect accepted East gait source/motion
provenance before blind44near-phase redraws; refine shared face/boot continuity,
expand complete48original phases/timing and native joins. West/cardinal/gear/
water/life/hazard/full-library master polish remains. Full goalactive/incomplete;
previous turn progress, all four current generation jobs terminal/raws saved.
Handoff:character/bill-east-walk-master-pilot-v1/HANDOFF.md.

Bounded East walk source trace: selected material builder grades fabric and stamps historical shared head on48 existing poses; underlying runtime-matte manifest records exact selected review-v9 PNGs/timing. Inspected files do not provide a reusable full-figure gait derivation from one new source. This is not an exhaustive absence claim. Preserve current art and trace evidence; do not replay historical identity stamping/grade as new whole-pose master repair. motion-source-trace.json freezes inspected paths. Continue full48authoring/temporal proof; four keys remain provisional.


## Bill East complete48 whole-source walking revision — October3,2026

`character/bill-east-walk-master-full-v1/` now has48 unique whole authored
walking poses, original48phase durations totaling2000ms,256canvas,pivot128224,
standingH148,stride.1796875. Normal/quarter APNGs decode96exactRGBAframes with
2000/8000ms timing. Source occupied-height deltas[-2,2], Ysole delta0all48;
whole uniform packing/lossless Yregistration only, no head stamps/local grade
or anatomical warping.49selected manifest/frame hashes and four prior preferred
keyframe hashes stable. All16 full/raw/master/density boards inspected.

The six-pose sheet trial failed scale/background/motion fidelity and was rejected
before extraction. Early individual trials4/6/7/8/10 grew or shifted anatomy;
their raws retained and replaced. Initial supporting walk image1254 versus
1024targets was an avoidable reference-size mismatch. Uniform source-derived
1024matched references plus explicit original geometry yielded useful repairs;
this combined change does not prove reference size alone caused the failures.
Six acceptable early individual poses retained with whole Yregistration. No
video provider/key used. All current48 raws saved with receipt/prompt/reference
hashes; all source-authoring jobs terminal. No partial four-hold loop substituted.

Browser normal/quarter displayed all48phases, respectively>=1/2 complete loops;
0/12/24/36/47 inspected enlarged and H82/54/27. Browser phase screenshots retained.
Advancement/static review do not establish full continuous cadence acceptance.
Native V2 actual main/Bill/default furnished ColdStore retained bare renderer:
1129checks0failures,192idle/walk/return prescribed samples,40world/source capture
pairs, four full fixed-crop pages inspected. Engine0/noERROR/WARNING,52.04s;
4707tested inputs and2931owner non-log files unchanged under scratchAPPDATA.
Current matte quilt detail/warm face survive room density; strict Ysole depth
passes. Walk phase prescribed directly for stationary source sampling because
gait advances by distance. Failed V1 retained:84fixture failures caused by
clock-only stationary walk sampling; two browser screenshots added during its
freeze were also detected. V2 sampled correctly and frozen inputs stayed stable.

This is scoped source-submission/size/depth proof, not natural locomotion,
2Dplanted feet, continuous idle/walk joins, normal admission, equipment/water,
natural job dispatch or fresh fullSave/TitleContinue. Face/collar/boot continuity
and phase36 width remain provisional. Current game loaders unchanged.14Python
syntax/494PNG LFS checks passed. Full Bill objective remains incomplete;
next close natural distance-driven walking/joins, then remaining West/cardinal/
gear/water/life/hazard/cargo full-library checks. Handoff:
`character/bill-east-walk-master-full-v1/HANDOFF.md`. Previous four-key notes are
historical:44missing sources have now been authored, not yet fully accepted.


## Bill East real actor walking/arrival comparison — October3,2026

`character/bill-east-walk-navigation-v1/` retains native navigationV2 evidence:
actual Bill.update/move/arrive on a clear320unit East segment selected from the
default furnished ColdStore graph, with segment/floor checks. Candidate and
selected traverse the exact route in348simulation steps of.02s,6.96s each,
displaying all48gait slots. Retained renderer phase increments equal actual
distance/384/stride*2.0seconds-cycle; no phase prescription or actor
teleport between samples. Before/after idle and190actual world/source pairs
retained; four full route comparison pages inspected. Normal/quarter APNGs are
exact native505x155room crops with actual simulation capture intervals; four
decoded movies total380frames byte/timing exact. Current face/matte quilt detail
survives movement; direct extended-stride first step and arrival-to-idle pose jump
remain in candidate and baseline. These joins are the next concrete defect, not
evidence of changed body scale. No continuous-cadence/fullvisual acceptance.

Engine exit0,4064checks0failures,87.2s,2931owner non-log hashes unchanged under
scratchAPPDATA. All tested Bill/renderer/source-bank inputs stable. Complete
4796input freeze did NOT pass: concurrent airlock_panel.gd,crew_work_panel.gd,
moonbay_panel.gd edits captured in before/after hashes. Scope this as as-tested
actor movement proof, not a clean full-project run. No repeat of unrelated UI
work and no rewriting the failed freeze to passed. Earlier navigationV1 retained:
four fixture failures because absent construction goal cancelled route; current
neutral route uses goalempty. Room inspector lookup was already corrected in
shared source from inspector_label.parent to inspector_details.parent beforeV2;
this task's attempted patch did not apply and no UI change is claimed here.

Main/tick disabled, route/source binding explicit; only actor.update is advanced.
Actual movement/navigation/arrival and distance-driven renderer exercised, not
autonomous goal choice/full station progression. Resources/failure flags unchanged.
SixPython syntax/11PNG LFS passed. Current normal Bill sources unchanged,
no export/commit. Full objective incomplete. Next author/review short whole-figure
first-step and stop joins without composited anatomy/ghosting, then normal family
admission and remaining West/cardinal/gear/water/life/cargo checks. Handoff:
`character/bill-east-walk-navigation-v1/HANDOFF.md`.


## Bill East whole-figure first-step/stop joins — October4,2026

`character/bill-east-walk-joins-v1/` adds four built-in authored half-settled
whole poses from walk anchors0/12/24/36 toward the exact current idle endpoint.
Four jobs terminal, raws saved immediately with generation/receipt/prompt/ref
hashes; original-master identity and same1024physical-profile references retained.
Initial idle-reference preparation incorrectly resized raw1254 into184profile;
detected during pre-submit image inspection, corrected to exact current184idle
canvas inside common256profile BEFORE any generation. No output used bad reference.
Uniform256packing and lossless whole Yregistration2/0/3/0; occupied heights
145/149/143/149,sole224all4, no anatomical fitting/head stamp/local grading or
crossfade ghosts. All whole raws and full walk/middle/idle/density board inspected.
Existing48master gait sources and2000ms timing remain byte unchanged.

`tools/bill_east_walk_join_candidate_v1.gd` is an opt-in provider through the
small nullable `human_walk_join` hook in grid_canvas.gd (normal defaultnull).
First step holds standing<45ms then authored middle to130ms before rejoining
the continuously distance-driven gait. Stop holds exact last displayed pose30ms,
then closest quarter-stride middle until140ms before live idle. Foot/path/speed
and underlying gait clock unchanged. Short moves stopped before visible first
step cancel without a phantom step; restarting during settle retains the current
displayed pose and branch. No normal loader/source selection change or art preload.

NativeV1 current-art-with-joins versus older selected art:4064checks0,4828inputs
unchanged,92.62s. V2 after interruption fixes isolates join effect with identical
current master gait/idle art for joined/unjoined controls:4064checks0,94.85s,
4846inputs unchanged;320unit legal ColdStore route,348steps/6.96s pervariant,
all48gait poses displayed,190actual world/source capture pairs. Both native runs
engine0/noERROR/WARNING;2931owner non-log hashes unchanged under scratchAPPDATA.
All eight full native comparison pages and current normal/quarter browser snapshots
inspected. 380current native APNG decoded frames exactRGBA/timing.
Targeted isolated headless checks536/0 cover all48stop phases, repeat-at-paused-time,
restart during settle, tiny-move cancellation and direct provider gear/water/
other-state bypass. That bypass is provider-unit evidence, not actual equipped/
water/death renderer dispatch acceptance (those paths may return before this hook).
12Python syntax,6new paired uniqueGDUIDs,38PNG LFS checked.

Visual outcome: smaller first-step/standing changes without changing the walking
art; current matte detail/warm face survive. Small face/collar/boot differences
remain provisional. Source/capture/branch review does not certify continuously
watched full cadence or2Dplanted feet. Normal family admission, run/carry/work
boundaries, actual context cancellation/equipment/water dispatch, autonomous jobs,
fresh fullSave/TitleContinue and remaining West/cardinal/life/hazard/cargo master
closeout still open. No commit/export. Full Bill objective incomplete; authorized
work continues. Handoff:character/bill-east-walk-joins-v1/HANDOFF.md.


## Bill walking joins: actual activity dispatch correction — October 4, 2026

Optional provider reset now occurs before gear/water/direction/other-state/action
early returns in scripts/grid_canvas.gd, and explicitly on death/inspection/meal
texture overrides. This closes stale walking/settle after special activity bypass.
Normal provider remains null; no loader/art admission or actor movement change.
Actual native getter checks:82/0,engine0/noERROR/WARNING,9 prescribed contexts
(helmet,water,West,run,carry,weld,construction entry,inspection,meal),12 retained
room/source captures,87.44s. Every special source equals provider-free control;
each dry East idle return equals current idle without stale gait. Scratch APPDATA,
all2931owner non-log hashes unchanged. NOT natural context choice/full gear/water
loops/death transition acceptance. Grid/helper frozen bytes unchanged during run.
Whole-project freeze FAILED: concurrent scripts/main.gd edit and two review-only
artifact additions. Raw failed validation preserved; no clean full-project claim.
New fixture omitted from broad runner input map; exact current fixture copied,
not asserted before/after-frozen. FivePython syntax/onepaireduniqueGDUID and PNG LFS.

context-review-v1 contains ten common-H148 source samples, native boundaries and
browser proof, all full boards visually inspected. Selected run/carry/weld remain
darker with coarser face/suit detail than current master idle/walk/reach. Physical
registration is declared whole-scale/pivot only; lean/gait bounds not forced.
First native review crop hid upper character, caught in image review and corrected
to315,155,820,310 without altering native captures. Review scope only; full loops
not accepted. Next concrete matching target is these three East activity banks,
then native boundary motion and family admission. No additional walk regeneration.
Current normal selection unchanged, full Bill objective incomplete; no commit/export.
Handoff:character/bill-east-walk-joins-v1/HANDOFF.md.


## Bill East complete six-pose running master repair — October 4, 2026

character/bill-east-run-master-v1 authors all6 East run figures using built-in
imagegen, after proving whole phases0/3; raw sources, exact prompts, reference
paths/hashes and6generation receipts retained. Each target/currentidle/master
uses matched1024physical profile. Returned raw squares are1254, not displayed1280;
actual file measurements establish density, avoiding a mistaken corrective scale.
Uniform whole raw→256 packing; no local grading, head stamp, anatomical splicing
or per-pose stretching. Disconnected <=3pixel components with maxalpha1 removed
as invisible background dust only. WholeY shifts0/0/0/0/0/-1, lossless alpha contact
registration to each original phase sole; height deltas1/1/1/0/1/3, sole delta0all6.
Original ordered6durations90/80/100/90/80/100 =540ms, loop and run stride.168 intact.
Original selected manifest+6frames remain byte unchanged. Four APNGs each6frames,
normal540/quarter2160ms,24decoded frames byte/timing exact.

NativeV1 preserved:75checks10failures because fixture seeded clock position with
actor.foot/gridCellSize, unlike actual getter's converted position/offset. Captures
repeated phase0. Corrected fixture only, no art workaround; V2 seeds actual
get_test_walker_position/gridCellSize. V2 engine0/noERROR/WARNING,75checks0,
16actual room/source pairs,52.55s,4960inputs unchanged INCLUDING candidate bank
and exact new fixture/runner,2931owner non-log fingerprints unchanged,scratchAPPDATA.
All6run source selections and last→first wrap verified plus current master idle
before/after, both selected/candidate. Explicit phases at fixed foot in default
furnished ColdStore: NOT physical running route, autonomous emergency goals,
moving boot contact or normal admission/full gear/save acceptance.

All6whole raws, full source comparison,4full native pages and normal/quarter
browser snapshots reviewed. Matte fabric/hardware/warm face closer to master;
small face/hair/badge differences andphase5height+3 remain provisional. Normal
selection unchanged. Preview:http://127.0.0.1:8791/character/bill-east-run-master-v1/.
8Python syntax,2paired uniqueGDUID,62PNG LFS checked. Next: East carry8
and torch6 appearance matching, then moving run/boundary motion and coherent
family admission. Full Bill objective incomplete; no commit/export.


## Bill East backward-running arm repair — October 4, 2026

Owner reported messed-up arm in the prior master-running candidate. Source review
found near shoulder patch pinned to a spare vertical chest sleeve while the
backward arm was drawn separately, especially phases0/5. V1 technical passes
did NOT establish anatomy acceptance; V1 review records complaint/supersession.
character/bill-east-run-master-v2 repairs two COMPLETE figures with built-in imagegen;
exact prompts, four reference hashes/roles, raw sources and receipts retained.
Patch now belongs to upper-arm sleeve; one chain shoulder→elbow→cuff→glove,
without duplicate chest arm. Four frames1/2/3/4 explicitly inherited and
byte-identical toV1. Uniform raw→256 and whole contact registration only,
no arm stencil/head stamp/local grading/per-pose stretching. Height deltas
3/1/1/0/1/3, sole0all6; original540ms/.168stride and selected7inputs unchanged.
APNG24decoded frames exactRGBA/timing. Original V1 raws/provenance preserved.

NativeV3 engine0/noERROR/WARNING,75checks0,16world/source pairs,54.93s,
4962inputs frozen unchanged INCLUDING revised bank/fixture,2931owner non-log
hashes unchanged,scratchAPPDATA. All6source phases and clock wrap plus master
idle before/after. Prescribed fixed-foot sources, NOT physical running route,
natural emergency choice, full gear/save or normal admission acceptance.
Two full raw edits, whole6pose board,4/5/0/1neighbor seam board,4native pages,
normal/quarter browser proof inspected. Direct playback compares reportedV1
against repairedV2. Small face/hair/badge andheight+3variations remain provisional;
no continuously watched native/full-world foot or owner acceptance claim.
6Python syntax,1paired uniqueGDUID,63PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-run-master-v2/.
Normal selection unchanged; coherent family admission and East carry/torch
matching remain next. Full Bill objective incomplete; no commit/export.


## Bill East carrying master pass — October 4, 2026

character/bill-east-carry-master-v1 contains eight complete built-in imagegen
edits, with exact prompts, three reference roles/hashes, saved raws and receipts.
Selected source is bill-carry-east-gait-v3/bare-manifest.json from the current
full closure. Matte suit detail and warm face restored against current idle and
original master. Whole raw resampling to256 and whole contact registration only;
no arm/head stamps, local grade or per-pose stretching. Height deltas0/1/0/1/0/2/1/2,
wholeY1/0/1/1/1/0/0/0, sole0all8. Original840ms/.12stride preserved, nine selected
inputs unchanged; four APNGs/32 decoded frames exactRGBA/timing.

Native carry player dispatch:90checks0,20world/source pairs,140.71s,
engine0/noERROR/WARNING,4974frozen inputs unchanged including exact
bank and fixture;2931owner non-log hashes unchanged, scratchAPPDATA.
All8sources, loop wrap and master idle before/after checked through the retained
furnished-room renderer. Prescribed stationary phases, NOT a physical cargo route,
pickup/turn/unload, autonomous job, save or normal-admission acceptance.
All eight full raws, complete source comparison, five native pages and browser normal/quarter snapshots inspected. Near shoulder, elbow and glove form a connected arm holding the case. Small case hardware/corner, hair/face/badge variation remains provisional; pose3 has visible far-side fingers. No physical cargo route, pickup/turn/unload or owner acceptance claim.
6Python syntax,1paired uniqueGDUID,77PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-carry-master-v1/.
Normal selection unchanged. Next East torch6 master matching, then coherent family
boundaries/admission and real gameplay coverage. Full Bill objective incomplete.


## Bill East torch master consistency — October 4, 2026

Prepared character/bill-east-torch-master-v1: six complete built-in image edits,
each retaining its prompt, three reference roles/hashes, raw source and receipt.
The selected source remains bill-torch-actions-v1/weld-east, previously accepted
for directional torch action. The new candidate restores master matte quilting,
hardware and warm face while maintaining a connected bent arm and East-facing tool.
Original six timings140/160/180/160/180/140 (960ms), loop, pivot128224 and H148
preserved. Uniform raw-to256 resampling and whole contact registration only;
heights+3/+1/+1/+1/0/+2, wholeY0/0/-1/-1/0/0, sole0all6. Seven selected inputs
unchanged. Four APNGs:24decoded frames verified exactRGBA/timing.

NativeV2 renderer evidence:75checks,0failures;16world/source pairs;49.38s;
engine0/noERROR/WARNING. 4960 frozen inputs unchanged, including exact
bank and fixture. Scratch APPDATA; 2936 owner non-log hashes
unchanged. All six source slots, loop wrap and master idle before/after verified
in the furnished ColdStore. These are prescribed fixed-foot phases, not a physical
repair/install job, tool draw/stow, autonomous goal, equipment/save or normal
admission acceptance. Six complete raws, all-pose source comparison, four native pages and normal/quarter browser screenshots inspected. Shoulder sleeve, elbow, cuff and torch grip remain connected. Matte quilting and warmer face approach the master. Small head/hair/patch, nozzle and flame-shape differences remain provisional; no exact pixel preservation or continuous native cadence claim.
FailedV1 retains wrong deferred startup method (zero captures) and concurrent
grid_canvas.gd freeze change. V2 repairs fixture startup only; artwork unchanged.
Eight Python syntax checks, two paired unique Godot UIDs, 62 PNG LFS checks.
Preview: http://127.0.0.1:8791/character/bill-east-torch-master-v1/.

Next: exercise repaired East idle/walk/reach/run/carry/torch family boundaries
together and review admission, before further source expansion. Normal selection
is unchanged. Full Bill objective remains incomplete; no commit or export.


## Bill East combined family audit — October 4, 2026

character/bill-east-family-review-v1 compares six repaired banks (idle72,
walk48, interact6, run6, carry8, weld6) and four existing handoffs (pickup11,
unload6, torch-draw6, torch-stow6):175total source slots and183protected source
inputs. No new artwork, resampling, recolouring or source manifest changes.
Preview pads whole figures only to common256/p128224/H148. Twenty normal/quarter
movies verified against original RGBA and durations, allowing lossless repeated
frame coalescing; direct idle/action/idle timelines are material comparisons,
not authored tool/cargo appearance/disappearance.

NativeV2:374checks0,175source slot identities,50retained room/source pairs,
58.16s;engine0/noERROR/WARNING. 4959 frozen inputs unchanged,
including combined review,183source files/manifests and exact fixture. Scratch
APPDATA;2936owner non-log hashes unchanged. All10banks loaded
together with snapshots of their exact rows before later manifests can override
them; each loop wraps, nonloop holds terminal and each returns to current master
idle. Explicit stationary source phases, NOT actual autonomous transitions,
physical run/carry routes, tool/cargo lifecycle, gear/save or normal admission.
V1 retained374/13 failed checks from fixture incorrectly truncating torch-draw
and torch-stow to torch; V2 preserves full state names, artwork unchanged.

The repaired six-bank family is substantially closer in matte material and identity at a common scale. Run leans and carry changes gait naturally; small pose/head/hair/insignia changes remain provisional. Existing pickup/unload and torch draw/stow remain darker and less detailed, creating material discontinuities at the repaired carry/weld boundaries. No normal admission or owner acceptance. Native comparisons select sources explicitly; they do not certify real tool/cargo handoff controllers or physical movement.
Source first/middle/last boards, all10native pages and normal/quarter browser
snapshots reviewed. Seven Python syntax checks,two paired uniqueGDUIDs,
139PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-family-review-v1/.
Next narrow scope: master-match four existing pickup/unload/torch-draw/torch-stow
handoffs, preserving selected motion/contact; then real lifecycle/moving and
coherent admission. Normal selection unchanged; full Bill objective incomplete.


## Bill East master torch draw/stow — October 4, 2026

Current torch handoff review: character/bill-east-torch-handoffs-master-v1.
Eight built-in whole image edits replace the intermediate sources of two selected
six-slot520ms nonloop clips. Four endpoints reuse current idle/weld whole pixels
exactly (idle padded36,52 into256). Raw1254square uniformly packed to256;
height deltas+1/0/+2/+2/+2/+2/+1/+1, original intermediate sole deltas0;
wholeY0/0/-1/-1/-1/-1/-1/-1. No per-pose scaling, tone masks or part stamping.
Ten normal/quarter APNGs preserve RGBA/durations,106decoded frames including
lossless repeated-endpoint coalescing. Full material sequence idle/draw/weld/stow/idle.
Original selected bank remains unchanged; new candidate is unselected.

Native:156checks0,18source slots, five production construction timer boundaries,
25retained ColdStore world/source pairs,49.38s. Production Bill
animation_state/action_elapsed verifies draw<.52, weld .52..9.48 and stow>=9.48.
Stationary prescribed timers/main disabled; not autonomous construction completion,
tool ownership, moving routes, gear/save or normal admission. Engine0/clean;
4996frozen inputs unchanged,21explicit protected source inputs,
scratchAPPDATA and2936owner non-log files unchanged.

Eight rebuilt intermediate poses retain connected near-arm sleeves, matte quilting and warm face, substantially closer to current idle/weld. Small head/hair/patch and tool hardware variation remain provisional. Exact four whole endpoints and selected520ms timing/contact preserved. Stationary production animation/action-clock boundaries checked; autonomous job/tool ownership, gear/save and normal admission untested.
All eight raw images,both full source boards,four native pages and normal/quarter
browser snapshots inspected. Six Python syntax checks,one paired uniqueGDUID,
99PNG LFS. Preview:
http://127.0.0.1:8791/character/bill-east-torch-handoffs-master-v1/.
This supersedes the family audit's torch draw/stow repair TODO only.
Pickup11/unload6 still need master matching; then real cargo/tool/moving lifecycle
and coherent admission. Other cardinal/equipment/water/life/hazard/save/title
coverage remains. Full Bill objective incomplete; no new owner acceptance inferred.


## Bill East master pickup/unload — October 4, 2026

Current review: character/bill-east-cargo-handoffs-master-v1. Fifteen unique
built-in whole edits cover pickup11/unload6, each original520ms/nonloop.
Shared original ground/held crate endpoints remain two exact whole aliases.
Uniform raw1254square->256 LANCZOS, only disconnected<=3px/maxalpha1 cleanup;
wholeY registration to each original complete-source bottom. No pose stretch,
local grade, head/body/crate stamp or invented pixel interpolation. Crouches keep
their own height. Unique height deltas1/0/1/0/0/0/-1/0/-1/1/0/0/-2/-1/0;
wholeY0/1/0/1/-8/0/1/1/1/1/1/1/2/1/0, bottom deltas0. The -8 shift registers
an entire correctly sized but lowered authored crouch, not a local body/foot edit.
Six first generation geometry mismatches retained with raws/receipts/prompts and
rejection notes: pickup1/4/8/9,unload3/4. Selected retries restore motion depth.
Ten normal/quarter APNGs verified against RGBA/clocks,150decoded frames including
lossless repeated endpoint coalescing; full pickup/carry/unload material sequence.

Native:157checks0,25source slots (pickup11,unload6,current carry8),27retained
ColdStore room/source pairs,34.16s. Production workshop unload state and
action_elapsed used; pickup/carry explicit stationary phases. Exact endpoint
aliases, original clocks and loop/nonloop terminals pass. Engine0/clean;
5071frozen inputs unchanged,29explicit protected originals/current
carry inputs, scratchAPPDATA and2936owner non-log files unchanged.
All15raws,17slot boards,six native pages,normal/quarter browser snapshots reviewed.
Six Python syntax checks,one paired uniqueGDUID,129PNG LFS.

Matte quilting and warm face substantially closer to current idle/carry. Original action depths, contact and clocks retained; identical source endpoints share exact repaired whole pixels. Minor hair/head/patch and case-latch/metal variation remain provisional. Source bounds and renderer checks do not prove named-hand/boot pressure or rigid case geometry. Six initial geometry mismatches rejected and preserved. No normal admission or owner acceptance; actual cargo dispatch/ownership/moving contact/completion/gear/save still untested.
This closes the family audit's four darker East handoff source-repair TODOs,
alongside bill-east-torch-handoffs-master-v1. It does not close actual cargo/tool
dispatch/ownership/completion, moving contact, coherent admission or gear/save.
Normal selected bank remains unchanged; no owner acceptance inferred. Next:
exercise actual production jobs and moving carry with the repaired family together,
then coherent admission and remaining cardinal/equipment/water/life/hazard/save/
title review. Full Bill objective incomplete. Preview:
http://127.0.0.1:8791/character/bill-east-cargo-handoffs-master-v1/.


## Bill actual construction/workshop jobs — October 4, 2026

character/bill-actual-jobs-v1: selected production Bill actor/player, fixture-only
repaired East idle/walk/reach/carry/weld/draw/stow/pickup/unload staging. Actual
paid corridor dispatched, approached, constructed and reservation released; all
18 draw/weld/stow slots visited. Real authored workshop bench entry followed by
production inspect/work/pickup, generated carrying route, arrival/stow and service
completion; all11 repaired East pickup slots displayed, route standing/segments
checked. Monotonic10ms simulation updates; no source-clock seeding. Other facing
and carry transition banks retain current selection. 2,978checks/0,36retained
room/source pairs,38.09s; engine0/clean,5,482frozen inputs and2,936owner non-log
files unchanged under scratchAPPDATA. FourPython syntax,onepaired uniqueUID,
7PNG LFS; six complete same-scale review boards and browser proof inspected.

All six sampled retained review boards visually inspected, plus browser proof. New East pickup/torch handoffs retain matte detail. Existing carry-start/turn and other cardinal banks remain visibly different; coherent normal admission still pending. Weld exits pose2 into stow0 in this job: completion passed, exact loop-to-stow pixel continuity is not claimed. Arrival stow controller presents its North unload through a carry pose; sampled entry/completion captures do not establish every unload-plan source slot or continuous cadence.
First native fixture v1 had21 failures from an invalid East-of-ColdStore build
site; preserved evidence/profile/input maps. Corrected to the actual core East
port for v3. v2 runner stopped before engine launch on output-version assertion.
The initially suspected missing pickup dispatch was disproved: CrewLife.pose and
CrewLife.elapsed already own this phase. No gameplay change was needed or made.
No normal admission, owner acceptance, gear, Continue, autonomous workshop choice
or inventory cargo-ownership assertion. Full Bill objective remains incomplete.
Next: reconcile selected carry entry/turn sources against the repaired family,
then coherent admission and save/resume checks. Review:
http://127.0.0.1:8791/character/bill-actual-jobs-v1/.


## Bill East carry entry master match — October 4, 2026

character/bill-east-carry-entry-master-v1: three built-in whole image edits replace
entry1/2/3; six original320ms holds. Entry0 exactly shares repaired pickup10;
entry4/5 exactly share repaired carry0. Actual generation calls, prepared pose
contracts, four-reference hashes, receipts and raw1254square sources retained.
Uniform256 LANCZOS and wholeY only; no local grade, anatomy/prop stamps or pose
stretching. Three whole intermediates visually match the repaired matte carry/warmer face. Height deltas0/1/0, wholeY1/0/2, all original whole-source bottoms retained. Exact whole pickup at0, exact gait0 at4/5. Original320ms entry and .104s production resume retained. Minor hair/patch/case hardware variation remains provisional; no rigid crate/hand-pressure proof. Other selected turns/cardinal banks and normal admission still separate.
Six normal/quarter APNGs validated:60decoded frames with repeated endpoint
coalescing; stationary source chain preserves .104s gait resume. All three raws,
complete six-slot comparison, two complete native boards and normal/quarter
browser snapshots reviewed. NativeV2:249checks0, all6holds plus actual gait resume,
7retained room/source pairs,26.22s,5,288inputs unchanged,2,936owner non-log files
unchanged under scratchAPPDATA, engine0/clean. Selected production actor/player
actually moves on a prescribed legal96-unit East floor segment at5ms steps.
Not natural workshop dispatch/turns, gear, Continue or normal admission.
SevenPython syntax/two paired uniqueUIDs/43PNG LFS. NativeV1 fixture failed
on JSONfloat-versus-int Array equality and PackedVector2Array.assign; stopped and
maps retained (owner unchanged, concurrent room_content_canvas/room_asset_library
edits detected and preserved). V2 corrects only fixture typing/path construction
and expands freeze to all staged carry/cargo sources. No gameplay changes.
Next: judge remaining turn mismatches at actual station scale, repair only material
join defects, then coherent admission/save-resume. Owner wants closeout soon;
avoid redoing completed sources or expanding polish without demonstrated need.
Full Bill objective incomplete. Preview:
http://127.0.0.1:8791/character/bill-east-carry-entry-master-v1/.


## Bill East master family installed — October 4, 2026

Normal selected source version: bill-east-master-family-v1-cardinal-arrival3.
scripts/bill_carry_player.gd loads ten whole-path master manifests for bare East
idle, walk, reach, run, carry, weld, draw/stow, pickup/unload and carry entry,
plus seven shared East turn programs: 18 states/238 unique logical slots,
310 manifest references (72 identical idle holds repeated by the reach bank).
Per-East stride overrides only; three previous source versions retain 22 source
keys with their clocks/strides and both gear rows. Existing helmet and other
sources remain exact. bill_carry_npc default uses new binding; grid_canvas
refreshes retained bare source tables when Continue restores a different bank,
guarded to the selected production player. No mid-pose source migration.

character/bill-carry-turn-east-seams-v1 reuses the repaired whole pickup10 in seven
held alias slots across seven existing programs; 50 intermediate slots untouched,
original 800/1600ms programs/geometry retained. No new art, local grade, stamps or
body transforms. 28 APNGs/228 decoded exact sources and clocks; 22 protected inputs
unchanged. Native 5,040 checks/0, all57 slots on seven prescribed legal segments,
57 retained room/source pairs,37.87s,5,348inputs and2,936owner non-log files exact.
Seven native first/middle/last boards visually reviewed at actual station pixels;
existing intermediate detail/directional shade acceptable at this scale.

Normal installation NativeV2:4,286/0; all310 manifest references exact RGBA,
four real disk carry-entry resumes (legacy/current × bare/helmet) with30 exact
future updates each, paid construction completes all18 draw/weld/stow slots,
workshop pickup visits all11 slots then generated route/arrival/service completion.
44 retained room/source pairs,40.13s,5,807inputs unchanged,2,936owner unchanged.
Fresh normal Title/main scenes in same native process:101/0, two actual Continue
and loading buttons for bare legacy/current saved entry; source/physical root/clock
and pause exact plus30 deterministic future steps each.4 retained pairs,48.59s,
5,807inputs and2,936owner files unchanged. All successful engines0/clean, scratch
APPDATA only. Nine installation/Title boards and published browser proof reviewed.

Historical fixture failures retained: installV1 used nonexistent Save.valid;
stopped after91.46s, owner unchanged, concurrent grid_canvas edit preserved.
InstallV2 native passed but wrapper expected238 rather than310 references;
validation-corrected.json explicitly corrects classification, no test rerun for
that count. Future wrapper corrected. Final Title run includes selected-player
guard and unchanged normal source code. 12 Python syntax checks,
4 paired unique native UIDs, 262 new preview/evidence PNGs LFS.

Registry/proof: character/bill-master-install-v1. Historical master manifests keep
their authoring statuses; this normal selection registry governs installation.
This is a scoped East installation milestone, not blanket full Bill acceptance.
Other direction/equipment/life/water banks retain selections; natural unforced
goal choice and a new exported build were not tested here. Next: reconcile final
coverage against this installed registry and existing recorded evidence; address
only demonstrated remaining defects, then concise closeout. Do not restart source
repairs or expand optional polish. Owner wants wrap soon. No commit/export requested.
http://127.0.0.1:8791/character/bill-master-install-v1/.


## Bill installed coverage reconciliation — October 4, 2026

character/bill-installed-coverage-2026-10-04 is the current full selected source
inventory. Actual normal grid loader plus inherited production carry banks:
216 bare/198 helmet states,1,860/1,716 slots,3,128 unique selected source paths.
Older literal-only audit missed inherited carry-start states and latest overrides;
historical212/194 counts remain evidence for their old resolution scope.
Current resolver appends36 inherited manifest loads in actual selection order.
Actual materialized normal-player validation agrees for every key/slot, raw RGBA,
authored timing/loop and declared density:11,974checks/0,11.56s,engine0/clean,
4,974 frozen inputs unchanged,2,936owner non-log files unchanged, scratchAPPDATA.
Headless source audit only, not new motion/world/Continue acceptance. Existing
normal East jobs and Continue evidence stays in bill-master-install-v1 registry.

Explicit131 required keys per gear (ordinary actions,cardinal life/basic water,
cargo starts and all12carry-turn programs,specialEastbunk) are all present.
18 theoretical missing bunk direction/gear combinations are intentional:
major_bill_npc.begin_life_station forcesEast; generic lie/sleep/get-up remains
cardinal. Eight retained helmet eat/drink keys are not a feeding-art repair task:
crew_life.pose selectsinspect for a sealed helmet. Three older specialEastbunk
keys per gear remain selected. No inferred replacement count from folder age.

Eight refreshed representative whole-source boards/80samples actually inspected
at common physicalH148/p160224. All3,311 comparison inputs exact at publication;
North authority remains prepared rear stance, not untouched original master.
Installed bareEast idle/walk/run/reach/carry/weld materially closer; remaining
kneel/repair/stand darker/smoother, swim face/light differs. West remains highest
visual priority: dry face/suit darker/softer than original, swim brighter.
South running cloth and face angle/shading vary; North running/welding quilt
details differ. Static80samples and bare reference do not prove all frames,
continuous cadence or equipped helmet-design acceptance. Full master-matching
objective remains open, despite complete explicit source coverage.

NativeV1 had8,398functional checks/0 but noisy Image.load_from_file warnings;
failure classification retained with all maps. V2 changes only fixture expected
decode to rawPNGbuffer (3,576extra decode assertions), engine clean. No runtime,
artwork,selected bank,owner save or exported-build change in this reconciliation.
EightPython syntax/two paired uniqueUIDs/9previewPNG LFS. Updated review,
source mapping,native reports/maps,browserproof,REVIEW.md,HANDOFF retained.
HEAD eb1cb03b plus dirty/untracked installation and concurrent work; no commit.

Next concrete work: boundedWest master consistency, review existing48phase study
before authoring again; keep rejected trials unselected and acceptedEast sources
intact. Then judge remaining demonstrated view/pose differences. Coverage limits
are not automatic new generation/export/all-route tasks. Owner wants closeout
soon; do not reopen unrelated historicalTODOs or label full visual objective done.
http://127.0.0.1:8791/character/bill-installed-coverage-2026-10-04/.


## Bill West whole master keyposes — October 4, 2026

character/bill-west-whole-master-pilot-v1: whole-source built-in edits for bare
walking landmarks000/012/024/036. Existing48phase head/material study inspected;
still provisional/unselected. Six exact generation calls/receipts/raw outputs
retained:fourpreferred,two rejected. Initial012/036 copied the wide000stance from
the supporting whole pose and failed closed-foot geometry; retained/rejected in
full. Retry uses target plus original high-resolution West master only, explicit
overlapping feet. No rejected partial art or anatomical correction admitted.

Preferred raws1254square uniformly export256 LANCZOS with wholeY only0/-1/0/+1.
Original complete-source bottoms exact; height deltas+1/+2/+1/-1,widths+4/0/+1/-2,
silhouetteIoU .942/.957/.967/.953. Reference352×320 sole-registered master crops
only transparent margin to256; complete original alpha retained, then common4x
reference export. Original high-resolution master supplements the reduced whole
reference. No local colour grade, head stamps, body stretching or per-part fit.
All six raws,four preferred packed poses,complete two-row comparison and
master/first-stride comparison visually inspected; browser gallery verified.
Angular warmer face/matte quilt detail improved; small hair/patch/harness variance
remains provisional. Exact bottoms/density are not rigid boot contact or motion
proof. Eight protected original/reference inputs unchanged,6Python syntax,
20PNG LFS. No Godot/native/profile run or runtime source change.

Important bounded lesson: a completed stride used as a whole material reference
can override a closed-foot target despite explicit preserve-pose wording. Reject
the wrong whole pose; use original high-resolution identity support and explicit
target foot arrangement. This is a demonstrated retry for these two poses, not a
universal recipe or proof for all48phases. Exact tool arguments govern provenance;
prepared prompt text is a separate authoring contract.

Four landmark poses are an uninstalled study, not a complete loop or partial
walking installation. Existing selected banks,installedEast and prior48study
remain intact. Next:complete the44intermediate whole phases against these
landmarks/original master,then verify full loop/source geometry and native
distance-driven playback before admission. Do not repeatedly reopen old rejected
trials or broaden unrelated polish. Full Bill objective still open; owner wants
wrap soon. No commit/export/paid external generation requested or performed.
http://127.0.0.1:8791/character/bill-west-whole-master-pilot-v1/.
