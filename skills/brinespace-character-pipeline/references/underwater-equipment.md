# Underwater animation and equipment workflow

## Current shared human helmets

For Bill, Veld and James shared-shell fit and colour continuity, read
[crew consistency](crew-consistency.md). Use the selected directional head/shell,
track collar through leaning motion, inspect alpha seams, and preserve individual
faces inside the common matte graphite/silver/glass design. The September 29 actor
handoffs distinguish installed equipment from retained and staged action coverage.

Use for requested swimming, death or wearable extensions. Preserve the user's full
scope; these requirements do not apply to an unrelated concept-only task.

## Establish coverage from current sources

Inspect each character's manifest and every affected consumer. Maintain separate
source, packaged, visual-review and runtime status by character/state/direction.
When revisions accumulate, keep one current inventory with source hashes and
move superseded chronology to linked history. Retained original clips should be
explicit entries, not falsely counted as missing revisions or newly authored art.
An inventory of files is not proof that a consumer loads them; verify selection
through the actual runtime path as a separate check.
A missing base animation cannot become equipped coverage through an idle fallback.
Bill's legacy renderer and Veld/Branforth's players both require verification.

Check whether flooding, exterior navigation, lockers and airlocks actually exist.
A room name, visual-bible example or synergy is not an interaction point. Author
locker geometry with the room workflow; do not reinterpret ordinary props as
implemented equipment stations. Preserve prototype economy and mortality rules.

## Generate and revise with stable references

Use canonical identity plus an appropriate motion reference. For transitions into
existing poses, start from a registered template of actual bare/equipped sprites.
Hold camera, body proportions, baseline, department markings and asymmetric tools.
Do not mirror opposite directions when near-side tools change anatomical sides.

Preserve every source and exact prompt. Inspect requested corrections locally:
a face repair can create an extra face in a carried helmet; glove edits can change
background borders. Reuse unaffected authored poses from prior candidates when
appropriate, recording the source and pose index for every selected frame.

Compare endpoints on a shared foot baseline at the same pixel scale. Measure
helmet, torso and legs separately before changing proportions. A smaller helmet
can make the whole actor appear thin even when body widths already match.

## Register and package

Marsh's selected side starts/stops use measured shoulder anchors and independent
east/west source rows. Preserve exact existing tread/swim endpoints; transparent
padding may differ by direction when a diagonal pose needs room. Extend derived
clearance to contain that pose and rerun the relevant route test. Supplemental
pack checks must validate the declared water flag rather than assuming every
supplement is dry. Observe actual transition completion when testing loop handoff;
decimal clock subtraction can land one sample before the nominal boundary.
See docs/MARSH_SIDE_SWIM_TRANSITIONS_2026-09-22.md in the project.

Marsh's north/south starts/stops complete the same contract using independently
authored front/rear rows. Use a head/shoulder ruler for these foreshortened views:
the first 0.27-scale audition shrank between endpoints; the selected fixed 0.30
scale and measured torso positions preserve the transition. Keep side-view recipes
unchanged when adding axial coverage. See MARSH_AXIAL_SWIM_TRANSITIONS_2026-09-22.md.

- Preserve accepted dry source pixels and palettes; do not rebuild unrelated art.
- Use a fixed anatomical scale across a row. Ground death retains a floor baseline;
  swimming uses an authored torso/shoulder anchor. Never normalize each crouched,
  prone or foreshortened pose to standing bounding-box height.
- Record source hashes, crop, scale and per-pose anchors. Rear head width may be a
  better calibration landmark than crown-to-collar height; name the measurement.
- Inspect real alpha before slicing. Painted checkerboards are not transparency.
  Key only verified flat backgrounds. Remove measured letterbox regions and
  threshold alpha before measuring bounds when faint debris would inflate them.
- Raised equipment may require a taller canvas. Preserve body scale and move the
  pivot with padding. Use actual texture dimensions in all renderers and reviews;
  the historical92x92/pivot46,86 profile is not a universal size constraint.
