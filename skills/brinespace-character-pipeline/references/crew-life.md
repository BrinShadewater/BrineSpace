# Crew life: pipeline and workflow lessons

For everyday actions, cargo and distress, track source production, registered
packaging, runtime selection and visual acceptance separately.

## Asset pipeline

- Inspect actual row facing before expanding coverage. Labels do not prove facing.
  Generate focused corrections; preserve rejected originals and exact prompts.
  Never mirror asymmetric body equipment to fill missing views.
- Preserve detached cargo during extraction. Equal-width cells can cut a boot or
  include neighboring pixels. Inspect transparent gutters and every resulting crop;
  correct frame counts alone do not validate a sheet.
- Share anatomical scale through a sequence. Calibrate reading to seated idle;
  never stretch crouched or prone poses to standing height.
- Check per-frame head anchors and equipment tilt through turns and prone poses.
  Nominal clip direction is insufficient. Review bare and fitted endpoints.
- Record reverse-action and composed-turn derivations. Join transitions to actual
  base cycles rather than inventing replacement poses in packaging code.

## Runtime workflow

- Resolve retained furniture in every rotation. A baseline sofa may be replaced
  by a wall installation. Provide safe approaches and prove navigation access.
- Keep navigation feet on accessible floor; use explicit visual offsets onto
  furniture. Review depth against chair backs, pillows and footboards. Fixed pivots
  alone do not prevent disappearing behind furniture.
- Use simulation clocks for transitions. Test pause, intermediate saves, restore
  and service interruption. Seated readers and sleepers should rise before leaving;
  interruption must not emit successful completion.
- Place pickup before extraction/credit. Test recall and duplicate-credit negative
  controls. Maintain the held case through carrying turns.
- Separate distress cues from oxygen rules. Check fitted bounds in tight spaces.
  A sealed helmet cannot be treated as an open mouth for meals.

## Evidence and closeout

Keep the entire target prop visible when reviewing work contact. Actor-follow crops
can omit equipment below the feet and make correct facing appear wrong. Resolve
the recorded foot against live prop geometry before changing directional art.
A generic proximity band establishes a destination, not hand/tool contact or a
suitable action; verify approach, service side and action together at native scale.
If an authored service point lies outside a generic destination band, grant its
reviewed station a bounded exception while retaining navigation and final-segment
clearance. Do not loosen collisions to force contact. Test blocked and unreviewed
orientations, and distinguish functional service completion from optional comms.
When adding a room service, check every need that can select it. Curiosity can
share maintenance furniture while bypassing generic service-availability guards;
cover both selection and interruption, including no benefit after power loss.
For save compatibility, safe floor is necessary but does not prove retained
furniture contact. Compare an active equipment action's saved contact/facing with
current geometry; cancel obsolete work without teleportation or service credit.
Keep matching-contact positive controls alongside stale-contact regressions.

For bed transitions, inspect the intermediate seated hip contact as well as the
sleep endpoint. Measure approach-to-rest travel relative to body height: a source
can fit the final mattress while floating across the floor during interpolation.
Resolve reachable entry and contact choreography together before expanding frames
or directions. A four-quarter capture count alone is not visual acceptance.
Use the real activity station in staged previews after validating its route. Keep
temporary draw-depth adjustments explicit: a compound bed/cabinet can cover a valid
floor entry because it sorts at the bed foot. Do not silently bake a furniture-only
depth workaround into a general standing pose or count a reversed preview as runtime
get-up coverage.
Before accepting a pose-hold GIF, sample the production animation player at the
actor's real transition duration. Calculate travel over the actual moving interval,
not the whole clip: a hold followed by one lowering frame can compress a large
displacement into a visible slide. Exact idle/sleep endpoints do not establish a
connected movement. Duration changes require matching actor timers and interruption
and restore checks, not just longer manifest frame durations.
Trace presentation coordinates through both the position getter and renderer.
Marsh's getter subtracts the same vertical lift GridCanvas adds back, so native
fixtures must place the external actor at the NPC foot without an additional lift.
Otherwise apparently precise contact and displacement measurements describe the
fixture rather than production behavior.
For a longer furniture-specific animation, persist its contact anchors and validate
its own duration without relaxing other characters' timer limits. Reverse an
interrupted entry from its current elapsed position; restarting a full rise causes
a pose jump. Battery/other emergency controllers must also leave furniture before
starting floor movement. Keep furniture-only extents out of shared locomotion or
swimming clearance when the runtime presents them with a separate contact offset.
Review the normal chooser's final walking segment: an activity's acceptance radius
can let a nearby graph node start a carefully authored contact animation too far
away. Opt furniture into exact approach only with stand/peer/segment clearance.
Review walking before and after the pose, since compound-prop depth can hide a
torso that the furniture animation's own depth offset correctly reveals.

