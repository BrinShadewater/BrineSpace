# BrineSpace current status

Updated September 24, 2026. Start here for current decisions and open work.
Latest Power report diagnosed: at seed 3862060672/cycle 457, both mining drones
have 100% battery; the only discovered mining deposit is exhausted. Nearby
surveyed piles require salvage. Charging is working in this captured state.
Drone battery/work status now precedes charging totals in the inspector; empty
mining surveys report depletion even without wreck entries. See
[full-Power drone report](DRONE_FULL_POWER_REPORT_2026-09-24.md).
Owner completion update: Construction Drone Bay, BRINE Core, Solar Array,
Reactor, Battery Array, Salvage Drone Bay, Gravity Loom and Tidal Condenser are
now decorated. Protect these eight rooms in all rotations, bringing the finished
list to 27. This supersedes their earlier classification as unfinished; do not
reapply the September 23 rotation cleanup. This records owner completion, not a
new visual or navigation validation. No saved layouts were changed.

September 23 Studio work preserved the then-finished 19 rooms and first rotations,
clears 84 secondary rotations in 28 unfinished rooms, and removes the reported
Listening Post floor plug. Owner layouts/recovery were backed up before applying.
Move to front/back is visible; late floor details remain editable and deletions
survive fallback hosts. Mining Bay walls, ordinary floor/riser joins, Airlock
180-degree locker placement and the changing bench's under-seat coil are fixed.
Walking-preview navigation is deferred during dragging; isolated preview cost
fell from 6.457 to 0.014 ms/update. Long-session hitch acceptance remains open.
Focused regressions, native Studio checks and captures pass; 44 cards refreshed.
See [Studio owner fixes](STUDIO_OWNER_DECORATION_FIXES_2026-09-23.md).

