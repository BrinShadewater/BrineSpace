---
name: brinespace-character-pipeline
description: Create, animate, repair, package, or integrate BrineSpace crew characters such as Major Bill and Dr. Veld. Use for character identity, sprite motion, and character-specific NPC integration; room machinery animation belongs to the room pipeline.
---

# BrineSpace character pipeline

For cryopod masters, physical sliding doors, thaw/fog sequences and visible
character landing handoffs, read [cryopod emergence](references/cryopod-emergence.md).
Use both pipelines and the latest owner-selected encounter geometry.

For master-to-animation drift, coherent local pose repairs or Marsh closeout,
read [master repair and motion evidence](references/master-repair.md). For Marsh
continuation, use the checkout's `docs/MARSH_SESSION_CLOSEOUT_2026-09-30.md` after
CURRENT_STATUS.

For ambient sea-life art, lighting textures or UI card frames, use the room
pipeline's references/effects-and-card-art.md in the active checkout. Its material
and opacity diagnostics also help review layered character imagery; card frame
geometry and UI colors do not apply to characters. For new companion behavior,
continue using this character pipeline alongside the room workflow.


For human crew material/proportion matching, idle-to-action continuity and shared
helmet fitting, read [crew consistency](references/crew-consistency.md). For actor
continuation after the September 29 closeout, read the checkout's
`docs/CREW_ANIMATION_SESSION_CLOSEOUT_2026-09-29.md` and its actor handoff.


For current human crew video generation, direct MiniMax access, spend tracking,
matte finish and gait/scale review, read [direct video workflow](references/direct-video.md).
This is the September 28 route for routine authorized Hailuo work; preserve the
reserved Higgsfield motion-transfer run and current runtime selections.

For companion rescue crates, occupant reveals and recovery handoffs, read
[companion rescue workflow](references/companion-rescue.md) and use both pipelines.

For existing Desktop selections, installation audits and acceptance closeout, read
[selected artwork audit](references/selected-art-audit.md). Start from current status
and the latest dated owner decisions before carrying forward older next steps.

For the September 26 room/animation closeout, read the active checkout's
`docs/ROOM_ART_SESSION_CLOSEOUT_2026-09-26.md` after CURRENT_STATUS.md.
It supersedes historical pending drone installation steps; immersion ideas remain deferred.

For drone NPC animation, launch/recovery effects or their closeout, read
[drone production lessons](references/drone-animation.md). Use both room and
character workflows when changing a drone and its dock interaction.


For coarse existing sprites, local detail/motion repair, or replacement of a full
active library, read [source density and replacement](references/source-density.md).

For nonhuman companions, swimming/flotation, or their animation closeout, read
[companion motion lessons](references/companion-motion.md).

For everyday crew actions, cargo transitions or their session closeout, read
[crew-life lessons](references/crew-life.md) for source extraction, furniture
contact, equipment fitting and checkpoint evidence.

For new matching portraits, profile revisions, accepted portrait masters and safe
native portrait verification, as well as procedural comms effects, read
[comms portrait guidance](references/comms-portraits.md).

For session consolidation or resuming interrupted animation work, read
[handoff guidance](references/handoff.md) to reconcile current source coverage,
transition defects and the limits of native or packaged evidence.

Deliver the requested character work with consistent identity, registered motion,
and evidence appropriate to its scope. Preserve accepted work and make revisions
inexpensive. This skill owns character decisions; existing sprite tools own
packaging, and the project visual bible owns shared art direction.

For current scope, read `docs/CURRENT_STATUS.md` first. For takeover or closeout,
use `docs/CLAUDE_HANDOFF_2026-09-24.md` and the maintained
`docs/ASSET_PIPELINE_AND_WORKFLOW.md`; dated reports retain their original scope.

## Locate the project and select the scope

Locate the active BrineSpace checkout through the workspace, not a fixed drive.
Read its AGENTS.md, `docs/DEVELOPMENT_NOTES.md`, and `NOTICE.md`. Project paths
below are relative to that checkout, even when this skill is installed elsewhere.
The repository's `skills/brinespace-character-pipeline/` is the maintained source;
prefer its newer references to an installed snapshot.

Infer the deliverable from the request and prior authorization:

- **Concept:** establish identity and same-scale appearance. Read
  [character-direction.md](references/character-direction.md).
- **Animation pack or repair:** establish required motion and engine exports.
  Read [animation-contract.md](references/animation-contract.md); read character
  direction when creating or changing identity.