- Keep timing, loop/one-shot and terminal hold in the manifest. Reversed authored
  poses may support removal; label derivation and author removal timing separately.
  A removal row ending with a held helmet does not depict returning it to a locker.

## Fit equipment without hiding defects

Use the correct authored helmet view; confirm facing visually. Check transparent
visor aperture, face visibility, hair coverage and collar fit per pose. Record
body/overlay hashes, placement, rotation and foreground source regions. Rotating
with expanded bounds changes the required top-left position: align the visor to
the face again. Preserve hands above a rim with registered original foreground
pixels where necessary. Exact composition checks prove provenance, not good fit.

Carried helmets must be empty; worn helmets must contain the actor's single head.
Gloves, tool ownership and department identity remain consistent through motion.
Check helmet dimensions against equipped idle, not only the large source sheet.

## Connect animation to behavior

Separate environment, locomotion, equipment and life state. Dry movement, swimming
and stationary treading need explicit selection. Death stops decisions/travel and
holds its terminal pose; water death must not settle onto an imaginary floor.

Use manifest duration and simulation time for equipment transitions. Cosmetic
visual time must not advance a paused action. Transition artwork contains its own
helmet, so do not overlay another one or require equipped-row lookup during it.
Commit equipment at the defined completion event. Block exterior departure until
required gear is equipped and block removal outside. Interruptions, death or
invalidated floor/navigation must cancel unfinished work without granting or
removing equipment, leaving no stale timer.

A complete locker interaction also needs an authored reachable approach, ownership
or reservation rules, pickup/return semantics, and safe interruption behavior.
A direct begin-action API or fixture trigger proves none of these by itself.

`begin_helmet_action_at_locker` accepts an explicit ID, cell, canonical station
interaction point and facing. It rejects inconsistent cells, unsupported facing,
blocked approach and points more than 12 station units from the actor. Current
action art supports east only. The caller must supply an actual authored locker;
this reach API does not discover props or reserve inventory.
`request_helmet_at_locker` routes to the supplied point through the crew navigation
graph, validates swept clearance, and starts the timed action only after arrival.
Preserve the exact interaction endpoint during traffic detours. Save the pending
request with its route; reject inconsistent endpoints, equipment or media, and
clear the request on death, obstruction or topology rebuild. Legacy saves default
to no request. Fixture points prove this interface, not production locker placement.

## Verify and record evidence