Follow-up paid native expedition: fresh seed 32 rescues Veld, survives disk Continue
and concludes at cycle 16 with zero failures. Reported Reactor repair/Continue and
drone battery regressions pass again. Lone-swimmer escape now skips duplicate
crew-avoidance searches; doorway-report warm search improves from about 199 to
125 ms, still a visible stall. Graph-valid paths rejected by final smoothing are
the next routing investigation. Scenery comparisons are ready for owner review.
See [expedition follow-up](EXPEDITION_FIX_FOLLOWUP_2026-09-23.md).
Submitted-report fixes: Bill recovers from cramped flooded doorway poses and can
retain repair routes across water transitions. Furnished-room repair positions and
air budgeting are corrected; unavailable repair jobs no longer replan every frame.
Unjoinable routes cannot trigger remote meals. Power storage now explicitly shows
FULL. Native replay seals the reported Reactor and verifies disk Continue; repair,
power, meal/rest, flood and navigation regressions pass. Profile-matched lag probe
improved from 100.70 to 13.25 ms mean simulation update; occasional 241–369 ms
routing spikes remain, so sustained rendering performance is not accepted.
Owner saves are untouched. See [report findings and evidence](OWNER_BUG_REPORT_FIXES_2026-09-23.md).
Studio deletion fix: saved wall-bank deletions no longer alter the Studio's source
furniture or disappear on subsequent saves. Pressure Control at 90° remains
cleared across reloads and rotation changes; source-layout checks pass for all
188 room/rotation combinations. Owner layouts and artwork are preserved. See
[deletion persistence evidence](STUDIO_DELETION_PERSISTENCE_2026-09-23.md).
Latest owner fix: mining/salvage drones charge from stored Power independently of
bay cycle allocation, preserving a shared reserve of 3 and resuming automatically
above it. Manual suspension and global pause/Power-off still hold charging;
prepaid charge is retained. Four focused suites and a native 16/3/4-Power fixture
pass; inspector feedback was reviewed. See
[stored-Power charging](DRONE_STORED_POWER_2026-09-23.md).
New owner direction: [procedural underwater sites](PROCEDURAL_SITES_2026-09-23.md)
are implemented locally. New loops retain a familiar opening, vary
terrain/resources/scenery and spread recovery chambers farther apart. First
profile sightings follow Veld → Branforth → Marsh; discovery occurs on survey,
separate from rescue/shop eligibility. Exterior scenery leaves the Room Layout
Studio catalogue while existing placements remain editable. Legacy saves retain
their maps. 1,000 deterministic seeds, discovery/save/Studio contracts and three
paid native expeditions pass. Seeds 32/73/118 rescue Veld and conclude at cycles
15/16/15 with normal costs, failures and 4× speed; native art comparison is recorded.
463 exterior props are hidden from new Studio placement; four low-rock/timber
choices are provisional. Owner visual/pacing acceptance remains open. Existing
test downloads predate this feature; no new packaging was requested.
Extended validation covers all three recoveries in a paid seed-32 checkpoint
chain, concluding alive at cycle 224. Test-player corrections between legs mean
this is neither an uninterrupted fresh-run pass nor accepted human pacing.
Native capture framing and surveyed scenery close-ups have been reviewed.
Repeat encounters now use an explicit expedition-wide seeded shuffle. All-starter
permutation/batching tests and a native disk-Continue check pass; first-sighting
order and already assigned occupants stay intact.
The test player now accounts for door-compatible routes, finite deposits, Hab
residents, owned salvage blueprints, turbine intakes, any first guest identity and
already learned matching-door recipes. Focused contracts and native fixtures pass;
fixtures with supplied hands remain separate from paid expedition evidence.
Production costs, yields and progression were unchanged by these corrections.
A progressed seed-73 checkpoint chain repeats known crew as Marsh → Branforth →
Veld. Marsh was recovered at 51, Branforth at 134 and Veld at 290, concluding with
six crew, 47 rooms and zero failures in the final leg. Earlier cutoffs at 163/221
remain failed all-three assertions. Intermediate conclusion awards are excluded
from copied profiles; this is a checkpoint chain, not uninterrupted fresh play.
Timing capture found two crew costs: unnecessary construction break searches and
Marsh replanning his charging route every movement frame. Both have focused fixes.
The same saved-station probe improves from 279.7 to 10.7 ms mean simulation frame
time (160 frames); it still has a 162.6 ms worst frame, so this is not smooth-frame
acceptance. Construction, meal/rest, battery and recovery/save regressions pass.
Native Continue/recharge/conclusion also passes, ending alive at cycle 309 with
zero errors; controller samples average 8.8 ms, with a remaining 326.5 ms spike.
These CPU measures exclude drawing/GPU time. The earlier 239.427-second event gap
recovered, but its exact cause is unproven. See the
[performance handoff](PROCEDURAL_PERFORMANCE_HANDOFF_2026-09-23.md) and
[routing handoff](PROCEDURAL_ROUTING_HANDOFF_2026-09-23.md).
The [owner review page](PROCEDURAL_SITES_OWNER_REVIEW.md) collects the comparison
captures and provisional artwork choices. Owner art and human pacing acceptance
remain open.
The broad animation, room-polish and stability goal remains unfinished.
The [complete preceding status](CURRENT_STATUS_HISTORY_POLISH_2026-09-22.md)
preserves dated implementation stages and evidence without alteration. Its older
pending statements and package names are historical, not a fresh task list.

## Objective and constraints

Continue Bill's pixel-layer/motion repair, other observed animation fixes, natural
bought-art furnishing, bug fixing and measured performance work. Maintain the
skills, visual bible and asset/release workflows.

Use large and medium props in logical work areas. Avoid accessory scatter and
blanket upscaling. Preserve the owner's Research Lab, Mycelium Nursery, Med Bay,
Pressure Control, Crew Lounge, Mining Drone Bay, Ore Refinery, Cryo Chamber,
Listening Post, Xeno Lab, Maintenance Bay, Crew Hab, Bio Lab, Clone Lab,
Isolation Vault, Current Turbine, Biomass Digester, Heat Recovery, Airlock,
Construction Drone Bay, BRINE Core, Solar Array, Reactor, Battery Array,
Salvage Drone Bay, Gravity Loom and Tidal Condenser layouts in all rotations. Other rooms retain their first rotation; their cleared
secondary rotations are intentional authoring space. Library names, categories, favourites and
retired marks are owner data. Local deterministic pixel editing is authorized.
**No Higgsfield without a fresh explicit request.** No commit, push or publication
is requested. Preserve source art and existing test packages.