Run affected tests and inspect native furniture and fitted motion at station scale.
On Windows, wait for Godot and read exit status/logs rather than assuming shell
return means completion. Respect browser security rejection; use native evidence
and local artifact links without claiming browser validation.

Record coverage, derivations, consumers, evidence and pending owner review at
closeout. Update maintained skill sources and their changed installed mirrors.
Preserve concurrent sessions' notes/code and leave other tasks alone.

Examples: `character/crew-life-v1/README.md`,
`docs/CREW_LIFE_EXPANSION_2026-09-08.md`, `tests/preview_crew_life.gd`,
`tests/test_crew_life_rooms.gd` and `tests/test_station_systems.gd`.

Furniture pose review must include draw sorting. Marsh's south reading frame was
valid but disappeared behind a sofa because its depth offset stayed zero. Native
shared-cast review exposed it; the canonical writer now supplies seated depth and
transition ramps. Keep depth separate from foot/pivot placement and sprite pixels.
A successful Bill pose does not establish other cast metadata compatibility.

Authored carry turns end on destination carry frame zero. At completed-turn exit,
reset the ordinary carry clock/position before resuming; otherwise old gait phase
and travel during the turn skip to a different pose. Verify actual catalog endpoint
pixels and following distance phase, honoring per-direction strides. Not all crew
have matching turn/equipment coverage (Marsh currently does not). Printed test
counters cannot override SCRIPT ERROR lines from invalid fixture assumptions.

Swimming turns have the same destination-frame-zero contract, verified across 144
registered selected turn endpoints. Compare clips after aligning texture pivots;
different transparent canvases are not pose differences. The playback guard covers
carry, swim and swim-carry separately: the latter already resets through its state
branch. Extend a fix only where actual phase/endpoint evidence shows the defect.

Bought bunk integration requires per-cast anatomical pillow anchors. Equal world
positions do not align sprites with different pivots, and head alignment alone
does not prove the feet fit inside the bed frame. Inspect source bounds and native
ladder/post occlusion together. Do not shrink a character or resize an owner layout
to conceal a too-long prone pose; author a furniture-specific compact pose and
verify continuous entry/rise. Keep fixture-only depth overrides out of general
sleep metadata until the furniture renderer owns that occlusion.

For stacked bunks, verify upper-mattress underside clearance through the entire
lowering pose. A lying endpoint can fit while an elbow-supported lean intersects
the bunk above. Review mattress-edge entry and short inward movement as a contact
sequence; fixed hip registration in source art need not imply fixed world position
through entry. Preserve separate key-pose, complete motion and controller evidence.
Prefer a single source sequence's sleeping endpoint when a separately generated
endpoint would pop; keep both sources and record the selected derivation.

When boarding furniture, switch depth by contact phase, not by the overall action
name. A boot still hanging off a mattress must draw in front of the front rail;
putting it inside the furniture layer can slice the shin into disconnected pieces.
Only fully boarded poses should enter the interior layer. Reverse the same contact
schedule for exit and preserve per-frame registration when anchoring poses. Verify
canonical idle pixels and native first/last equality separately from motion quality.

For partial reversal, test both interior times and every exact source frame boundary.
Half-open forward and reverse intervals can select adjacent poses at the boundary
although all interior samples match. Human lie-down interruption uses completed
entry time, with a 1e-7s bias toward the current pose and full-duration cap. Check
contact offsets and the actual service-loss update as well as isolated clip pixels;
a full rise from partial entry visibly jumps even if both individual clips are valid.


For furniture-specific runtime profiles, test the normal goal chooser and exact
arrival before restoring intermediate poses. Persist contact anchors and validate
finite coordinates, supported direction/medium, transition duration and entry-foot
agreement. Keep longer furniture timing typed to that actor/profile; do not relax
all human save limits. Verify both equipped and bare disk restores, service-loss
reversal, and rejection of incompatible furniture transforms. Rebuild supplements
through the canonical pipeline and prove they do not enlarge movement clearance.

### Marsh first carry turns - September 22, 2026

East/north carry poses keep the case in front of the actor as the torso
occludes it; never move cargo onto the back to keep it visible. The local
builder uses .25 scale, measured centers and a common boot baseline,
with exact existing carry endpoints. Both turns are required by the
native handoff test. Dry metadata is distinct from swimming turns.

West/north carry uses independent source landmarks and .265 scale; the
east sheet remains .25. Same sheet dimensions do not imply equal body
density. Compare registered head/boot height before installing. Both
carry pairs now reproduce twenty frames and are required by handoff tests.