- **Integrated NPC:** deliver the pack plus the requested behavior and runtime
  verification. Also read [godot-integration.md](references/godot-integration.md).

For swimming, death or wearable-equipment extensions, also read
[underwater-equipment.md](references/underwater-equipment.md). Track new coverage
separately from the accepted dry pack, including missing states and integration.

Read the applicable section of [acceptance.md](references/acceptance.md) before
review or handoff. A concept does not require NPC code; a walk repair does not
require extra actions. Continue already-authorized work without inventing new
approval gates. Ask only for information that materially blocks the requested result.

## Establish and exercise the contract

Inspect the current character sources, manifest, and consumers before specifying
dimensions or states. Record identity, department, canonical reference, camera,
frame registration, state/direction coverage, timing, and requested scope.

Use the available `sprite-animation-maker` skill for general sprite production
and its existing helpers when applicable. Use the available image generation
capability for new visual sources; preserve a user-selected authoring method.
Local scripts handle deterministic processing, not invented replacement artwork.
If a capability is missing, complete independent local work and report the missing
capability; a reference to another skill does not install it.

For new packs, prove a representative idle, walk, and role action before expanding
the matrix. For narrow repairs, work directly on the failed portion. Preserve raw
sources and exact prompts; save each generated result into the project immediately.
Record rejected candidates and intentionally omitted states separately.

Package accepted sources into frames, manifest, requested engine exports, and
review media. Rebuilds should use local sources without calling a generation
service. Review identity and motion at actual station scale as well as full size.

## Non-obvious constraints

- Bill/Veld's 92 × 92 canvas and foot pivot (46, 86) are a compatibility profile,
  not a universal character size. Inspect the consumer before changing them.
- Opposite views cannot be mirrored when equipment, markings, or lighting would
  change sides incorrectly. Record derived/reversed frames separately from new art.
- A fixed pivot does not mean forcing every pose to the same bounding-box height.
  Kneeling must lower the body while the ground contact remains registered.
- Veld's `repair` state means sample inspection. Preserve controller compatibility
  while recording character-specific action meanings.
- Pixel/manifest tests do not certify visual identity, smoothness, occlusion, or
  owner acceptance. Record technical checks and visual review separately.

Use `skills/brinespace-room-pipeline/SKILL.md` in the active checkout when the task
also changes room art, prop registration, or door layouts. Existing room geometry
is input to character integration; do not redesign rooms merely to pass a crew test.

Report the requested scope, completed states, generation/packaging/integration
status, checks actually run, and remaining limitations. When revising this skill,
use [evaluation cases](evals/cases.json) and the evaluation guidance in acceptance.

## September 28 engineering notes

- Crew navigation: corridor `library/tileset-` pieces never block crew; hallway furniture blocks walkers but not swimmers (`swim_blockers`).
- Crew animation packs still load eagerly (~2.3 GB at startup); load each crew member on first appearance once this pipeline's session is idle.
- Cleanup rule: unreferenced `review/` candidate folders may go; `generated/` and `sources/` stay because build tools and playtests read them.


## Veld north lounge depth diagnosis — October 1, 2026

Real main-scene/default lounge contact audit uses fixture-only paired north seated
candidate, actual clear RoomActivity approach, four rotations/both gears.192checks,
0failures,engine0/44.31s/no script or artwork errors; all2931non-log
owner files unchanged with scratch APPDATA.32prescribed-stage captures plus8held
depth diagnostics. Candidate texture admission and retained crew slot verified;
wait for observable slot submission before capturing nested retained drawing.

Visual contact/depth remains FAILED: normal held character is hidden behind chair
in all8gear/rotation views. Same source/position becomes visible with temporary
+200world-unit depth metadata; restored after capture. Diagnostic isolates depth,
not an approved offset or final seat/motion acceptance. No source/manifests/normal
selection/owner furniture changes. Staged candidate remains unselected.
Earlier112/176check intervals retained; technical pass never certified visibility.

Lesson: a valid source texture and fixed physical foot do not prove actual room
visibility. Review furniture contact and sort order separately from source scale,
pose clocks and pixel protection. Never fix an occlusion bug by distorting anatomy
or globally drawing the character over all furnishings. Next registered seat/depth
path for down/held/rise, native full motion, interruptions/Continue, other cardinal
seated sources and full-set polish. Full goal active/incomplete.
Handoff: character/veld-seated-north-coherent-v1/STATION_REVIEW.md.