Normal play retains paid building, resource failures, hidden discoveries,
three-cycle pattern stabilization and Conclude Expedition. Doctrines, timed
directives and scenario victory stay retired. Free building/disabled failures are
fixture-only. Preserve prototype saves and paired script UIDs; no broad refactor.
Read [development notes](DEVELOPMENT_NOTES.md) before gameplay changes and
[NOTICE](../NOTICE.md) for rights.

## Installed character and drone work

- [Cryopod and crew review](CRYO_AND_CREW_REVIEW_2026-09-22.md): human pods now
  play their exit poses in the final1.2seconds instead of spreading them over
  the full thaw. Timing/recovery tests and native Bill release pass. Existing
  test builds include this change. Other-crew action review flags Branforth repair
  detail consistency and Marsh repair/transition readability for follow-up.
  [Branforth south repair](BRANFORTH_SOUTH_REPAIR_INTEGRATION_2026-09-22.md) is
  now installed with connected kneel/stand and fitted equipment:36frames,
  exact rebuild/joins, native rendering and19,475crew checks pass. North-facing
  repair was subsequently installed in the
  [north repair pass](BRANFORTH_NORTH_REPAIR_INTEGRATION_2026-09-22.md): another
  36 frames, exact rebuild/joins and native player review pass. West candidates
  were rejected for broader/younger identity. The subsequent
  [west repair pass](BRANFORTH_WEST_REPAIR_INTEGRATION_2026-09-22.md) is installed:
  36 frames with canonical face/helmet, exact joins, native and station rendering.
  All 108 selected south/north/west frames reproduce exactly; 19,475 crew checks
  pass. [Marsh maintenance](MARSH_MAINTENANCE_REPAIR_2026-09-22.md) now uses his
  existing diagnostic controller art in connected draw/check/stow chains across
  four facings: 48 frames, exact rebuild/joins and real-controller native review
  pass. [Marsh side swim transitions](MARSH_SIDE_SWIM_TRANSITIONS_2026-09-22.md)
  now supply east/west starts and stops: 20 frames with exact endpoints, native
  handoff and battery/route checks pass. The subsequent
  [north/south pass](MARSH_AXIAL_SWIM_TRANSITIONS_2026-09-22.md) completes all eight
  swim start/stop clips: 40 frames rebuild exactly; native handoff and route checks
  pass. The [east/north swim turn pass](MARSH_SWIM_TURNS_2026-09-22.md) adds two
  directed turns, ten frames, exact endpoint handoffs and native playback checks.
  The [west/north pass](MARSH_WEST_NORTH_SWIM_TURNS_2026-09-22.md) adds two more
  directed turns with unchanged existing frames and clearance. Four of twelve
  swimming turns were installed at that checkpoint. The subsequent
  [east/south pass](MARSH_EAST_SOUTH_SWIM_TURNS_2026-09-22.md) brings this to six
  of twelve swimming turns. The [west/south pass](MARSH_WEST_SOUTH_SWIM_TURNS_2026-09-22.md)
  completes all eight adjacent-direction swimming turns. Current complete-pack
  check at that checkpoint: 19,939 checks passing. The
  [opposite-facing pass](MARSH_OPPOSITE_SWIM_TURNS_2026-09-22.md) completes all
  twelve swimming turns: 76 turn frames reproduce exactly, native handoffs and
  20,135 complete-pack checks pass. Twenty-four cargo turns remain: twelve dry
  carrying and twelve swimming with cargo at that checkpoint. The
  [first carry pair](MARSH_CARRY_TURNS_2026-09-22.md) now adds east/north and its
  reverse: ten frames, native handoff and 20,193 complete-pack checks pass.
  The [west/north carry pair](MARSH_WEST_CARRY_TURNS_2026-09-22.md) adds ten more
  frames with unchanged earlier art and clearance; 20,251 complete-pack checks pass.
  The [east/south carry pair](MARSH_SOUTH_CARRY_TURNS_2026-09-22.md) brings dry
  carrying to six directed turns; 20,309 complete-pack checks pass. Eighteen cargo
  turns remained at that checkpoint. The
  [west/south carry pass](MARSH_WEST_SOUTH_CARRY_2026-09-22.md) completes all eight
  adjacent carrying turns; 20,367 complete-pack checks pass. Sixteen cargo turns
  remained at that checkpoint. The [carry half-turn pass](MARSH_CARRY_HALF_TURNS_2026-09-22.md)
  completes all twelve dry-carry turns; 20,563 complete-pack checks pass. Only
  Marsh's twelve swimming-with-cargo turns remained at that checkpoint. Bill, Veld
  and Branforth each have all twelve turns in all three families, bare and helmeted.
  Coverage does not establish owner motion acceptance, which remains open.
  [Loaded-swim foundation audit](MARSH_SWIM_CARGO_FOUNDATION_2026-09-22.md): Marsh's
  existing east swim-carry frame is empty-handed, with no separate rendered case.
  The [east loaded-swim repair](MARSH_LOADED_SWIM_EAST_2026-09-22.md) is now
  installed with connected pickup, exact loaded endpoint, native playback and
  93-sample route checks passing. All24 old loaded-swim frames were empty-handed;
  the [west loaded-swim pass](MARSH_LOADED_SWIM_WEST_2026-09-22.md) now repairs
  west pickup/transport too, preserving the east frames. The
  [north loaded-swim pass](MARSH_LOADED_SWIM_NORTH_2026-09-22.md) now supplies a
  foreshortened rear pickup/transport sequence. The
  [south loaded-swim pass](MARSH_LOADED_SWIM_SOUTH_2026-09-22.md) completes all four
  pickup/loaded-loop replacements:48 frames reproduce, native playback and
  93-sample route checks pass. The subsequent
  [loaded-swimming turn pass](MARSH_SWIM_CARRY_TURNS_2026-09-22.md) completes all
  twelve cargo-swimming turns:76 new frames, exact current endpoints and native
  playback. Marsh now has all twelve turns in each of the three families. All72
  crew handoff/restore cases,21,263 pack checks and93 route samples pass.
  [Controller expedition review](MARSH_EXPEDITION_PRESENTATION_2026-09-22.md)
  then found and fixed two integration defects: the real pickup renderer omitted
  the0.52s timing mapping, and Marsh's exterior clearance suppressed turns.
  Delivery, empty recall and loaded recall now pass with real controller/renderer,
  six pickup/four unload poses, cargo accounting and loaded disk restore/pause.
  These are dedicated prebuilt-station tests, not normal paid-loop acceptance.
  [Cargo drainage transition](MARSH_CARGO_DRAIN_2026-09-22.md) now replaces the
  abrupt switch with four-facing rising poses tied to saved chamber drainage.
  Feet stay planted during pressure equalization; normal carry resumes on exit.
  All24 source-derived frames reproduce;21,399 pack checks pass. Native delivery
  and recall checks cover all five rising poses plus pause, power loss, death
  precedence and disk restore. The subsequent [release validation](CREW_POLISH_TEST_BUILDS_2026-09-22.md)
  completes four rotated deliveries plus empty/loaded recall in the actual Windows
  executable: six journeys, zero failures. Current Windows/Mac test packages include
  these integrations. Owner motion acceptance and native Mac testing remain open.