East/south carrying exposes the front of the case while retaining both
hand contacts at waist height. Its larger source uses .23 scale and
measured centers. Three pairs now reproduce thirty carry frames with
exact current endpoints; native handoff checks require all six clips.

West/south completes all eight adjacent carrying turns. Independent source
uses .24 scale and measured centers, retaining both hand contacts and
exact existing endpoints. All forty carry-turn frames reproduce exactly.
Half-turn composition and normal station transport review remain separate.

Carrying half-turns compose adjacent poses through an identical cardinal
frame, stored once with combined120ms duration. Four800ms clips complete
Marsh dry-carry coverage. All76 carry frames reproduce; all twelve turns
are required in handoff tests. Catalog audits distinguish coverage from
visual acceptance: other humans have all three turn families, including
helmet versions; Marsh still lacks twelve swimming-with-cargo turns.

### Loaded-swim foundation audit - September 22, 2026

Do not infer visible cargo from a swim-carry state name. Marsh east
currently uses empty-handed art; the direct texture renderer adds no case.
Audit base frames and pickup/unload joins before generating missing turns.
An east loaded-swim candidate is review-only under marsh-swim-cargo-v1.
Keep coverage counts separate from base-art correctness and acceptance.

East loaded swimming is now selected by a replacement manifest. Remove
old state entries to avoid duplicate catalogs, retain original PNGs and
reapply selection after canonical rebuild. Coverage is a union when
supplemental contracts replace existing keys. Detached pickup cargo must
survive component extraction; use measured cell edges for crossing boots.
Pickup maps six150ms slots to existing0.52s controller time and joins
exact loaded frame zero. All24 previous loaded frames were empty-handed;
other three directions still need repair. Native route passed93 samples.

West loaded swimming now uses independent loop/pickup sheets and measured
shoulder anchors. Preserve the detached case in first reach; inspect its
bounds as well as body bounds before installation. East/west replacements
reproduce24 frames with exact salvage/loaded endpoints. Both directions
are included in the canonical rebuild; north/south remain unresolved.

North loaded-swim source01 was too upright/elongated. Selected source02
foreshortens torso and legs without reducing head/shoulder scale. Rear
cargo is ahead of the torso, partly occluded, with hands forward; do not
move the case onto the back to improve visibility. North loop .25 and
pickup .28 scales are measured independently. All36 selected frames
across east/west/north reproduce with exact endpoints; south remains.

South completes all four loaded-swim/pickup replacements:48 frames reproduce.
Independent south sources use loop .25 and pickup .24 scales, measured
shoulders and exact salvage/loaded endpoints. Check lifted-case boot
bounds before installing; adjust registration, not anatomy, for clipping.
All four loaded endpoints are now ready for twelve cargo-swimming turns.
Native playback and93 route samples pass; full expedition review remains.

Loaded-swimming turns now complete Marsh's three turn families. Freeze the
selected supplemental loaded endpoints, never old empty-handed base PNGs.
Preserve actual source dimensions: new sheets include2170x725 as well as
2172x724; measured cells and shoulder registration must reflect those sizes.
East/north and east/south source02 correct a premature cardinal third
pose; only that corrected cell is selected. Half-turns share exact
cardinal pixels once with combined120ms timing. All76 new frames reproduce,
and native handoff requires all twelve loaded directions. Full expedition
and owner motion review remain separate from turn-matrix completion.

Real expedition review corrected two integration gaps missed by direct-player
fixtures: pickup0.52s-to-clip mapping was only in the preview, and Marsh
exterior clearance tested missing station floor, suppressing turns. Verify
through grid_canvas and a real dispatched route, not a fixture that supplies
the intended mapping or allow-transition flag itself. Pickup has6 poses;
existing unload has4. Pause tests must use the production gated entry,
not directly call an internal stepping helper. Three controller journeys
now pass. Loaded water-to-dry silhouette change remains abrupt.

Loaded airlock drainage now uses four-facing rise art tied to saved interlock
progress, not cosmetic time. Hold the authored planted pose while pressure
equalizes; an exact carry frame0 reference can be a stride with one boot raised
and should only resume when exit movement starts. Rear carry lowers hands
toward waist and permits torso occlusion. Read measured source cell edges when
a prone figure crosses equal cell boundaries. Preserve per-frame water metadata
and test pause, power loss, disk restore and death precedence through renderer.
Four-facing texture checks do not prove four rotated-airlock journeys.

Rotated expedition fixtures must preserve cryo/charging wards: deleting a ward
breaks the saved architect roster and can make Save.read silently recover an older
backup. Require the just-written primary checkpoint and expected expedition home
before restore. The maintained fixture now covers all four airlock rotations plus
empty/loaded recall; six cases also pass through the actual release executable.
Keep manual stepping evidence separate from real-time motion and pacing acceptance.