## Veld north seated registered chair depth — October 1, 2026

Staged north seated pair now opts into actual seat contact depth. The lounge
resolver records each seat prop's front sort contact plus0.01world-unit tie break;
CrewLife.seated_draw_depth keeps the greater of natural actor depth and that
registered edge. Only marked dry sit/down/held/rise textures use it; exact standing
entry/exit and unmarked textures retain ordinary depth. Veld's layered room member
carries explicit depth; room queue honors it while defaulting other crew to their
existing ordering. No arbitrary foreground bias, anatomy/palette/navigation/owner
layout change. All12sprite hashes exactly match the previous paired milestone.

60package checks including deterministic rebuilds;1184actual main-scene/default
lounge candidate checks,0failures,engine0/61.27s/no errors. All2931
non-log real profile files unchanged under scratch APPDATA.112prescribed source
pose/join captures in both gears/four rotations plus8same-pose unmarked comparisons.
Full14pose paired native crop boards/all4rotations and held room board reviewed:
Veld remains visible on the chair through lowering/held/rising.64controlled
interruptions retain exact source pixels, visual contact position, registered
depth, navigation foot and valid actor snapshot admission. Not actual world
service-loss dispatch, fresh-scene Continue, natural cadence or owner acceptance.

Candidate remains unselected; existing selected actors lack the opt-in metadata.
Source preview links separate actual lounge review in station-review.html.
Native screenshot visibility/depth is evidence separate from source/clock tests.
Per-pose depth offsets should not bake a room-specific approach distance into art;
use registered seat depth at rendering so lower/rise and interruptions retain
geometry-relative ordering and foreground props remain forward. Prior failed
visual diagnosis and each native interval retained, no retroactive acceptance.
Next actual interruption/Continue, held breathing, other cardinal seated/life
sources, rest/death joins and whole-set polish. Full goal active/incomplete.
Handoff: character/veld-seated-north-coherent-v1/STATION_REVIEW.md.


## Veld north seated interruption and fresh Continue — October 1, 2026

Fixture-only paired north seated candidate exercised actual NPC update guard for
power loss and room suspension at six lowering phases plus settled seat, both
equipment variants:28interruptions. Actual service guard dispatches rise, clears
goal, retains displayed source pixels, contact/navigation foot and bounded chair
depth. Prescribed station entry, not natural chooser/routing or all hazard exits.

Six actual disk checkpoints (lower/held/rise x two gears), read and restored into
separately created main scenes via production RunSave.restore_staged. Candidate
overrides explicitly appended in each scene; no normal art selection. Exact
equipment/stage/action clock/pixels/contact/depth/paused persistence verified.
All six before/after native room/actor crops visually reviewed. 5are byte
equal; first bare lowering crop has broad small room-shade differences up to
5/255 per channel despite exact source pixels/contact/depth. Cause not
proven, no whole-room pixel equality or renderer-shade continuity claim for it.
346checks,0failures,engine0/207.63s/no errors. Scratch APPDATA.
All2931non-log owner files unchanged. Real selected architect Veld released through advance_core; no failure
or free-build switches, real save folder never used. No source/sprite/runtime edit
needed for this verification;60package/1184room pose/depth checks retain prior scope.

Failed first fixture omitted maintenance from four-key needs and correctly failed
actor/whole-checkpoint validation. Fixed only fixture, added immediate admission
guard; retained failed38.34s interval. Subsequent334checks/six restores passed,
but first before-camera captured preceding viewport despite valid retained source.
Retained that runtime-valid/visually-incomplete interval. New camera guard observes
actual world room center after frame_post_draw as well as retained source/depth;
latest full six-restore rerun supplies corrected camera before/after evidence.
Residual first-crop shade difference retained separately from camera registration.

Lesson: keep complete actor schema in full-save fixtures. Texture/slot readiness
does not prove deferred camera/scroll layout readiness after startup or Continue;
observe rendered viewport geometry, not a fixed sleep. Whole-window pixels can
differ in UI while registered room/actor crops and source state remain exact.
Next coherent held breathing, first-pair shade investigation, natural approach/exit/hazard routing and remaining
directional seated/life sources; rest/death joins and whole-set polish remain.
Full goal active/incomplete; candidate remains staged. No owner acceptance claim.
Handoff: character/veld-seated-north-coherent-v1/CONTINUE_HANDOFF.md.