For stroke repairs, inspect arm propulsion separately from leg kicks. Define
reach, pull and recovery silhouettes before generating a loop; six different leg
poses can still leave the arms effectively static. Compare the old and revised
rows on a shared clock and anatomical anchor. A longer forward reach may require
more canvas width; preserve body scale rather than shrinking the whole swimmer.
Check torso pitch and the last-to-first transition before promoting a revision,
then rebuild its per-pose helmet fittings and verify the actual renderer.
When a near-side forearm crosses a helmet collar, preserve the reviewed original
arm pixels as an explicit foreground region and record it with the overlay offset.
Check the region does not restore a face or torso patch over the helmet. Longer
reach also changes the swimmer's visual footprint: a clear standing foot point
does not establish that the swimming body clears nearby props.
Rebuild `character/crew-underwater-v1/build_swim_clearance.py` after changes to
swim/tread bodies, helmets, timing manifests or pivots. It exports per-facing
cycle bounds in station units with source hashes; revision validation rejects
stale clearance data. Test a clear foot route whose reaching body hits a prop,
an unobstructed stroke, and a missing-floor boundary for every actor. A movement
guard that stops an unsafe stroke does not prove the planner can find a safe route.
Water route search must include facing in its search state: arriving at the same
node from another direction can change whether the next turn fits. Validate each
shortcut again with the incoming/outgoing silhouettes so smoothing cannot cut
across an obstacle avoided by the original route. Test both a completed detour
and a disconnected destination, then separately measure full-station performance.
Apply the same checks to crew-avoidance joins, shortcuts and exact destination
segments. A traffic fixture must include a peer on an otherwise unobstructed long
edge: disabling nearby nodes alone cannot detect that crossing. Keep peer-edge
checks inside traffic route search, and verify temporary graph exclusions clear.
Measure route search on authored room graphs, not only sparse synthetic graphs.
For rooms with complete rectangular blocker geometry, use exact swept-envelope
tests and missing-cell checks; reserve dense floor sampling for corridor/legacy
shapes. Re-run collision and arrival tests after optimizing, and report graph
size, route scope and measured times rather than a general performance guarantee.
Test connected-room passages explicitly. Avoid double-counting the standing foot
radius when expanding obstacles for a full-body envelope. Measure travel and
treading poses separately: a union of both can reject a passage that the swimmer
fits horizontally. A safe geometric lane may also fall between navigation nodes;
diagnose the lane and grid resolution before changing room art or character scale.
Keep horizontal travel and upright treading envelopes separate. If a stopped
swimmer cannot tread safely at the current anchor, retain the horizontal swim
pose; resume treading only where its own full cycle fits. Verify this behavior
at the doorway and after arrival, including all requested crew and helmets.
Broad-phase sweep pruning should use bounds derived from the actual registered
blockers, including wall thickness/padding, rather than an assumed room rectangle.
Refresh those bounds when rebuilding geometry and rerun doorway, obstacle and dry
navigation regressions. Keep performance numbers tied to the measured fixture.
For native fixtures, set the instantiated game as `current_scene` before capture
when renderers resolve it there. Verify the actual room and subject are visible; controller assertions can pass
while screenshots contain only UI. Store each capture run separately and list
exact files so failed captures cannot mix into a later successful sequence.
For stationary animation fixtures, distinguish a blocked pose from a missing
animation. Record actor, position and full-cycle clearance when state selection
differs. Assert the intended safe fallback at the blocked point before choosing
a clear visual-sampling point; never weaken production geometry for a screenshot.
Size review crops for the whole moving silhouette across every captured phase,
not just the shoulder or middle frame. When a limb appears clipped, compare the
original station capture before changing the sprite: the review crop may be the
cause. Distinguish ordered-frame inspection from real-time playback review.

Check dimensions, nonempty margins, alpha, timing/counts, source hashes and exact
registered compositions. Detect stale derived frames after upstream changes.
For open visors, verify alpha inside the opening as well as outside the silhouette.
A generated checkerboard may be opaque RGB artwork. Inspect file channels and
the final downsampled aperture, then composite over every actor's actual face;
an empty window alone does not prove that its placement reveals the face.
Track body and equipment coverage for each direction independently. A finished
directional contact sheet must also be compared with the opposite-facing body
at the same anatomical scale. A head-on south camera and overhead north camera
can make the same swimmer appear to shrink when turning; scaling by the head
cannot repair that projection mismatch. Correct the source camera first, keeping
the torso and limb projection consistent, then register the shoulder and fit gear.
If two poses overlap only in their horizontal extents, column-gap extraction may
merge them. Inspect the source before slicing: disconnected silhouettes can be
separated by connected components. Check detached tools and highlights explicitly
before discarding small components; component count alone does not prove a whole
character was preserved.
Validate the full stroke envelope against representative passages. A wide catch
can block routing even when both endpoints fit. If the authored motion is too
wide, revise the arm articulation while preserving anatomy and body scale, then
rebuild equipment and bounds and rerun the same failed route. Do not shrink the
whole character or weaken wall clearance to conceal the animation mismatch.
A finished fitting is still a candidate until its corresponding directional body pack is
integrated and exercised in the runtime. Shared comparison pages must select
both body and fitting paths from the same direction; test every supported
direction rather than assuming a working default covers the alternatives.
When promoting a directional revision, update the runtime loader, review pack
selection, clearance exporter and reproducible builder status together. Exercise
the reverse route explicitly: opposite-facing equipment and asymmetric silhouettes
can change clearance even when the doorway is unchanged. Keep its evidence file
separate so it does not overwrite the forward-route result.
Verify the review player itself advances in a real browser before judging motion.
Size shared review canvases from the union of frame extents relative to their
pivots, retaining one common anchor. A horizontal-swim canvas can crop vertical
swimmers even when every source frame has valid margins. Check draw bounds with
actual image dimensions for each supported direction and equipment variant.
Initialize its clock from the first animation callback, clamp negative deltas,
and derive frame selection from manifest durations. A loaded page or successful
HTTP response does not prove that its animation loop survived the first draw.
For playback, sample phase interiors, terminal holds, pause and equipment toggles.
For persistence, write/read real disk saves midway through both actions; compare
NPC state and exact frame bytes, reject contradictory checkpoints without mutation,
and complete the restored action. Also round-trip a pending locker trip, sweep
every movement step against room geometry, and verify gear remains unchanged
until arrival and action completion. Test all requested crew, including Bill's path.