- Bill's four repaired walks, north/west work identity, standing endpoints and
  approximately14% smaller normal helmet are installed. Exact current source
  and motion evidence is indexed in the archived status. Do not shrink the helmet
  again merely because the old clarification reappears.
- Bill and Branforth locker identity repairs are installed and canonically
  reproducible. Airlock shelf helmets fit each human. Veld's reviewed art remains
  unchanged. [Bill locker](BILL_LOCKER_IDENTITY_INTEGRATION_2026-09-22.md),
  [Branforth locker](BRANFORTH_LOCKER_IDENTITY_INTEGRATION_2026-09-22.md),
  [shelf fit](AIRLOCK_SHELF_FIT_2026-09-22.md).
- All four cast have bought-bunk profiles for the reviewed unmirrored bed. Contact,
  interruption, restore, shared occupancy and reachable-bed eligibility are covered
  by bounded native checks. Marsh's legacy berth remains supported. Other bed
  sizes/orientations are not thereby accepted.
  [Multi-crew review](BUNK_MULTI_CREW_REVIEW_2026-09-22.md),
  [eligibility](BUNK_ELIGIBILITY_FIX_2026-09-22.md).
- Life Support uses an exact keyboard-side approach and standing console action.
  Power loss and stale saved contact cancel work without granting benefits or
  teleporting crew. All48 shared activity cases pass; Bill's approach, three work
  cycles and departure were captured. [Console evidence](LIFE_SUPPORT_CONSOLE_CONTACT_2026-09-22.md).
