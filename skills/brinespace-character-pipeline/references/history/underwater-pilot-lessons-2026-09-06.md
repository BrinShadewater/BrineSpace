# Underwater and equipment extensions

Read when adding swimming, death or wearable equipment. This is conditional
guidance, not a requirement to add these states to every character request.

## Lessons from the first underwater pilot

- A transparency request returned an opaque RGB checkerboard. Inspect pixel alpha
  before slicing. Preserve the rejected source; regenerate against a flat chroma
  background when removing the painted pattern would damage the subject.
- Standing-height normalization stretches swimming bodies. Establish scale from
  matching anatomical landmarks, then choose a canvas that contains the limbs.
  Bounding-box centering is provisional: kicks change the box and introduce bob.
  Register final swim frames to a stable torso landmark, not the lowest boot.
  Store source-pixel anchors with the source hash and reject stale annotations on
  rebuild. A fixed anchor does not fix changing torso pitch: review pose geometry
  separately and regenerate excessive rocking rather than hiding it by recentering.
- A four-view helmet sheet is a reference, not a working overlay. Verify actual
  facing (the pilot returned side views in reversed order), clear visor alpha,
  neck fit, hair coverage and head anchors separately for every supported pose.
  Do not mirror asymmetric fittings or bake a helmet into an unhelmeted base.
- Keep original dry-pack pixels and palettes stable when adding a new family.
  Reusing a builder that recomputes the whole palette can change accepted art.

## Coverage and integration contract

Maintain a character/state/direction/equipment coverage ledger with independent
source, packaging, visual-review and runtime statuses. Missing directions are
missing coverage; a fallback idle frame does not count as swimming or death.

Separate environment (dry/flooded/exterior), locomotion (moving/treading), equipment
(helmet owned/equipped) and life state. Death is a one-shot with a held terminal
pose; underwater death must not use a floor-collapse ending. Preserve equipment
on death and through saves. Do not invent mortality rates for an animation task.

Before claiming integration, inspect whether flooding, exterior routing and locker
interactions exist. A fixture or state hook proves only its own scope. Locker
pickup must complete before equipment is equipped or exterior departure is allowed;
safe return/removal and interrupted interactions need explicit behavior.

For final review, check unhelmeted/helmeted poses at station scale, every affected
direction, dry-to-wet transitions, stationary water movement, death interruption,
old saves, visor transparency and hull/prop occlusion. Record sampled playback
inspection accurately; do not claim continuous video perception from screenshots.


## Opposite-view generation finding

A canonical standing reference plus tighter text produced an upright swim pose.
Using the existing swim row as a motion reference held the horizontal posture
more closely, but generated opposite views still reproduced near-side tools as
if mirrored. Therefore inspect pose and equipment identity as separate gates.
An instruction saying "not mirrored" is not evidence of correct handedness.
Supply both canonical identity and motion references for retries; isolate a failed
accessory correction rather than accepting a whole-row identity regression.

Grounded-death packaging uses one anatomical scale across the row and a shared
floor baseline. Never resize each crouched or lying pose to standing height.
A death preview should play once, and the runtime manifest must explicitly disable
looping and retain the terminal pose; a GIF preview alone does not prove that.


Expansion manifests can now be loaded with
`CrewSpritePlayer.load_manifest(path, true)` to retain existing textures, stride
metadata and playback state. The default still replaces a pack. Use
`tests/test_crew_death_pack.gd` for grounded-death manifest compatibility, timed
poses, terminal holds and saved playback. This does not establish NPC mortality
or station death rendering: those require controller/consumer integration.

Bill still uses a separate station playback path from Veld/Branforth. Extension
loading into CrewSpritePlayer alone does not cover Bill: verify the legacy
consumer and its animation clock as well. `tests/test_crew_death_save.gd` checks
all three through a disk round trip mid-death, including exact pose restoration.

Water pilots use torso pivots distinct from dry floor pivots. A player that loads
a manifest successfully may still have a renderer hardcoded to (46,86); audit
texture metadata and every room/legacy consumer before declaring water integration.

The player now carries manifest pivots as `crew_pivot` texture metadata. Both the
shared whole-room actor renderer and the three legacy crew draw paths honor it,
with (46,86) as the compatibility fallback. Water pilots use (61,44).
`tests/test_crew_water_death_pack.gd` checks every water frame's metadata alongside
dry-pivot preservation and terminal playback. `tests/test_crew_death_save.gd`
still passes through the real station scene after this renderer change. These
checks establish plumbing and dry regression, not visual acceptance of swimming
in a flooded room; that still needs a station-scale water fixture.

Direction-specific pivots are intentional: Bill's south swim uses (46,44), while
east uses (61,44). Do not copy an east-facing shoulder offset to a centered front
view. `build_pilot.py --character bill --direction south` reproduces the six-pose
pilot from hash-locked source annotations. Compare head scale across directions;
the foreshortened body's shorter silhouette must not be enlarged to match the
side-view bounding box. Review source and packed contact separately, then check
direction changes in the station before marking the new direction accepted.