Inspect native station output and endpoint comparisons for every affected actor.
Record sampled frames as samples, not continuous motion review. Fixed fixture
positions do not prove travel clearance. Clear legacy architect population state
only in dedicated three-crew fixtures, never normal gameplay to force a test pass.

Evidence must identify source/frame/fixture revisions. Rebuilding captures can
invalidate old hashes even when filenames stay the same. Keep current coverage
summaries above history, and do not equate mechanical passes with visual acceptance
or owner approval. Run relevant skill evaluation cases when changing this workflow;
case specifications are not execution results.

Historical experiments and revision-specific findings are preserved in
[the pilot history](history/underwater-pilot-lessons-2026-09-06.md). Consult it only
for provenance or a specific failure; current manifests/code/evidence govern status.

### Locker actions: source, timing and handoff

Use each actor's original authored action source for identity and proportions,
and the actual runtime boundary frame for registration. Measure actor-specific
foot anchors and body scale; never normalize each pose independently or reuse
another actor's source measurements. Enlarging a tiny frame adds no detail.

Keep stage packs as reproducible sources. Record reused/reversed pose order and
hashes; author deposit timing separately. For a linear action with one atomic
gear commit, composition under the existing action key/timer can preserve the
controller's save, reservation and cancellation semantics. Both renderer and NPC
duration reader must select the same composed manifest.

Include the actual bare and equipped idle cycles around action sequences, not
only the internal stage joins. Compare idle-to-pickup, donning-to-equipped-idle,
and deposit-to-bare-idle at a shared foot anchor; matching canvas pivots does not
prove body proportions or helmet silhouettes match.

Inspect both sides of each join at game scale. An identical endpoint guarantees
only that frame's pixels: the preceding pose can still change helmet size, body
proportions or hand position abruptly. Inspect combined dwell when two stages
share that image. Preserve source durations, record composition overrides and
recalculate handoff times from final durations. Runtime selection can remain
provisional while defects are tracked; do not label it visually accepted.

Drive shelf visibility from named grasp/release events and the saved simulation
timer. Select events by ID, not list order or visual callbacks. The first empty-
handed deposit pose needs a persistent world-side helmet on a visible support.
Preserve the existing reusable-gear semantics; a staged spare must not silently
introduce finite inventory. Metadata alone does not implement a transfer.

Review actual runtime durations at a shared pivot. Seek just before boundaries,
show deliberate holds explicitly and stop at the terminal pose rather than
inventing a removal-to-pickup loop. Capture native frames immediately before and
after each handoff for every actor and applicable room rotation. Inspect shelf
height, support, hand contact, occlusion and shared-prop silhouette differences.
Ordered stills and a working browser clock do not establish continuous acceptance.

Write/read disk saves during every stage, including just after release in the
actual room. Compare restored pixels, action timer, equipment and shelf visibility;
then complete and cancel late-stage work. Reject contradictory checkpoints without
mutation. Keep visual findings separate from these mechanical checks.

Current project implementations (relative to the checkout):

- `character/crew-underwater-v1/build_pickup_revision.py`: source registration.
- `build_deposit_revision.py`, `build_locker_sequences.py` in that directory:
  explicit pose reuse and composition timing.
- `build_locker_review.py` and `revisions/locker-review.html`: stage review using
  composed timing; `build_review.py`: main runtime pack selection.
