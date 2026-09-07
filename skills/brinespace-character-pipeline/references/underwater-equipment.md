# Underwater animation and equipment workflow

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