The east/south swim pilots for all three crew are covered by
`tests/test_crew_swim_packs.gd`: six frames, direction-specific pivots,
distance-driven phases, looping and retained dry textures. Sample phase interiors
instead of exact floating-point cycle boundaries. Branforth's south row needed a
localized grey-hair correction after motion transfer from Bill; inspect age and
hair palette across every phase even when clothing and silhouette are correct.

Rear-facing swim generation can produce an almost full-length standing silhouette
despite a prone-motion prompt. Check visible body length against anatomical head
scale before packing. Bill's first north candidate was retained but rejected for
insufficient foreshortening; revision 02 improves it, with station-scale comparison
still pending. Do not shrink the whole sprite merely to make its box fit. The north
pilot uses shoulder pivot (46,30) to leave room for trailing boots; this is a
direction-specific registration, not evidence that the camera is fully accepted.

Rebuild the shared review with `python character/crew-underwater-v1/build_review.py`
after changing manifests or coverage. Serve `character/crew-underwater-v1/review.html`
through the project HTTP server. It compares all three crew on a shared clock,
supports phase scrubbing and 1x/2x/3x pixel scales, and draws each manifest's anchor
at the same location. Missing clips remain missing rather than using idle fallbacks.
Review both direction changes and terminal death holds here before station tests;
this isolated canvas is not evidence of hull occlusion or environment behavior.

Veld's first north pilot preserves the rear-view bun and right-side vials, but
inherits the remaining body-length concern from Bill's motion reference. A
reference marked pilot can propagate its unresolved camera problem into another
character. Carry that concern into the new coverage entry and resolve the shared
camera before treating either direction as final; successful slicing is not
visual acceptance.

Treading must use elapsed time, not traveled distance: a stationary swimmer still
needs motion. The builder accepts `--state tread`; its looping manifest omits a
tread stride. The swim-pack test now checks Bill's six south tread poses and a
complete loop with an unchanged position. This proves playback, not automatic
selection when an NPC stops in water. Review hand sculling and kick continuity
before using this first tread pilot as a motion reference for other crew.

All three south tread pilots now have stationary-cycle and saved-phase coverage
in `tests/test_crew_swim_packs.gd`. Run `check_pilots.py` in the underwater pack
for frame bounds, binary alpha, timing counts and recorded source hashes; its
JSON evidence explicitly excludes artistic acceptance. Branforth's first tread
source had alpha but stray pixels joined pose columns, so transparency alone did
not guarantee sliceability. Preserve the failed source and correct separation;
do not silently treat merged columns as valid frames.

Front helmet production now has an open-visor source and `build_helmet.py` alpha
checks. `fit_helmet.py` composes it over all 18 south tread poses with source-frame
and overlay hashes, retaining original body frames. The fitting contact shows
faces through the opening and stable collars. This is tread-only fitting evidence:
do not reuse those coordinates for prone swimming, falling or another direction.
Review hair/goggle occlusion and face visibility per pose family before registering
an equipped runtime state. A clear cutout has no glass tint/reflection layer yet.

`CrewSpritePlayer.load_equipment_manifest(equipment, path)` validates matching
base states, frame counts, timing and pivots before installing equipment rows.
Pass the equipment id as the optional fifth `frame` argument; it selects pixels
using the existing animation clock. The swim-pack test checks all three tread
rows without phase resets, rejected mismatched states and missing equipment.
Missing equipment coverage returns null, so callers must check coverage before
entering that state and must handle null. These player hooks are not yet station
locker ownership, equip transitions or Bill's separate legacy renderer integration.

The shared review includes a Diving helmet fitting toggle. It swaps fitted pixels
on the same clock and explicitly labels unsupported clips as missing. Its builder
checks equipped timing, frame count and pivot against the base manifest. Compare
equipment on/off at the same phase instead of comparing separately started GIFs;
otherwise a phase difference can look like an anchor error.

`fit_helmet.py --clip swim-east` now builds side-helmet fitting pilots for all
three crew; the default remains tread-south. Contacts and registration files are
named by clip. Equipment loading merges validated rows so adding a swim fit does
not erase tread coverage. The swim-pack test checks this plus equipped distance
playback. The side fitting contact was inspected for hair coverage and visible
faces; its larger helmet silhouette still needs station-scale and prop review.

Water-death side fittings use per-pose helmet coordinates because the head shifts
relative to the shoulder anchor. Rebuild with `fit_helmet.py --clip death-water-east`.
The preview builder now honors manifest loop flags, including equipment variants.
The water-death pack test checks equipped terminal holds for all three characters;
this does not establish controller mortality or equipment persistence in game saves.