- `tests/test_crew_death_pack.gd`, `tests/test_crew_death_save.gd`,
  `tests/test_crew_medium.gd`, `tests/test_airlock.gd`: phase, persistence,
  cancellation and real-room handoff checks.

Inspect current code/manifests before reusing values. Revision-specific status and
logs belong in `character/crew-underwater-v1/locker/README.md`. The pre-consolidation
notes are retained in [locker history](history/locker-handoff-lessons-2026-09-06.md).

For current locker rebuilds, use `python character/crew-underwater-v1/rebuild_locker_pipeline.py` in the checkout. It orchestrates existing builders and source checks in dependency order, without generation or native acceptance. Keep builder defaults aligned with the selected per-actor revisions and reject unsupported actor/source combinations explicitly; verify a routine rebuild preserves selected frame bytes before changing production defaults.

When verifying shared equipment across role actions, sample the union of each actor's phase interiors if timings differ. Compare actual renderer pixels and the manifest pivot with the selected fitted source, then inspect native captures for face/head coverage and hand occlusion. A pass on equipment action clips does not verify dry idle/walk/kneel overlays; each changed fitting needs appropriate coverage.

For distance-driven locomotion fixtures, advance positions by each actor's own stride distance times the desired cycle fraction, with a matching initial clock sample. Time-only changes can leave the same walk frame displayed throughout a test. Check sampled segments against existing geometry and compare actual renderer pixels to selected phase sources. Describe a synthetic straight segment as such; it does not establish autonomous route or turning behavior.

For facing-only locomotion changes, inspect whether the player resets its gait. Preserve normalized cycle fraction across directional clips of the same distance-driven state when appropriate, including differing durations; then add traveled distance. Keep action changes, teleports and time rewinds as explicit resets. Test all playback implementations (Bill has a separate clock) and repeated same-time samples. Clock continuity does not prove directional silhouettes match visually.

For cross-direction swim review, `character/crew-underwater-v1/build_swim_turn_review.py` compares the current hashed body/equipment selections at equal normalized stroke fractions and anatomical scale. This can expose camera/foreshortening differences that a per-direction loop review hides. Treat them as source defects before changing scale or clearance. Preserve full pivot-relative extents in the comparison so clipping is not mistaken for an anatomy problem.

When selecting a different directional revision, update runtime loading, review selection, phase fixtures, coverage inventory and clearance inputs together. Regenerate envelopes from every selected bare/equipped phase before routing checks; corrected foreshortening can enlarge the body footprint despite unchanged canvas and pivot. Keep source-specific evidence in the revision README, and distinguish a passing furnished-room route from continuous motion acceptance.


### Tread helmet polish, September 12, 2026

Fit dense tread equipment to the actual head and visor aperture, not doubled legacy pilot bounds. Re-extract the original helmet cutout at the fitted resolution; preserve body pixels and palette. Review every pose in all four directions and propagate shared tread endpoints into swim start/stop through the source recipe. Record changed-frame hashes so unrelated animation remains demonstrably unchanged. Bill uses 34x36 side/rear helmets and a 36x40 front helmet on the 184px tread canvas; these are Bill-specific registrations, not universal crew dimensions.


### Airlock occupied-chamber rendering - September 12, 2026

Keep chamber deck and fill-water drawing in the floor pass. Sorting the entire pressure chamber as a foreground prop paints over its occupant. Keep rail/hatch drawing separate and use chamber-local water depth for the actor, restoring the room water value after drawing. Native visibility regression must compare occupied and empty chamber pixels in all four rotations, both dry and flooded. Before dispatching a native fixture, settle its first rendered layout and rebuild navigation; initial layout geometry registration can otherwise cancel the request. Full journeys use the actual locker and expedition controllers, with source/native and release evidence recorded separately.
# Equipment continuity across dry work states

