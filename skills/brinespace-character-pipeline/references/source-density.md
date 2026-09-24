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