The controller now saves `movement_medium` (old saves default to dry) and exposes
`animation_state()` for swim/tread selection. Water death is chosen at death time.
Station renderers load the available pilot clips and call this selector, including
Bill's legacy playback path and swim stride metadata. The station death/save
regression passes after loading these additions. Room flooding and exterior travel
still do not set the medium automatically, missing directions remain incomplete,
and helmet equipment is not yet supplied by station renderers. Do not call these
hooks complete gameplay integration.

`tests/playtest_crew_water.gd` exercises the actual station scene with a directly
set flooded medium, captures three tread phases and seven water-death times, and
checks terminal controller behavior. The tread and terminal death crops were
inspected. This is not a flood simulation. Floating bodies extend farther from
their navigation anchor than standing sprites; the maintenance-bay capture shows
a body reaching toward nearby machinery. Audit water silhouette clearance and
occlusion rather than assuming the dry foot radius proves water safety.

West-view equipment corrections now read as the intended rectangular scanner or
meter instead of near-side vials/wrench. However Branforth's meter correction also
flattened his kick. A localized edit request does not guarantee localized output:
review the entire motion row again after any accessory correction. All four swim
directions now have packaging/player checks, but the coverage ledger still carries
this motion regression and the cross-direction camera concerns. Do not promote
those mechanical checks into visual acceptance.

### Motion repair and review clock continuity

Branforth west revision 03 restores knee changes while retaining the corrected amber meter. Source and packed contact review still shows repeated extension poses and abrupt raised-knee transitions: keep visual acceptance pending even when six files and runtime phase checks pass. Inspect adjacent poses and the last-to-first transition separately from frame uniqueness. Preserve rejected flat-kick sources for comparison.

Review controls must derive displayed poses from one elapsed clock while playing and paused. Scrubbing sets that clock to the selected pose start; pause preserves its current time. A separate paused-frame index can silently jump to pose one and resume at an unrelated time, undermining motion comparisons.

### Directional tread camera and motion transfer

Treat side-facing tread as upright suspension with bent knees, not horizontal swimming or walking. Bill east revision 01 rotated the torso in middle frames; revision 02 constrained all six to the same profile and reduced the sculling radius. Use a character identity source plus a proven motion/camera source when extending to another crew member, and explicitly specify anatomical equipment sides. Inspect camera stability in every frame before packaging; a correct facing head alone does not prove a consistent torso view.

East tread now has six packaged poses for Bill, Veld and Branforth. Register shoulder (46,35) using measured head scale, preserve source hashes, and verify all six phases while position is fixed. Small hand changes can disappear at station scale; successful clock tests do not establish readable sculling. Keep motion review and helmet fitting pending until inspected in their actual context.

### Fitting provenance after body revisions

East tread now has helmet composites for all three crew. Fitting is reproducible through `fit_helmet.py --clip tread-east`; the open side helmet retains visible faces, but apparent helmet size still needs station review. Tests verify all six equipped phases and unchanged clock on toggle.

Run `check_pilots.py` after every body or overlay rebuild. It now checks all fitted packs against recorded body hashes and overlay hash, matches their timing/frame lists/pivot to the base, and reproduces each registered composite for an exact pixel comparison. A body repair must invalidate its old fittings rather than silently displaying a previous pose beneath the helmet. These checks establish provenance, not visual fit.

### Rear tread reference contamination

Bill rear tread revisions inherited a swimming overhead reach from the prone reference. Removing it improved action semantics, but the wide-arm revision joined neighboring pose columns and failed extraction. Keep packaging marked failed until the source is repaired; do not treat an older passing pack audit as proof that the attempted clip built. Prefer an upright tread motion reference plus a rear identity reference, and require enough horizontal gutters for the maximum arm span.

Rear tread revision 03 resolves the overlapping columns. Bill now packages into six frames at shoulder anchor (46,32); moving the anchor up three pixels retains the boots at the measured head scale. Contact review still shows a large rear silhouette and repetitive legs, so it remains outside the station loader. Packing within bounds does not resolve cross-direction apparent-scale or motion defects.

### Rear-view scale calibration correction

Bill rear tread revision 04 uses the upright south motion reference first and rear suit reference second. This corrects the prone-looking paired soles and restores alternating knees. Rear crown-to-collar height is not equivalent to front crown-to-chin height: blindly assigning both a 14px target enlarged the rear body. The revised calibration matches ~60px source head width to ~10px packed width, consistent with the south width at 14/85 scale. Record the anatomical measurement and projection in registration notes; compare at common shoulder anchors before propagating a template. This revision returns to shoulder (46,35) without clipping. It is still a pilot pending motion and station review.

Veld rear tread revision 02 packages six upright poses with anatomical-right vials and anatomical-left scanner. The first attempt copied the front reference equipment screen positions despite explicit rear-side instructions. Correct equipment locally and inspect all six poses afterward; prompts do not establish sidedness. Rear head width calibration excludes the bun so hairstyle volume does not resize the body. Hand sculling remains subtle and station review is pending.