- Drone chassis/tool shear, welding endpoints, hatch scale continuity and exposed
  clearance work-face selection are repaired. Preserve intentional hull occlusion.
  [Drone integration](DRONE_MOTION_REVIEW_2026-09-21.md).

Recent review evidence does not establish owner motion acceptance:

- [Current crew comparison](CREW_GAIT_COMPARISON_2026-09-22.md):90 native frames,
  Bill/Veld/Branforth in four directions at equal travel speed. Bill north/south
  cadence matches Veld; shorter side strides give a quicker cycle. No new timing
  defect established, no speed or source edit from this comparison.
- [Salvage follow-up](SALVAGE_MOTION_FOLLOWUP_2026-09-22.md):670 samples complete
  clearance, recharge and return. Separate unobstructed working poses reviewed;
  this is manually stepped synthetic evidence, not real-time expedition pacing.
- [Paid save/resume observation](EXPEDITION_RESUME_REVIEW_2026-09-22.md): bounded
  normal-process observation survives cycles4-9 and resumes a disk checkpoint.
  This is not a complete human expedition or every saved action state.

## Room composition and asset state

Nonprotected rooms have received multiple composition passes; do not restart from
rejected first pilots. Maintenance r05, Bio Lab r04, Hydroponics r3 and Life Support
r4 are installed. Crew Hab retains provisional positive owner feedback. Current
nonprotected layouts are agent-reviewed playtest layouts, not blanket owner approval.
The archived status indexes per-room routes, live-scale and saved/default evidence.

Latest [Biodome polish](BIODOME_POLISH_REVIEW_2026-09-22.md) replaces loose-plant
scatter with a medium shrub trough and groups the basin beside seating. Four
saved/default keys, card and review ledger were updated; unrelated keys/marks
preserved. Four-view/640 walking samples and exact candidate parity pass.

Anomaly's separated orb, kiosk/tank screens, q3 amber placement, card and actual
station pause checks are already installed/verified. Older 'prototype only' and
'pause pending' notes are superseded. [Anomaly evidence](ANOMALY_ROOM_REVIEW_2026-09-21.md).
Radio/Holo/Command/Reactor and other installed operating-display passes retain their
recorded scope; static machine bodies are not missing animation by default.

[Room-review ledger audit](ROOM_REVIEW_LEDGER_AUDIT_2026-09-22.md):47 cards decode;
card-bound records were1 current /3 stale /43 missing. A subsequent scoped
[pilot card review](PILOT_CARD_REVIEW_2026-09-22.md) binds Maintenance/Bio/Crew Hab
to inspected current cards:4 current /3 stale /40 missing. These are
review-binding gaps, not bad or missing rooms. Reconcile relevant recent handoffs
before scheduling another art pass. Do not auto-approve ledger entries.

## Performance and current test packages

Fit preparation now splits the floor redraw into separate frames by default.
Two candidate peaks109.848/109.910ms versus references125.710/162.927ms; total
transition time is not improved. Final images match, controlled mid-zoom samples
and settled/full-rebuild parity pass. This change is included in the current test builds.
[Fit evidence and scope](FIT_BUTTON_PROFILE_2026-09-22.md).

The simulation budget passes800 updates at1.67ms mean/24.9ms worst. Large-station
render timings remain instrumented measurements, not FPS; zero net Bill motion in
100-room samples limits moving-crew conclusions. Earlier retention, shadow and
call-local door/light optimizations retain their specific parity evidence.
[Latest baseline](POLISH_PERFORMANCE_REVIEW_2026-09-22.md).