When an equipped actor changes posture, compare the actual overlay dimensions and
opaque shell pixels against standing/walking at the same standingHeight. Shared
source art and valid anchors do not prevent a scale pop: Bill's west work fit used
34x40 while dry standing used48x56. The corrected work fits record size and offset
explicitly, preserving body pixels and endpoints. Review each other direction's fit
visually before applying the same correction. North/south have now passed that
review and are corrected as well; tests compare all three views' shell pixels
against standing. See BILL_WORK_HELMET_CONTINUITY_2026-09-21.md.

For newly generated poses using an existing shell, inspect hair buns outside the
rotated helmet silhouette at enlarged scale. Tuck only registered equipped head
regions while preserving the authored visor opening; do not enlarge every helmet
or alter the bare source to hide that mismatch. Record cleanup boxes, source/overlay
hashes, head centers and rotation. Verify canonical equipped idle, bare immutability,
matching furnitureFrames and native clearance through both entry and exit. Staged
entry/exit gear does not establish sleep-loop or controller/checkpoint coverage.


### Marsh east/north turns, September 22, 2026

A rear swimming intermediate must foreshorten the legs while preserving head
and shoulder scale. Source 01 overextended them; use only source 02 cell three
and preserve source 01 cells one and two. The deterministic recipe is
`tools/build_marsh_swim_turns.py`; north-to-east reverses the selected poses.
Keep exact destination swim frame zero, and test the first resumed frame.
The handoff fixture must follow the configured clock: Marsh swim currently
uses elapsed time, whereas stride-configured clips use movement distance.
Do not add a stride setting solely to satisfy a test assumption. New padded
turns enlarge north/east lower clearance; the 93-sample battery route passed.

The subsequent west/north pair uses independently authored `west-north-01.png`
and the same .23 extraction scale; its shoulder anchors are explicit in the
pair-aware builder. Both pairs are rebuilt and pixel-compared by
`tests/test_marsh_swim_turns.py`. Adding a pair must also update the canonical
builder pair list and require both directions in the runtime handoff test.
West/north did not enlarge clearance or alter any existing runtime PNG.

East/south turns now use the independently authored `east-south-01.png`.
Front-facing foreshortening must hide trailing legs behind the torso,
rather than turn the swimmer upright. Register head motion as well as
shoulders: the middle/near-front trial required -5/-10 horizontal pixels.
Six directed swimming turns now reproduce locally with exact endpoints.

West/south completes all eight adjacent-direction swimming turns. Its
independent source has explicit shoulder landmarks in the pair builder;
do not reuse east/south landmarks or mirror the sheet. Forty frames now
reproduce exactly, with prior frames and clearance unchanged. Opposite
turns still need their own integration and motion review.

Opposite swimming turns compose two authored quarter-turns through an exact
shared cardinal frame. Assert the center pixels match; store that frame
once with combined120ms duration to preserve the two400ms clocks. The
separate opposite builder is included in canonical rebuild and all76
turn frames are reproduction-tested. All twelve directed swimming turns
are required in the native handoff test. Composition is derived motion,
not new authored art or owner visual acceptance.


### Water-family promotion - September 30, 2026
Audit selected full-density water frames rather than legacy pilot fittings. A
master-matching treading head alone does not repair start/stop/swim continuity.
Stage the coherent family until required joins match, then update actual selected
clearance and verify runtime loads. Native upright master components may fit
upright treading at unchanged scale; pitched/foreshortened swimmers need separate
camera and collar decisions. Keep body material drift explicitly open when only
head identity has been repaired; inventory counts do not certify motion quality.


### Axial swim head camera - September 30, 2026
For prone swimming toward the camera, explicitly place rear collar upscreen,
crown dominant and visor as lower crescent; a smaller front portrait still has
wrong pitch. Preserve a rejected candidate and state the camera defect. Exact
side components can be rotated at measured per-pose face anchors; overhead views
may need generated source artwork. Calibrate fixed head width against equipped
masters, grade source once and preserve source foreground limbs. Retain complete
manifest metadata when writing supplemental packs, including canvas dimensions,
precomposition, water flags and stride. Local fit/packaging checks do not prove
full water-family joins or motion quality.