Rear tread coverage now includes all three crew with six poses each, available through the station pilot loader. Branforth source/contact inspection confirms viewer-right wrench and viewer-left meter. The shared runtime test exercises each rear pose while stationary, verifies shoulder (46,35), and checks loop restart. Repeated kick extremes still need motion refinement; loader inclusion and passing phase checks do not imply finished animation.

Bill west tread now has six extracted pilot poses using the same side-view head scale and shoulder (46,35) as east. Source/contact inspection finds stable torso orientation but nearly static legs and similar middle hand poses. Check motion of each limb independently: unique whole-frame hashes can be produced by hand changes while the kick remains frozen. Keep this distinct from packaging success.

Directional station evidence: the water native fixture now captures east and north tread at 80/400/720ms for all three crew. The 400ms crops show comparable apparent sizes and sampled prop clearance after rear calibration. Record the exact inspected samples separately from all captures. Stationary screenshots cannot establish full-cycle smoothness, route clearance, or actual flooded-room behavior.

Veld west tread revision 02 packages six frames with visible left-hip scanner. Revision 01 returned real alpha with detached specks that created extra extraction groups; a flat-magenta background repair restored clean isolation without relaxing the six-pose check. Reinspect character identity and limb motion after background repair because the generation edit may redraw the figure. Source and contact were inspected; station review remains pending.

Base expansion coverage now includes four swim and four tread directions plus ground/water death east for each of three crew (30 base clips). West tread is enabled in the station pilot loader and tested for six stationary phases, loop and shoulder pivot. Branforth west has correct near-left amber meter but nearly static hands. Matrix coverage is not motion acceptance; preserve explicit per-limb refinement findings and independent helmet/equip/locker/environment gaps.

West tread station evidence now covers all three crew at 80/400/720ms, with the 400ms crop inspected for size and sampled prop clearance. Directional evidence records hashes of inspected captures and the base frames used, so subsequent animation edits can be identified as outside that evidence. Re-run the relevant station review after source/frame changes; a prior screenshot cannot certify a new revision.

### Rear helmet reuse and explicit fitting views

The authored four-view helmet source already contains a usable opaque rear shell. `build_helmet.py --view north` extracts its second column and records both the source region and crop, rather than generating redundant art. Rear shells intentionally have no visor aperture: apply open-visor assertions only to views with visible faces. `fit_helmet.py --clip tread-north` fits all 18 rear tread poses, recording the explicit overlay view and source hashes. Runtime tests confirm every rear equipped phase and unchanged clock on toggle. Contact inspection confirms rear head coverage; station helmet sizing/rendering remains pending.

West helmet extraction and fitting: the generated source contained faint alpha debris beyond the shell. Applying the binary-alpha contract before measuring its crop removed that debris and prevented underscaling. The open visor is checked before and after reduction. `fit_helmet.py --clip tread-west` now covers all 18 west tread poses; contact inspection shows visible faces and covered hair. Phase/toggle tests pass for all crew. All four tread directions now have helmet fitting pilots; station sizing/rendering, swimming coverage and locker/equip transitions remain independent unfinished work.

West swim fittings now cover all 18 poses using character-specific helmet offsets. Contact review confirms face visibility and hair coverage, but the helmet-to-body silhouette looks bulky and requires station sizing review. Tests exercise each equipped pose using distance-driven phase rather than elapsed time and verify that equipment toggles preserve the stride clock. A tread fitting cannot be reused at its upright offset for swimming; calibrate the head location for the actual clip.

North swim helmet composites are provisional: a single overlay over the whole body can cover overhead hands in the stroke. Source/fitting hash checks cannot detect incorrect depth order. Review head coverage and hand visibility separately, and introduce authored foreground limb masks or revise stroke clearance before accepting the equipped animation. Do not assume a helmet placement proven for upright tread transfers to an overhead swimming stroke.

South swim fittings now expose the same depth-order limitation as north: faces remain visible but the collar/shell covers forward hands in some poses. All swim/tread directions have provisional fittings, not accepted equipment animation. Resolve per-pose foreground limbs before promoting north/south swim; do not mark a complete fitting matrix as visual completion.

South swim foreground repair: phases 1/5/6 now recompose authored body pixels in hand region [39,53,54,63] above the helmet collar. The rectangles are recorded per frame in fitting evidence; the checker independently reconstructs body, helmet, then foreground order. Contact review shows forward gloves restored without covering faces. Region selection is authored for these registered frames and must be reviewed after source or scale changes; do not infer universal masks for other views. North hand layering and station validation remain pending.

North swim foreground repair now preserves top glove regions in phases 1/6 and lateral hand regions in phase 5. These authored rectangles avoid the central head area so bare hair is not composited above the shell. The contact sheet shows restored glove tips; tight clearance still requires playback review. Foreground region selection is centralized in the fitter and emitted into provenance for exact reconstruction checks.