Current Windows and Mac test build: **brinespace-6600876d650b0d68**.

- Windows: `builds/BrineSpace-stability-2026-09-23/BrineSpace.exe` plus its PCK.
- Mac: `builds/BrineSpace-mac-stability-2026-09-23/BrineSpace.zip`.

The Continue-dialogue, open-empty human pod and near-closed hatch repairs are now
packaged alongside previous crew/room/camera/audio work. Both exact PCK audits:
15,619 assets, zero discrepancies. Actual Windows New Game, simulation, Continue,
Fit, F8,527 crew/pod pixel references and66 hatch boundary samples pass. Normal
later-station comparison identified a blocked intake and inaccessible ore. Normal
rock clearance funded Solar Array and a clear-intake turbine; restoring the ward
work area let Veld finish. Latest frozen checkpoint:cycle35/eleven rooms/three
crew, no orders, generation10/demand5, stored Power11/Food6/Metal4. All actual
release runs have zero errors; finite-resource and owner balance acceptance remain open.
[Current build evidence](STABILITY_TEST_BUILDS_2026-09-23.md).

Mac Universal2 structure passes; ad-hoc and not notarized. Native Apple Silicon
launch/gameplay/Gatekeeper and owner visual/audio acceptance remain open.
Previous builds remain intact, with their distinct
[crew expedition evidence](CREW_POLISH_TEST_BUILDS_2026-09-22.md).

## Next work and acceptance gaps

The [September23 normal release review](NORMAL_RELEASE_REVIEW_2026-09-23.md)
reaches cycle8/seven rooms with normal costs/failures and exact disk Continue,
then concludes without engine errors. Corrected gameplay crops cover Bill's four
walk directions and north torch draw/weld/stow; owner motion review remains open.
It exposed a repeated starter wake line after Continue. Source now restores the
comms observer's crew baseline; all-four-starter, new-wake, archive, save and native
conversation checks pass, including the actual frozen checkpoint. The September22 packages predated this repair; the current September23 builds
include it.

The [continued paid-recovery review](PAID_CREW_RECOVERY_REVIEW_2026-09-23.md)
extends current-source play to cycle14/eight rooms/two crew. Normal production
funds the eight-Metal ward repair, Veld thaws and announces herself, and Bill's
starter line remains suppressed. Both native runs and the frozen two-crew save
check pass. That review exposed an open-to-closed pod snap at recovery. The
subsequent [open-empty handoff repair](CRYO_OPEN_HANDOFF_2026-09-23.md) is installed:
three matching human pod poses retain the open lid and exit registration. Veld's
paid gameplay recovery, exact pause/Continue pixels, timing/architect regression
and asset rebuild/dependency checks pass. The September22 test downloads predated this art/renderer change and dialogue
repair; both are now in the September23 builds. Owner motion review remains open.

[Natural two-crew activity review](TWO_CREW_ACTIVITY_REVIEW_2026-09-23.md):
150 seconds of source play advanced cycle14 to22 and eight to nine rooms. Normal
income paid for Crew Hab; Bill completed it and total crew rose to three. Bill's
console/construction/meal and Veld's sample/scanner/berth activities were observed
without forced needs. Native run:331 captures, zero errors/failures. Sampled
furniture alignment reviewed; no production changes justified in this pass.
A later frozen checkpoint is retained for the next continuation. This does not
establish complete motion, balance or owner acceptance.

[New music review](NEW_MUSIC_MIX_REVIEW_2026-09-22.md): all five newer tracks and
four original tracks measure -17.50 LUFS after existing per-track gains. Audio
regression passes; native new-track transition capture peaks at -14.82 dBFS with
no dropped frames. Rebuild tool now preserves newer gains and pairing metadata.
Runtime mix unchanged; owner listening remains separate from measured checks.

The [five-minute opening extension](EXTENDED_EXPEDITION_REVIEW_2026-09-22.md)
reaches cycle13/seven rooms and conclusion with normal costs/failures, exit0 and
no logged engine errors. Metal and power recover after reaching zero. Its bounded
automated build strategy does not establish unrestricted growth or human pacing.