### Water transition anatomy - September 30, 2026
Check full start/stop body silhouettes as well as endpoint pixels: inherited middle
poses can enlarge the head and torso despite exact joins. Repair body source when
that happens; a helmet graft cannot fix anatomy. Calibrate one source anatomy
scale, register at named head/shoulder anchors and preserve exact loop endpoints.
Generated atlas bodies can overlap equal-cell bounding boxes while remaining
separate alpha components; use inspected connected bodies for extraction rather
than blindly equal-width cuts. Keep source-wide grade and independent opposite
views. Functional join checks do not establish body-grade or motion acceptance.


### Protect completed heads during cloth grading - September 30, 2026
When water bodies retain an older blue-green material cast, derive one source-family
cloth correction against selected directional masters and apply it from immutable
inputs. Protect exact head/component support as well as changed pixel masks:
coincidentally equal body/head colors do not establish material ownership. Preserve
alpha, non-cloth accents and independently completed grade on new source interiors;
replace transition endpoints from corrected loops to retain exact joins. Native
candidate loading proves playback/metadata, not installed selection or full identity.
Godot load_manifest returns void and defaults to replacement; supplementary native
fixtures must append explicitly and inspect loaded states. Save diagnostics and
profile fingerprints even on fixture timeout/failure.


### Directional water transition source authority - September 30, 2026
Inspect original opposite-view body master before drawing: west Veld exposes the
scanner where east exposes cylinders. Referencing only a looping pose can retain
old equipment or lose details; use independent full-body construction plus registered
motion endpoints. A generated atlas's requested virtual scale remains a hypothesis:
record fixed fitted scale and inspect physical head/shoulder rulers and silhouette
bounds without normalizing projected pose height. Save new axial sources as pending
until camera/pitch and anatomy are fitted. Expand native review canvases with added
state rows; green playback checks can coexist with a clipped review screenshot.

### Axial transition source scale audit — September 30, 2026
Do not transfer a side-atlas extraction scale to an independently generated axial
atlas without physical rulers. A fixed-scale contact bracketed by exact directional
loop endpoints exposed oversized head/shoulder mass in both Veld axial sources.
Center silhouettes only for anatomy diagnostics; motion acceptance needs named
landmarks and world-pivot registration. Compare upright and prone helmet components
before authoring intermediates: preserve shell construction while changing pitch.
Keep raw source, pending status and camera defects separate from staged clip counts.

### Master authority versus old water endpoints — September 30, 2026
An exact join to an inherited loop can preserve a wrong body. Veld north source
fitting exposed different rear armor and projected proportions in the older swim
body despite previously corrected cloth/head fits. Compare old endpoint and new
source directly with selected dry and original construction masters. If the old
body remains unproven, rebuild the loop and transition as a coherent family rather
than distort new source anatomy solely to meet it. Keep preview manifests outside
candidate-selection counts until motion is repaired. Record source-specific ruler
hypotheses and native head XY calibration; dimension checks are not motion proof.

### Coherent axial water body family — September 30, 2026
Repair tread/swim/start/stop together when their inherited rear armor/proportions
have drifted. Veld north uses independent six-pose loop sources, fixed physical
head-ruler calibration per atlas, named world head anchors and one combined cloth/
patch curve. Replace transition joins with exact new loop endpoints; reverse stop
is derived. Compare native anatomical scales, not equal canvas heights. Retain
foreground gloves where they cross fitted shell support. Explicit candidate loaders
must stage older body/equipment together before a differently-sized paired override:
load_equipment_manifest validates against the currently loaded body canvas. Classify
combined helmet manifests explicitly, skip shadowed old states in assertions/counts,
and preserve failed-run logs/profile evidence before rerunning a repaired fixture.

### South overhead body and shell source fitting — September 30, 2026
South prone source must keep rear collar upscreen and face as a lower crescent for
ALL stroke phases. A visible hair silhouette changes when crown/bun is exposed;
calibrate head together with shoulder/hip rulers, not a north/upright hair-width
constant. Preserve isolated dense source crops, exact generation refs/prompts and
trial status. Width-correct helmet sources can still miss endpoint height/camera:
Veld35px trial heads were5px shorter than masters. Record that gap and review
collar/crown fitting with body rather than presenting dimension checks as completion.