Equipped swim validation now spans all four directions and all three crew, exercising all six distance-driven phases and unchanged clock on same-time equipment toggle. This includes the north/south foreground composites. Passing texture-selection tests proves the intended fitted frames are selected; it does not prove visual hand clearance or station equipment integration. Keep those review gates separate.

Station helmet rendering now has native evidence. The fixture injects renderer equipment selection, captures all four tread directions and underwater death, and passes. East/rear tread and terminal death crops were inspected: all three crew render equipped, though shells remain bulky. Bill equipment textures retain his legacy renderer metadata and use his existing frame index; Veld/Branforth use the shared player equipment selection. Renderer selection is presentation state, not locker ownership or save persistence. Do not report this fixture as completed equipment gameplay.

NPC equipment state now drives station helmet rendering directly; the temporary renderer equipment dictionary is removed. `helmet_equipped` is included in snapshots/restoration and validated as a boolean. Exterior medium requires it, removal outside and equipment changes after death are rejected. The native fixture now equips each NPC through its setter and passes. Full disk round-trip and locker proximity/completion are still pending. Dry equipped animation coverage is also required before normal locker-to-airlock travel can use this state without missing frames.

Equipment persistence now has actual disk evidence in `test_crew_death_save.gd`: all three crew retain helmet/exterior medium and exact equipped terminal water-death pixels after restore. Invalid exterior-without-helmet and nonboolean equipment checkpoints are rejected; the rejected exterior case leaves live Bill unchanged. Existing dry/legacy regressions still pass. Keep save verification separate from locker acquisition and equip/remove motion, which remain unfinished.

Dry helmet coverage starts with south idle for all three crew, built by `fit_dry_helmet.py` from the original dry manifest/frame paths. Preserve the original pivot, durations and all base pixels, record source and overlay hashes, and keep outputs under equipment/dry. The initial contact shows faces at different vertical positions inside the shared helmet placement; per-character fitting refinement is required before runtime promotion. Dry walk/run/action coverage remains missing.

Dry south idle fitting now uses character-specific helmet positions: Bill (34,10), Veld (34,7), Branforth (34,9). The dry fitter also accepts `--state walk`, preserving original six-frame timing and pivot. Contact inspection confirms visible faces across the initial south walk cycle; runtime loading and other dry directions remain pending. Do not assume shared canvas dimensions imply shared head placement.

### Dry helmet fitting coverage and provenance

All three crew now have provisional helmet fittings for idle and walk in all four
cardinal directions: 24 clips, 144 frames. `fit_dry_helmet.py` preserves original
body frames, timing, loop flags and pivots. Front, east, west and rear use their
own overlay views; fitting offsets vary by character. East/west walk contact
sheets retain visible faces; the rear shell covers the head consistently across
six phases. These are isolated contact-sheet observations, not station acceptance.

`check_pilots.py` now verifies every dry fitting against the original manifest,
original frame hashes, overlay hash and exact registered composition. Preserve
this chain when adding actions: a successful rebuild alone does not establish
correct head tracking. Review each pose for visor alignment and limb occlusion.
Dry fittings are not yet loaded into gameplay or the shared water review page.
Run/actions, equipped ground death, equip/remove motion and locker integration
remain outstanding. Do not count idle/walk coverage as complete equipment support.

The shared `build_review.py` now includes the 24 dry idle/walk fittings and their
original unequipped sources alongside the 30 water/death base clips. Both sides
use the original timing and pivot; toggling the helmet preserves the shared clock.
Original frame URLs resolve relative to the review directory, including parent
paths, rather than assuming every asset lives inside the expansion pack. The live
review page loaded with all eight idle/walk options present. Full playback and
station acceptance remain separate checks. This supersedes the earlier note that
dry fittings were absent from the shared review; gameplay loading is still pending.

Dry idle/walk helmet fittings now load in `grid_canvas.gd` for all three crew.
Bill validates these against his original dry manifest in a separate player and
merges only equipment rows into his legacy renderer; water rows and original dry
playback remain intact. Veld and Branforth load fittings into their own players.
The expanded swim-pack test checks every dry phase and unchanged clocks across
helmet toggles (24 clips). It passed, as did the real-save regression.

The save fixture needed an explicit legacy three-crew setup: current gameplay
now gates actors behind architect pod recovery. Clearing `architect_run` only in
this fixture restores its intended legacy population. Do not bypass recovery in
normal gameplay to satisfy an animation test. The passing save regression measured
20.36 minimum foot separation. Native dry helmet playback is still unreviewed;
run/actions and equipped ground death remain uncovered, and lockers are unfinished.

Bill's four original run cycles now have provisional helmet fittings (24 frames),
loaded by the dry equipment helper and included in the shared review. All four
contact sheets were inspected: face aperture remains visible in front/side views
and rear shell alignment is consistent. Dry phase/toggle tests now cover these
four additional clips and pass. Native running playback remains unreviewed.
Veld and Branforth have no run states in their authoritative base manifests;
the fitter reports MISSING BASE ANIMATION and leaves their rows empty. Never
claim a wearable state exists because the same state exists on another character.
Current dry equipment count is 28 clips / 168 frames; this is still partial
coverage, with role actions, ground death and equip/remove transitions unfinished.