[Native mixed-audio capture](NATIVE_AUDIO_REVIEW_2026-09-22.md) has no clipping or
dropped capture frames in its32second sample (peak-14.85dBFS). No gain changes.
This scheduled-cue fixture does not establish owner listening or expedition mix quality.

Latest [normal-clock opening](NORMAL_EXPEDITION_REVIEW_2026-09-22.md) uses the dealt
hand, normal costs/failures and comms pauses for120wall-clock seconds. It reaches
cycle4/five rooms and an inspected expedition report; saving returns success.
No restore in that first run, no audio listening and no human pacing acceptance.
Automated legal placement is recorded explicitly. The subsequent
[disk continuation](NORMAL_CHECKPOINT_CONTINUATION_2026-09-22.md) preserves Bill's
active weld, resources, rooms and cycle exactly; Resume completes saved construction
and advances cycles3->5. The displaced camera is now repaired: hidden viewport
layout caused incorrect centering. Continue reapplies core focus after reveal;
native controlled review and the extended staged-restore regression pass.
[Camera fix and diagnostic correction](CONTINUE_CAMERA_FIX_2026-09-22.md).
This fix is verified in the current actual Windows executable; Mac PCK identity matches.

1. Exercise a normal expedition journey across current rooms, crew actions,
   save/resume, opening power feedback and conclusion. Record actual observed
   defects and repair them; do not substitute more isolated passing fixtures for
   pacing, audio mix, visual coherence or real-time motion review.
2. Incorporate owner feedback on the current gait and room previews. No anatomical
   foot-lock or whole-game visual acceptance is established. Preserve connected
   pose regions and character identity when a specific defect needs revision.
3. Run the included native Apple Silicon checklist when hardware evidence is
   available. Windows and ZIP inspection cannot close it. The current matching
   test builds include the renderer changes, with actual Windows Continue/Fit
   verification recorded above; do not repeat packaging for a documentation edit.
4. Preserve staged owner-room findings without installation: Research q2 route,
   Pressure Control clipping and Listening Post console extent. Evidence remains
   under `output/owner-room-references-2026-09-21` for owner review.
5. Dialogue note17 still needs its exact offending real-session line. The available
   trace and controlled paid builds do not reproduce early completion dialogue;
   F8 now includes the optional trace. Do not patch timing speculatively.
   [Diagnostic evidence](ROOM_DIALOGUE_TIMING_REVIEW_2026-09-21.md).
6. Improve reported coarse/unclean props individually at actual game scale. Small
   prop retirement is a separate decision. Fan-card note14 has fixes; remaining
   readability judgment is not an uninvestigated global viewport defect. Inspector
   note16 was completed; do not rebuild it from an old checklist.

Latest [expedition continuation and hatch fix](EXPEDITION_HATCH_FIX_2026-09-23.md):
a normal paid source run reached cycle 10/seven rooms, with exact cycle-3 disk
restore and no repeated starter wake line. It exposed a near-closed mining hatch
polygon that could not triangulate. Source now skips only undrawable tiny apertures;
66 native boundary samples and six drone handoff comparisons pass. A fresh
100-second checkpoint continuation reaches cycle 7/seven rooms and conclusion with
zero engine errors. Native station/warning/report screenshots were inspected;
human pacing, listening and continuous motion acceptance remain open. The September22 packages predated both repairs; the September23 builds now
include them, with66 actual-release hatch boundary cases passing.

## Workflow

Use maintained `skills/brinespace-character-pipeline` and
`skills/brinespace-room-pipeline`; sync verified reference changes to installed
copies. The [visual bible](BRINESPACE_VISUAL_AESTHETIC_BIBLE.md) owns art direction;
[release workflow](RELEASE_WORKFLOW.md) owns packaging gates. Canonical builders
resolve archived source provenance; never generate missing originals to pass a check.

Scope searches away from `output/`; read evidence by exact known path. Guard and
back up layout keys before writes. Await observable startup/state in fixtures.
Inspect logs as well as exit codes. Capture runs with GPU readback are not timing
baselines. Run relevant tests only; preserve visual review where it proves quality.
At milestones, update this concise state and link detailed evidence rather than
appending successive contradictory implementation stages.