### Near-prone collar ownership and body anchor trials — September 30, 2026
A width/height-correct source may still put the neck gasket on the wrong side of
an overhead face. Revised Veld south pitch matched native dimensions within1px,
but last source retained a front buckle below chin; exact prone master places rear
collar upscreen. Reuse canonical prone component for near-prone final interior when
camera already approaches it, and record derived reuse rather than claim a new
angle. Review visible face/collar landmarks, not just silhouette counts. Register
south bare swimmer at a measured face-bottom anchor, pair it with physical shoulder/
hip rulers, and preserve provisional body fits outside selected manifests until
paired occlusion, material grade, exact joins and native playback are verified.

### Facial anchors and material ownership — September 30, 2026
Warm boot metal can satisfy skin RGB thresholds. Veld south's first composite put
helmets down the body while border/protected-body checks passed; visual review
caught it. Use connected face support for geometric anchors AND face grading, not
all warm pixels. Keep cyan scanner/chest lamps separate from blue patch correction;
RGB mask overlap can silently dim equipment. Source/camera/identity review is a
separate gate from native loaded pixels/clocks. Rerun native checks when material
ownership changes exported pixels; keep prior evidence scoped to prior revision.
North's earlier broad blue selector remains an explicit cross-family audit item.

### Veld coherent side water source fitting — September30,2026
Replace inherited side bodies when face/hair/outfit construction differs from
master, rather than adding whole-sprite exposure fixes. Pair independent tread,
prone and pitch sources against original directional master; source references
must preserve visible hip equipment ownership. One fixed scale per atlas from
selected face ruler (east17px) is a hypothesis verified with torso/hip/camera
boards, not a per-pose face resize or automatic anatomy acceptance. Head support
must be excluded from neutral cloth/blue patch masks so brown hair and silver
streak are not accidentally graded; skin still gets its connected face curve.
Derive starts/stops from new exact loop endpoints; never join coherent new bodies
to inherited incompatible loops. Review pitch progression and cadence separately
from exact joins and native API coverage. Preserve original source/prompt/hash.

### West water ruler and clean evidence — September30,2026
Use each selected direction's measured face ruler: Veld west16px, east17px.
Calibrate one scale per atlas, then inspect torso/hip/limb proportions and camera;
matching a face ruler does not prove all anatomy. Independent west sources keep
nearhip scanner and partially hidden farhip cylinders; do not mirror east bodies.
Verify alpha and pixels outside all explicit grade masks before resampling.
Paired browser previews need one shared clock and original duration ratios;
independently loaded GIFs can show different phases and obscure head/body fit.
A Godot exit0 and all candidate assertions can coexist with engine parse errors.
Parse complete logs for SCRIPT ERROR/ERROR and reject such runs as clean native
integration. Preserve failed evidence, isolate the first failing dependency,
repair a clear syntax defect narrowly, and rerun only the affected gate with
scratch APPDATA/profile fingerprints. Never claim world/owner acceptance from
candidate texture/clock checks alone.

### Selected water installation and scoped route evidence — September30,2026

For partial water replacement, measure alpha-qualified bounds at the actual
renderer scale and declared pivot, union new swim/tread/start-stop geometry with
old conservative envelopes until retained turn art is also replaced. Leave other
action/life bounds intact. Verify normal-loader pixels, per-frame containment,
actual collision probes and furnished graph routes separately. Veld32states192refs
passed1338 installed checks and8 direction/profile routes; this does not establish
exterior/traffic/flood simulation or owner acceptance. Record reused clean cases
and why the changed fixture cannot affect their route assertions. Reject engine
errors even when route assertions and process exit pass. On fixture shutdown,
disable processors before stop_audio clears streams, then drain playback as the
normal shutdown does; do not suppress Ogg leaks or null-stream errors. Preserve
failed evidence and isolate every Godot invocation from real owner profiles.