East interaction now has helmet fittings for all three characters (18 frames),
using their original action timing and pivots. Contact inspection shows hands and
tools remaining below the helmet rim; no foreground mask was needed for these
poses. Renderer loading, shared review, composition checks and per-phase toggle
tests include them. Dry coverage is now 31 clips / 186 frames, still provisional.
Treat interaction separately from equip/remove: reaching forward does not show a
helmet being picked up, donned or returned. Do not substitute it for locker art.
Maintain a current coverage summary above historical notes to prevent old counts
or earlier integration limitations being mistaken for the present state.

Kneel-east now has provisional six-pose helmet fittings for all three crew.
Per-pose vertical AND horizontal anchors are required: the initial lowered fits
obscured faces despite following head height. Moving lowered overlays four pixels
left restored visible face apertures in the contact sheet. Preserve explicit
registration per pose rather than assuming a fixed idle attachment offset.
These 18 frames pass original-source and exact-composition checks and appear in
the shared review, but are not yet loaded by the gameplay helper. Repair and stand
must be fitted next so the entire action chain retains equipment continuously.
Dry packaged total is 34 clips / 204 frames; renderer coverage remains 31 clips.

Repair/stand helmet fittings now complete the packaged kneel-repair-stand chain
for all three crew (54 action frames total), and all three actions load in the
renderer. Stand uses reversed attachment positions from kneel after inspecting
its original source poses; repair retains the terminal kneel attachment. This
reuses registration only, not newly mirrored or invented artwork. Contact sheets
show face apertures and tools; full native chain playback remains unreviewed.
All 40 dry equipment clips / 240 frames pass registered composition and per-phase
clock-preservation checks. Review includes 70 base clips overall. This supersedes
prior notes saying kneel is review-only or repair/stand are missing. Ground-death
helmets and actual locker equip/remove transitions remain outstanding.

Native dry action review now runs before the water fixture: all three NPCs equip
helmets, then show idle/kneel/repair/stand/idle at fixed positions. The fixture
asserts all actors are active and each renderer returns an equipped action frame.
The native run passed. Inspected kneel 400ms, repair 400ms and stand 800ms crops
show readable faces/tools, retained helmets and no nearby prop overlap at those
samples. Hash-linked evidence lives in `pilot/dry-helmet-station-evidence.json`.
This proves sampled station rendering, not continuous chain smoothness, travel
clearance or locker behavior. Keep those scopes separate in future acceptance.

Ground-death equipment now has an initial 18-frame fitting candidate across all
three crew in equipment/fitting. Front helmet overlays rotate per pose using
nearest-neighbor sampling with expanded bounds; explicit rotation degrees join
positions and source hashes in registration. The pixel checker reconstructs the
same rotation and passes. The shared review includes these candidates.
Visual review found face occlusion in intermediate falling poses. They are NOT
loaded into gameplay and are not accepted. Refine attachment positions and/or
use a better matching tilted view before integration. Rotating a front overlay
is a fitting experiment, not evidence that the camera matches a falling head.

Ground-death fitting revision 2 corrects rotated-bounds displacement: intermediate
positions move upward 3/5/7 pixels, with Bill's fourth pose also shifted right.
Contact inspection now shows faces inside the visor throughout the fall. All
three ground-death fittings load in the renderer. Tests verify all six equipped
phases, unchanged clocks, and restored terminal equipment frames; they pass.
Composition checks also pass. Native grounded-death playback is still unreviewed.
This supersedes the initial candidate's face-obscured/not-loaded status. The
lesson is to align the rotated visor aperture to the face, not retain the original
unrotated top-left attachment after expand=True changes the overlay bounds.

Native ground-death helmet review now captures all three crew at 80,400,620,820
and 3000ms. The run passes. Inspected 400/620/3000ms samples retain helmets through
the fall and terminal pose without nearby prop overlap at these fixed positions.
Evidence hashes are in pilot/ground-helmet-station-evidence.json. This supersedes
native-ground-death-unreviewed notes, but does not establish continuous motion,
arbitrary-position body clearance, mortality triggers or locker integration.
Fixture restoration uses restore_snapshot(game, data); retain full API arguments
when temporarily restoring living actors after a terminal-animation capture.

Bill equip-helmet candidate 01 is preserved in generated with its exact prompt.
It shows six distinct phases: waist carry, chest lift, overhead lift, lowering,
collar securing, equipped rest. Identity and hand/helmet continuity read clearly,
but the camera is too front-facing for the existing east-facing dry endpoint.
Do not package this as accepted east-facing animation. Use it as motion reference
for a corrected camera pass, then match both bare and equipped endpoints at
station scale. Raised-helmet clearance must be checked against the 92px canvas
without shrinking the character solely to fit the overhead prop. Locker pickup
and return are separate from this carried-helmet donning sequence.

Bill equip candidate 02 corrects the camera using actual bare/equipped idle-east
frames as endpoint references. Source and exact prompt are preserved. A clearance
study (`probe_equip.py`, pilot/equip-clearance) calibrates bare crown-to-boot height
to 74 pixels: the overhead pose is 89px high, exceeding the old foot86 canvas
clearance. A provisional 92x104 canvas with pivot46,98 preserves body scale and
fits all six poses. Do not shrink the body or clip the overhead helmet to force
92x92 compatibility. Runtime/review drawing must support actual frame dimensions
before this transition can be packaged for gameplay. Study is not a runtime pack;
endpoint silhouette matching and locker pickup/return remain unfinished.

Crew rendering now uses each texture's actual dimensions in the grid legacy
renderers and whole/modular nursery actor rendering. Pivot metadata remains the
attachment point, and pixel scale still derives from the established 74px body
profile. Modular nursery now reads the pivot rather than hard-coding46,86.
This supports taller overhead frames without stretching their contents into a
92px square. Existing real-save/render regression passes (20.36 minimum crew
separation). Taller donning frames still need native rendering evidence and
packaging; this regression only establishes existing-state compatibility.

Bill donning candidate02 is now packaged as a provisional non-looping six-frame
92x104 pack at pilot/bill-equip-helmet-east, pivot46,98. The source/clearance data
remain attached. No gameplay state or locker event loads it yet. The shared review
includes it; missing Veld/Branforth rows remain explicit. Review drawing now uses
image dimensions, a common pivot baseline and sufficient top/bottom space rather
than stretching every image to92x92 or clipping tall poses at a centered anchor.
Pixel validation reads each manifest's dimensions and all31 base pilot packs pass.
Browser/native tall-frame rendering still needs direct verification; packaging
and code changes alone do not certify endpoint matching or transition smoothness.

Tall donning frames now have native fixture evidence. The 92x104 texture retains
its dimensions and overhead pose without cropping; fixed foot registration reads
correctly. Comparing the final donning pose with existing equipped idle reveals a
slimmer body and different helmet silhouette. This candidate is NOT endpoint
accepted. Refine source proportions rather than scaling only the final frame or
claiming renderer success proves art continuity. See pilot/donning-station-evidence.json.
The pack is injected only by the art fixture; no locker behavior is implemented.

Donning candidate03 broadens Bill and enlarges the helmet; preserved source and
prompt are packaged into the current provisional pilot. Bare body calibration is
74/442 with boot baseline715 and explicit boot centers. All31 pixel packs pass.
The endpoint-comparison.png places equipped idle, candidate terminal, and bare
idle on one foot baseline at2x. It reveals overcorrection: the candidate torso is
wider/more front-facing than the actual east sprite and helmet silhouette still
differs. Candidate03 is NOT endpoint accepted; target those exact differences in
the next source edit. Do not use vague 'stockier' prompts as a substitute for
comparing actual silhouette widths at a common pivot. Prior native evidence is
for candidate02 and must not certify candidate03 pixels.

Donning candidate04 uses a registered six-cell template made from the actual bare
idle sprite and equipped endpoint. This constrained edit matches body/camera and
helmet silhouette much more closely than broad concept/proportion prompts. The
current pilot uses candidate04; endpoint-comparison.png is now rebuilt by the
packager rather than left stale after source changes. Source has white letterbox
bands: remove only the measured outside bands before magenta extraction. Body
scale remains74px; overhead bounds start at y4 on the104px canvas.
Remaining art issue: generated action hands are bare instead of dark gloves.
Correct those in the source before acceptance. Previous native captures refer to
older candidates and do not certify this revision. All31 pixel packs passed.

Donning candidate05 corrects the exposed hands to dark full-finger gloves while
retaining candidate04's registered-template proportions. Current packaged source
is05. The source band starts slightly lower; crop152..531 in the683-high preview
before keying, avoiding a white boundary row that inflated source bounds despite
vanishing after reduction. Native fixture passes; inspected overhead440ms and
terminal1100ms captures retain body scale and fit the raised helmet. These are
sampled visual checks, not complete transition/locker acceptance. Earlier native
capture files were refreshed by this run; preserve source revision when citing them.
Next required work includes other crew's donning, removal/pickup/return and actual
locker-triggered equipment timing. All31 base pixel packs pass.

Veld now has a six-frame donning pilot on92x104/pivot46,98, built from her actual
sprite template. Candidate01 preserved stance/gloves but lost faces in worn poses.
Candidate02 restored worn faces but also hallucinated a second face in the raised
helmet. Select01 poses0-2 and02 poses3-5 during packaging; do not propagate the
failed overhead edit. Each frame records source/hash/crop/scale/placement in
sources.json; source hashes are checked. Contact inspection shows a single head,
gloved hands and visible worn face. All32 base pixel packs pass; review contains
both Bill and Veld. Veld still needs endpoint/native review; no locker integration.

Veld donning now runs alongside Bill in the native fixture. Tall dimensions and
frame availability pass; overhead and terminal samples were inspected beside
existing equipped idle. Veld's donning endpoint is narrower and its helmet smaller
than the equipped idle reference. Keep this as a correction requirement, not an
accepted transition. Evidence includes current Veld frame hashes and capture
hashes in pilot/veld-donning-station-evidence.json. Retained capture filenames
begin bill-donning but now contain both actors; scope is stated explicitly.
Template-derived art still needs endpoint comparison after scaling: a recognizable
identity does not prove consistent silhouette or attachment dimensions.

Veld endpoint measurements corrected the earlier visual diagnosis: torso/leg widths
were already close (19/18 versus idle18/18); helmet width was21 versus23. Candidate03
targets helmet size and removes the duplicate overhead face, retaining body scale.
All six current poses now use03; earlier per-pose01/02 selection is historical.
Source/contact inspected with one head per figure and gloved grips. Endpoint width
report is saved beside the pilot; pixel/source checks pass for all32 base packs.
Native evidence from the earlier candidate is stale for current pixels. Measure
parts separately before a proportion edit; do not widen a body based solely on
an impression caused by a small helmet or different shading.

Branforth's registered-template donning candidate01 is packaged in six92x104
frames and included in review. build_veld_donning.py now accepts --actor branforth,
retaining per-actor calibration and source hashes. Source/contact show gloved grips,
empty carried helmet, face in worn poses, orange uniform and stowed tool. All33
base pixel packs pass. Native fixture now injects all three donning pilots and
passes dimension/frame checks; overhead440ms and terminal1100ms samples inspected.
All three render without clipping. This is still fixture-only; endpoint/motion
acceptance and locker pickup/removal/return remain distinct unfinished requirements.

All three crew now have removal pilots derived from donning pose order5,4,3,2,1,0,
with separate removal durations140,260,220,220,180,220ms and no loop. The sequence
ends holding the helmet; it does not depict locker return. build_helmet_removal.py
records exact source frame hashes and derived ordering, preserving all pixels.
Contact sheets inspected for collar/lift/lower order; native removal is pending.
Godot tests now sample all six phases of both transitions for all three actors,
verify92x104/pivot46,98 and terminal holds. Tests pass, as do all36 pixel packs.
Shared review includes removal. Reversal is explicit pose reuse, not newly authored
art; retain separate timing and assess physical plausibility before acceptance.

NPCs now expose begin_helmet_action/advance_helmet_action shared by all three crew.
Durations come from each transition manifest; equipment changes only on completion.
Actions require active stationary dry crew, reject duplicates/busy work, and block
medium/equipment setters while in progress. Removal is blocked outside. Death
interrupts the action and preserves the pre-completion equipment state. Snapshot
validation recognizes the two states and rejects contradictory equipment/medium.
All-three-actor tests pass for delayed equip, exterior restriction and death during
removal. These APIs are not yet called by lockers. Renderer transition routing,
clock synchronization, interrupted-save coverage and locker ownership remain
unfinished; API tests are not end-to-end gameplay acceptance.

Helmet transitions now load normally for all three renderers. Transition frames
are selected from manifest duration minus NPC remaining timer, independent of the
cosmetic visual clock. Removal/donning carry their own helmet pixels, so they bypass
normal equipment overlay selection. Native fixture now calls begin_helmet_action,
advances its timer, and asserts that a100-second visual-clock jump does not change
the selected frame or equip early. All three timed actions complete correctly;
native fixture and existing real-save regression pass. This replaces fixture-only
frame injection. Actual locker trigger/ownership and mid-transition disk restore
remain unverified; do not equate the existing save regression with that new case.

Mid-transition disk save/restore is now verified for all three crew in both equip
and removal at0.55s. The regression writes/reads actual save files, mutates actions
to completion, restores, compares full NPC snapshots and exact rendered frame
bytes, rejects prematurely changed equipment without mutation, then completes the
restored actions. It passes. Evidence is pilot/mid-action-save-evidence.json.
This supersedes earlier unverified-mid-action-save notes. Locker location,
reservation/ownership, pickup/return and actual environment travel remain outside
this fixture; do not imply they are tested by state restoration.

Current room data contains no authored diving-locker points or personnel-airlock
mechanics; visual-bible references and Clinical Airlock synergy are not physical
locker geometry. Author interaction locations explicitly rather than treating
ordinary doorways or storage props as already implemented airlocks.
Navigation rebuild now cancels an unfinished helmet action, resets its timer and
preserves pre-completion equipment. Obstructed occupied floor also cancels. All
three actors pass equip/removal cancellation tests; the real-save fixture rebuilds
navigation mid-action, verifies cancellation, then restores the saved action and
completes it. This avoids stale timers after topology invalidation. Locker geometry,
reservation and pickup/return still need implementation.
